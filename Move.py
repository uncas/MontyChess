from Square import *

class Move:
    
    def __init__(self, piece, destination):
        self.Piece = piece
        self.Origin = piece.Position
        self.Destination = destination
        self.IsCastling = False
        self._isCapture = False
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
        move = Move(piece, destination)
        move.IsCastling = True
        move._rook = rook
        return move

    @staticmethod
    def Capture(board, piece, destination, capturedPiece):
        move = Move(piece, destination)
        move._isCapture = True
        move._capturedPiece = capturedPiece
        move._board = board
        return move

    def Apply(self):
        self.Piece.Position = self.Destination
        self.Piece.HasMoved = True
        if self.IsCastling:
            self._applyRookCastlingMove()
        if self._isCapture:
            self._removeCapturedPiece()

    def Revert(self):
        self.Piece.Position = self.Origin
        self.Piece.HasMoved = self._oldHasMoved
        if self.IsCastling:
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

    def _removeCapturedPiece(self):
        self._board.RemovePiece(self._capturedPiece)
