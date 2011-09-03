from Move import *
from Square import *

class Piece:
    
    def __init__(self, color, kind, position):
        self.Color = color
        self.Kind = kind
        self.Position = position
        self.CanJump = kind == Kind.Knight

    def GetMoves(self):
        result = []
        originFile = self.Position.File
        originRank = self.Position.Rank
        if self.Kind == Kind.Pawn:
            direction = 3 - 2 * self.Color
            result.append(self.GetMove(originFile, originRank + direction))
            if (self.Color == Color.White and originRank == 2) or (self.Color == Color.Black and originRank == 7):
                result.append(self.GetMove(originFile, originRank + 2 * direction))
        if self.Kind == Kind.Knight:
            for knightStep in (-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1):
                destinationFile = originFile + knightStep[0]
                destinationRank = originRank + knightStep[1]
                if File.A <= destinationFile and destinationFile <= File.H and 1 <= destinationRank and destinationRank <= 8:
                    result.append(self.GetMove(destinationFile, destinationRank))
        if self.Kind == Kind.Rook:
            # Moving across the rank:
            for file in File.All:
                if file != originFile:
                    result.append(self.GetMove(file, originRank))
            # Moving down the file:
            for rank in Rank.All:
                if rank != originRank:
                    result.append(self.GetMove(originFile, rank))
        return result

    def GetMove(self, destinationFile, destinationRank):
        return Move(self.Position, Square(destinationFile, destinationRank))

    def __repr__(self):
        return self.ColorString() + " " + self.KindString()

    def ColorString(self):
        if self.Color == 1:
            return "White"
        else:
            return "Black"

    def KindString(self):
        kindStrings = "Pawn", "Rook", "Knight", "Bishop", "Queen", "King"
        return kindStrings[self.Kind-1]
    

class Color:
    White = 1
    Black = 2

class Kind:
    Pawn = 1
    Rook = 2
    Knight = 3
    Bishop = 4
    Queen = 5
    King = 6
