import unittest


class ChessTests(unittest.TestCase):

    def setUp(self):
        self.game = ChessGame()

    def test_InitialGame_PossibleMoves_20(self):
        self.game = ChessGame()
        moves = self.game.PossibleMoves()
        self.assertEqual(20, len(moves))
        firstMove = moves[0]
        fromSquare = firstMove.From


class ChessGame:

    def PossibleMoves(self):
        result = []
        for move in range(20):
            result.append(Move())
        return result


class Move:

    def __init__(self):
        self.From = 0


if __name__ == "__main__":
    unittest.main()
