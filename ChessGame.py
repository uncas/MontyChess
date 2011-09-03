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
        return piece.GetMoves()

    def Move(self, origin, destination):
        piece = self.GetPiece(origin.File, origin.Rank)
        piece.Position = destination
        self.SideToPlay = Color.Black
