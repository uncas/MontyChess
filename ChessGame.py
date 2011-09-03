from Board import *
from Move import *
from Piece import *

class ChessGame:

    def __init__(self):
        self.board = Board()
        self.SideToPlay = Color.White
        self.Pieces = self.board.Pieces

    def PossibleMoves(self):
        result = []
        for piece in self.Pieces:
            for move in self.GetPieceMoves(piece):
                result.append(move)
        return result

    def GetPiece(self, file, rank):
        return self.board.GetPiece(file, rank)

    def GetPieceMoves(self, piece):
        result = []
        if piece.Color != self.SideToPlay:
            return result;
        for move in piece.GetMoves():
            pieceAtDestination = self.GetPiece(move.Destination.File, move.Destination.Rank)
            if pieceAtDestination == None or pieceAtDestination.Color != piece.Color:
                result.append(move)
        return result

    def Move(self, origin, destination):
        piece = self.GetPiece(origin.File, origin.Rank)
        if piece == None:
            raise Exception("No piece to move at that position.")
        piece.Position = destination
        self.SideToPlay = 3 - self.SideToPlay
