from ChessBoard import ChessBoard, ChessBoardSquare
from ChessPiece import Pawn, Queen, King, Rook, Bishop, Knight, ChessPiece
from common import PlayerSide
from typing import Iterable, List, Set, Tuple, Optional
from enum import Enum
from abc import ABC

from exceptions import (
    ChessGameException, 
    InvalidEnumOrClassException, 
    InvalidMoveException, 
    NoChessPieceAtSquareWhenThereShouldBeException
    )

class CheckStatus(Enum):
    NOT_IN_CHECK = 1
    IN_CHECK = 2
    IN_CHECK_MATE = 3
    IN_STALEMATE = 4

class GameStatus(Enum):
    NOT_CONCLUDED = 1
    WHITE_WINS = 2
    BLACK_WINS = 3
    STALEMATE = 4

    def __eq__(self, other) -> bool:
        # TODO type check that other is PlayerSide
        # it works differently with enum so instanceof or type is type doesn't work
        return self.value == other.value

class CastleSide(Enum):
    KingSide = 1
    QueenSide = 2

    def __eq__(self, other) -> bool:
        # TODO type check that other is PlayerSide
        # it works differently with enum so instanceof or type is type doesn't work
        return self.value == other.value

class ChessMoveBase(ABC):
    # this class should never be instantiated directly
    def __init__(self, 
                 from_square: ChessBoardSquare, 
                 to_square: ChessBoardSquare, 
                 moved_piece: ChessPiece, 
                 chess_squares_with_pieces_removed: Iterable[ChessBoardSquare] = {}, 
                 chess_squares_with_pieces_added: Iterable[ChessBoardSquare] = {}
                 ):
        self.from_square = from_square
        self.to_square = to_square
        self.moved_piece = moved_piece
        self.chess_squares_with_pieces_removed: Set[ChessBoardSquare] = set(chess_squares_with_pieces_removed).union({from_square, to_square})
        self.chess_squares_with_pieces_added: Set[Tuple[ChessBoardSquare, ChessPiece]] = set(chess_squares_with_pieces_added).union({(to_square, moved_piece)})

class ChessMoveWithCapture(ChessMoveBase):
    def __init__(self, from_square: ChessBoardSquare, to_square: ChessBoardSquare, moved_piece: ChessPiece):
        super().__init__(
            from_square=from_square,
            to_square=to_square,
            moved_piece=moved_piece,
            chess_squares_with_pieces_removed=[from_square, to_square],
            chess_squares_with_pieces_added=[(to_square, moved_piece)]
        )

class EnPassantMove(ChessMoveBase):
    def __init__(self, from_square: ChessBoardSquare, to_square: ChessBoardSquare, player_side: PlayerSide):
        en_passant_target = ChessBoardSquare(from_square.row, to_square.col)
        moved_pawn = Pawn(player_side)

        super().__init__(
            from_square=from_square,
            to_square=to_square,
            moved_piece=moved_pawn,
            chess_squares_with_pieces_removed=[from_square, en_passant_target],
            chess_squares_with_pieces_added=[(to_square, moved_pawn)]
        )

