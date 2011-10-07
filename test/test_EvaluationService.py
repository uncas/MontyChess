import sys
import unittest

sys.path.append("../src")

from ChessEngine import *
from ChessGame import *

class EvaluationServiceTests(unittest.TestCase):

    def setUp(self):
        self._evaluationService = EvaluationService()

    def test_Evaluation_InitialBoard_0(self):
        game = ChessGame()
        evaluation = self._evaluationService.Evaluate(game)
        self.assertEqual(0, evaluation)

    def test_Evaluation_WhiteCapturedPawn_Positive(self):
        game = ChessGame()
        game.Move(Square(File.D, 2), Square(File.D, 4))
        game.Move(Square(File.E, 7), Square(File.E, 5))
        game.Move(Square(File.D, 4), Square(File.E, 5))
        evaluation = self._evaluationService.Evaluate(game)
        self.assertGreater(evaluation, 0)


if __name__ == "__main__":
    unittest.main()
