This is a basic chess game to get the feel for self-motivated programming again.

Pieces:
Pawn
Knight
Bishop
Rook
Queen
King

TODO
- file and rank are getting crossed with Tuples
- sort this out in Chessboard and everywhere
- it breaks move logic

Game Mechanics
- pawn promotion
- en passant
- castling

En Passant:
- an opposing pawn takes 2-step 
- that pawn is adjacent to current player's pawn
- this pawn can move behind opposing's 2-step pawn

Game Functionality
- Undo move


# In chess algebraic notation, 
castling is represented by "0-0" for kingside (short) castling and 
"0-0-0" for queenside (long) castling.

# what are the ways to handle different moves?
## arguing for just square_a to square_b
# pawn promotion -> requires additional input
# en passant -> nothing special
# castling -> can interpret "move king to specific cell for king or queen side castle"

# when calculating check, also need to consider the aggressive moves they can make
# vs just move moves
# like in getting opponent's moves, this is actually getting what cells they currently threaten
    # en-passant or castling to a cell doesn't mean it's threatened