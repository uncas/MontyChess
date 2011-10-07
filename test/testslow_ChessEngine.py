import sys
import unittest

sys.path.append("../src")

from ChessEngine import *
from ChessGame import *

class ChessEngineTests(unittest.TestCase):

    def setUp(self):
        self._game = ChessGame()
        self._engine = ChessEngine(self._game)

    def test_3BestMoves_Returns3Moves(self):
        bestMoves = self._engine.BestMoves(3)
        self.assertEqual(3, len(bestMoves))

    def test_10PlySequence_WithoutErrors(self):
        for moveIndex in range(10):
            bestMoves = self._engine.BestMoves(1)
            move = bestMoves[0].Move
            self._game.ApplyMove(move)

    def test_WhiteCanCapturePawn_CaptureIsBestMove(self):
        self._game.Move(Square(File.D, 2), Square(File.D, 4))
        self._game.Move(Square(File.E, 7), Square(File.E, 5))

        bestMoves = self._engine.BestMoves(1)

        piece = self._game.GetPiece(File.D, 4)
        expected = Move(piece, Square(File.E, 5))
        self.assertEqual(1, len(bestMoves))
        self.assertEqual(expected, bestMoves[0].Move)

    def test_WhiteCanGiveAwayPawn_OtherMovesAreBetter(self):
        self._game.Move(Square(File.A, 2), Square(File.A, 4))
        self._game.Move(Square(File.A, 7), Square(File.A, 5))
        self._game.Move(Square(File.B, 2), Square(File.B, 3))
        self._game.Move(Square(File.B, 7), Square(File.B, 6))

        bestMoves = self._engine.BestMoves(1)

        piece = self._game.GetPiece(File.B, 3)
        #        print(bestMoves[0].Move)
        notExpected = Move(piece, Square(File.B, 4))
        self.assertEqual(1, len(bestMoves))
        self.assertNotEqual(notExpected, bestMoves[0].Move)


if __name__ == "__main__":
    unittest.main()
