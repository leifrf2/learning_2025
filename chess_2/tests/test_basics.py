###
# BASIC TESTS
###

from typing import List, Tuple
from ChessBoard import ChessBoard
from ChessBoardSquare import ChessBoardSquare
from ChessGame import ChessGame, ChessGameTurn, GameStatus
from ChessPiece import Pawn
from common import PlayerSide, chess_algebra_to_chess_square


def test_create_chessboard():
    chess_board = ChessBoard()
    state = chess_board.get_initial_board_state()
    print(state)

def test_first_turn():
    game = ChessGame()
    from_square = ChessBoardSquare(6, 0)
    to_square = ChessBoardSquare(5,0)
    game.perform_turn(from_square, to_square)

    expected_board = ChessBoard()
    expected_board.board[5][0] = expected_board.board[6][0]
    expected_board.board[6][0] = None

    assert game.board == expected_board
    assert game.game_status == GameStatus.NOT_CONCLUDED
    assert game.turn_index == 2
    assert game.player_turn == PlayerSide.Black
    assert game.turn_history == [
        ChessGameTurn(
            from_square=from_square,
            from_square_piece=Pawn(PlayerSide.White),
            to_square=to_square,
            to_square_piece=None
        )
    ]

def test_chess_algebra_to_chess_square():
    # col,row -> row,col
    # a8      -> 0,0
    # c2      -> 7,3

    algebra_board = [
        ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"],
        ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
        ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
        ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
        ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
        ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
        ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
        ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"],
    ]
    
    for i in range(len(algebra_board)):
        for j in range(len(algebra_board[0])):
            assert ChessBoardSquare(i, j) == chess_algebra_to_chess_square(algebra_board[i][j])
