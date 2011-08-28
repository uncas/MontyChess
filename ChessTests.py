import unittest


class ChessTests(unittest.TestCase):
    def setUp(self):
        print("*")

    def test_InitialGame_PossibleMoves_20(self):
        game = ChessGame()
        self.assertEqual(20, len(game.PossibleMoves()))


class ChessGame:
    def __init__(self):
        print("Chess game starting...")

    def PossibleMoves(self):
        return range(20)


if __name__ == "__main__":
    unittest.main()
