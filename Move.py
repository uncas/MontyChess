class Move:
    
    def __init__(self, piece, destination):
        self.Piece = piece
        self.Destination = destination
        self.Origin = piece.Position
        self.IsCastling = False

    def __repr__(self):
        return "Move " + str(self.Piece) + " from " + str(self.Origin) + " to " + str(self.Destination) + "."

    def __eq__(self, other):
        return self.Origin == other.Origin and self.Destination == other.Destination

    def Apply(self):
        self.Piece.Position = self.Destination
        self.Piece.HasMoved = True

    def Revert(self):
        self.Piece.Position = self.Origin

    @staticmethod
    def Castle(piece, destination):
        castlingMove = Move.Normal(piece, destination)
        castlingMove.IsCastling = True
        return castlingMove

    @staticmethod
    def Normal(piece, destination):
        return Move(piece, destination)
