from Board import *
from Move import *
from Piece import *
from Square import *


class ChessGame:

    # The 'ChessGame' class represents the overall chess game.
    # The 'ChessGame' class will delegate groups of logic to specialized classes.
    # TODO: Refactor: Extract move logic to new class, for example 'MoveEngine'.

    def __init__(self):
        self._board = Board()
        self.SideToPlay = Color.White
        self.Pieces = self._board.Pieces
        self._moves = []

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
        for move in piece.GetMoves():
            if self._isValidMove(piece, move):
                result.append(move)
        for capture in piece.GetCaptureMoves():
            if self._isValidCapture(piece, capture):
                result.append(capture)
        castlingPossibility = self._getCastlingPossibility(piece)
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
            self.Pieces.remove(pieceAtDestination)
        if self._isCastling(piece, destination):
            rook = self._getRookToCastleWith(destination)
            move = Move.Castle(piece, destination, rook)
        else:
            move = Move.Normal(piece, destination)
        move.Apply()
        self.SideToPlay = Color.OtherColor(self.SideToPlay)
        self._moves.append(move)
        self._lastMove = move

    def CheckStatus(self):
        whiteIsChecked = self._isColorChecked(Color.White)
        blackIsChecked = self._isColorChecked(Color.Black)
        return CheckStatus(whiteIsChecked, blackIsChecked)

    def _isColorCheckedAfterMove(self, color, move):
        return self._isColorChecked(color)

    def _isColorChecked(self, color):
        otherColor = Color.OtherColor(color)
        return self._isSquareThreatenedByColor(self._board.GetKingPosition(color), otherColor)

    def _isSquareThreatenedByColor(self, position, color):
        # TODO: Implement properly.
        return False
        threatenedSquares = []
        for piece in self._board.GetPieces(color):
            threatenedSquares.extend(self._getSquaresThreatenedByPiece(piece))
        for square in threatenedSquares:
            if square == position:
                return True
        return False

    def _getSquaresThreatenedByPiece(self, piece):
        moves = []
        for capture in piece.GetCaptureMoves():
            if self._isValidCapture(piece, capture):
                moves.append(capture)
        return [move.Destination for move in moves]

    def _getRookToCastleWith(self, kingDestination):
        if kingDestination.File == File.G:
            rookOriginFile = File.H
        else:
            rookOriginFile = File.A
        return self.GetPiece(rookOriginFile, kingDestination.Rank)
        

    def _isCastling(self, piece, destination):
        return piece.IsKing and abs(piece.Position.File - destination.File) == 2

    def _getCastlingPossibility(self, piece):
        if not piece.IsKing or piece.HasMoved:
            return CastlingPossibility(False, False)
        rank = piece.Position.Rank
        return CastlingPossibility(self._isCastlingSidePossible(File.A, rank), self._isCastlingSidePossible(File.H, rank))

    def _isCastlingSidePossible(self, rookFile, rank):
        rook = self.GetPiece(rookFile, rank)
        if rook is None or rook.HasMoved:
            return False
        if rookFile == File.H:
            file1 = File.F
            file2 = File.H
        else:
            file1 = File.B
            file2 = File.E
        for file in range(file1, file2):
            piece = self.GetPiece(file, rank)
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
        pieceAtSquare = self.GetPiece(square.File, square.Rank)
        return pieceAtSquare != None and pieceAtSquare.Color == piece.Color

    def _squareIsOccupiedByOpponent(self, piece, square):
        pieceAtSquare = self.GetPiece(square.File, square.Rank)
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
        pieceNextToPawn = self.GetPiece(square.File, piece.Position.Rank)
        if pieceNextToPawn is None \
            or pieceNextToPawn.Color == piece.Color \
            or not pieceNextToPawn.IsPawn:
            return False
        if piece.Color == Color.White:
            originRank = 7
        else:
            originRank = 2
        return self._lastMove.Destination == Square(square.File, piece.Position.Rank) \
            and self._lastMove.Origin.Rank == originRank

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
            pieceAtSquare = self.GetPiece(piece.Position.File + step * fileDirection, piece.Position.Rank + step * rankDirection)
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
