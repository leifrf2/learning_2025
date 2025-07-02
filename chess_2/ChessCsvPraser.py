# https://en.wikipedia.org/wiki/Algebraic_notation_(chess)

"""
https://www.chess.com/games/view/765

1. e4 e5 2. Nf3 d6 3. d4 Bg4 4. dxe5 Bxf3 5. Qxf3 dxe5 6. Bc4 Nf6 7. Qb3 Qe7 8.
Nc3 c6 9. Bg5 b5 10. Nxb5 cxb5 11. Bxb5+ Nbd7 12. O-O-O Rd8 13. Rxd7 Rxd7 14.
Rd1 Qe6 15. Bxd7+ Nxd7 16. Qb8+ Nxb8 17. Rd8# 1-0
"""

"""
Naming Squares
Each square of the board is identified by a unique coordinate pair—a letter and a number—from 
White's point of view. The vertical columns of squares, called files, are labeled a 
through h from White's left (the queenside) to right (the kingside). 
The horizontal rows of squares, called ranks, are numbered 1 to 8 starting from White's side of the board. 
Thus each square has a unique identification of file letter followed by rank number.
For example, the initial square of White's king is designated as "e1".

Naming Pieces
K=King
Q=Queen
R=Rook
B=Bishop
N=Knight
None=Pawn

Notation for Moves
In standard (or short-form) algebraic notation, each move of a piece is indicated by the piece's uppercase letter, 
plus the coordinates of the destination square. For example, Be5 (bishop moves to e5), Nf3 (knight moves to f3). 
For pawn moves, a letter indicating pawn is not used, only the destination square is given. For example, 
c5 (pawn moves to c5).

    x = capture
    + = check
    # = checkmate
    0-0-0 = queenside castle
    0-0 = kingside castle

Disambiguating moves
the file of departure (if they differ); (eg Rdf8)
the rank of departure (if the files are the same but the ranks differ). (R1a3)
if neither is sufficient (rare case of 3 queens), then both file and rank are used (Qh4e1)

Pawn Promption
When a pawn promotes, the piece promoted to is indicated at the end. 
For example, a pawn on e7 promoting to a queen on e8 may be variously rendered as e8Q, e8=Q, e8(Q), e8/Q etc.

"""

"""
e4 e5
Nf3 d6
d4 Bg4
dxe5 Bxf3
Qxf3 dxe5
Bc4 Nf6
Qb3 Qe7
Nc3 c6
Bg5 b5
Nxb5 cxb5
Bxb5+ Nbd7
O-O-O Rd8
Rxd7 Rxd7
Rd1 Qe6
Bxd7+ Nxd7
Qb8+ Nxb8
Rd8# 1-0
"""

from typing import Dict, List, Optional
from ChessPiece import ChessPiece, Pawn, Queen, King, Rook, Bishop, Knight
from common import ChessBoardSquare, PlayerSide, chess_algebra_to_chess_square, is_valid_chess_algebra_square, is_valid_rank, is_valid_file, map_file_to_col, map_rank_to_row
from ChessGame import CheckStatus
from exceptions import InvalidEnumOrClassException

class ChessAlgebraParsingException(Exception):
    pass

notation_piece_map: Dict[str, ChessPiece] = {
    "K" : King,
    "Q" : Queen,
    "R" : Rook,
    "B" : Bishop,
    "N" : Knight
}

class ParsedMove:
    def __init__(self,
                piece_type_to_move: ChessPiece,
                to_square: ChessBoardSquare,
                player_side: PlayerSide,
                expected_check_status: CheckStatus=CheckStatus.NOT_IN_CHECK,
                expected_capture: bool=False,
                col_match: Optional[int]=None,
                row_match: Optional[int]=None,
                promotion_piece: Optional[ChessPiece]=None,
                ):
        self.piece_type_to_move = piece_type_to_move
        self.to_square = to_square
        self.player_side = player_side
        self.expected_check_status = expected_check_status
        self.expected_capture = expected_capture
        self.col_match = col_match
        self.row_match = row_match
        self.promotion_piece = promotion_piece

    def __eq__(self, other):
        return isinstance(other, ParsedMove) \
        and self.piece_type_to_move == other.piece_type_to_move \
        and self.to_square == other.to_square \
        and self.player_side == other.player_side \
        and self.expected_check_status == other.expected_check_status \
        and self.expected_capture == other.expected_capture \
        and self.col_match == other.col_match \
        and self.row_match == other.row_match \
        and self.promotion_piece == other.promotion_piece

