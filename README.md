
Board chess with pieces. 
Program is making sure all of the moves are legal.

Illegal moves:

- Any play where a piece is moved with an inappropriate movement (for example, moving a Knight as if it were a Bishop).
- Moving a piece to a square occupied by another piece of the same color.
- Moving a piece to a square occupied by an opponent’s piece and not removing the board’s captured piece.
- Moving Bishop, Rook, or Queen is passing over other pieces.
- Move a pawn to the last row, and do not replace it with another chess piece.
- Moving a pawn to the last row and replacing it with any object that is not a Queen, Rook, Bishop, or Knight of the same color as the Pawn.
- Make a move leaving your own King in check.
- Castling when it is not valid to do so.

You can set the board by passing FEN string to class Board(FEN). 
Online FEN string generator:
http://www.netreal.de/Forsyth-Edwards-Notation/index.php

