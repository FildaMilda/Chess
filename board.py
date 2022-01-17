from pieces import *

def is_empty(l1):

    """
    Checks if board list is empty

    Returns:
        (bool)
    """

    for row in l1:
        for l0 in row:
            if bool(l0):
                return False

    return True

class Board:

    def __init__(self, FEN="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):

        # Info from FEN string
        self.FEN = FEN
        
        self.whites_turn = True
        self.castle_rights = [False, False, False, False]
        self.en_passant_available = None

        # FEN notation tools
        self.FEN_notation = {"P" : Pawn, "R" : Rook, "N" : Knight, "B" : Bishop, "K" : King, "Q" : Queen}
        self.pieces = {"pawn" : Pawn, "rook" : Rook, "knight" : Knight, "bishop" : Bishop, "king" : King, "queen" : Queen}
        self.FEN_castle = {"K" : 0, "Q" : 1, "k" : 2, "q" : 3}
        self.FEN_castle2 = {0 : "K", 1 : "Q", 2 : "k", 3 : "q"}

        # Board
        self.width = 8
        self.height = 8

        self.convert_FEN(FEN)

        # Move history
        self.move_history_dict = {"pawn" : "P", "rook" : "R", "knight" : "N", "bishop" : "B", "king" : "K", "queen" : "Q"}
        self.coor_string = "ABCDEFGH"
        self.move_history = []
        self.move_history_lenght = -1
        self.board_history = [list(self.board)]

        self.promotion_dict = {0 : Queen, 1 : Rook, 2 : Knight, 3 : Bishop}

    def get_board(self):
        return self.board

    def reset_board(self):
        self.convert_FEN(self.FEN)
        self.move_history = []
        self.board_history = [list(self.board)]

    def get_FEN(self, board):

        """
        Returns FEN string

        Args:
            board (list) : Board (Current state)

        Returns:
            (string): FEN string
        """

        FEN = ""

        i = 0
        for row in board:
            for square in row:

                if square is None:
                    i += 1

                else:
                    FEN += str(i) if i != 0 else ""
                    i = 0
                    FEN += square.notation

            FEN += str(i) if i != 0 else ""
            i = 0
            FEN += "/"

        FEN = FEN[:-1] + " "
        FEN += "w" if self.whites_turn else "b"
        FEN += " "

        if not self.castle_rights[0] and not self.castle_rights[1] and not self.castle_rights[2] and not self.castle_rights[3]:
            FEN += "-"
        else:
            for i in range(4):

                if self.castle_rights[i]:
                    FEN += self.FEN_castle2[i]

        FEN += " - 0 1"

        return FEN

    def convert_FEN(self, FEN):

        """
        Gets information from FEN string

        Args:
            FEN (string) : FEN string
        """

        row = [None for _ in range(self.width)]
        self.board = [list(row) for _ in range(self.height)]

        FEN_board, FEN_color, FEN_castle, FEN_en_passant, FEN_halfmove, FEN_fullmove = FEN.split()

        # Inputing board
        c = 0
        r = 0

        for char in FEN_board:

            if char == "/":
                r += 1
                c = 0
                
            elif char.isdigit():
                c += int(char)

            else:
                self.place_piece(self.FEN_notation[char.upper()](True if char.isupper() else False, (r, c)), (r, c))
                c += 1

        # Inputing the first turn
        self.whites_turn = True if FEN_color == "w" else False

        # Inputing castle rights
        if FEN_castle != "-":
            for char in FEN_castle:
                self.castle_rights[self.FEN_castle[char]] = True

        # Inputing en passant
        if FEN_en_passant != "-":
            r = self.height - int(FEN_en_passant[1])
            c = self.coor_string.index(FEN_en_passant[0].upper())
            self.en_passant_available = (r, c)

    def find(self, board, piece, color=None):

        """
        Finds pieces on a board

        Args:
            board (list) : Board you want to find pieces in
            piece (Piece) : Type of piece you are looking for
            color (bool) : Piece color

        Returns:
            (list): List with pieces
        """

        pieces = []

        for row in board:
            for square in row:

                if square is not None and square.name == piece:
                    if color is None:
                        pieces.append(square)

                    else:
                        if square.color == color:
                            pieces.append(square)
                        
        return pieces

    def place_piece(self, piece, coor):
        self.board[coor[0]][coor[1]] = piece

    def remove_piece(self, coor):
        self.board[coor[0]][coor[1]] = None

    def get_piece(self, coor):
        return self.board[coor[0]][coor[1]]

    def move_piece(self, from_coor, to_coor, check_if_legal=True, castle=True):

        piece = self.get_piece(from_coor)

        if check_if_legal:
            moves = self.board_moves[piece.row][piece.column]

        else:
            moves = self.get_correct_moves(piece)

        if from_coor is not None and to_coor is not None and piece is not None:
            if to_coor in moves:

                piece.move(to_coor)
                self.place_piece(piece, (to_coor))
                self.remove_piece(from_coor)

                self.handle_en_passant_move(piece, from_coor, to_coor)
                if castle:
                    self.handle_castling(piece, from_coor, to_coor)
                self.update_castle_rights()

                self.whites_turn = not self.whites_turn
                self.update_move_history(from_coor, to_coor, piece)

    def get_correct_moves(self, piece):

        """
        Specification for getting moves per piece

        Returns:
            (list)
        """

        if piece.name == "pawn":
            piece_moves = piece.get_moves(self.board, self.en_passant_available)

        elif piece.name == "king":
            piece_moves = piece.get_moves(self.board, self.castle_rights)

        else:
            piece_moves = piece.get_moves(self.board)

        return piece_moves

    def handle_castling(self, piece, from_coor, to_coor):

        self.is_last_move_castle = False

        if piece.name == "king":
            if from_coor == (to_coor[0], to_coor[1] - 2) or from_coor == (to_coor[0], to_coor[1] + 2):

                a = (1, -1) if from_coor == (to_coor[0], to_coor[1] - 2) else (-2, 1)
                piece.castled = True
                rook = self.get_piece((piece.row, piece.column + a[0]))

                self.remove_piece(rook.coor)
                rook.move((piece.row, piece.column + a[1]))
                self.place_piece(rook, (piece.row, piece.column + a[1]))

                self.is_last_move_castle = True

    def handle_en_passant_move(self, piece, from_coor, to_coor):

        if piece.name == "pawn":
            if to_coor == self.en_passant_available:
                r, c = self.en_passant_available
                self.remove_piece((r - piece.direction, c))

            if from_coor[0] +  2 * piece.direction == to_coor[0]:
                self.update_en_passant(piece)
            else:
                self.update_en_passant(piece, reset=True)
        else:
            self.update_en_passant(piece, reset=True)

    def update_move_history(self, from_coor, to_coor, piece, castle=None):

        piece_notation = self.move_history_dict[piece.name] if piece.color else self.move_history_dict[piece.name].lower()
        f_coor_notation = self.coor_string[from_coor[1]] + str(self.width - from_coor[0])
        t_coor_notation = self.coor_string[to_coor[1]] + str(self.width - to_coor[0] + 1)

        self.move_history.append(f"{piece_notation} {f_coor_notation} - {t_coor_notation} |")
        self.board_history.append(list(self.board))

    def in_check(self):

        king = self.find(self.board, "king", self.whites_turn)[0]
        enemy_moves = self.get_enemy_moves()

        if king.coor in enemy_moves:
            return True
        else:
            return False

    def get_game_state(self):

        if self.stalemate():
            return "stalemate"

        elif self.checkmate():
            return "checkmate"

        else:
            return None

    def is_pawn_promoting(self):

        pawns = self.find(self.board, "pawn")

        for pawn in pawns:

            if pawn.color and pawn.row == 0 or not pawn.color and pawn.row == self.height -1:
                return True, pawn

        return False

    def promote_pawn(self, pawn, to):

        piece = self.promotion_dict[to]
        self.place_piece(self.promotion_dict[to](pawn.color, pawn.coor), pawn.coor)

    def board_changed(self):

        """
        Checks if board changed (Someone moved)

        Returns:
            (bool)
        """

        if self.move_history_lenght != len(self.move_history):
            self.move_history_lenght = len(self.move_history)
            return True
        
        return False

    def update(self):

        if self.board_changed():
            self.board_moves = self.get_moves()
            self.print_info()

    def checkmate(self):

        # Looks for checkmate

        if self.in_check and is_empty(self.board_moves):
            return True

        return False

    def stalemate(self):

        # Looks for stalemate

        if is_empty(self.board_moves) and not self.in_check():
            return True
        
        return False

    def get_enemy_moves(self):
        
        moves = []

        for r in range(self.height):
            for c in range(self.width):

                piece = self.get_piece((r, c))

                if piece is not None:
                    if piece.color != self.whites_turn:

                        piece_moves = self.get_correct_moves(piece)
                        moves += piece_moves

        return moves

    def get_my_moves(self):

        moves = []

        for r in range(self.height):
            for c in range(self.width):

                if self.board[r][c] is not None and self.get_piece((r, c)).color == self.whites_turn:
                    moves += self.board_moves[r][c]

        return moves

    def get_moves(self):

        # Returns all (legal) moves for current board

        row = [[] for _ in range(self.width)]
        moves = [list(row) for _ in range(self.height)]
        FEN = self.get_FEN(self.board)

        for r in range(self.height):
            for c in range(self.width):

                piece = self.get_piece((r, c))

                if piece is not None:
                    if piece.color == self.whites_turn:

                        piece_moves = self.get_correct_moves(piece)
                        legal_moves = []

                        for move in piece_moves:
                            if self.is_legal(piece, move, FEN) is True:
                                legal_moves.append(move)

                        moves[r][c] = legal_moves

        return moves

    def is_legal(self, piece, move, FEN):

        # Checks if move is legal

        test_board = Board(FEN)
        test_board.whites_turn = not test_board.whites_turn

        test_board.move_piece(piece.coor, move, check_if_legal=False, castle=False)
        return not test_board.in_check()

    def update_en_passant(self, piece, reset=False):

        # updates en passant variable

        if reset:
            self.en_passant_available = None
        else:
            self.en_passant_available = (piece.row - piece.direction, piece.column)

    def update_castle_rights(self):

        rooks = self.find(self.board, "rook", self.whites_turn)
        king = self.find(self.board, "king", self.whites_turn)[0]
        original_rook_coors = king.rooks
        i = (0, 1) if king.color else (2, 3)

        if king.moved or king.castled:
            self.castle_rights[i[0]] = False
            self.castle_rights[i[1]] = False

        else:
            for rook in rooks:
                if rook.moved:
                    if rook.original_coor in original_rook_coors:
                        a = original_rook_coors.index(rook.original_coor)
                        self.castle_rights[i[a]] = False

    def get_score(self, board):

        score = 0

        for row in board:
            for piece in row:

                if piece is not None:

                    score += piece.value if piece.color else -piece.value

        return score

    def print_info(self):
        turn = "white" if self.whites_turn else "black"
        score = str(self.get_score(self.board))
        check = "True" if self.in_check() else "False"
        checkmate = "True" if self.checkmate() else "False"
        stalemate = "True" if self.stalemate() else "False"

        print("--- Move history:")
        print(*self.move_history)
        print()
        print("Turn: " + turn)
        print("Piece score: " + score)
        print("In check: " + check)
        print(f"En passant: {self.en_passant_available}")
        print("Castle rights: K  Q  k  q")
        print(self.castle_rights)
        print("Number of available moves: " + str(len(self.get_my_moves())))
        print("Checkmate: " + checkmate)
        print("Stalemate: " + stalemate)
        print()
