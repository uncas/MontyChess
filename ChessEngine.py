from Piece import *


class ChessEngine:

    def __init__(self, game):
        self._game = game

    def BestMoves(self, count):
        possibleMoves = self._game.PossibleMoves()
        return possibleMoves[:count]


class EvaluationService:

    def Evaluate(self, game):
        pieces = game.Pieces
        result = 0
        for piece in pieces:
            result += self._getPieceEvaluation(piece)
        return result

    def _getPieceEvaluation(self, piece):
        sign = 3 - 2 * piece.Color
        return sign * self._getKindEvaluation(piece.Kind)

    def _getKindEvaluation(self, kind):
        if kind == Kind.Pawn:
            return 1.0
        elif kind == Kind.Knight:
            return 3.0
        elif kind == Kind.Bishop:
            return 3.0
        elif kind == Kind.Rook:
            return 4.5
        elif kind == Kind.Queen:
            return 9.0
        elif kind == Kind.King:
            return 100.0
