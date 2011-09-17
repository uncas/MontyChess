from Square import *


class Piece:
    
    def __init__(self, color, kind, position):
        self.Color = color
        self.Kind = kind
        self.Position = position
        self.Direction = 3 - 2 * self.Color
        self.IsPawn = kind == Kind.Pawn
        self.IsKnight = kind == Kind.Knight
        self.IsBishop = kind == Kind.Bishop
        self.IsRook = kind == Kind.Rook
        self.IsQueen = kind == Kind.Queen
        self.IsKing = kind == Kind.King
        self.CanJump = self.IsKnight
        self.HasMoved = False

    def __repr__(self):
        return self._colorString() + " " + self._kindString()

    def __eq__(self, other):
        if self is None or other is None:
            return False
        return self.Kind == other.Kind and self.Color == other.Color and self.Position == other.Position

    def IsAtStartRank(self):
        return (self.Color == Color.White and self.Position.Rank == 2) or (self.Color == Color.Black and self.Position.Rank == 7)

    def _colorString(self):
        if self.Color == 1:
            return "White"
        else:
            return "Black"

    def _kindString(self):
        kindStrings = "Pawn", "Rook", "Knight", "Bishop", "Queen", "King"
        return kindStrings[self.Kind-1]


class Color:
    White = 1
    Black = 2

    @staticmethod
    def OtherColor(color):
        return 3 - color
        

class Kind:
    Pawn = 1
    Rook = 2
    Knight = 3
    Bishop = 4
    Queen = 5
    King = 6
#    Promotion = Kind.Rook, Kind.Knight, Kind.Bishop, Kind.Queen
