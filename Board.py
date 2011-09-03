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
        self.addPieces()

    def GetPiece(self, position):
        for piece in self.Pieces:
            if piece.Position == position:
                return piece

    def addPieces(self):
        for file in File.All:
            self.Pieces.append(Piece(Color.White, Kind.Pawn, Square(file, Board.WhitePawnRank)))
            self.Pieces.append(Piece(Color.Black, Kind.Pawn, Square(file, Board.BlackPawnRank)))
        self.addOfficers(Color.White, Board.WhiteOfficerRank)
        self.addOfficers(Color.Black, Board.BlackOfficerRank)

    def addOfficers(self, color, rank):
        for file in Board.RookFiles:
            self.Pieces.append(Piece(color, Kind.Rook, Square(file, rank)))
        for file in Board.KnightFiles:
            self.Pieces.append(Piece(color, Kind.Knight, Square(file, rank)))
        for file in Board.BishopFiles:
            self.Pieces.append(Piece(color, Kind.Bishop, Square(file, rank)))
        self.Pieces.append(Piece(color, Kind.Queen, Square(Board.QueenFile, rank)))
        self.Pieces.append(Piece(color, Kind.King, Square(Board.KingFile, rank)))
