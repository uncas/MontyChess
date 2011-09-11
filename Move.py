from Square import *

class Move:
    
    def __init__(self, piece, destination):
        self.Piece = piece
        self.Origin = piece.Position
        self.Destination = destination
        self._oldHasMoved = piece.HasMoved

    def __repr__(self):
        return "Move " + str(self.Piece) + " from " + str(self.Origin) + " to " + str(self.Destination) + "."

    def __eq__(self, other):
        return self.Origin == other.Origin and self.Destination == other.Destination

    @staticmethod
    def Normal(piece, destination):
        return Move(piece, destination)

    @staticmethod
    def Castle(piece, destination, rook):
        return CastlingMove(piece, destination, rook)

    @staticmethod
    def Capture(board, piece, destination, capturedPiece):
        return CaptureMove(board, piece, destination, capturedPiece)

    def Apply(self):
        self.Piece.Position = self.Destination
        self.Piece.HasMoved = True

    def Revert(self):
        self.Piece.Position = self.Origin
        self.Piece.HasMoved = self._oldHasMoved


class CastlingMove(Move):

    def __init__(self, piece, destination, rook):
        Move.__init__(self, piece, destination)
        self._rook = rook

    def Apply(self):
        Move.Apply(self)
        self._applyRookCastlingMove()

    def Revert(self):
        Move.Revert(self)
        self._revertRookCastlingMove()

    def _applyRookCastlingMove(self):
        if self.Destination.File == File.G:
            rookDestinationFile = File.F
        else:
            rookDestinationFile = File.D
        self._rook.Position.File = rookDestinationFile
        self._rook.HasMoved = True

    def _revertRookCastlingMove(self):
        if self.Destination.File == File.G:
            rookOriginFile = File.H
        else:
            rookOriginFile = File.A
        self._rook.Position.File = rookOriginFile
        self._rook.HasMoved = False


class CaptureMove(Move):

    def __init__(self, board, piece, destination, capturedPiece):
        Move.__init__(self, piece, destination)
        self._board = board
        self._capturedPiece = capturedPiece

    def Apply(self):
        Move.Apply(self)
        self._board.RemovePiece(self._capturedPiece)

    def Revert(self):
        Move.Revert(self)
        self._board.AddPiece(self._capturedPiece)
