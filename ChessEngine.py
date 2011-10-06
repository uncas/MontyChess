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
        return sign * MaterialEvaluation.Pieces[piece.Kind]


class MaterialEvaluation:
    Pawn = 1.0
    Knight = 3.0
    Bishop = 3.0
    Rook = 4.5
    Queen = 9.0
    King = 100.0
    Pieces = {Kind.Pawn: Pawn, Kind.Knight: Knight, Kind.Bishop: Bishop, Kind.Rook: Rook, Kind.Queen: Queen, Kind.King: King}
