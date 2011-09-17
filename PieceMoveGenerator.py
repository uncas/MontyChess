from Move import *
from Piece import *
from Square import *

class PieceMoveGenerator:
    
    KnightSteps = Step(-2,-1), Step(-2,1), Step(-1,-2), Step(-1,2), Step(1,-2), Step(1,2), Step(2,-1), Step(2,1)

    def __init__(self, board):
        self._board = board

    def GetCaptureMoves(self, piece):
        if not piece.IsPawn:
            # TODO: Return proper CaptureMove here:
            return self.GetMoves(piece)
        result = []
        originFile = piece.Position.File
        originRank = piece.Position.Rank
        # TODO: Return proper CaptureMove or EnPassantMove here:
        if originFile > File.A:
            if self._canMakePromotionMove(piece):
                for kind in Kind.Rook, Kind.Queen, Kind.Bishop, Kind.Knight:
                    result.append(Move.Promotion(self._board, piece, Square(originFile - 1, originRank + piece.Direction), kind))
            else:
                result.append(self._getMove(piece, originFile - 1, originRank + piece.Direction))
        if originFile < File.H:
            if self._canMakePromotionMove(piece):
                for kind in Kind.Rook, Kind.Queen, Kind.Bishop, Kind.Knight:
                    result.append(Move.Promotion(self._board, piece, Square(originFile + 1, originRank + piece.Direction), kind))
            else:
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
        for knightStep in PieceMoveGenerator.KnightSteps:
            destinationFile = originFile + knightStep.FileDelta
            destinationRank = originRank + knightStep.RankDelta
            if Square.WithinBoard(destinationFile, destinationRank):
                result.append(self._getMove(piece, destinationFile, destinationRank))

    def _appendPawnMoves(self, piece, result, originFile, originRank):
        if self._canMakePromotionMove(piece):
            destination = Square(originFile, originRank + piece.Direction)
            for kind in Kind.Rook, Kind.Queen, Kind.Bishop, Kind.Knight:
                result.append(Move.Promotion(self._board, piece, destination, kind))
            return
        result.append(self._getMove(piece, originFile, originRank + piece.Direction))
        if piece.IsAtStartRank():
            result.append(self._getMove(piece, originFile, originRank + 2 * piece.Direction))

    def _canMakePromotionMove(self, piece):
        return (piece.Color == Color.White and piece.Position.Rank == 7) \
                or (piece.Color == Color.Black and piece.Position.Rank == 2)

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
