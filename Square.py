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

    def AddFiles(self, files):
        return Square(self.File + files, self.Rank)

    def AddRanks(self, ranks):
        return Square(self.File, self.Rank + ranks)

    def AddFilesAndRanks(self, files, ranks):
        return Square(self.File + files, self.Rank + ranks)

    def AddStep(self, step):
        return Square(self.File + step.FileDelta, self. Rank + step.RankDelta)

    def IsWithinBoard(self):
        return Square.WithinBoard(self.File, self.Rank)

    @staticmethod
    def WithinBoard(file, rank):
        return File.A <= file and file <= File.H and 1 <= rank and rank <= 8

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
