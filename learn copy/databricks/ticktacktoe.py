from typing import List, Tuple

# ~15min before
# 7:02 now
# 7:17 done

class Game:

    def __init__(self,
                 num_rows: int,
                 num_cols : int,
                 num_tokens: int):
        
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_tokens = num_tokens
        self.current_player = "X"
        self.board: List[List[str]] = self.create_board()

    def set_next_player(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    def create_board(self):
        board = list()

        for _ in range(self.num_rows):
            board.append(['.'] * self.num_cols)

        return board

    def print_board(self):
        print_str = '\n'.join(' '.join(row) for row in self.board)
        print(print_str)

    def array_is_winning(self, arr: List[Tuple[int, int]]) -> bool:
        arr_in_bounds = [x for x in arr if (x[0] >= 0 and x[0] < self.num_rows) 
                         and (x[1] >= 0 and x[1] < self.num_cols)]
        arr_cells = [self.board[x[0]][x[1]] for x in arr_in_bounds]

        while len(arr_cells) >= self.num_tokens:
            if len([x for x in arr_cells[:self.num_tokens] if x == self.current_player]) == self.num_tokens:
                return True
            arr_cells = arr_cells[1:]

        return False

    def player_has_won(self, row: int, col: int):
        complete_range = range(-self.num_tokens + 1, self.num_tokens)

        row_indices = [(row, col + i) for i in complete_range]
        col_indices = [(row + i, col) for i in complete_range]
        diag_1_indices = [(row + i, col + i) for i in complete_range]
        diag_2_indices = [(row - i, col + i) for i in complete_range]

        return any(self.array_is_winning(arr) for arr in [
            row_indices,
            col_indices,
            diag_1_indices,
            diag_2_indices
        ])
    
    def play(self, row: int, col: int):
        if self.board[row][col] != ".":
            raise ValueError(F"cell already in use: {row},{col}")
        
        self.board[row][col] = self.current_player

        self.print_board()

        if self.player_has_won(row, col):
            print(f"Player {self.current_player} has won!")
        
        print()
        
        self.set_next_player()

def test_1():
    game = Game(5, 5, 3)

    moves = [
        (0, 0),
        (3, 4),
        (1, 1),
        (4, 4),
        (2, 2),
    ]

    for move in moves:
        game.play(move[0], move[1])

test_1()