from board import Board
from window import Promote_window

import pygame
import os

pygame.font.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

light_0 = (238,238,210)
dark_0 = (186,202,68)

light_1 = (243, 229, 171)
dark_1 = (139,69,19)

light_red = (220,20,60)

palet = [(255, 192, 79), (255, 105, 87), (255, 175, 168), (76, 170, 139)]

class Window:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.board_width = 8
        self.board_height = 8

        self.square_width = width // 8
        self.square_height = height // 8

        self.icon = pygame.image.load("..\piece_images\icon.png")

        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chess")
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.fps = 15

        # Load piece images

        self.images = {}
        for image in os.listdir("..\piece_images"):

            self.images[image[:-4]] = pygame.transform.scale(pygame.image.load("../piece_images/" + image), (self.square_width, self.square_height))

        self.selected_square = None

        self.promotion_images = [self.images["white_queen"], self.images["white_rook"], self.images["white_knight"], self.images["white_bishop"], self.images["black_queen"], self.images["black_rook"], self.images["black_knight"], self.images["black_bishop"]]
        self.promote_win = Promote_window(self.width // 2 - (4 * (self.square_width + 10)) // 2, self.height // 2 - (self.square_height + 10) // 2, self.square_width, self.square_height, self.win, self.promotion_images)

        # Load text/fonts

        self.font72 = pygame.font.SysFont("arial.ttf", 72)
        self.font32 = pygame.font.SysFont("arial.ttf", 32)

        self.chekmate_text = self.font72.render("CHECKMATE", True, black)
        self.stalemate_text = self.font72.render("STALEMATE", True, black)
        self.restart_text = self.font32.render("Press [BACKSPACE] to restart", True, black)

    def get_coor(self, position):

        """
        Gets board coordination from mouse position

        Args:
            position (tuple) : Mouse position

        Returns:
            (tuple): Board coordinance
        """

        return position[1] // self.square_height, position[0] // self.square_width

    def loop(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

                if event.key == pygame.K_BACKSPACE:
                    board.reset_board()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.update_selected_square(pygame.mouse.get_pos(), event.button)

        self.update()
        self.draw()

        self.clock.tick(self.fps)

    def draw(self):
        self.win.fill(white)

        self.draw_board(white, (204, 204, 255))
        self.highlight_selected_square()
        self.highlight_checkmate()
        self.highlight_check()
        self.draw_pieces(board.get_board())
        self.draw_moves(board.board_moves)
        self.draw_gameover_text()

        pygame.display.update()

    def draw_board(self, light_color, dark_color):

        """
        Args:
            light_color (RGB) : board light color
            dark_color (RGB) : board dark color
        """

        for x in range(self.board_width):
            for y in range(self.board_height):

                pygame.draw.rect(self.win, light_color if (x + y) % 2 == 0 else dark_color, (x * self.square_width, y * self.square_height, self.square_width, self.square_height))

    def draw_pieces(self, board):

        for row in board:
            for piece in row:

                if piece is not None:
                    self.win.blit(self.images[piece.image], (piece.column * self.square_width, piece.row * self.square_height))

    def draw_moves(self, all_moves):

        """
        Draws possible moves per piece

        Args:
            all_moves (list) : List of all possible moves 
        """

        if self.selected_square is not None:

            r, c = self.selected_square

            for move in all_moves[r][c]:

                rm, cm = move
                pygame.draw.rect(self.win, (102, 255, 102), (cm * self.square_width + self.square_width // 2 - ((self.square_width // 4) // 2), rm * self.square_height + self.square_height // 2 - ((self.square_height // 4) // 2), self.square_width // 4, self.square_height // 4), 0, 4)

    def draw_gameover_text(self):

        state = board.get_game_state()
        if state is not None:

            text = self.chekmate_text if state == "checkmate" else self.stalemate_text
            x, y = self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2 
            self.win.blit(text, (x, y))
            self.win.blit(self.restart_text, ( self.width // 2 - self.restart_text.get_width() // 2, y + text.get_height() + 20 ))

    def highlight_selected_square(self):

        if self.selected_square is not None:
            r, c = self.selected_square

            pygame.draw.rect(self.win, (102, 255, 102), (c * self.square_width, r * self.square_height, self.square_width, self.square_height), 8, 10)

    def highlight_check(self):

        if board.in_check():
            king = board.find(board.board, "king", board.whites_turn)[0]
            if king.color == board.whites_turn:
                r, c = king.coor

            pygame.draw.rect(self.win, (255, 102, 102), (c * self.square_width, r * self.square_height, self.square_width, self.square_height), 8, 10)

    def highlight_checkmate(self):

        if board.checkmate():
            king = board.find(board.board, "king", board.whites_turn)[0]

            pygame.draw.rect(self.win, (255, 152, 152), (king.column * self.square_width, king.row * self.square_height, self.square_width, self.square_height))

    def update(self):
        self.handle_promoting()
        board.update()

    def update_selected_square(self, mouse_pos, button):

        """
        Keeps track of selected square/Changes selected square/Moves the piece

        Args:
            mouse_pos (tuple) : Mouse position
            button (int) : Pressed mouse button
        """

        coor = self.get_coor(mouse_pos)
        piece = board.get_piece(coor)

        if button == 1:
            if self.selected_square is None:
                if piece is not None and piece.color == board.whites_turn:
                    self.set_selected_square(coor)

            else:
                if self.selected_square == coor:
                    self.reset_selected_square()

                else:
                    board.move_piece(self.selected_square, coor)
                    self.reset_selected_square()

        elif button == 3:
            self.reset_selected_square()

    def handle_promoting(self):

        prom = board.is_pawn_promoting()

        if prom:
            pawn = prom[1]
            promote_to = self.promote_win.pop(pawn.color)

            board.promote_pawn(pawn, promote_to)

    def reset_selected_square(self):
        self.selected_square = None

    def set_selected_square(self, coor):
        self.selected_square = coor

render = Window(800, 800)
board = Board()

while True:
    render.loop()