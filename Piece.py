from Move import *
from Square import *

class Piece:
    
    def __init__(self, color, kind, position):
        self.Color = color
        self.Kind = kind
        self.Position = position
        self._direction = 3 - 2 * self.Color
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

    def GetCaptureMoves(self):
        if not self.IsPawn:
            return self.GetMoves()
        result = []
        originFile = self.Position.File
        originRank = self.Position.Rank
        if originFile > File.A:
            result.append(self._getMove(originFile - 1, originRank + self._direction))
        if originFile < File.H:
            result.append(self._getMove(originFile + 1, originRank + self._direction))
        return result

    def GetMoves(self):
        result = []
        originFile = self.Position.File
        originRank = self.Position.Rank
        if self.IsPawn:
            self._appendPawnMoves(result, originFile, originRank)
        if self.IsKnight:
            self._appendKnightMoves(result, originFile, originRank)
        if self.IsRook:
            self._appendRookMoves(result, originFile, originRank)
        if self.IsBishop:
            self._appendBishopMoves(result, originFile, originRank)
        if self.IsQueen:
            self._appendRookMoves(result, originFile, originRank)
            self._appendBishopMoves(result, originFile, originRank)
        if self.IsKing:
            self._appendKingMoves(result, originFile, originRank)
        return result

    def IsInList(self, pieces):
        for piece in pieces:
            if piece == self:
                return True
        return False

    def _appendKnightMoves(self, result, originFile, originRank):
        for knightStep in (-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1):
            destinationFile = originFile + knightStep[0]
            destinationRank = originRank + knightStep[1]
            if self._isWithinBoard(destinationFile, destinationRank):
                result.append(self._getMove(destinationFile, destinationRank))

    def _appendPawnMoves(self, result, originFile, originRank):
        result.append(self._getMove(originFile, originRank + self._direction))
        if self._isStartRank():
            result.append(self._getMove(originFile, originRank + 2 * self._direction))

    def _appendKingMoves(self, result, originFile, originRank):
        for fileDelta in -1,0,1:
            for rankDelta in -1,0,1:
                if fileDelta == 0 and rankDelta == 0:
                    continue
                destinationFile = originFile + fileDelta
                destinationRank = originRank + rankDelta
                if self._isWithinBoard(destinationFile, destinationRank):
                    result.append(self._getMove(destinationFile, destinationRank))

    def _appendRookMoves(self, result, originFile, originRank):
        # Moving across the rank:
        for file in File.All:
            if file != originFile:
                result.append(self._getMove(file, originRank))
        # Moving down the file:
        for rank in Rank.All:
            if rank != originRank:
                result.append(self._getMove(originFile, rank))

    def _appendBishopMoves(self, result, originFile, originRank):
        for step in range(1, 7):
            for fileDelta in -1,1:
                for rankDelta in -1,1:
                    destinationFile = originFile + step * fileDelta
                    destinationRank = originRank + step * rankDelta
                    if self._isWithinBoard(destinationFile, destinationRank):
                        result.append(self._getMove(destinationFile, destinationRank))

    def _getMove(self, destinationFile, destinationRank):
        return Move(self.Position, Square(destinationFile, destinationRank))

    def _isStartRank(self):
        return (self.Color == Color.White and self.Position.Rank == 2) or (self.Color == Color.Black and self.Position.Rank == 7)

    def _isWithinBoard(self, file, rank):
        return File.A <= file and file <= File.H and 1 <= rank and rank <= 8

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

class Kind:
    Pawn = 1
    Rook = 2
    Knight = 3
    Bishop = 4
    Queen = 5
    King = 6
