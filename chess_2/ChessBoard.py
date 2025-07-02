from collections import namedtuple
from typing import List, Union, Optional, Tuple, Any
from ChessPiece import Pawn, Queen, King, Rook, Bishop, Knight, ChessPiece
from enum import Enum
from common import PlayerSide
from exceptions import SquareNotOnBoardException, NoChessPieceAtSquareWhenThereShouldBeException
from common import ChessBoardSquare

class SquareColor(Enum):
    White = 1
    Black = 2

class ChessBoard:
    """
    A basic chess board
    """

    BOARD_SIZE = 8

    def __init__(self, empty_board=False):
        self.board = self.get_empty_board() if empty_board else self.get_initial_board_state()

    def get_player_piece_positions(self, side: PlayerSide) -> List[ChessBoardSquare]:
        return [
            ChessBoardSquare(i, j)
            for i in range(self.BOARD_SIZE) 
            for j in range(self.BOARD_SIZE) 
            if self.board[i][j] is not None and self.board[i][j].side == side
            ]

    def get_king_position(self, side: PlayerSide) -> ChessBoardSquare:
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                piece = self.board[i][j]
                if isinstance(piece, King) and piece.side == side:
                    return ChessBoardSquare(i, j)
        
        raise ValueError(f"No King found for player {side.name}")

    def get_player_direction(self, side: PlayerSide) -> int:
        if side == PlayerSide.White:
            return -1
        elif side == PlayerSide.Black:
            return 1
        else:
            return ValueError(f"unsupported player side: {side}")

    def get_player_back_row(self, side: PlayerSide) -> int:
        if side == PlayerSide.White:
            return 7
        elif side == PlayerSide.Black:
            return 0
        else:
            return ValueError(f"unsupported player side: {side}")
 
    def square_is_on_board(self, square: ChessBoardSquare) -> bool:
        return square.row >= 0 and square.row < self.BOARD_SIZE and square.col >= 0 and square.col < self.BOARD_SIZE

    def validate_square(self, square: ChessBoardSquare) -> None:
        if not self.square_is_on_board(square):
            raise SquareNotOnBoardException(square)

    def get_square_color(self, square: ChessBoardSquare) -> SquareColor:
        self.validate_square(square)
        return SquareColor.White if (square.row + square.col) % 2 == 0 else SquareColor.Black

    def get_empty_board(self) -> List[List[ChessPiece]]:
        return [[None] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]

    def get_initial_board_state(self) -> List[List[ChessPiece]]:
        WHITE = PlayerSide.White
        BLACK = PlayerSide.Black

        return [
            [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK), King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)],
            [Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)],
            [Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE), King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)],
        ]

    def get_piece_at_square(self, square: ChessBoardSquare) -> Optional[ChessPiece]:
        self.validate_square(square)
        return self.board[square.row][square.col]

    def clear_square(self, square: ChessBoardSquare) -> None:
        self.board[square.row][square.col] = None

    def set_square(self, square: ChessBoardSquare, piece: ChessPiece) -> None:
        self.board[square.row][square.col] = piece

    def move_piece(self, origin: ChessBoardSquare, destination: ChessBoardSquare) -> None:
        if self.board[origin.row][origin.col] is None:
            raise NoChessPieceAtSquareWhenThereShouldBeException(origin)
        
        self.board[destination.row][destination.col] = self.board[origin.row][origin.col]
        self.board[origin.row][origin.col] = None

    def __str__(self):
        # There is a dependency on the printing format in test output highlighting
        # in test_chess.py
        # if this function is changed, that highlighting logic needs to be changed as well
        # more advanced "print this turn for this board" is a long-term solution
        return "\n".join(
            " ".join(
                [val.__repr__() if val else "___" for val in row]
            )
            for row in self.board
        )
    
    def __eq__(self, other):
        if not isinstance(other, ChessBoard):
            return False
        elif other.BOARD_SIZE != self.BOARD_SIZE:
            return False
        else:
            return all(
                self.board[i][j] == other.board[i][j]
                for i in range(self.BOARD_SIZE) 
                for j in range(self.BOARD_SIZE)
                )

    def clone(self) -> Any: #ChessBoard
        new_board = ChessBoard(empty_board=True)
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                new_board.board[i][j] = self.board[i][j]
        
        return new_board
