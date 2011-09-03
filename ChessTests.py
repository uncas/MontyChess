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

    def test_GetMoves_WhitePawnE2_2(self):
        piece = Piece(Color.White, Kind.Pawn, Square(File.E, 2))
        moves = piece.GetMoves()
        self.assertEqual(2, len(moves))

    def test_GetMoves_WhitePawnE3_1(self):
        piece = Piece(Color.White, Kind.Pawn, Square(File.E, 3))
        moves = piece.GetMoves()
        self.assertEqual(1, len(moves))

    def test_GetMoves_BlackPawnE7_2(self):
        piece = Piece(Color.Black, Kind.Pawn, Square(File.E, 7))
        moves = piece.GetMoves()
        self.assertEqual(2, len(moves))

    def test_GetMoves_BlackPawnE6_1(self):
        piece = Piece(Color.Black, Kind.Pawn, Square(File.E, 6))
        moves = piece.GetMoves()
        self.assertEqual(1, len(moves))

    def test_GetMoves_BlackPawnE2_1(self):
        piece = Piece(Color.Black, Kind.Pawn, Square(File.E, 2))
        moves = piece.GetMoves()
        self.assertEqual(1, len(moves))

    def test_GetMoves_WhitePawnE7_1(self):
        piece = Piece(Color.White, Kind.Pawn, Square(File.E, 7))
        moves = piece.GetMoves()
        self.assertEqual(1, len(moves))

    def test_GetMoves_WhiteRookA1_14(self):
        piece = Piece(Color.White, Kind.Rook, Square(File.A, 1))
        moves = piece.GetMoves()
        self.assertEqual(14, len(moves))


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

    def test_PossibleMoves_Ply1_20(self):
        moves = self.game.PossibleMoves()
        self.assertEqual(20, len(moves))
        for file in File.All:
            self.assertTrue(self.ContainsMove(moves, Move(Square(file, 2), Square(file, 3))))
            self.assertTrue(self.ContainsMove(moves, Move(Square(file, 2), Square(file, 4))))
        self.assertTrue(self.ContainsMove(moves, Move(Square(File.B, 1), Square(File.A, 3))))
        self.assertTrue(self.ContainsMove(moves, Move(Square(File.B, 1), Square(File.C, 3))))
        self.assertTrue(self.ContainsMove(moves, Move(Square(File.G, 1), Square(File.F, 3))))
        self.assertTrue(self.ContainsMove(moves, Move(Square(File.G, 1), Square(File.H, 3))))

    def test_PossibleMoves_Ply2_20(self):
        self.Ply1()
        moves = self.game.PossibleMoves()
        self.assertEqual(20, len(moves))

    def test_GetPiece_A2_IsPawn(self):
        pawnA2 = self.game.GetPiece(File.A, 2)
        self.assertEqual(Color.White, pawnA2.Color)
        self.assertEqual(Kind.Pawn, pawnA2.Kind)
        self.assertEqual(File.A, pawnA2.Position.File)
        self.assertEqual(2, pawnA2.Position.Rank)

    def test_GetPieceMoves_Ply1WhiteKnight_2(self):
        knightB1 = self.game.GetPiece(File.B, 1)
        knightB1Moves = self.game.GetPieceMoves(knightB1)
        self.assertEqual(2, len(knightB1Moves))
        self.assertTrue(self.ContainsMove(knightB1Moves, Move(Square(File.B, 1), Square(File.A, 3))))
        self.assertTrue(self.ContainsMove(knightB1Moves, Move(Square(File.B, 1), Square(File.C, 3))))

    def test_GetPieceMoves_Ply1WhitePawn_2(self):
        pawnA2 = self.game.GetPiece(File.A, 2)
        pawnA2Moves = self.game.GetPieceMoves(pawnA2)
        self.assertEqual(2, len(pawnA2Moves))
        self.assertTrue(self.ContainsMove(pawnA2Moves, Move(Square(File.A, 2), Square(File.A, 3))))
        self.assertTrue(self.ContainsMove(pawnA2Moves, Move(Square(File.A, 2), Square(File.A, 4))))

    def test_GetPieceMoves_Ply1WhiteRook_0(self):
        rookA1 = self.game.GetPiece(File.A, 1)
        rookA1Moves = self.game.GetPieceMoves(rookA1)
        self.assertEqual(0, len(rookA1Moves))

    def test_GetPieceMoves_Ply2BlackKnight_2(self):
        self.Ply1()
        knightB8 = self.game.GetPiece(File.B, 8)
        knightB8Moves = self.game.GetPieceMoves(knightB8)
        self.assertEqual(2, len(knightB8Moves))
        self.assertTrue(self.ContainsMove(knightB8Moves, Move(Square(File.B, 8), Square(File.A, 6))))
        self.assertTrue(self.ContainsMove(knightB8Moves, Move(Square(File.B, 8), Square(File.C, 6))))

    def test_GetPieceMoves_Ply2BlackPawn_2(self):
        self.Ply1()
        pawnA7 = self.game.GetPiece(File.A, 7)
        pawnA7Moves = self.game.GetPieceMoves(pawnA7)
        self.assertEqual(2, len(pawnA7Moves))
        self.assertTrue(self.ContainsMove(pawnA7Moves, Move(Square(File.A, 7), Square(File.A, 6))))
        self.assertTrue(self.ContainsMove(pawnA7Moves, Move(Square(File.A, 7), Square(File.A, 5))))

    def test_GetPieceMoves_Ply2WhitePawn_0(self):
        self.Ply1()
        pawnA2 = self.game.GetPiece(File.A, 2)
        pawnA2Moves = self.game.GetPieceMoves(pawnA2)
        self.assertEqual(0, len(pawnA2Moves))

    def x_test_GetPieceMoves_Ply3E4E5WhitePawnE4_0(self):
        self.game.Move(Square(File.E, 2), Square(File.E, 4))
        self.game.Move(Square(File.E, 7), Square(File.E, 5))
        pawnE4 = self.game.GetPiece(File.E, 4)
        pawnE4Moves = self.game.GetPieceMoves(pawnE4)
        self.assertEqual(0, len(pawnE4Moves))

