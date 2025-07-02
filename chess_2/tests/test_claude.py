###
# CLAUDE TESTS
###

from typing import Dict, List, Tuple
from csv import DictReader
from itertools import groupby
from os import getcwd
import pytest

from ChessGame import ChessGame, ChessBoardSquare, InvalidMoveException, PlayerSide, Queen, Bishop
from utils import color_print_pieces, ConsoleColor
from common import chess_algebra_to_chess_square

def _parse_test_file(file_path: str) -> Dict[int, List[Tuple[ChessBoardSquare,ChessBoardSquare]]]:
    # game_id,move_number,white_move,black_move
    # 1,1,e2-e4,e7-e5
    all_game_lines = list()
    with open(file_path, 'r') as csv_file:
        reader = DictReader(csv_file)
        for row in reader:
            if "checkmate" not in row.values():
                all_game_lines.append(row)
        
    grouped_games = groupby(all_game_lines, key=lambda x: x['game_id'])
    results: Dict[int, List[Tuple[ChessBoardSquare, ChessBoardSquare]]] = dict()
    for (game_id, game_lines) in grouped_games:
        game_id_int = int(game_id)
        results[game_id_int] = list()
        for game_line in sorted(game_lines, key=lambda x: int(x['move_number'])):
            white_move_from, white_move_to = [
                chess_algebra_to_chess_square(s) 
                for s in game_line['white_move'].split("-")
                ]
            results[game_id_int].append((white_move_from, white_move_to))

            black_move_from, black_move_to = [
                chess_algebra_to_chess_square(s) 
                for s in game_line['black_move'].split("-")
                ]
            results[game_id_int].append((black_move_from, black_move_to))

    return results

TEST_FILE_FOLDER = "/tests/claude_games/"

@pytest.fixture
def pawn_take_pawn_exception() -> List[Tuple[ChessBoardSquare, ChessBoardSquare]]:
    return [
            (ChessBoardSquare(6,0), ChessBoardSquare(4,0)),
            (ChessBoardSquare(1,1), ChessBoardSquare(3,1)),
            (ChessBoardSquare(4,0), ChessBoardSquare(3,1))
        ]

def test_parse_test_file():
    test_file_path = getcwd() + TEST_FILE_FOLDER + "test_data_3.csv"
    test_games = _parse_test_file(test_file_path)
    print(test_games.keys())
    for i in range(1,11):
        i in test_games.keys()

@pytest.fixture
def game_1_moves():
    test_file_path = getcwd() + TEST_FILE_FOLDER + "test_data_3.csv"
    return _parse_test_file(test_file_path).get(1, None)

@pytest.fixture
def game_2_moves():
    test_file_path = getcwd() + TEST_FILE_FOLDER + "test_data_3.csv"
    return _parse_test_file(test_file_path).get(2, None)

def run_test_game(game_moves: List[Tuple[ChessBoardSquare, ChessBoardSquare]]):
    game = ChessGame()
    for i, (from_sq, to_sq) in enumerate(game_moves):
        print(f"\nturn: {i + 1}: {from_sq} to {to_sq}")
        game.perform_turn(from_sq, to_sq)
        # highlight the origin square
        # highlight the destination square
        game_board_str = color_print_pieces(
            str(game.board),
            [
                (from_sq, ConsoleColor.YELLOW),
                (to_sq, ConsoleColor.RED)
            ]
        )

        print(game_board_str)

def test_failure_1(pawn_take_pawn_exception: List[Tuple[ChessBoardSquare, ChessBoardSquare]]):
    run_test_game(pawn_take_pawn_exception)

def test_game_1_en_passant_kingside_castle(game_1_moves):
    # this game has an invalid move on turn 38
    # queen from d5 to h5
    # this was confirmed by replaying the game on chess.com
    """
    B:r ___ ___ ___ ___ B:r B:K ___
    ___ ___ ___ ___ B:b B:p B:p ___
    B:p ___ B:Q B:k ___ ___ B:p ___
    ___ B:p B:p W:Q B:p ___ W:b ___
    ___ ___ ___ ___ ___ ___ ___ ___
    ___ ___ W:p ___ ___ W:k ___ W:p
    W:p W:p ___ ___ ___ W:p W:p ___
    W:r ___ ___ ___ W:r W:k W:K ___    
    """
    try:
        run_test_game(game_1_moves)
    except InvalidMoveException as e:
        assert e.from_square == ChessBoardSquare(3, 3)
        assert e.to_square == ChessBoardSquare(3, 7)
        assert e.piece_to_move == Queen(PlayerSide.White)

def test_game_2_queenside_castle(game_2_moves):
    # this game has an invalid move on turn 38
    # queen from d5 to h5
    # this was confirmed by replaying the game on chess.com
    """
    B:r ___ B:b B:Q ___ B:r B:K ___
    B:p B:p ___ ___ B:p B:p B:b B:p
    ___ ___ ___ ___ ___ ___ B:p ___
    ___ ___ ___ ___ ___ ___ ___ ___
    ___ ___ ___ B:k W:p W:b ___ ___
    ___ W:k W:k ___ ___ ___ ___ ___
    W:p W:p W:p ___ ___ B:k W:p W:p
    W:r ___ W:K W:r ___ W:b ___ ___
    """
    try:
        run_test_game(game_2_moves)
    except InvalidMoveException as e:
        assert e.from_square == ChessBoardSquare(7, 5)
        assert e.to_square == ChessBoardSquare(6, 5)
        assert e.piece_to_move == Bishop(PlayerSide.White)