# TODO simplify castling constructor to just take castle_side and player_side
# and infer the correct squares and pieces for super constructor
class CastleMove(ChessMoveBase):
    def __init__(self,
                 from_square: ChessBoardSquare,
                 to_square: ChessBoardSquare,
                 player_side: PlayerSide
                 ):
        
        # infer castle side
        if to_square.col == 6:
            # it's king side
            castle_side = CastleSide.KingSide
        elif to_square.col == 2:
            castle_side = CastleSide.QueenSide
        else:
            raise InvalidEnumOrClassException(CastleSide, to_square.col)

        match (castle_side, player_side):
            case (CastleSide.KingSide, PlayerSide.White):
                # white is at bottom of board
                # king is to the right
                chess_squares_with_pieces_removed = [
                    ChessBoardSquare(7, 4), # white king
                    ChessBoardSquare(7, 7) # white right rook
                ]
                chess_squares_with_pieces_added = [
                    (ChessBoardSquare(7, 5), Rook(PlayerSide.White)),
                    (ChessBoardSquare(7, 6), King(PlayerSide.White))
                ]
            case (CastleSide.KingSide, PlayerSide.Black):
                # black is at top of board
                # king is to the right
                chess_squares_with_pieces_removed = [
                    ChessBoardSquare(0, 4), # black king
                    ChessBoardSquare(0, 7) # black right rook
                ]
                chess_squares_with_pieces_added = [
                    (ChessBoardSquare(0, 5), Rook(PlayerSide.Black)),
                    (ChessBoardSquare(0, 6), King(PlayerSide.Black))
                ]
            case (CastleSide.QueenSide, PlayerSide.White):
                # white is at bottom of board
                # queen is to the left
                chess_squares_with_pieces_removed = [
                    ChessBoardSquare(7, 4), # white king
                    ChessBoardSquare(7, 0) # white left rook
                ]
                chess_squares_with_pieces_added = [
                    (ChessBoardSquare(7, 3), Rook(PlayerSide.White)),
                    (ChessBoardSquare(7, 2), King(PlayerSide.White))
                ]  
            case (CastleSide.QueenSide, PlayerSide.Black):
                # black is at top of board
                # queen is to the left
                chess_squares_with_pieces_removed = [
                    ChessBoardSquare(0, 4), # black king
                    ChessBoardSquare(0, 0) # black right rook
                ]
                chess_squares_with_pieces_added = [
                    (ChessBoardSquare(0, 3), Rook(PlayerSide.Black)),
                    (ChessBoardSquare(0, 2), King(PlayerSide.Black))
                ]                
            case _:
                # TODO create a better exception for this
                raise ChessGameException(f"invalid castling maneuver")

        super().__init__(
            from_square=from_square,
            to_square=to_square,
            moved_piece=King(player_side),
            chess_squares_with_pieces_removed=chess_squares_with_pieces_removed,
            chess_squares_with_pieces_added=chess_squares_with_pieces_added
            )

class PromotionMove(ChessMoveBase):
    def __init__(self, from_square: ChessBoardSquare, to_square: ChessBoardSquare, piece_to_create: ChessPiece):
        chess_squares_with_pieces_removed = [
            from_square, to_square
        ]
        chess_squares_with_pieces_added = [
            (to_square, piece_to_create)
        ]
        super().__init__(from_square, to_square, piece_to_create, chess_squares_with_pieces_removed, chess_squares_with_pieces_added)

pawn_promotion_options: List[ChessPiece] = [
    Rook,
    Bishop,
    Queen,
    Knight
]

class ChessGameTurn:
    def __init__(self,
                 from_square: ChessBoardSquare,
                 from_square_piece: ChessPiece,
                 to_square: ChessBoardSquare,
                 to_square_piece: Optional[ChessPiece]):
        self.from_square = from_square
        self.from_square_piece = from_square_piece
        self.to_square = to_square
        self.to_square_piece = to_square_piece

    def __str__(self) -> str:
        base_str = f"Moved {self.from_square_piece} from {self.from_square} to {self.to_square}"
        if self.to_square_piece is not None:
            return base_str + f" taking piece {self.to_square_piece}"
        else:
            return base_str

    def __eq__(self, other) -> bool:
        if not isinstance(other, ChessGameTurn):
            return False

        return self.from_square == other.from_square and \
               self.from_square_piece == other.from_square_piece and \
               self.to_square == other.to_square and \
               self.to_square_piece == other.to_square_piece

