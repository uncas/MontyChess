from Move import *
from Square import *

class Piece:
    
    def __init__(self, color, kind, position):
        self.Color = color
        self.Kind = kind
        self.Position = position
        self.CanJump = kind == Kind.Knight

    def GetCaptureMoves(self):
        if self.Kind != Kind.Pawn:
            return self.GetMoves()
        result = []
        direction = 3 - 2 * self.Color
        originFile = self.Position.File
        originRank = self.Position.Rank
        if originFile > File.A:
            result.append(self.GetMove(originFile - 1, originRank + direction))
        if originFile < File.H:
            result.append(self.GetMove(originFile + 1, originRank + direction))
        return result

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
            self.AppendRookMoves(result, originFile, originRank)
        if self.Kind == Kind.Bishop:
            self.AppendBishopMoves(result, originFile, originRank)
        if self.Kind == Kind.Queen:
            self.AppendRookMoves(result, originFile, originRank)
            self.AppendBishopMoves(result, originFile, originRank)
        if self.Kind == Kind.King:
            for fileDelta in -1,0,1:
                for rankDelta in -1,0,1:
                    if fileDelta == 0 and rankDelta == 0:
                        continue
                    destinationFile = originFile + fileDelta
                    destinationRank = originRank + rankDelta
                    if File.A <= destinationFile and destinationFile <= File.H and 1 <= destinationRank and destinationRank <= 8:
                        result.append(self.GetMove(destinationFile, destinationRank))
        return result

    def AppendRookMoves(self, result, originFile, originRank):
        # Moving across the rank:
        for file in File.All:
            if file != originFile:
                result.append(self.GetMove(file, originRank))
        # Moving down the file:
        for rank in Rank.All:
            if rank != originRank:
                result.append(self.GetMove(originFile, rank))

    def AppendBishopMoves(self, result, originFile, originRank):
        for step in range(1, 7):
            for fileDelta in -1,1:
                for rankDelta in -1,1:
                    destinationFile = originFile + step * fileDelta
                    destinationRank = originRank + step * rankDelta
                    if File.A <= destinationFile and destinationFile <= File.H and 1 <= destinationRank and destinationRank <= 8:
                        result.append(self.GetMove(destinationFile, destinationRank))

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
