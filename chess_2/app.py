from ChessGame import ChessGame, GameStatus
from ChessBoard import ChessBoardSquare
from typing import Tuple

def parse_row_col_input(input_str: str) -> ChessBoardSquare:
    split_input = input_str.split(",")
    if len(split_input) != 2:
        raise ValueError(f"Invalid row,col input: {input_str}")
    
    row = int(split_input[0])
    col = int(split_input[1])

    return ChessBoardSquare(row, col)

def get_console_move() -> Tuple[ChessBoardSquare, ChessBoardSquare]:
    input_origin_row_col_str = input(f"Input origin square in format row,col ")
    origin_square = parse_row_col_input(input_origin_row_col_str)

    input_destination_row_col_str = input(f"Input destination square in format row,col ")
    destination_square = parse_row_col_input(input_destination_row_col_str)

    return origin_square, destination_square

def main():
    game = ChessGame()

    while game.game_status is GameStatus.NOT_CONCLUDED:
        print("================")
        print(f"{game.player_turn.name} to move. Turn {game.turn_index}\n")
        print(game.board)
        print("================")
        
        try:
            from_square, to_square = get_console_move()
            game.perform_turn(from_square, to_square)
        except Exception as e:
            print(e)

        print()

    print(f"game over: {game.game_status.name}")

if __name__=="__main__":
    main()