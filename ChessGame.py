from Board import *
from Move import *
from Piece import *

class ChessGame:

    def __init__(self):
        self.Pieces = []
        for file in File.All:
            self.Pieces.append(Piece(Color.White, Kind.Pawn, Square(file, 2)))
            self.Pieces.append(Piece(Color.Black, Kind.Pawn, Square(file, 7)))
        self.AddOfficers(Color.White, 1)
        self.AddOfficers(Color.Black, 8)

    def AddOfficers(self, color, rank):
        for file in (File.A, File.H):
            self.Pieces.append(Piece(color, Kind.Rook, Square(file, rank)))
        for file in (File.B, File.G):
            self.Pieces.append(Piece(color, Kind.Knight, Square(file, rank)))
        for file in (File.C, File.F):
            self.Pieces.append(Piece(color, Kind.Bishop, Square(file, rank)))
        self.Pieces.append(Piece(color, Kind.Queen, Square(File.D, rank)))
        self.Pieces.append(Piece(color, Kind.King, Square(File.E, rank)))

    def PossibleMoves(self):
        result = []
        # Duplicated code here:
        # TODO: Remove duplication by putting the move logic into each piece.
        for file in File.All:
            result.append(Move(Square(file, 2), Square(file, 3))) 
            result.append(Move(Square(file, 2), Square(file, 4))) 
        result.append(Move(Square(File.B, 1), Square(File.A, 3)))
        result.append(Move(Square(File.B, 1), Square(File.C, 3)))
        result.append(Move(Square(File.G, 1), Square(File.F, 3)))
        result.append(Move(Square(File.G, 1), Square(File.H, 3)))
        return result
