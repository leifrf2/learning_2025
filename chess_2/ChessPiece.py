from abc import ABC, abstractmethod
from common import PlayerSide, AbstractClassError

class ChessPiece(ABC):
    def __init__(self, side: PlayerSide):
        self.side = side
    
    @abstractmethod
    def get_ascii_icon(self) -> str:
        raise AbstractClassError()

    def __str__(self):
        return self.get_ascii_icon()
    
    def __repr__(self):
        return f"{self.side.name[0]}:{self.get_ascii_icon()}"

    def __eq__(self, other):
        return type(self) is type(other) and self.side is other.side
        
    def __hash__(self):
        return hash(type(self)) + hash(self.side)

class Pawn(ChessPiece):
    def __init__(self, side: PlayerSide):
        super().__init__(side)
    
    def get_ascii_icon(self) -> str:
        return "p"

class Knight(ChessPiece):
    def __init__(self, side: PlayerSide):
        super().__init__(side)

    def get_ascii_icon(self) -> str:
        return "k"

class Rook(ChessPiece):
    def __init__(self, side: PlayerSide):
        super().__init__(side)

    def get_ascii_icon(self) -> str:
        return "r"

class Bishop(ChessPiece):
    def __init__(self, side: PlayerSide):
        super().__init__(side)

    def get_ascii_icon(self) -> str:
        return "b"

class King(ChessPiece):
    def __init__(self, side: PlayerSide):
        super().__init__(side)

    def get_ascii_icon(self) -> str:
        return "K"
    
class Queen(ChessPiece):
    def __init__(self, side: PlayerSide):
        super().__init__(side)
    
    def get_ascii_icon(self) -> str:
        return "Q"