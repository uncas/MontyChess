import sys
import unittest

sys.path.append("../src")

from ChessGame import *

class test_ThreatCalculator(unittest.TestCase):

    def test_IsSquareThreatenedByColor_InitialBoardA4ByWhite_No(self):
        board = Board()
        calculator = ThreatCalculator(board)
        isThreatened = calculator.IsSquareThreatenedByColor(Square(File.A, 4), Color.White)
        self.assertFalse(isThreatened)

    def test_IsSquareThreatenedByColor_InitialBoardA3ByWhite_No(self):
        board = Board()
        calculator = ThreatCalculator(board)
        isThreatened = calculator.IsSquareThreatenedByColor(Square(File.A, 3), Color.White)
        self.assertTrue(isThreatened)

    def test_IsSquareThreatenedByColor_InitialBoardA3ByBlack_No(self):
        board = Board()
        calculator = ThreatCalculator(board)
        isThreatened = calculator.IsSquareThreatenedByColor(Square(File.A, 3), Color.Black)
        self.assertFalse(isThreatened)

    def test_IsSquareThreatenedByColor_AfterE4ByWhiteD5_Yes(self):
        board = Board()
        calculator = ThreatCalculator(board)
        move = Move.Normal(board.GetPiece(Square(File.E, 2)), Square(File.E, 4))
        move.Apply()
        isThreatened = calculator.IsSquareThreatenedByColor(Square(File.D, 5), Color.White)
        self.assertTrue(isThreatened)

    def test_IsSquareThreatenedByColor_AfterNF3ByWhiteE5_Yes(self):
        board = Board()
        calculator = ThreatCalculator(board)
        move = Move.Normal(board.GetPiece(Square(File.G, 1)), Square(File.F, 3))
        move.Apply()
        isThreatened = calculator.IsSquareThreatenedByColor(Square(File.E, 5), Color.White)
        self.assertTrue(isThreatened)

    def test_IsSquareThreatenedByColor_AfterE4ByWhiteA6_Yes(self):
        board = Board()
        calculator = ThreatCalculator(board)
        move = Move.Normal(board.GetPiece(Square(File.E, 2)), Square(File.E, 4))
        move.Apply()
        isThreatened = calculator.IsSquareThreatenedByColor(Square(File.A, 6), Color.White)
        self.assertTrue(isThreatened)

    def test_IsSquareThreatenedByColor_AfterE4ByWhiteH5_Yes(self):
        board = Board()
        calculator = ThreatCalculator(board)
        move = Move.Normal(board.GetPiece(Square(File.E, 2)), Square(File.E, 4))
        move.Apply()
        isThreatened = calculator.IsSquareThreatenedByColor(Square(File.H, 5), Color.White)
        self.assertTrue(isThreatened)

    def test_IsSquareThreatenedByColor_AfterA4ByWhiteA4_Yes(self):
        board = Board()
        calculator = ThreatCalculator(board)
        move = Move.Normal(board.GetPiece(Square(File.A, 2)), Square(File.A, 4))
        move.Apply()
        isThreatened = calculator.IsSquareThreatenedByColor(Square(File.A, 4), Color.White)
        self.assertTrue(isThreatened)


if __name__ == "__main__":
    unittest.main()
