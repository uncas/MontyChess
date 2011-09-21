from Piece import *


class ChessEngine:

    def __init__(self, game):
        self._game = game
        self._evaluationService = EvaluationService()

    def BestMoves(self, count):
        reverse = self._game.SideToPlay == Color.White
        result = []
        moves = self._game.PossibleMoves()
        for move in moves:
            result.append(MoveEvaluation(move, self._evaluateMove(move)))
        sortedResult = sorted(result, key=lambda move: move.Evaluation, reverse=reverse)
        return sortedResult[:count]

    def _evaluateMove(self, move):
        self._game.ApplyMove(move)
        moves = self._game.PossibleMoves()
        nextEvaluations = []
        for nextMove in moves:
            self._game.ApplyMove(nextMove)
            nextEvaluation = self._evaluationService.Evaluate(self._game)
            self._game.RevertMove(nextMove)
            nextEvaluations.append(nextEvaluation)
        self._game.RevertMove(move)
        if self._game.SideToPlay == Color.White:
            return max(nextEvaluations)
        else:
            return min(nextEvaluations)


class MoveEvaluation:

    def __init__(self, move, evaluation):
        self.Move = move
        self.Evaluation = evaluation


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
