from Piece import *
from Square import *

class Board:

    RookFiles = File.A, File.H
    KnightFiles = File.B, File.G
    BishopFiles = File.C, File.F
    QueenFile = File.D
    KingFile = File.E

    WhiteOfficerRank = 1
    WhitePawnRank = 2
    BlackPawnRank = 7
    BlackOfficerRank = 8

    def __init__(self):
        self.Pieces = []
        self._addPieces()

    def GetPieces(self, color):
        return [piece for piece in self.Pieces if piece.Color == color] 

    def GetPiece(self, position):
        for piece in self.Pieces:
            if piece.Position == position:
                return piece

    def GetKingPosition(self, color):
        return [piece.Position for piece in self.Pieces if piece.Color == color and piece.Kind == Kind.King]

    def _addPieces(self):
        for file in File.All:
            self._addPiece(Color.White, Kind.Pawn, file, Board.WhitePawnRank)
            self._addPiece(Color.Black, Kind.Pawn, file, Board.BlackPawnRank)
        self._addOfficers(Color.White, Board.WhiteOfficerRank)
        self._addOfficers(Color.Black, Board.BlackOfficerRank)

    def _addOfficers(self, color, rank):
        for file in Board.RookFiles:
            self._addPiece(color, Kind.Rook, file, rank)
        for file in Board.KnightFiles:
            self._addPiece(color, Kind.Knight, file, rank)
        for file in Board.BishopFiles:
            self._addPiece(color, Kind.Bishop, file, rank)
        self._addPiece(color, Kind.Queen, Board.QueenFile, rank)
        self._addPiece(color, Kind.King, Board.KingFile, rank)

    def _addPiece(self, color, kind, file, rank):
        self.Pieces.append(Piece(color, kind, Square(file, rank)))
