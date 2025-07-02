from typing import Iterable, List, Tuple
import pytest
from ChessCsvPraser import ParsedMove, parse_single_move, parse_move_string
from ChessGame import CheckStatus
from ChessPiece import Knight, Pawn, Bishop, Queen, Rook
from common import PlayerSide, chess_algebra_to_chess_square, map_file_to_col, map_rank_to_row


@pytest.fixture
def get_full_game_parse() -> List[str]:
    return [
    'e4 e5',
    'Nf3 d6',
    'd4 Bg4',
    'dxe5 Bxf3',
    'Qxf3 dxe5',
    'Bc4 Nf6',
    'Qb3 Qe7',
    'Nc3 c6',
    'Bg5 b5',
    'Nxb5 cxb5',
    'Bxb5+ Nbd7',
    #'O-O-O Rd8',
    'Rxd7 Rxd7',
    'Rd1 Qe6',
    'Bxd7+ Nxd7',
    'Qb8+ Nxb8',
    'Rd8# 1-0'
    ]

@pytest.fixture
def get_algebra_strings() -> Iterable[str]:
    return  [
        'e4',
        'e5',
        'Nf3',
        'd6',
        'd4',
        'Bg4',
        'dxe5',
        'Bxf3',
        'Qxf3',
        'dxe5',
        'Bc4',
        'Nf6',
        'Qb3',
        'Qe7',
        'Nc3',
        'c6',
        'Bg5',
        'b5',
        'Nxb5',
        'cxb5',
        'Bxb5+',
        'Nbd7',
        #'O-O-O',
        'Rd8',
        'Rxd7',
        'Rxd7',
        'Rd1',
        'Qe6',
        'Bxd7+',
        'Nxd7',
        'Qb8+',
        'Nxb8',
        'Rd8#',
        #'1-0'
    ]

DEFAULT_PLAYER_SIDE = PlayerSide.White

@pytest.fixture
def get_algebra_strings_with_expected() -> Iterable[Tuple[str, ParsedMove]]:
    return  [
        ('e4', ParsedMove(
            to_square=chess_algebra_to_chess_square('e4'),
            piece_type_to_move=Pawn,
            player_side=DEFAULT_PLAYER_SIDE
            )
        ),
        ('Nf3', ParsedMove(
            to_square=chess_algebra_to_chess_square('f3'),
            piece_type_to_move=Knight,
            player_side=DEFAULT_PLAYER_SIDE
            )
        ),
        ('Bc4', ParsedMove(
            to_square=chess_algebra_to_chess_square('c4'),
            piece_type_to_move=Bishop,
            player_side=DEFAULT_PLAYER_SIDE
            )
        ),
        ('dxe5', ParsedMove(
            to_square=chess_algebra_to_chess_square('e5'),
            piece_type_to_move=Pawn,
            player_side=DEFAULT_PLAYER_SIDE,
            expected_capture=True,
            col_match=map_file_to_col('d')
            )
        ),
        ('Bxf3', ParsedMove(
            to_square=chess_algebra_to_chess_square('f3'),
            piece_type_to_move=Bishop,
            player_side=DEFAULT_PLAYER_SIDE,
            expected_capture=True
            )
        ),
        ('Bxb5+', ParsedMove(
            to_square=chess_algebra_to_chess_square('b5'),
            piece_type_to_move=Bishop,
            player_side=DEFAULT_PLAYER_SIDE,
            expected_capture=True,
            expected_check_status=CheckStatus.IN_CHECK
            )
        ),
        ('Nbd7', ParsedMove(
            to_square=chess_algebra_to_chess_square('d7'),
            piece_type_to_move=Knight,
            player_side=DEFAULT_PLAYER_SIDE,
            col_match=map_file_to_col('b')
            )
        ),
        ('Rd8#', ParsedMove(
            to_square=chess_algebra_to_chess_square('d8'),
            piece_type_to_move=Rook,
            player_side=DEFAULT_PLAYER_SIDE,
            expected_check_status=CheckStatus.IN_CHECK_MATE
            )
        ),
        ('Rdf8', ParsedMove(
            to_square=chess_algebra_to_chess_square('f8'),
            piece_type_to_move=Rook,
            player_side=DEFAULT_PLAYER_SIDE,
            col_match=map_file_to_col('d')
            )
        ),
        ('R1a3', ParsedMove(
            to_square=chess_algebra_to_chess_square('a3'),
            piece_type_to_move=Rook,
            player_side=DEFAULT_PLAYER_SIDE,
            row_match=map_rank_to_row(1)
            )
        ),
        ('Qh4e1', ParsedMove(
            to_square=chess_algebra_to_chess_square('e1'),
            piece_type_to_move=Queen,
            player_side=DEFAULT_PLAYER_SIDE,
            row_match=map_rank_to_row(4),
            col_match=map_file_to_col('h')
            )
        ),
        ('a8N', ParsedMove(
            to_square=chess_algebra_to_chess_square('a8'),
            piece_type_to_move=Pawn,
            player_side=DEFAULT_PLAYER_SIDE,
            promotion_piece=Knight
            )
        ),
        ('dxe8Q+', ParsedMove(
            to_square=chess_algebra_to_chess_square('e8'),
            piece_type_to_move=Pawn,
            player_side=DEFAULT_PLAYER_SIDE,
            expected_capture=True,
            expected_check_status=CheckStatus.IN_CHECK,
            col_match=map_file_to_col('d'),
            promotion_piece=Queen
            )
        ),        
        #'O-O-O',
        #'1-0'
    ]

def test_single_str_algebra_parse(get_algebra_strings):
    for input_str in get_algebra_strings:
        parse_single_move(input_str, DEFAULT_PLAYER_SIDE)

def test_single_str_algebra_equals(get_algebra_strings_with_expected):
    for input_str, expected_move in get_algebra_strings_with_expected:
        assert parse_single_move(input_str, DEFAULT_PLAYER_SIDE) == expected_move

def test_str_algebra_parse(get_full_game_parse):
    for move_line in get_full_game_parse:
        parse_move_string(move_line)


def test_str_algebra_parse_first_moves(get_full_game_parse):
    assert parse_move_string(get_full_game_parse[0]) == [
        ParsedMove(
            to_square=chess_algebra_to_chess_square('e4'),
            piece_type_to_move=Pawn,
            player_side=PlayerSide.White
            ),
        ParsedMove(
            to_square=chess_algebra_to_chess_square('e5'),
            piece_type_to_move=Pawn,
            player_side=PlayerSide.Black
            )
    ]


# TODO equality for expected created moves