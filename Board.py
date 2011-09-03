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
            self.addPiece(Color.White, Kind.Pawn, file, Board.WhitePawnRank)
            self.addPiece(Color.Black, Kind.Pawn, file, Board.BlackPawnRank)
        self.addOfficers(Color.White, Board.WhiteOfficerRank)
        self.addOfficers(Color.Black, Board.BlackOfficerRank)

    def addOfficers(self, color, rank):
        for file in Board.RookFiles:
            self.addPiece(color, Kind.Rook, file, rank)
        for file in Board.KnightFiles:
            self.addPiece(color, Kind.Knight, file, rank)
        for file in Board.BishopFiles:
            self.addPiece(color, Kind.Bishop, file, rank)
        self.addPiece(color, Kind.Queen, Board.QueenFile, rank)
        self.addPiece(color, Kind.King, Board.KingFile, rank)

    def addPiece(self, color, kind, file, rank):
        self.Pieces.append(Piece(color, kind, Square(file, rank)))
