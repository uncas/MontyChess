class Square:

    def __init__(self, file, rank):
        self.File = file
        self.Rank = rank

    def __repr__(self):
        return self.GetFileLetter(self.File) + str(self.Rank)

    def GetFileLetter(self, file):
        return chr(ord('A') + file - 1)


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