#    def test_GetPieceMoves_Ply3E4E5WhiteKnighG1_3(self):
#    def test_GetPieceMoves_Ply3E4E5WhiteBishopF1_6(self):
#    def test_GetPieceMoves_Ply3E4E5WhiteQueenD1_5(self):

    def test_SideToPlay_Ply1_White(self):
        self.assertEqual(Color.White, self.game.SideToPlay)

    def test_SideToPlay_Ply2_Black(self):
        self.Ply1()
        self.assertEqual(Color.Black, self.game.SideToPlay)

    def test_SideToPlay_Ply3_White(self):
        self.Ply1()
        self.Ply2()
        self.assertEqual(Color.White, self.game.SideToPlay)

    def test_Move_E4_PawnIsMovedToE4(self):
        self.assertTrue(self.ContainsPiece(self.game.Pieces, Piece(Color.White, Kind.Pawn, Square(File.E, 2))))
        self.game.Move(Square(File.E, 2), Square(File.E, 4))
        self.assertFalse(self.ContainsPiece(self.game.Pieces, Piece(Color.White, Kind.Pawn, Square(File.E, 2))))
        self.assertTrue(self.ContainsPiece(self.game.Pieces, Piece(Color.White, Kind.Pawn, Square(File.E, 4))))

    def test_Move_NoPieceAtRequestedSquare_Exception(self):
        self.assertRaises(Exception, self.game.Move, Square(File.E, 4), Square(File.E, 5))

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
            if self.SameSquare(m.Origin, move.Origin) and self.SameSquare(m.Destination, move.Destination):
                return True
        return False

    def ContainsPiece(self, pieces, piece):
        for p in pieces:
            if p.Kind == piece.Kind and self.SameSquare(p.Position, piece.Position):
                return True
        return False

    def Ply1(self):
        self.game.Move(Square(File.E, 2), Square(File.E, 4))

    def Ply2(self):
        self.game.Move(Square(File.E, 7), Square(File.E, 5))

    def SameSquare(self, square1, square2):
        return square1.File == square2.File and square1.Rank == square2.Rank


if __name__ == "__main__":
    unittest.main()
