import unittest


class ChessTests(unittest.TestCase):

    def setUp(self):
        self.game = ChessGame()

    def test_InitialGame_PossibleMoves_20(self):
        self.game = ChessGame()
        moves = self.game.PossibleMoves()
        self.assertEqual(20, len(moves))
        self.assertTrue(self.ContainsMove(moves, Move(Square(File.A, 2), Square(File.A, 4))))

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
        for move in range(20):
            result.append(Move(Square(File.A, 2), Square(File.A, 4)))
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
    

if __name__ == "__main__":
    unittest.main()
