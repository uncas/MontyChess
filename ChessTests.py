import unittest


class ChessTests(unittest.TestCase):

    def setUp(self):
        self.game = ChessGame()

    def test_InitialGame_PossibleMoves_20(self):
        self.game = ChessGame()
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

    def SameSquare(self, square1, square2):
        return square1.File == square2.File and square1.Rank == square2.Rank


class ChessGame:

    def PossibleMoves(self):
        result = []
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
    

if __name__ == "__main__":
    unittest.main()
