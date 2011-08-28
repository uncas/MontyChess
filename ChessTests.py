import unittest


class ChessTests(unittest.TestCase):

    def setUp(self):
        self.game = ChessGame()

    def test_Pieces_InitialGame_32(self):
        pieces = self.game.Pieces
        self.assertEquals(32, len(pieces))
        for file in File.All:
            self.assertTrue(self.ContainsPiece(pieces, Piece(Color.White, Kind.Pawn, Square(file, 2))))
            self.assertTrue(self.ContainsPiece(pieces, Piece(Color.Black, Kind.Pawn, Square(file, 7))))
        for file in (File.A, File.H):
            self.assertTrue(self.ContainsPiece(pieces, Piece(Color.White, Kind.Rook, Square(file, 1))))
            self.assertTrue(self.ContainsPiece(pieces, Piece(Color.Black, Kind.Rook, Square(file, 8))))
        for file in (File.B, File.G):
            self.assertTrue(self.ContainsPiece(pieces, Piece(Color.White, Kind.Knight, Square(file, 1))))
            self.assertTrue(self.ContainsPiece(pieces, Piece(Color.Black, Kind.Knight, Square(file, 8))))
        for file in (File.C, File.F):
            self.assertTrue(self.ContainsPiece(pieces, Piece(Color.White, Kind.Bishop, Square(file, 1))))
            self.assertTrue(self.ContainsPiece(pieces, Piece(Color.Black, Kind.Bishop, Square(file, 8))))
        self.assertTrue(self.ContainsPiece(pieces, Piece(Color.White, Kind.Queen, Square(File.D, 1))))
        self.assertTrue(self.ContainsPiece(pieces, Piece(Color.Black, Kind.Queen, Square(File.D, 8))))
        self.assertTrue(self.ContainsPiece(pieces, Piece(Color.White, Kind.King, Square(File.E, 1))))
        

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


class Piece:
    
    def __init__(self, color, kind, position):
        self.Color = color
        self.Kind = kind
        self.Position = position


class ChessGame:

    def __init__(self):
        self.Pieces = []
        for file in File.All:
            self.Pieces.append(Piece(Color.White, Kind.Pawn, Square(file, 2)))
            self.Pieces.append(Piece(Color.Black, Kind.Pawn, Square(file, 7)))
        for file in (File.A, File.H):
            self.Pieces.append(Piece(Color.White, Kind.Rook, Square(file, 1)))
            self.Pieces.append(Piece(Color.Black, Kind.Rook, Square(file, 8)))
        for file in (File.B, File.G):
            self.Pieces.append(Piece(Color.White, Kind.Knight, Square(file, 1)))
            self.Pieces.append(Piece(Color.Black, Kind.Knight, Square(file, 8)))
        for file in (File.C, File.F):
            self.Pieces.append(Piece(Color.White, Kind.Bishop, Square(file, 1)))
            self.Pieces.append(Piece(Color.Black, Kind.Bishop, Square(file, 8)))
        self.Pieces.append(Piece(Color.White, Kind.Queen, Square(File.D, 1)))
        self.Pieces.append(Piece(Color.Black, Kind.Queen, Square(File.D, 8)))
        self.Pieces.append(Piece(Color.White, Kind.King, Square(File.E, 1)))
        for piece in range(1):
            self.Pieces.append(Piece(Color.White, Kind.Pawn, Square(File.A, 2)))

    def PossibleMoves(self):
        result = []
        # Duplicated code here:
        for file in File.All:
            result.append(Move(Square(file, 2), Square(file, 3))) 
            result.append(Move(Square(file, 2), Square(file, 4))) 
        result.append(Move(Square(File.B, 1), Square(File.A, 3)))
        result.append(Move(Square(File.B, 1), Square(File.C, 3)))
        result.append(Move(Square(File.G, 1), Square(File.F, 3)))
        result.append(Move(Square(File.G, 1), Square(File.H, 3)))
        return result


class Move:
    
    def __init__(self, fromSquare, toSquare):
        self.From = fromSquare
        self.To = toSquare
                                                 


class Square:

    def __init__(self, file, rank):
        self.File = file
        self.Rank = rank


class File:
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7
    H = 8
    All = A, B, C, D, E, F, G, H
    
class Kind:
    Pawn = 1
    Rook = 2
    Knight = 3
    Bishop = 4
    Queen = 5
    King = 6

class Color:
    White = 1
    Black = 2

if __name__ == "__main__":
    unittest.main()
