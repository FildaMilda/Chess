
class Piece:

    def __init__(self, color, name, coor):

        self.color = color
        self.name = name

        self.coor = coor
        self.row = coor[0]
        self.column = coor[1]

    def __repr__(self):
        return f"{self.name}({self.color}, {self.coor})"

    def move(self, coor):
        self.coor = coor
        self.row = coor[0]
        self.column = coor[1]
        self.moved = True

    def get_moves(self, board, en_passant=None):
        legal_moves = []

        for move in self.move_set:
            for i in range(1, self.move_set_loops + 1):

                r = self.row + move[0] * i
                c = self.column + move[1] * i

                if c not in range(0, 8) or r not in range(0, 8):
                    break

                elif board[r][c] == None:
                    legal_moves.append((r, c))
                    continue

                elif board[r][c].color != self.color:
                    legal_moves.append((r, c))
                    break

                elif board[r][c].color == self.color:
                    break

        return legal_moves

class King(Piece):
    def __init__(self, color, coor):
        super().__init__(color, "king", coor)

        self.color = color
        self.image = "white_king" if color else "black_king"
        self.move_set = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0]
        self.move_set_loops = 1
        self.moved = False
        self.rooks = [(7, 0), (7, 7)] if color else [(0, 0), (0, 7)]
        self.notation = "K" if color else "k"
        self.value = 0
        self.castle_rights_indexes = (0, 1) if color else (2, 3)
        self.castled = False
        self.original_square = (7, 4) if color else (0, 4)

    def get_moves(self, board, castle_rights, in_check=False, delete_check_moves=True):
        legal_moves = []

        for move in self.move_set:
            for i in range(1, self.move_set_loops + 1):

                r = self.row + move[0] * i
                c = self.column + move[1] * i

                if c not in range(0, 8) or r not in range(0, 8):
                    break

                elif board[r][c] == None:
                    legal_moves.append((r, c))
                    continue

                elif board[r][c].color != self.color:
                    legal_moves.append((r, c))
                    break

                elif board[r][c].color == self.color:
                    break

        if delete_check_moves:
            return self.delete_moves_in_check(board, legal_moves, castle_rights)

        return legal_moves

    def generate_attacking_moves(self, board, castle_rights):

        enemy_moves = []
        my_moves = []

        for row in board:
            for piece in row:

                if piece is not None:

                    if piece.name == "pawn":
                        if piece.color != self.color:
                            enemy_moves += piece.get_attack_moves()
                        else:
                            my_moves += piece.get_attack_moves()

                    elif piece.name == "king":
                        if piece.color != self.color:
                            enemy_moves += piece.get_moves(board, castle_rights, delete_check_moves=False)
                        else:
                            my_moves += piece.get_moves(board, castle_rights, delete_check_moves=False)

                    else:
                        if piece.color != self.color:
                            enemy_moves += piece.get_moves(board)
                        else:
                            my_moves += piece.get_moves(board)

        return my_moves, enemy_moves

    def delete_moves_in_check(self, board, legal_moves, castle_rights):
        enemy_moves = self.generate_attacking_moves(board, castle_rights)[1]
        legal_moves = list(set(legal_moves) - set(enemy_moves))
        legal_moves += self.add_castle(board, castle_rights, legal_moves, (self.row, self.column) in enemy_moves)
        return legal_moves 

    def add_castle(self, board, castle_rights, legal_moves, in_check):

        def clear_squares(n, right):

            for i in range(1, n+1):
                c = self.column + i if right else self.column - i
                if c not in range(0, 8) or board[self.row][c] is not None:
                    return False

            return True


        castles = []

        if self.coor == self.original_square and not in_check:
            if (self.row, self.column - 1) in legal_moves and castle_rights[self.castle_rights_indexes[0]] and board[self.row][self.column - 4] is not None and board[self.row][self.column - 4].name == "rook" and clear_squares(3, False):
                castles.append((self.row, self.column - 2))

            if (self.row, self.column + 1) in legal_moves and castle_rights[self.castle_rights_indexes[1]] and board[self.row][self.column + 3] is not None and board[self.row][self.column + 3].name == "rook" and clear_squares(2, True):
                castles.append((self.row, self.column + 2))

        return castles

class Queen(Piece):
    def __init__(self, color, coor):
        super().__init__(color, "queen", coor)

        self.color = color
        self.image = "white_queen" if color else "black_queen"
        self.move_set = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0]
        self.move_set_loops = 8
        self.moved = False
        self.notation = "Q" if color else "q"
        self.value = 9

class Rook(Piece):
    def __init__(self, color, coor):
        super().__init__(color, "rook", coor)

        self.color = color
        self.image = "white_rook" if color else "black_rook"
        self.move_set = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if (x == 0 or y == 0) and (x != 0 or y != 0)]
        self.move_set_loops = 8
        self.moved = False
        self.notation = "R" if color else "r"
        self.original_coor = coor
        self.value = 5

class Bishop(Piece):
    def __init__(self, color, coor):
        super().__init__(color, "bishop", coor)

        self.color = color
        self.image = "white_bishop" if color else "black_bishop"
        self.move_set = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 and y != 0]
        self.move_set_loops = 8
        self.moved = False
        self.notation = "B" if color else "b"
        self.value = 3

class Knight(Piece):
    def __init__(self, color, coor):
        super().__init__(color, "knight", coor)

        self.color = color
        self.image = "white_knight" if color else "black_knight"
        self.move_set = [(x, y) for x in range(-2, 3) for y in range(-2, 3) if x != 0 and y != 0 and abs(x) != abs(y)]
        self.move_set_loops = 1
        self.moved = False
        self.notation = "N" if color else "n"
        self.value = 3

class Pawn(Piece):
    def __init__(self, color, coor):
        super().__init__(color, "pawn", coor)
        
        self.color = color
        self.image = "white_pawn" if color else "black_pawn"
        self.direction = -1 if color else 1
        self.move_set = [(self.direction, 0)]
        self.moved = False
        self.move_set_loops = 1
        self.attacking_moves = [(self.direction, 1), (self.direction, -1)]
        self.notation = "P" if color else "p"
        self.value = 1
        self.original_squares = [(6, c) for c in range(8)] if color else [(1, c) for c in range(8)]

    def get_moves(self, board, en_passant):
        legal_moves = []

        self.double_forward()
        legal_moves += self.add_attack_moves(board, en_passant)

        for move in self.move_set:
            for i in range(1, self.move_set_loops + 1):

                r = self.row + move[0] * i
                c = self.column + move[1] * i

                if c not in range(0, 8) or r not in range(0, 8):
                    break

                elif board[r][c] == None:
                    legal_moves.append((r, c))
                    continue

                elif board[r][c].color != self.color:
                    break

                elif board[r][c].color == self.color:
                    break

        return legal_moves

    def get_attack_moves(self):
        
        legal_moves = []

        for move in self.attacking_moves:

            r = self.row + move[0]
            c = self.column + move[1]

            if c in range(0, 8) and r in range(0, 8):
                legal_moves.append((r, c))

        return legal_moves


    def double_forward(self):
        self.move_set_loops = 1 if self.moved else 2

    def add_attack_moves(self, board, en_passant):

        legal_moves = []

        for move in self.attacking_moves:

            r = self.row + move[0]
            c = self.column + move[1]

            if c in range(0, 8) and r in range(0, 8):
                if en_passant is not None and en_passant == (r, c):
                    legal_moves.append((r, c))

                if board[r][c] is not None and board[r][c].color != self.color:
                    legal_moves.append((r, c))

        return legal_moves
