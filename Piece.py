from Move import *
from Square import *

class Piece:
    
    def __init__(self, color, kind, position):
        self.Color = color
        self.Kind = kind
        self.Position = position

    def GetMoves(self):
        result = []
        direction = 3 - 2 * self.Color
        originFile = self.Position.File
        originRank = self.Position.Rank
        if self.Kind == Kind.Pawn:
            result.append(self.GetMove(originFile, originRank + direction))
            result.append(self.GetMove(originFile, originRank + 2 * direction))
        if self.Kind == Kind.Knight:
            result.append(self.GetMove(originFile - 1, originRank + 2 * direction))
            result.append(self.GetMove(originFile + 1, originRank + 2 * direction))
        return result

    def GetMove(self, destinationFile, destinationRank):
        return Move(self.Position, Square(destinationFile, destinationRank))
        

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
