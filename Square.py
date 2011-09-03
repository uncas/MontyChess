class Square:

    def __init__(self, file, rank):
        self.File = file
        self.Rank = rank

    def __repr__(self):
        return self._getFileLetter() + str(self.Rank)

    def __eq__(self, other):
        return self.File == other.File and self.Rank == other.Rank

    def _getFileLetter(self):
        return chr(ord('A') + self.File - 1)


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

class Rank:
    All = 1, 2, 3, 4, 5, 6, 7, 8
