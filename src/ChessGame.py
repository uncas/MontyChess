from Board import *
from Move import *
from Piece import *
from PieceMoveGenerator import *
from Square import *


class ChessGame:

    # The 'ChessGame' class represents the overall chess game.
    # The 'ChessGame' class will delegate groups of logic to specialized classes.
    # TODO: Refactor: Extract move generation logic to new class, for example 'MoveGenerator'.

    def __init__(self):
        self._board = Board()
        self.SideToPlay = Color.White
        self.Pieces = self._board.Pieces
        self._moves = []
        self._threatCalculator = ThreatCalculator(self._board)
        self._pieceMoveGenerator = PieceMoveGenerator(self._board)
        self._lastMove = None
        self._moveGenerator = MoveGenerator(self)

    def PossibleMoves(self):
        result = []
        for piece in self._board.GetPieces(self.SideToPlay):
            result.extend(self.GetPieceMoves(piece, True))
        return result

    def GetPiece(self, file, rank):
        return self._board.GetPiece(Square(file, rank))

    def GetPieceMoves(self, piece, onlyIfSideToPlay):
        result = []
        if onlyIfSideToPlay and piece.Color != self.SideToPlay:
            return result
        for move in self._pieceMoveGenerator.GetMoves(piece):
            if self._moveGenerator._isValidMove(piece, move):
                result.append(move)
        for capture in self._pieceMoveGenerator.GetCaptureMoves(piece):
            if self._moveGenerator._isValidCapture(piece, capture):
                result.append(capture)
        castlingPossibility = self._moveGenerator._getCastlingPossibility(piece)
        if castlingPossibility.KingSide:
            kingDestination = Square(File.G, piece.Position.Rank)
            rook = self._getRookToCastleWith(kingDestination)
            result.append(Move.Castle(piece, kingDestination, rook))
        if castlingPossibility.QueenSide:
            kingDestination = Square(File.C, piece.Position.Rank)
            rook = self._getRookToCastleWith(kingDestination)
            result.append(Move.Castle(piece, kingDestination, rook))
        return [move for move in result if not self._isColorCheckedAfterMove(piece.Color, move)]

    def Move(self, origin, destination):
        piece = self.GetPiece(origin.File, origin.Rank)
        if piece is None:
            raise Exception("No piece to move at that position.")
        pieceAtDestination = self.GetPiece(destination.File, destination.Rank)
        if pieceAtDestination != None:
            move = Move.Capture(self._board, piece, destination, pieceAtDestination)
        elif self._isCastling(piece, destination):
            rook = self._getRookToCastleWith(destination)
            move = Move.Castle(piece, destination, rook)
        else:
            move = Move.Normal(piece, destination)
        self.ApplyMove(move)

    def _isCastling(self, piece, destination):
        return piece.IsKing and abs(piece.Position.File - destination.File) == 2

    def ApplyMove(self, move):
        move.Apply()
        self.SideToPlay = Color.OtherColor(self.SideToPlay)
        self._moves.append(move)
        self._lastMove = move

    def RevertMove(self, move):
        move.Revert()
        self.SideToPlay = Color.OtherColor(self.SideToPlay)
        self._moves.remove(move)
        if len(self._moves) > 0:
            self._lastMove = self._moves[len(self._moves) - 1]
        else:
            self._lastMove = None

    def CheckStatus(self):
        whiteIsChecked = self._isColorChecked(Color.White)
        blackIsChecked = self._isColorChecked(Color.Black)
        return CheckStatus(whiteIsChecked, blackIsChecked)

    def Result(self):
        moves = self.PossibleMoves()
        if len(moves) == 0:
            sideToPlayIsChecked = self._isColorChecked(self.SideToPlay)
            if not sideToPlayIsChecked:
                return GameResult.Draw
            elif self.SideToPlay == Color.White:
                return GameResult.BlackWins
            else:
                return GameResult.WhiteWins
        return GameResult.Undecided

    def _isColorCheckedAfterMove(self, color, move):
        move.Apply()
        isColorCheckedAfterMove = self._isColorChecked(color)
        move.Revert()
        return isColorCheckedAfterMove

    def _isColorChecked(self, color):
        otherColor = Color.OtherColor(color)
        return self._threatCalculator.IsSquareThreatenedByColor(self._board.GetKingPosition(color), otherColor)

    def _getRookToCastleWith(self, kingDestination):
        if kingDestination.File == File.G:
            rookOriginFile = File.H
        else:
            rookOriginFile = File.A
        return self.GetPiece(rookOriginFile, kingDestination.Rank)