def parse_single_move(single_move_str: str, player_side: PlayerSide) -> ParsedMove:
    """
    Disambiguation
    the file of departure (if they differ); (eg Rdf8)
    the rank of departure (if the files are the same but the ranks differ). (R1a3)
    if neither is sufficient (rare case of 3 queens), then both file and rank are used (Qh4e1)
    """


    """
    e4 e5
    Nf3 d6
    d4 Bg4
    dxe5 Bxf3
    Qxf3 dxe5
    Bc4 Nf6
    Qb3 Qe7
    Nc3 c6
    Bg5 b5
    Nxb5 cxb5
    Bxb5+ Nbd7
    O-O-O Rd8
    Rxd7 Rxd7
    Rd1 Qe6
    Bxd7+ Nxd7
    Qb8+ Nxb8
    Rd8# 1-0
    """    

    if any(char in single_move_str for char in ['=', '(', ')']):
        raise ChessAlgebraParsingException(f"Invalid chess algebra notation. Suspected non-FIDE pawn promotion notation: {single_move_str}")

    match single_move_str[-1]:
        case "#":
            expected_check_status = CheckStatus.IN_CHECK_MATE
            single_move_str_to_parse = single_move_str[:-1]
        case "+":
            expected_check_status = CheckStatus.IN_CHECK
            single_move_str_to_parse = single_move_str[:-1]
        case _:
            expected_check_status = CheckStatus.NOT_IN_CHECK
            single_move_str_to_parse = single_move_str
    # done with last character

    # returns on its own
    if single_move_str_to_parse == "O-O-O":
        if player_side == PlayerSide.White:
            to_square = ChessBoardSquare(7, 2)
        elif player_side == PlayerSide.Black:
            to_square = ChessBoardSquare(0, 2)
        else:
            raise InvalidEnumOrClassException(PlayerSide, player_side)
        
        # queenside castle
        return ParsedMove(
            piece_type_to_move=King,
            to_square=to_square,
            player_side=player_side,
            expected_check_status=expected_check_status,
            expected_capture=None,
            col_match=None,
            row_match=None,
            promotion_piece=None
        )
 
    # returns on its own
    if single_move_str_to_parse == "O-O":
        if player_side == PlayerSide.White:
            to_square = ChessBoardSquare(7, 6)
        elif player_side == PlayerSide.Black:
            to_square = ChessBoardSquare(0, 6)
        else:
            raise InvalidEnumOrClassException(PlayerSide, player_side)
        
        # kingside castle
        return ParsedMove(
            piece_type_to_move=King,
            to_square=to_square,
            player_side=player_side,
            expected_check_status=expected_check_status,
            expected_capture=None,
            col_match=None,
            row_match=None,
            promotion_piece=None
        )

    first_char = single_move_str_to_parse[0]
    if first_char in notation_piece_map.keys():
        # this is not a pawn move
        piece_type_to_move: ChessPiece = notation_piece_map[first_char]
        single_move_str_to_parse = single_move_str_to_parse[1:]
        promotion_piece = None
    else:
        # this is a pawn move
        piece_type_to_move: ChessPiece = Pawn
        # check if there is a promotion piece
        last_char = single_move_str_to_parse[-1]
        if last_char in notation_piece_map.keys():
            # it is a promotion move
            promotion_piece = notation_piece_map[last_char]
            single_move_str_to_parse = single_move_str_to_parse[:-1]
        else:
            promotion_piece = None

    # the last 2 characters can only be destination square now
    destination_square_str = single_move_str_to_parse[-2:]
    if not is_valid_chess_algebra_square(destination_square_str):
        raise ChessAlgebraParsingException(f"invalid chess algebra notation: {single_move_str}")

    to_square = chess_algebra_to_chess_square(destination_square_str)
    single_move_str_to_parse = single_move_str_to_parse[:-2]

    if len(single_move_str_to_parse) > 0:
        # only in here if there is a capture
        # or if there are row/col specifiers

        # the last char can be x or part of move notation
        if single_move_str_to_parse[-1] == "x":
            expected_capture = True
            single_move_str_to_parse = single_move_str_to_parse[:-1]
        else:
            expected_capture = False
        
        match len(single_move_str_to_parse):
            case 0:
                col_match = None
                row_match = None
            case 1:
                # either col match or row match
                if single_move_str_to_parse.isnumeric():
                    rank_val = int(single_move_str_to_parse)
                    if is_valid_rank(rank_val):
                        col_match = None
                        row_match = map_rank_to_row(rank_val)
                    else:
                        raise ChessAlgebraParsingException(f"Encountered invalid rank value {rank_val} when parsing {single_move_str}")
                elif is_valid_file(single_move_str_to_parse):
                    col_match = map_file_to_col(single_move_str_to_parse)
                    row_match = None
                else:
                    raise ChessAlgebraParsingException(f"Encountered invalid col/row match when parsing {single_move_str}")
            case 2:
                file_val = single_move_str_to_parse[0]
                rank_val = int(single_move_str_to_parse[1])
                if is_valid_rank(rank_val) and is_valid_file(file_val):
                    col_match = map_file_to_col(file_val)
                    row_match = map_rank_to_row(rank_val)
                else:
                    raise ChessAlgebraParsingException(f"Parsing failure for {single_move_str}")    
            case _:
                raise ChessAlgebraParsingException(f"Parsing failure for {single_move_str}")
    else:
        expected_capture = False
        col_match = None
        row_match = None

    return ParsedMove(
        piece_type_to_move=piece_type_to_move,
        to_square=to_square,
        player_side=player_side,
        expected_check_status=expected_check_status,
        expected_capture=expected_capture,
        col_match=col_match,
        row_match=row_match,
        promotion_piece=promotion_piece
    )

def parse_move_string(move_str: str) -> List[ParsedMove]:
    """
    examples:
    e4 e5
    Nxb5 cxb5
    Rd1 Qe6
    """

    resolved_moves: List[ParsedMove] = list()
    moves_split = move_str.split(' ')

    if moves_split[0] != "0-1":
        #  else black has won, no moves to parse
        resolved_moves.append(parse_single_move(moves_split[0], PlayerSide.White))

        if moves_split[1] != "1-0":
            # else white has won, no black move to parse
            resolved_moves.append(parse_single_move(moves_split[1], PlayerSide.Black))
    # TODO stalemate notation
    
    return resolved_moves