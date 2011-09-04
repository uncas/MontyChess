from Board import *
from Move import *
from Piece import *
from Square import *

class ChessGame:

    def __init__(self):
        self._board = Board()
        self.SideToPlay = Color.White
        self.Pieces = self._board.Pieces

    def PossibleMoves(self):
        result = []
        for piece in self.Pieces:
            result.extend(self.GetPieceMoves(piece))
        return result

    def GetPiece(self, file, rank):
        return self._board.GetPiece(Square(file, rank))

    def GetPieceMoves(self, piece):
        result = []
        if piece.Color != self.SideToPlay:
            return result;
        for move in piece.GetMoves():
            if self._isValidMove(piece, move):
                result.append(move)
        for capture in piece.GetCaptureMoves():
            if self._isValidCapture(piece, capture):
                result.append(capture)
        if self._castlingIsPossible(piece):
            result.append(Move.Castling(piece.Position, Square(File.G, piece.Position.Rank)))
        return result

    def Move(self, origin, destination):
        piece = self.GetPiece(origin.File, origin.Rank)
        if piece == None:
            raise Exception("No piece to move at that position.")
        pieceAtDestination = self.GetPiece(destination.File, destination.Rank)
        if pieceAtDestination != None:
            self.Pieces.remove(pieceAtDestination)
        if self._isCastling(piece, destination):
            move = Move.Castling(origin, destination)
            if destination.File == File.G:
                rookOriginFile = File.H
                rookDestinationFile = File.F
            else:
                rookOriginFile = File.A
                rookDestinationFile = File.D
            rook = self.GetPiece(rookOriginFile, destination.Rank)
            rook.Position.File = rookDestinationFile
        else:
            move = Move(origin, destination)
        piece.Position = destination
        self.SideToPlay = 3 - self.SideToPlay
        self._lastMove = move

    def _isCastling(self, piece, destination):
        return piece.IsKing and abs(piece.Position.File - destination.File) == 2

    def _castlingIsPossible(self, piece):
        if not piece.IsKing or piece.Position.File != File.E:
            return False
        pieces = []
        for file in File.B, File.C, File.D, File.F, File.G:
            pieces.append(self.GetPiece(file, piece.Position.Rank))
        return (pieces[0] == None and pieces[1] == None and pieces[2] == None) \
            or (pieces[3] == None and pieces[4] == None)

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
        if pieceNextToPawn == None \
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
