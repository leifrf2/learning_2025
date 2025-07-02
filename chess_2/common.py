from enum import Enum
from typing import Any, List


from ChessBoardSquare import ChessBoardSquare
from exceptions import SquareNotOnBoardException

class PlayerSide(Enum):
    White = 1
    Black = 2

    def get_opponent(self) -> Any: # Any is always PlayerSide here
        if self == PlayerSide.White:
            return PlayerSide.Black
        elif self == PlayerSide.Black:
            return PlayerSide.White
        else:
            raise ValueError (f"unknown opponent for player side: {self}")

    def __eq__(self, other) -> bool:
        # TODO type check that other is PlayerSide
        # it works differently with enum so instanceof or type is type doesn't work
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

class AbstractClassError(NotImplementedError):
    """Custom exception class"""
    def __init__(self, details=None):
        message = "function must be implemented in inheriting class"
        super().__init__(message)
        self.details = details

_FILE_NAME_TO_COL_MAP = {
        "a" : 0,
        "b" : 1,
        "c" : 2,
        "d" : 3,
        "e" : 4,
        "f" : 5,
        "g" : 6,
        "h" : 7
    }

FILE_NAMES_ORDERED: List[str] = _FILE_NAME_TO_COL_MAP.keys()

def map_file_to_col(file: str) -> int:
    if file not in _FILE_NAME_TO_COL_MAP.keys():
        raise SquareNotOnBoardException(ChessBoardSquare(None, file))
    else:
        return _FILE_NAME_TO_COL_MAP[file]

def map_rank_to_row(rank: int) -> int:
    if rank not in range(1, 9):
        raise ValueError(f"unrecognized row value: {rank}")

    return 8 - rank

def is_valid_file(file: str) -> bool:
    return file in _FILE_NAME_TO_COL_MAP.keys()

def is_valid_rank(rank: int) -> bool:
    return rank in range(1, 9)

# col,row -> row,col
# a8      -> 0,0
# c2      -> 6,3
def is_valid_chess_algebra_square(algebra_str : str) -> bool:
    if len(algebra_str) != 2:
        return False
    
    file_val, rank_val = algebra_str[0], int(algebra_str[1])
    return is_valid_file(file_val) and is_valid_rank(rank_val)


def chess_algebra_to_chess_square(algebra_str: str) -> ChessBoardSquare:
    if algebra_str == "O-O":
        raise NotImplementedError(f"king-side castling not supported")
    elif algebra_str == "O-O-O":
        raise NotImplementedError(f"queen-side castling not supported")
    else:
        # e2
        if len(algebra_str) != 2:
            raise ValueError(f"unrecognized chess algebra string: {algebra_str}")
        
        file_val, rank_val = algebra_str[0], int(algebra_str[1])

        col_val = map_file_to_col(file_val)
        row_val = map_rank_to_row(rank_val)
                
        return ChessBoardSquare(row_val, col_val)
    