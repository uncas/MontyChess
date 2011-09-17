from Square import *


class Step:
    def __init__(self, fileDelta, rankDelta):
        self.FileDelta = fileDelta
        self.RankDelta = rankDelta

    def Times(self, times):
        return Step(self.FileDelta*times, self.RankDelta*times)


class Move:
    
    def __init__(self, piece, destination):
        self.Piece = piece
        self.Origin = piece.Position
        self.Destination = destination
        self._oldHasMoved = piece.HasMoved
        self._isApplied = False

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

    @staticmethod
    def Promotion(board, piece, destination, promotionKind):
        return PromotionMove(board, piece, destination, promotionKind)

    def Apply(self):
        if self._isApplied:
            raise Exception("Move has already been applied, and cannot be applied again.")
        self._isApplied = True
        self.Piece.Position = self.Destination
        self.Piece.HasMoved = True

    def Revert(self):
        if not self._isApplied:
            raise Exception("Move has not been applied, and cannot be reverted.")
        self._isApplied = False
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


class PromotionMove(Move):

    def __init__(self, board, piece, destination, promotionKind):
        Move.__init__(self, piece, destination)
        self._board = board
        self._promotionKind = promotionKind

    def Apply(self):
        Move.Apply(self)
        #self._promotionPiece = Piece(self.Piece.Color, self._promotionKind, self.Destination)
        #self._board.AddPiece(self._promotionPiece)

    def Revert(self):
        Move.Revert(self)
        #self._board.RemovePiece(self._promotionPiece)
