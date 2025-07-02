from collections import namedtuple
from typing import Any
from common import ChessBoardSquare

class SquareNotOnBoardException(ValueError):
    def __init__(self, square: ChessBoardSquare, details=None):
        self.square = square
        message = f"Square is not on board: {square}"
        super().__init__(message)
        self.details = details        

class ChessGameException(Exception):
    """Specific exception type."""
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details

class InvalidMoveException(ValueError):
    """Specific exception type."""
    def __init__(self, piece_to_move, from_square, to_square, details=None):
        self.piece_to_move = piece_to_move
        self.from_square = from_square
        self.to_square = to_square
        message = f"Moving piece {piece_to_move} at square {from_square} to square {to_square} is an invalid move"
        super().__init__(message)
        self.details = details

class InvalidEnumOrClassException(ValueError):
    """Specific exception type."""
    def __init__(self, type: type, value: Any, details=None):
        message = f"Unrecognized value {value} for {type}"
        super().__init__(message)
        self.details = details

class NoChessPieceAtSquareWhenThereShouldBeException(Exception):
    """Specific exception type."""
    def __init__(self, chess_Square: ChessBoardSquare, details=None):
        message = f"no chess piece at {chess_Square}"
        super().__init__(message)
        self.details = details

