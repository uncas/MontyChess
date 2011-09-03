import unittest

from Board import *
from ChessGame import *
from Move import *
from Piece import *


class BoardTests(unittest.TestCase):

    def test_Square_A1(self):
        square = Square(File.A, 1)
        self.assertEqual(File.A, square.File)
        self.assertEqual(1, square.Rank)


class PieceTests(unittest.TestCase):

    def test_Piece_WhiteRookA1(self):
        piece = Piece(Color.White, Kind.Rook, Square(File.A, 1))
        self.assertEqual(Color.White, piece.Color)
        self.assertEqual(Kind.Rook, piece.Kind)
        self.assertEqual(File.A, piece.Position.File)
        self.assertEqual(1, piece.Position.Rank)


class ChessTests(unittest.TestCase):

    def setUp(self):
        self.game = ChessGame()

    def test_Pieces_InitialGame_32(self):
        pieces = self.game.Pieces
        self.assertEquals(32, len(pieces))
        for file in File.All:
            for colorAndRank in (Color.White, 2), (Color.Black, 7):
                color = colorAndRank[0]
                rank = colorAndRank[1]
                self.assertTrue(self.ContainsPiece(pieces, Piece(color, Kind.Pawn, Square(file, rank))))
        for colorAndRank in (Color.White, 1), (Color.Black, 8):
            color = colorAndRank[0]
            rank = colorAndRank[1]
            self.AssertInitialOfficers(pieces, color, rank)

    def test_PossibleMoves_InitialGame_20(self):
        moves = self.game.PossibleMoves()
        self.assertEqual(20, len(moves))
        for file in File.All:
            self.assertTrue(self.ContainsMove(moves, Move(Square(file, 2), Square(file, 3))))
            self.assertTrue(self.ContainsMove(moves, Move(Square(file, 2), Square(file, 4))))
        self.assertTrue(self.ContainsMove(moves, Move(Square(File.B, 1), Square(File.A, 3))))
        self.assertTrue(self.ContainsMove(moves, Move(Square(File.B, 1), Square(File.C, 3))))
        self.assertTrue(self.ContainsMove(moves, Move(Square(File.G, 1), Square(File.F, 3))))
        self.assertTrue(self.ContainsMove(moves, Move(Square(File.G, 1), Square(File.H, 3))))

#    def test_GetPiece_A2_IsPawn(self):
#        pawnA2 = self.game.GetPiece(File.A, 2)
#        self.assertEqual(Kind.Pawn, pawnA2.Kind)

    def test_PawnMove_InitialGame_2(self):
        pawnA2 = self.game.GetPiece(File.A, 2)
        pawnA2Moves = self.game.GetPieceMoves(pawnA2)
        self.assertEqual(2, len(pawnA2Moves))

    def AssertInitialOfficers(self, pieces, color, rank):
        for file in (File.A, File.H):
            self.assertTrue(self.ContainsPiece(pieces, Piece(color, Kind.Rook, Square(file, rank))))
        for file in (File.B, File.G):
            self.assertTrue(self.ContainsPiece(pieces, Piece(color, Kind.Knight, Square(file, rank))))
        for file in (File.C, File.F):
            self.assertTrue(self.ContainsPiece(pieces, Piece(color, Kind.Bishop, Square(file, rank))))
        self.assertTrue(self.ContainsPiece(pieces, Piece(color, Kind.Queen, Square(File.D, rank))))
        self.assertTrue(self.ContainsPiece(pieces, Piece(color, Kind.King, Square(File.E, rank))))

    def ContainsMove(self, moves, move):
        for m in moves:
            if self.SameSquare(m.From, move.From) and self.SameSquare(m.To, move.To):
                return True
        return False

    def ContainsPiece(self, pieces, piece):
        for p in pieces:
            if p.Kind == piece.Kind and self.SameSquare(p.Position, piece.Position):
                return True
        return False

    def SameSquare(self, square1, square2):
        return square1.File == square2.File and square1.Rank == square2.Rank


if __name__ == "__main__":
    unittest.main()
