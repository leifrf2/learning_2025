
from typing import Iterable, Tuple

from ChessBoardSquare import ChessBoardSquare


class ConsoleColor:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'  # Reset to default color

###
# UTILITIES
###

def color_print_pieces(game_board_str: str, color_squares: Iterable[Tuple[ChessBoardSquare, ConsoleColor]]) -> str:
    row_length = 7 + 3 * 8 # 7 spaces and 8 pieces of length 3

    for square, color in sorted(color_squares, key=lambda x: x[0].row * 10 + x[0].col, reverse=True):
        # update the board in reverse order so that we don't need to address offsets
        row_offset = square.row # number of \n to add
        start_in_row = 4 * square.col

        str_piece_position = row_length * square.row + row_offset + start_in_row
        str_piece_end_position = str_piece_position + 3
        game_board_str = \
            game_board_str[:str_piece_position] + \
                color + \
                    game_board_str[str_piece_position:str_piece_end_position] + \
                        ConsoleColor.RESET + game_board_str[str_piece_end_position:]
        
    return game_board_str


