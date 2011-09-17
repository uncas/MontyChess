from Move import *
from Square import *


class Piece:
    
    KnightSteps = Step(-2,-1), Step(-2,1), Step(-1,-2), Step(-1,2), Step(1,-2), Step(1,2), Step(2,-1), Step(2,1)

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
        self._pieceMoveGenerator = PieceMoveGenerator()

    def __repr__(self):
        return self._colorString() + " " + self._kindString()

    def __eq__(self, other):
        if self is None or other is None:
            return False
        return self.Kind == other.Kind and self.Color == other.Color and self.Position == other.Position

    def GetCaptureMoves(self):
        return self._pieceMoveGenerator.GetCaptureMoves(self)

    def GetMoves(self):
        return self._pieceMoveGenerator.GetMoves(self)

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


class PieceMoveGenerator:
    
    def GetCaptureMoves(self, piece):
        #        return Piece.GetPieceCaptureMoves()
        #   @staticmethod
        #  def GetPieceCaptureMoves():
        if not piece.IsPawn:
            # TODO: Return proper CaptureMove here:
            return self.GetMoves(piece)
        result = []
        originFile = piece.Position.File
        originRank = piece.Position.Rank
        # TODO: Return proper CaptureMove or EnPassantMove here:
        if originFile > File.A:
            result.append(self._getMove(piece, originFile - 1, originRank + piece.Direction))
        if originFile < File.H:
            result.append(self._getMove(piece, originFile + 1, originRank + piece.Direction))
        return result

    def GetMoves(self, piece):
        result = []
        originFile = piece.Position.File
        originRank = piece.Position.Rank
        if piece.IsPawn:
            self._appendPawnMoves(piece, result, originFile, originRank)
        if piece.IsKnight:
            self._appendKnightMoves(piece, result, originFile, originRank)
        if piece.IsRook:
            self._appendRookMoves(piece, result, originFile, originRank)
        if piece.IsBishop:
            self._appendBishopMoves(piece, result, originFile, originRank)
        if piece.IsQueen:
            self._appendRookMoves(piece, result, originFile, originRank)
            self._appendBishopMoves(piece, result, originFile, originRank)
        if piece.IsKing:
            self._appendKingMoves(piece, result, originFile, originRank)
        return result

    def _appendKnightMoves(self, piece,result, originFile, originRank):
        for knightStep in Piece.KnightSteps:
            destinationFile = originFile + knightStep.FileDelta
            destinationRank = originRank + knightStep.RankDelta
            if Square.WithinBoard(destinationFile, destinationRank):
                result.append(self._getMove(piece, destinationFile, destinationRank))

    def _appendPawnMoves(self, piece, result, originFile, originRank):
        result.append(self._getMove(piece, originFile, originRank + piece.Direction))
        if piece.IsAtStartRank():
            result.append(self._getMove(piece, originFile, originRank + 2 * piece.Direction))

    def _appendKingMoves(self, piece, result, originFile, originRank):
        for fileDelta in -1,0,1:
            for rankDelta in -1,0,1:
                if fileDelta == 0 and rankDelta == 0:
                    continue
                destinationFile = originFile + fileDelta
                destinationRank = originRank + rankDelta
                if Square.WithinBoard(destinationFile, destinationRank):
                    result.append(self._getMove(piece, destinationFile, destinationRank))

    def _appendRookMoves(self, piece, result, originFile, originRank):
        # Moving across the rank:
        for file in File.All:
            if file != originFile:
                result.append(self._getMove(piece, file, originRank))
        # Moving down the file:
        for rank in Rank.All:
            if rank != originRank:
                result.append(self._getMove(piece, originFile, rank))

    def _appendBishopMoves(self, piece, result, originFile, originRank):
        for step in range(1, 7):
            for fileDelta in -1,1:
                for rankDelta in -1,1:
                    destinationFile = originFile + step * fileDelta
                    destinationRank = originRank + step * rankDelta
                    if Square.WithinBoard(destinationFile, destinationRank):
                        result.append(self._getMove(piece, destinationFile, destinationRank))

    def _getMove(self, piece, destinationFile, destinationRank):
        return Move.Normal(piece, Square(destinationFile, destinationRank))


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