class MoveGenerator:

    def __init__(self, game):
        self._game = game

    def _getCastlingPossibility(self, piece):
        if not piece.IsKing or piece.HasMoved:
            return CastlingPossibility(False, False)
        rank = piece.Position.Rank
        return CastlingPossibility(self._isCastlingSidePossible(File.A, rank), self._isCastlingSidePossible(File.H, rank))

    def _isCastlingSidePossible(self, rookFile, rank):
        rook = self._game.GetPiece(rookFile, rank)
        if rook is None or rook.HasMoved:
            return False
        if rookFile == File.H:
            file1 = File.F
            file2 = File.H
        else:
            file1 = File.B
            file2 = File.E
        for file in range(file1, file2):
            piece = self._game.GetPiece(file, rank)
            if piece != None:
                return False
        return True

    def _isValidMove(self, piece, move):
        return not self._squareIsOccupiedByOwnPiece(piece, move.Destination) \
            and not self._moveIsObstructedByPiece(piece, move.Destination) \
            and not self._squareIsOccupiedByOpponent(piece, move.Destination)

    def _isValidCapture(self, piece, capture):
        return not self._squareIsOccupiedByOwnPiece(piece, capture.Destination) \
            and not self._moveIsObstructedByPiece(piece, capture.Destination) \
            and self._opponentIsCapturedAtSquare(piece, capture.Destination)

    def _squareIsOccupiedByOwnPiece(self, piece, square):
        pieceAtSquare = self._game.GetPiece(square.File, square.Rank)
        return pieceAtSquare != None and pieceAtSquare.Color == piece.Color

    def _squareIsOccupiedByOpponent(self, piece, square):
        pieceAtSquare = self._game.GetPiece(square.File, square.Rank)
        return pieceAtSquare != None and pieceAtSquare.Color != piece.Color

    def _opponentIsCapturedAtSquare(self, piece, square):
        return self._squareIsOccupiedByOpponent(piece, square) \
            or self._enPassantIsPossibleAtSquare(piece, square)

    def _enPassantIsPossibleAtSquare(self, piece, square):
        if not piece.IsPawn:
            return False
        if piece.Color == Color.White and piece.Position.Rank != 5:
            return False
        if piece.Color == Color.Black and piece.Position.Rank != 4:
            return False
        pieceNextToPawn = self._game.GetPiece(square.File, piece.Position.Rank)
        if pieceNextToPawn is None \
            or pieceNextToPawn.Color == piece.Color \
            or not pieceNextToPawn.IsPawn:
            return False
        if piece.Color == Color.White:
            originRank = 7
        else:
            originRank = 2
        return self._game._lastMove.Destination == Square(square.File, piece.Position.Rank) \
            and self._game._lastMove.Origin.Rank == originRank

    def _moveIsObstructedByPiece(self, piece, destination):
        if piece.CanJump:
            return False
        fileDelta = destination.File - piece.Position.File
        rankDelta = destination.Rank - piece.Position.Rank
        fileDirection = 0
        rankDirection = 0
        if fileDelta != 0:
            fileDirection = fileDelta / abs(fileDelta)
        if rankDelta != 0:
            rankDirection = rankDelta / abs(rankDelta)
        steps = max(abs(fileDelta), abs(rankDelta))
        if steps < 1 or steps > 7:
            raise Exception("Invalid step when moving " + str(piece) + " from " + str(piece.Position) + " to " + str(destination))
        for step in range(1, steps):
            pieceAtSquare = self._game.GetPiece(piece.Position.File + step * fileDirection, piece.Position.Rank + step * rankDirection)
            if pieceAtSquare != None:
                return True
        return False


