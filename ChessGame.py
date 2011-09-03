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
        return result

    def Move(self, origin, destination):
        piece = self.GetPiece(origin.File, origin.Rank)
        if piece == None:
            raise Exception("No piece to move at that position.")
        pieceAtDestination = self.GetPiece(destination.File, destination.Rank)
        if pieceAtDestination != None:
            self.Pieces.remove(pieceAtDestination)
        piece.Position = destination
        self.SideToPlay = 3 - self.SideToPlay

    def _isValidMove(self, piece, move):
        return not self._squareIsOccupiedByOwnPiece(piece, move.Destination) \
            and not self._moveIsObstructedByPiece(piece, move.Destination) \
            and not self._squareIsOccupiedByOpponent(piece, move.Destination)

    def _isValidCapture(self, piece, capture):
        return not self._squareIsOccupiedByOwnPiece(piece, capture.Destination) \
            and not self._moveIsObstructedByPiece(piece, capture.Destination) \
            and self._squareIsOccupiedByOpponent(piece, capture.Destination)

    def _squareIsOccupiedByOwnPiece(self, piece, square):
        pieceAtSquare = self.GetPiece(square.File, square.Rank)
        return pieceAtSquare != None and pieceAtSquare.Color == piece.Color

    def _squareIsOccupiedByOpponent(self, piece, square):
        pieceAtSquare = self.GetPiece(square.File, square.Rank)
        return pieceAtSquare != None and pieceAtSquare.Color != piece.Color

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