class ChessGame:

    def __init__(self):
        self.board = ChessBoard()
        self.player_turn = PlayerSide.White
        self.turn_index = 1
        self.game_status = GameStatus.NOT_CONCLUDED
        self.turn_history: List[ChessGameTurn] = list()
    
    def set_next_turn(self) -> None:
        self.turn_index += 1

        if self.player_turn == PlayerSide.White:
            self.player_turn = PlayerSide.Black
        elif self.player_turn == PlayerSide.Black:
            self.player_turn = PlayerSide.White
        else:
            raise InvalidEnumOrClassException(PlayerSide, self.player_turn)

    def player_is_in_check(self, player: PlayerSide, board:ChessBoard) -> bool:
        return board.get_king_position(player) in self.get_squares_threatened_by_player(player.get_opponent(), board)

    def player_has_move_to_not_check(self, player: PlayerSide, board: ChessBoard) -> bool:
        player_piece_positions = board.get_player_piece_positions(player)

        # player has a way out of check
        player_has_move_resulting_in_not_check = False
        for square in player_piece_positions:
            if player_has_move_resulting_in_not_check:
                break
            else:
                for piece_move in self.get_precheck_moves_for_piece_at_square(square, board):
                    new_board: ChessBoard = board.clone()
                    self.update_board_for_move(new_board, piece_move)
                    if not self.player_is_in_check(player, new_board):
                        player_has_move_resulting_in_not_check = True
                        break
        
        return player_has_move_resulting_in_not_check

    # it is this player's turn
    # need to only check 1 turn from now
    def get_player_check_status(self, player: PlayerSide, board:ChessBoard) -> CheckStatus:

        # opponent is currently threaning player's king
        # we don't need to check valid moves for the opponent's pieces
        # because the board must be in a valid state at this time
        player_in_check = self.player_is_in_check(player, board)

        # even if the player is not currently in check,
        # still need to check if they have a move not resulting in check
        # to determine if it's a stalemate
        player_has_move_resulting_in_not_check = self.player_has_move_to_not_check(player, board)

        if not player_in_check and player_has_move_resulting_in_not_check:
            return CheckStatus.NOT_IN_CHECK
        elif not player_in_check and not player_has_move_resulting_in_not_check:
            return CheckStatus.IN_STALEMATE
        elif player_in_check and player_has_move_resulting_in_not_check:
            return CheckStatus.IN_CHECK
        elif player_in_check and not player_has_move_resulting_in_not_check:
            return CheckStatus.IN_CHECK_MATE
        else:
            raise InvalidEnumOrClassException(CheckStatus, f"player_in_check:{player_in_check}, player_has_move_resulting_in_not_check:{player_has_move_resulting_in_not_check}")

    def move_results_in_self_check(self, move: ChessMoveBase, board: ChessBoard, player_side:PlayerSide):
        new_board: ChessBoard = board.clone()
        for removed in move.chess_squares_with_pieces_removed:
            new_board.clear_square(removed)
        for addded, piece in move.chess_squares_with_pieces_added:
            new_board.set_square(addded, piece)

        return self.player_is_in_check(player_side, new_board)

    def get_knight_moves(self, origin_square: ChessBoardSquare, board: ChessBoard) -> List[ChessMoveWithCapture]:
        this_piece = board.get_piece_at_square(origin_square)

        possible_new_squares = [
            ChessBoardSquare(origin_square.row + 2, origin_square.col + 1),
            ChessBoardSquare(origin_square.row + 2, origin_square.col - 1),
            ChessBoardSquare(origin_square.row - 2, origin_square.col + 1),
            ChessBoardSquare(origin_square.row - 2, origin_square.col - 1),
            ChessBoardSquare(origin_square.row + 1, origin_square.col + 2),
            ChessBoardSquare(origin_square.row + 1, origin_square.col - 2),
            ChessBoardSquare(origin_square.row - 1, origin_square.col + 2),
            ChessBoardSquare(origin_square.row - 1, origin_square.col - 2),
        ]

        # square is on the board
        on_board_squares = [
            square for square in possible_new_squares
            if board.square_is_on_board(square)
        ]

        # square does not contain a friendly piece
        return [
            ChessMoveWithCapture(origin_square, sq, this_piece) for sq in on_board_squares 
            if (board.get_piece_at_square(sq) is None) or
            board.get_piece_at_square(sq).side != this_piece.side
        ]

    def get_pawn_moves(self, origin_square: ChessBoardSquare, board: ChessBoard) -> List[ChessMoveWithCapture | PromotionMove | EnPassantMove]:
        this_piece = board.get_piece_at_square(origin_square)
        if not this_piece:
            raise NoChessPieceAtSquareWhenThereShouldBeException(origin_square)
        
        direction = board.get_player_direction(this_piece.side)

        valid_moves: List[ChessMoveWithCapture | PromotionMove | EnPassantMove] = list()

        def get_promotion_moves(target_square: ChessBoardSquare) -> Iterable[PromotionMove]:
            return (PromotionMove(origin_square, target_square, piece) for piece in pawn_promotion_options)

        # the pawn is one step away from promotion
        # next step can only be promotion
        next_step_promotes = (direction == +1 and origin_square.row == board.BOARD_SIZE - 2) or \
           (direction == -1 and origin_square.row == 1)

        one_step = ChessBoardSquare(origin_square.row + direction, origin_square.col)
        if board.get_piece_at_square(one_step) is None:
            
            if next_step_promotes:
                valid_moves.extend(get_promotion_moves(one_step))
            else:
                valid_moves.append(ChessMoveWithCapture(origin_square, one_step, this_piece))

                if (direction == -1 and origin_square.row == board.BOARD_SIZE - 2) or \
                    (direction == +1 and origin_square.row == 1):
                    # need to be in the second rank for this player to move twice

                    # continue checking two_step
                    two_step = ChessBoardSquare(origin_square.row + direction * 2, origin_square.col)
                    if board.get_piece_at_square(two_step) is None:
                        valid_moves.append(ChessMoveWithCapture(origin_square, two_step, this_piece))

        take_squares = [
            ChessBoardSquare(origin_square.row + direction, origin_square.col + 1),
            ChessBoardSquare(origin_square.row + direction, origin_square.col - 1),
        ]

        for square in take_squares:
            if board.square_is_on_board(square):
                square_piece = board.get_piece_at_square(square)
                if square_piece is not None and this_piece.side != square_piece.side:
                    if next_step_promotes:
                        valid_moves.extend(get_promotion_moves(square))
                    else:
                        valid_moves.append(ChessMoveWithCapture(origin_square, square, this_piece))
        
        # - an opposing pawn takes 2-step 
        # - that pawn is adjacent to current player's pawn
        # - this pawn can move behind opposing's 2-step pawn
        if len(self.turn_history) > 0:
            last_turn = self.turn_history[-1]
            if isinstance(last_turn.from_square_piece, Pawn) \
                and abs(last_turn.from_square.col - last_turn.to_square.col) == 2:
                assert last_turn.from_square_piece.side != this_piece.side, \
                    f"Invalid turn history - last moved piece is the same side as this turn"
                
                # opponent pawn did 2-step last turn
                opponent_2_step_pawn = self.board.get_piece_at_square(last_turn.to_square)
                assert isinstance(opponent_2_step_pawn, Pawn), \
                    f"Invalid turn history. Piece at destination square is not a pawn when it must be a pawn"

                if last_turn.to_square.row == origin_square.row \
                    and abs(last_turn.to_square.col - origin_square.col) == 1:
                    # they are in the same row and adjacent to each other
                    # only need to check this one opponent's pawn, because en-passant
                    # only applies immediately after oponnent did 2-step
                    # so even if there are 2 adjacent pawns, only this one from last turn
                    # could still be relevant

                    # technically a regular take and an en-passant take would both add the same target cell
                    # however for en-passant to be a valid move, then the same target cell for regular take
                    # is not possible
                    # so the two cases are disjoint

                    # TODO this doesn't handle removing the captured pawn
                    valid_moves.append(
                        EnPassantMove(
                            origin_square, 
                            ChessBoardSquare(last_turn.to_square.row  + direction, last_turn.to_square.col), 
                            this_piece.side
                        )
                    )

        return valid_moves

    def _move_directional_piece(self, origin_square: ChessBoardSquare, move_directions: List[Tuple[int, int]], board: ChessBoard) -> List[ChessMoveWithCapture]:
        this_piece = board.get_piece_at_square(origin_square)

        valid_moves: List[ChessMoveWithCapture] = list()

        for move_direction in move_directions:
            for i in range(1, 8):
                next_square = ChessBoardSquare(origin_square.row + (i * move_direction[0]), origin_square.col + (i * move_direction[1]))
                if board.square_is_on_board(next_square):
                    next_piece = board.get_piece_at_square(next_square)
                    if next_piece is None:
                        valid_moves.append(ChessMoveWithCapture(origin_square, next_square, this_piece))
                    elif this_piece.side != next_piece.side:
                        valid_moves.append(ChessMoveWithCapture(origin_square, next_square, this_piece))
                        break
                    else:
                        break
                else:
                    break

        return valid_moves

    def get_bishop_moves(self, origin_square: ChessBoardSquare, board: ChessBoard) -> List[ChessMoveWithCapture]:
        move_directions = [
            [+1, +1],
            [+1, -1],
            [-1, +1],
            [-1, -1]
        ]

        return self._move_directional_piece(origin_square, move_directions, board)

    def get_rook_moves(self, origin_square: ChessBoardSquare, board: ChessBoard) -> List[ChessMoveWithCapture]:
        move_directions = [
            [+1, +0],
            [+0, -1],
            [-0, +1],
            [-1, -0]
        ]

        return self._move_directional_piece(origin_square, move_directions, board)

    def get_queen_moves(self, origin_square: ChessBoardSquare, board: ChessBoard) -> List[ChessMoveWithCapture]:
        move_directions = [
            [+1, +0],
            [+0, -1],
            [-0, +1],
            [-1, -0],

            [+1, +1],
            [+1, -1],
            [-1, +1],
            [-1, -1]
        ]

        return self._move_directional_piece(origin_square, move_directions, board)

    def get_castling_moves(self, origin_square: ChessBoardSquare, board: ChessBoard) -> List[CastleMove]:
        """
        1. you may only castle if you haven't moved your king and your rook (on the side where you want to castle). 
        2. no piece can be between your king and the rook on the side where you want to castle.
        3. If you are in check, you cannot castle. 
        4. You cannot castle if any square the king is moving through is attacked by your opponent's pieces.
        5. You cannot castle into check.
        """
        valid_moves: List[CastleMove] = list()
        
        this_piece = board.get_piece_at_square(origin_square)

        if not any(king_move for king_move in self.turn_history if king_move.from_square_piece == this_piece):
            # if the king hasn't moved, then it can still castle

            opponent_target_squares: Set[ChessBoardSquare] = self.get_squares_threatened_by_player(this_piece.side.get_opponent(), board)

            # king side 4, 5, 6, 7
            back_row = board.get_player_back_row(this_piece.side)

            king_side_rook_square = ChessBoardSquare(back_row, 7)
            if not any(rook_move for rook_move in self.turn_history if rook_move.from_square == king_side_rook_square):
                # both king and rook are able to castle

                king_side_castle_squares = {
                    # this also evalutes if the king is currently in check
                    ChessBoardSquare(back_row, col) for col in [4, 5, 6]
                }

                # now evaluate check conditions
                if opponent_target_squares.isdisjoint(king_side_castle_squares) and \
                    all(board.get_piece_at_square(square) is None for square in [ChessBoardSquare(back_row, 5), ChessBoardSquare(back_row, 6)]):
                    # the opponent isn't threatening any square in the kingside castle maneuver
                    # and there are no pieces in the way
                    valid_moves.append(
                        CastleMove(origin_square, ChessBoardSquare(back_row, 6), this_piece.side)
                    )
            
            # queen side 0, 1, 2, 3, 4
            queen_side_rook_square = ChessBoardSquare(back_row, 0)
            if not any(rook_move for rook_move in self.turn_history if rook_move.from_square == queen_side_rook_square):
                # both king and rook are able to castle

                queen_side_castle_squares = {
                    # this also evalutes if the king is currently in check
                    ChessBoardSquare(back_row, col) for col in [2, 3, 4]
                }

                # now evaluate check conditions
                if opponent_target_squares.isdisjoint(queen_side_castle_squares)  and \
                    all(board.get_piece_at_square(square) is None for square in [ChessBoardSquare(back_row, 2), ChessBoardSquare(back_row, 3)]):
                    # the opponent isn't threatening any square in the Queenside castle maneuver
                    # and there are no pieces in the way
                    valid_moves.append(
                        CastleMove(origin_square, ChessBoardSquare(back_row, 2), this_piece.side)
                    )
        
        return valid_moves

    def get_king_moves(self, origin_square: ChessBoardSquare, board: ChessBoard) -> List[ChessMoveWithCapture | CastleMove]:
        this_piece = board.get_piece_at_square(origin_square)

        square_moves = [
            [+1, +0],
            [+0, -1],
            [-0, +1],
            [-1, -0],

            [+1, +1],
            [+1, -1],
            [-1, +1],
            [-1, -1]
        ]

        valid_moves: List[ChessMoveWithCapture | CastleMove] = list()

        # basic movement
        for new_row, new_col in square_moves:
            new_square = ChessBoardSquare(origin_square.row + new_row, origin_square.col + new_col)
            if board.square_is_on_board(new_square):
                square_piece = board.get_piece_at_square(new_square)
                if square_piece is None:
                    valid_moves.append(ChessMoveWithCapture(origin_square, new_square, this_piece))
                elif this_piece.side != square_piece.side:
                    valid_moves.append(ChessMoveWithCapture(origin_square, new_square, this_piece))
                # else it's a piece on the same side as this piece
                # so can't move there

        return valid_moves

    def get_squares_threatened_by_player(self, player_side: PlayerSide, board: ChessBoard) -> Set[ChessBoardSquare]:
        # this includes en passant moves
        # that should not be a problem
        return {
            move.to_square 
            for position in board.get_player_piece_positions(player_side) 
            for move in self.get_non_castling_precheck_moves_at_square(position, board)
        }

    def get_non_castling_precheck_moves_at_square(self, square: ChessBoardSquare, board: ChessBoard) -> List[ChessMoveBase]:
        chess_piece: Optional[ChessPiece] = board.get_piece_at_square(square)

        if not chess_piece:
            raise NoChessPieceAtSquareWhenThereShouldBeException(square)
        
        else:
            if isinstance(chess_piece, Knight):
                return self.get_knight_moves(square, board)
            elif isinstance(chess_piece, Pawn):
                return self.get_pawn_moves(square, board)
            elif isinstance(chess_piece, Bishop):
                return self.get_bishop_moves(square, board)
            elif isinstance(chess_piece, Rook):
                return self.get_rook_moves(square, board)
            elif isinstance(chess_piece, Queen):
                return self.get_queen_moves(square, board)
            elif isinstance(chess_piece, King):
                return self.get_king_moves(square, board)
            else:
                raise InvalidEnumOrClassException(ChessPiece, type(chess_piece))

    def get_castling_precheck_moves_at_square(self, square:ChessBoardSquare, board: ChessBoard) -> List[CastleMove]:
        chess_piece: Optional[ChessPiece] = board.get_piece_at_square(square)

        if not chess_piece:
            raise NoChessPieceAtSquareWhenThereShouldBeException(square)
        elif isinstance(chess_piece, King):
            return self.get_castling_moves(square, board)
        else:
            raise InvalidEnumOrClassException(King, type(chess_piece))

    def get_precheck_moves_for_piece_at_square(self, square: ChessBoardSquare, board: ChessBoard) -> List[ChessMoveBase]:
        moves = self.get_non_castling_precheck_moves_at_square(square, board)
        if isinstance(board.get_piece_at_square(square), King):
            moves.extend(self.get_castling_precheck_moves_at_square(square, board))
        return moves

    def get_valid_moves_for_piece_at_square(self, origin_square: ChessBoardSquare, board: ChessBoard) -> List[ChessMoveBase]:
        player_side = board.get_piece_at_square(origin_square).side
        return [
                move for move in self.get_precheck_moves_for_piece_at_square(origin_square, board) 
                if not self.move_results_in_self_check(move, board, player_side)
                ]

    def update_board_for_move(self, board: ChessBoard, move: ChessMoveBase):
        for cleared_square in move.chess_squares_with_pieces_removed:
            board.clear_square(cleared_square)
        for square, piece in move.chess_squares_with_pieces_added:
            board.set_square(square, piece)

    def execute_move(self, from_square: ChessBoardSquare, to_square: ChessBoardSquare, promotion_piece: Optional[ChessPiece]) -> None:
        piece_to_move = self.board.get_piece_at_square(from_square)
        if piece_to_move is None:
            raise NoChessPieceAtSquareWhenThereShouldBeException(from_square)

        if piece_to_move.side != self.player_turn:
            raise InvalidMoveException(piece_to_move, from_square, to_square)

        valid_moves = self.get_valid_moves_for_piece_at_square(from_square, self.board)
        matched_moves = [move for move in valid_moves if move.from_square == from_square and move.to_square == to_square]
        
        # either it's a promotion, and the promotion piece is valid
        # or there's only one move that matches
        if len(matched_moves) == 0:
            raise InvalidMoveException(piece_to_move, from_square, to_square)
        elif all(isinstance(move, PromotionMove) for move in matched_moves):
            matched_promotion_moves = [move for move in matched_moves if move.moved_piece == promotion_piece]
            if len(matched_promotion_moves) == 1:
                chosen_move = matched_promotion_moves[0]
            else:
                raise InvalidMoveException(piece_to_move, from_square, to_square) # TODO add promotion exception here
        elif len(matched_moves) == 1:
            chosen_move = matched_moves[0]
        else:
            raise InvalidMoveException(piece_to_move, from_square, to_square)

        self.update_board_for_move(self.board, chosen_move)

    def update_game_status(self) -> None:
        game_status = self.get_player_check_status(self.player_turn, self.board)
        if game_status == CheckStatus.IN_STALEMATE:
            self.game_status = GameStatus.STALEMATE
        elif game_status == CheckStatus.IN_CHECK_MATE:
            if self.player_turn == PlayerSide.White:
                self.game_status = GameStatus.BLACK_WINS
            elif self.player_turn == PlayerSide.Black:
                self.game_status = GameStatus.WHITE_WINS
            else:
                raise InvalidEnumOrClassException(PlayerSide, self.player_turn)
        else:
            self.game_status = GameStatus.NOT_CONCLUDED

    def perform_turn(self, from_square: ChessBoardSquare, to_square: ChessBoardSquare, promotion_piece: Optional[ChessPiece] = None) -> ChessGameTurn:
        # TODO new logic:
        """
        Setup git tracking before making this major change

        1. convert from_square, to_square arguments into a move type
            1.1 add an optional "promotion" piece type in case it's a promotion move
        2. add castle move support
        3. for each piece or move
            3.1 return ChessMoveBase subtypes in list
        4. on check test
            4.1 filter opponent moves to only those with threaten
                (this is ChessMoveWithCapture or Promotion-special case)
        5. turn history is the executed move (and some metadta)
        """

        # convert from_square to_square to a move type

        if self.game_status == GameStatus.NOT_CONCLUDED:
            # this doesn't completely capture the turn
            # but it's enough for en passant and castling
            staged_turn = ChessGameTurn(
                from_square,
                self.board.get_piece_at_square(from_square),
                to_square,
                self.board.get_piece_at_square(to_square)
            )

            # TODO resolve move
            """
            Need to resolve move type:
            1. castle
            2. promotion
            3. en passant
            4. regular chess move

            if pawn ->
                en passant
                promotion
                regular
            if king ->
                regular
                castle
            else ->
                regular
            
            ... further thinking
            there is only one move going to_square for a given from_square

            rather, it's an assertion to execute the move which is from_square to_square
            is the player or the game responsible for providing the move type which applies?

            if there were multiple paths between two cells, then the user would need to specify
            since there is only one path, the user does not need to specify


            """

            # this will throw an exception if the move is invalid
            self.execute_move(from_square, to_square, promotion_piece)
            
            # at this stage it's guaranteed that the move is valid
            self.turn_history.append(staged_turn)
            self.update_game_status()

            if self.game_status == GameStatus.NOT_CONCLUDED:
                self.set_next_turn()

            return staged_turn
        else:
            raise ChessGameException(f"Game is already concluded with status {self.game_status}")