class CastlingPossibility:

    def __init__(self, queenSide, kingSide):
        self.QueenSide = queenSide
        self.KingSide = kingSide


class CheckStatus:

    def __init__(self, whiteIsChecked, blackIsChecked):
        self.WhiteIsChecked = whiteIsChecked
        self.BlackIsChecked = blackIsChecked


class ThreatCalculator:

    def __init__(self, board):
        self._board = board

    def IsSquareThreatenedByColor(self, square, color):
        return self._isSquareThreatenedByPawn(square, color) \
            or self._isSquareThreatenedByKnight(square, color) \
            or self._isSquareThreatenedByBishopOrQueenOnDiagonal(square, color) \
            or self._isSquareThreatenedByRookOrQueenOnFileOrRank(square, color) \
            or self._isSquareThreatenedByKing(square, color)

    def _isSquareThreatenedByPawn(self, square, color):
        if color == Color.White:
            direction = 1
        else:
            direction = -1
        threateningPawn1 = self._board.GetPiece(square.AddFilesAndRanks(1, -direction))
        threateningPawn2 = self._board.GetPiece(square.AddFilesAndRanks(-1, -direction))
        return (threateningPawn1 is not None and threateningPawn1.Kind == Kind.Pawn and threateningPawn1.Color == color) \
            or (threateningPawn2 is not None and threateningPawn2.Kind == Kind.Pawn and threateningPawn2.Color == color)

    def _isSquareThreatenedByKnight(self, square, color):
        for step in PieceMoveGenerator.KnightSteps:
            otherSquare = square.AddStep(step)
            if not otherSquare.IsWithinBoard():
                continue
            piece = self._board.GetPiece(otherSquare)
            if piece is not None and piece.Kind == Kind.Knight and piece.Color == color:
                return True
        return False

    def _isSquareThreatenedByBishopOrQueenOnDiagonal(self, square, color):
        for step in Step(1,1), Step(1,-1), Step(-1,1), Step(-1,-1):
            for times in range(1, 8):
                otherSquare = square.AddStep(step.Times(times))
                if not otherSquare.IsWithinBoard():
                    break
                piece = self._board.GetPiece(otherSquare)
                if piece is not None:
                    if (piece.Kind == Kind.Bishop or piece.Kind == Kind.Queen) and piece.Color == color:
                        return True
                    break
        return False

    def _isSquareThreatenedByRookOrQueenOnFileOrRank(self, square, color):
        for step in Step(1,0), Step(-1,0), Step(0,1), Step(0,-1):
            for times in range(1, 8):
                otherSquare = square.AddStep(step.Times(times))
                if not otherSquare.IsWithinBoard():
                    break
                piece = self._board.GetPiece(otherSquare)
                if piece is not None:
                    if (piece.Kind == Kind.Rook or piece.Kind == Kind.Queen) and piece.Color == color:
                        return True
                    break
        return False

    def _isSquareThreatenedByKing(self, square, color):
        for step in Step(1,0), Step(-1,0), Step(0,1), Step(0,-1), Step(1,1), Step(1,-1), Step(-1,1), Step(-1,-1):
            otherSquare = square.AddStep(step)
            if not otherSquare.IsWithinBoard():
                continue
            piece = self._board.GetPiece(otherSquare)
            if piece is not None and piece.Kind == Kind.King and piece.Color == color:
                return True
        return False


class GameResult:
    Undecided = 0
    Draw = 1
    WhiteWins = 2
    BlackWins = 3
