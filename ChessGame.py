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
        for piece in self.Pieces:
            for move in self.GetPieceMoves(piece):
                result.append(move)
        result.append(Move(Square(File.B, 1), Square(File.A, 3)))
        result.append(Move(Square(File.B, 1), Square(File.C, 3)))
        result.append(Move(Square(File.G, 1), Square(File.F, 3)))
        result.append(Move(Square(File.G, 1), Square(File.H, 3)))
        return result

    def GetPiece(self, file, rank):
        for piece in self.Pieces:
            if piece.Position.Rank == rank and piece.Position.File == file:
                return piece

    def GetPieceMoves(self, piece):
        result = []
        if piece.Kind != Kind.Pawn or piece.Color != Color.White:
            return result
        result.append(Move(Square(piece.Position.File, 2), Square(piece.Position.File, 3)))
        result.append(Move(Square(piece.Position.File, 2), Square(piece.Position.File, 4)))
        return result
