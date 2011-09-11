import unittest

from Board import *
from ChessGame import *
from Move import *
from Piece import *


class ThreatCalculatorTests(unittest.TestCase):

    def test_IsSquareThreatenedByColor_InitialBoardA4ByWhite_No(self):
        board = Board()
        calculator = ThreatCalculator(board)
        isThreatened = calculator.IsSquareThreatenedByColor(Square(File.A, 4), Color.White)
        self.assertFalse(isThreatened)


class MoveTests(unittest.TestCase):

    def test_Apply(self):
        # Arrange:
        board = Board()
        pawnA2 = board.GetPiece(Square(File.A, 2))
        move = Move.Normal(pawnA2, Square(File.A, 3))
        # Act:
        move.Apply()
        # Assert:
        self.assertEqual(File.A, pawnA2.Position.File)
        self.assertEqual(3, pawnA2.Position.Rank)
        self.assertEqual(2, move.Origin.Rank)
        self.assertTrue(pawnA2.HasMoved)

    def test_Revert(self):
        # Arrange:
        board = Board()
        pawnA2 = board.GetPiece(Square(File.A, 2))
        move = Move.Normal(pawnA2, Square(File.A, 3))
        move.Apply()
        # Act:
        move.Revert()
        # Assert:
        self.assertEqual(File.A, pawnA2.Position.File)
        self.assertEqual(2, pawnA2.Position.Rank)
        self.assertEqual(2, move.Origin.Rank)
        self.assertEqual(3, move.Destination.Rank)
        self.assertFalse(pawnA2.HasMoved)

    def test_Capture(self):
        # Arrange:
        board = Board()
        pawnA2 = board.GetPiece(Square(File.A, 2))
        move = Move.Normal(pawnA2, Square(File.A, 4))
        move.Apply()
        pawnB7 = board.GetPiece(Square(File.B, 7))
        move = Move.Normal(pawnB7, Square(File.B, 5))
        move.Apply()
        move = Move.Capture(board, pawnA2, Square(File.B, 5), pawnB7)
        # Act:
        move.Apply()
        # Assert:
        self.assertEqual(File.B, pawnA2.Position.File)
        self.assertEqual(5, pawnA2.Position.Rank)
        self.assertTrue(pawnA2.HasMoved)
        self.assertEqual(31, len(board.Pieces))

    def test_CaptureRevert(self):
        # Arrange:
        board = Board()
        pawnA2 = board.GetPiece(Square(File.A, 2))
        move = Move.Normal(pawnA2, Square(File.A, 4))
        move.Apply()
        pawnB7 = board.GetPiece(Square(File.B, 7))
        move = Move.Normal(pawnB7, Square(File.B, 5))
        move.Apply()
        move = Move.Capture(board, pawnA2, Square(File.B, 5), pawnB7)
        move.Apply()
        self.assertEqual(File.B, pawnA2.Position.File)
        # Act:
        move.Revert()
        # Assert:
        self.assertEqual(File.A, pawnA2.Position.File)
        self.assertEqual(4, pawnA2.Position.Rank)
        self.assertEqual(32, len(board.Pieces))


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

    def test_GetCaptureMoves_WhitePawnE2_2(self):
        piece = Piece(Color.White, Kind.Pawn, Square(File.E, 2))
        moves = piece.GetCaptureMoves()
        self.assertEqual(2, len(moves))

    def test_GetCaptureMoves_WhitePawnA2_1(self):
        piece = Piece(Color.White, Kind.Pawn, Square(File.A, 2))
        moves = piece.GetCaptureMoves()
        self.assertEqual(1, len(moves))

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

    def test_GetMoves_WhiteKnightB1_3(self):
        piece = Piece(Color.White, Kind.Knight, Square(File.B, 1))
        moves = piece.GetMoves()
        self.assertEqual(3, len(moves))

    def test_GetMoves_WhiteBishopC1_7(self):
        piece = Piece(Color.White, Kind.Bishop, Square(File.C, 1))
        moves = piece.GetMoves()
        self.assertEqual(7, len(moves))

    def test_GetMoves_WhiteQueenD1_21(self):
        piece = Piece(Color.White, Kind.Queen, Square(File.D, 1))
        moves = piece.GetMoves()
        self.assertEqual(21, len(moves))

    def test_GetMoves_WhiteKingE1_5(self):
        piece = Piece(Color.White, Kind.King, Square(File.E, 1))
        moves = piece.GetMoves()
        self.assertEqual(5, len(moves))


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
                self.assertTrue(Piece(color, Kind.Pawn, Square(file, rank)) in pieces)
        for colorAndRank in (Color.White, 1), (Color.Black, 8):
            color = colorAndRank[0]
            rank = colorAndRank[1]
            self._assertInitialOfficers(pieces, color, rank)

    def test_PossibleMoves_Ply1_20(self):
        moves = self._possibleMoves()
        self.assertEqual(20, len(moves))
        for file in File.All:
            self.assertTrue(self._getMove(Square(file, 2), Square(file, 3)) in moves)
            self.assertTrue(self._getMove(Square(file, 2), Square(file, 4)) in moves)
        self.assertTrue(self._getMove(Square(File.B, 1), Square(File.A, 3)) in moves)
        self.assertTrue(self._getMove(Square(File.B, 1), Square(File.C, 3)) in moves)
        self.assertTrue(self._getMove(Square(File.G, 1), Square(File.F, 3)) in moves)
        self.assertTrue(self._getMove(Square(File.G, 1), Square(File.H, 3)) in moves)

    def test_PossibleMoves_Ply2_20(self):
        self._ply1()
        moves = self._possibleMoves()
        self.assertEqual(20, len(moves))

    def test_PossibleMoves_Ply3_29(self):
        self._ply1()
        self._ply2()
        moves = self._possibleMoves()
        self.assertEqual(29, len(moves))

    def test_PossibleMoves_Ply4_30(self):
        self._ply1()
        self._ply2()
        self._ply3()
        self.assertEqual(32, len(self.game.Pieces))
        moves = self._possibleMoves()
        self.assertEqual(30, len(moves))

    def test_PossibleMoves_Ply5_38(self):
        self._ply1()
        self._ply2()
        self._ply3()
        self._ply4()
        self.assertEqual(31, len(self.game.Pieces))
        moves = self._possibleMoves()
        self.assertEqual(38, len(moves))

    def test_GetPiece_A2_IsPawn(self):
        pawnA2 = self.game.GetPiece(File.A, 2)
        self.assertEqual(Color.White, pawnA2.Color)
        self.assertEqual(Kind.Pawn, pawnA2.Kind)
        self.assertEqual(File.A, pawnA2.Position.File)
        self.assertEqual(2, pawnA2.Position.Rank)

    def test_GetPieceMoves_Ply1WhiteKnight_2(self):
        knightB1Moves = self._getPieceMoves(File.B, 1)
        self.assertEqual(2, len(knightB1Moves))
        self.assertTrue(self._getMove(Square(File.B, 1), Square(File.A, 3)) in knightB1Moves)
        self.assertTrue(self._getMove(Square(File.B, 1), Square(File.C, 3)) in knightB1Moves)

    def test_GetPieceMoves_Ply1WhitePawn_2(self):
        pawnA2Moves = self._getPieceMoves(File.A, 2)
        self.assertEqual(2, len(pawnA2Moves))
        self.assertTrue(self._getMove(Square(File.A, 2), Square(File.A, 3)) in pawnA2Moves)
        self.assertTrue(self._getMove(Square(File.A, 2), Square(File.A, 4)) in pawnA2Moves)

    def test_GetPieceMoves_Ply1WhiteRook_0(self):
        rookA1Moves = self._getPieceMoves(File.A, 1)
        self.assertEqual(0, len(rookA1Moves))

    def test_GetPieceMoves_Ply2BlackKnight_2(self):
        self._ply1()
        knightB8Moves = self._getPieceMoves(File.B, 8)
        self.assertEqual(2, len(knightB8Moves))
        self.assertTrue(self._getMove(Square(File.B, 8), Square(File.A, 6)) in knightB8Moves)
        self.assertTrue(self._getMove(Square(File.B, 8), Square(File.C, 6)) in knightB8Moves)

    def test_GetPieceMoves_Ply2BlackPawn_2(self):
        self._ply1()
        pawnA7Moves = self._getPieceMoves(File.A, 7)
        self.assertEqual(2, len(pawnA7Moves))
        self.assertTrue(self._getMove(Square(File.A, 7), Square(File.A, 6)) in pawnA7Moves)
        self.assertTrue(self._getMove(Square(File.A, 7), Square(File.A, 5)) in pawnA7Moves)

    def test_GetPieceMoves_Ply2BlackRook_0(self):
        self._ply1()
        rookMoves = self._getPieceMoves(File.A, 8)
        self.assertEqual(0, len(rookMoves))

    def test_GetPieceMoves_Ply2WhitePawn_0(self):
        self._ply1()
        pawnA2Moves = self._getPieceMoves(File.A, 2)
        self.assertEqual(0, len(pawnA2Moves))

    def test_GetPieceMoves_Ply3E4E5WhitePawnE4_0(self):
        self._ply1()
        self._ply2()
        pawnE4Moves = self._getPieceMoves(File.E, 4)
        self.assertEqual(0, len(pawnE4Moves))

    def test_GetPieceMoves_Ply3E4E5WhiteKnightG1_3(self):
        self._ply1()
        self._ply2()
        knightMoves = self._getPieceMoves(File.G, 1)
        self.assertEqual(3, len(knightMoves))

    def test_GetPieceMoves_Ply3E4E5WhiteBishopF1_5(self):
        self._ply1()
        self._ply2()
        bishopMoves = self._getPieceMoves(File.F, 1)
        self.assertEqual(5, len(bishopMoves))

    def test_GetPieceMoves_Ply3E4E5WhiteKingE1_1(self):
        self._ply1()
        self._ply2()
        kingMoves = self._getPieceMoves(File.E, 1)
        self.assertEqual(1, len(kingMoves))

    def test_GetPieceMoves_Ply3E4E5WhiteQueenD1_4(self):
        self._ply1()
        self._ply2()
        queenMoves = self._getPieceMoves(File.D, 1)
        self.assertEqual(4, len(queenMoves))

    def test_SideToPlay_Ply1_White(self):
        self.assertEqual(Color.White, self.game.SideToPlay)

    def test_SideToPlay_Ply2_Black(self):
        self._ply1()
        self.assertEqual(Color.Black, self.game.SideToPlay)

    def test_SideToPlay_Ply3_White(self):
        self._ply1()
        self._ply2()
        self.assertEqual(Color.White, self.game.SideToPlay)

    def test_Move_E4_PawnIsMovedToE4(self):
        self.assertTrue(Piece(Color.White, Kind.Pawn, Square(File.E, 2)) in self.game.Pieces)
        self._ply1()
        self.assertFalse(Piece(Color.White, Kind.Pawn, Square(File.E, 2)) in self.game.Pieces)
        self.assertTrue(Piece(Color.White, Kind.Pawn, Square(File.E, 4)) in self.game.Pieces)

    def test_Move_NoPieceAtRequestedSquare_Exception(self):
        self.assertRaises(Exception, self._move, Square(File.E, 4), Square(File.E, 5))

    def test_GetPieceMoves_InLastPlyAnOpponentPawnTookADoubleStepToTheSquareNextToThePawn_EnPassantIsPossible(self):
        self._move(Square(File.E, 2), Square(File.E, 4))
        self._move(Square(File.E, 7), Square(File.E, 6))
        self._move(Square(File.E, 4), Square(File.E, 5))
        self._move(Square(File.D, 7), Square(File.D, 5))
        pawnMoves = self._getPieceMoves(File.E, 5)
        self.assertEqual(1, len(pawnMoves))

    def test_GetPieceMoves_InLastPlyAnOpponentPawnTookASingleStepToTheSquareNextToThePawn_EnPassantIsNotPossible(self):
        self._move(Square(File.E, 2), Square(File.E, 4))
        self._move(Square(File.E, 7), Square(File.E, 6))
        self._move(Square(File.E, 4), Square(File.E, 5))
        self._move(Square(File.D, 7), Square(File.D, 6))
        self._move(Square(File.D, 2), Square(File.D, 4))
        self._move(Square(File.D, 6), Square(File.D, 5))
        pawnMoves = self._getPieceMoves(File.E, 5)
        self.assertEqual(0, len(pawnMoves))

    def test_GetPieceMoves_InEarlierPlyAnOpponentPawnTookADoubleStepToTheSquareNextToThePawn_EnPassantIsNotPossible(self):
        self._move(Square(File.E, 2), Square(File.E, 4))
        self._move(Square(File.D, 7), Square(File.D, 5))
        self._move(Square(File.E, 4), Square(File.E, 5))
        self._move(Square(File.E, 7), Square(File.E, 6))
        pawnMoves = self._getPieceMoves(File.E, 5)
        self.assertEqual(0, len(pawnMoves))

    def test_GetPieceMoves_EmptyBetweenKingAndRook_CastlingIsPossible(self):
        self._move(Square(File.E, 2), Square(File.E, 4))
        self._move(Square(File.E, 7), Square(File.E, 5))
        self._move(Square(File.G, 1), Square(File.F, 3))
        self._move(Square(File.B, 8), Square(File.C, 6))
        self._move(Square(File.F, 1), Square(File.B, 5))
        self._move(Square(File.G, 8), Square(File.F, 6))
        kingMoves = self._getPieceMoves(File.E, 1)
        self.assertEqual(3, len(kingMoves))

    def test_GetPieceMoves_RookAlreadyMoved_CastlingIsNotPossible(self):
        self._move(Square(File.E, 2), Square(File.E, 4))
        self._move(Square(File.E, 7), Square(File.E, 5))
        self._move(Square(File.G, 1), Square(File.F, 3))
        self._move(Square(File.B, 8), Square(File.C, 6))
        self._move(Square(File.F, 1), Square(File.B, 5))
        self._move(Square(File.G, 8), Square(File.F, 6))
        self._move(Square(File.H, 1), Square(File.G, 1))
        self._move(Square(File.D, 7), Square(File.D, 6))
        self._move(Square(File.G, 1), Square(File.H, 1))
        self._move(Square(File.D, 6), Square(File.D, 5))
        kingMoves = self._getPieceMoves(File.E, 1)
        self.assertEqual(2, len(kingMoves))

    def test_GetPiece_Castling_KingAndRookHaveMoved(self):
        self._move(Square(File.E, 2), Square(File.E, 4))
        self._move(Square(File.E, 7), Square(File.E, 5))
        self._move(Square(File.G, 1), Square(File.F, 3))
        self._move(Square(File.B, 8), Square(File.C, 6))
        self._move(Square(File.F, 1), Square(File.B, 5))
        self._move(Square(File.G, 8), Square(File.F, 6))
        self._move(Square(File.E, 1), Square(File.G, 1))
        king = self._getPiece(File.G, 1)
        self.assertIsNotNone(king)
        rook = self._getPiece(File.F, 1)
        self.assertIsNotNone(rook)

    def test_GetPieceMoves_EmptyBetweenKingAndQueenSideRook_CastlingIsPossible(self):
        self._move(Square(File.D, 2), Square(File.D, 4))
        self._move(Square(File.D, 7), Square(File.D, 5))
        self._move(Square(File.B, 1), Square(File.C, 3))
        self._move(Square(File.B, 8), Square(File.C, 6))
        self._move(Square(File.C, 1), Square(File.F, 4))
        self._move(Square(File.G, 8), Square(File.F, 6))
        self._move(Square(File.D, 1), Square(File.D, 2))
        self._move(Square(File.E, 7), Square(File.E, 6))
        kingMoves = self._getPieceMoves(File.E, 1)
        self.assertEqual(2, len(kingMoves))

    def test_GetPieceMoves_QueenSideCastling_KingAndRookHaveMoved(self):
        self._move(Square(File.D, 2), Square(File.D, 4))
        self._move(Square(File.D, 7), Square(File.D, 5))
        self._move(Square(File.B, 1), Square(File.C, 3))
        self._move(Square(File.B, 8), Square(File.C, 6))
        self._move(Square(File.C, 1), Square(File.F, 4))
        self._move(Square(File.G, 8), Square(File.F, 6))
        self._move(Square(File.D, 1), Square(File.D, 2))
        self._move(Square(File.E, 7), Square(File.E, 6))
        self._move(Square(File.E, 1), Square(File.C, 1))
        king = self._getPiece(File.C, 1)
        self.assertIsNotNone(king)
        rook = self._getPiece(File.D, 1)
        self.assertIsNotNone(rook)

    def test_CheckStatus_InitialGame_NoChecks(self):
        checkStatus = self._checkStatus()
        self.assertEqual(False, checkStatus.WhiteIsChecked)
        self.assertEqual(False, checkStatus.BlackIsChecked)

    def xtest_CheckStatus_E4F5QH5Check_BlackIsChecked(self):
        self._move(Square(File.E, 2), Square(File.E, 4))
        self._move(Square(File.F, 7), Square(File.F, 5))
        self._move(Square(File.D, 1), Square(File.H, 5))
        checkStatus = self._checkStatus()
        self.assertEqual(False, checkStatus.WhiteIsChecked)
        self.assertEqual(True, checkStatus.BlackIsChecked)

    def xtest_PossibleMoves_E4F5QH5Check_1(self):
        self._move(Square(File.E, 2), Square(File.E, 4))
        self._move(Square(File.F, 7), Square(File.F, 5))
        self._move(Square(File.D, 1), Square(File.H, 5))
        moves = self._possibleMoves()
        self.assertEqual(1, len(moves))

    def _checkStatus(self):
        return self.game.CheckStatus()

    def _assertInitialOfficers(self, pieces, color, rank):
        for file in (File.A, File.H):
            self.assertTrue(Piece(color, Kind.Rook, Square(file, rank)) in pieces)
        for file in (File.B, File.G):
            self.assertTrue(Piece(color, Kind.Knight, Square(file, rank)) in pieces)
        for file in (File.C, File.F):
            self.assertTrue(Piece(color, Kind.Bishop, Square(file, rank)) in pieces)
        self.assertTrue(Piece(color, Kind.Queen, Square(File.D, rank)) in pieces)
        self.assertTrue(Piece(color, Kind.King, Square(File.E, rank)) in pieces)

    def _getPiece(self, file, rank):
        return self.game.GetPiece(file, rank)

    def _getPieceMoves(self, file, rank):
        piece = self._getPiece(file, rank)
        return self.game.GetPieceMoves(piece, True)

    def _getMove(self, origin, destination):
        piece = self.game.GetPiece(origin.File, origin.Rank)
        return Move.Normal(piece, destination)

    def _move(self, origin, destination):
        self.game.Move(origin, destination)

    def _ply1(self):
        self._move(Square(File.E, 2), Square(File.E, 4))

    def _ply2(self):
        self._move(Square(File.E, 7), Square(File.E, 5))

    def _ply3(self):
        self._move(Square(File.D, 2), Square(File.D, 4))

    def _ply4(self):
        self._move(Square(File.E, 5), Square(File.D, 4))

    def _possibleMoves(self):
        return self.game.PossibleMoves()


if __name__ == "__main__":
    unittest.main()
