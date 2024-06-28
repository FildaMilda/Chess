import pygame

class Piece:

    def __init__(self, coor):

        self.coor = coor

class Promote_window:

    def __init__(self, x, y, square_width, square_height, win, images):

        self.x = x
        self.y = y

        self.square_width = square_width
        self.square_height = square_height
        self.border = 10

        self.width = 4 * (square_width + self.border)
        self.height = (square_height + self.border)

        self.win = win
        self.run = True

        self.white_images = images[0:4]
        self.black_images = images[4:8]

        self.clock = pygame.time.Clock()
        self.piece_index = None

    def loop(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_input()

        self.clock.tick(30)

    def mouse_input(self):

        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos

        if mouse_x in range(self.x, self.x + self.width) and mouse_y in range(self.y, self.y + self.height):
            self.run = False
            self.piece_index = (mouse_x - self.x) // (self.square_width + self.border) 

    def highlight_squares(self, piece_squares):

        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos

        if mouse_x in range(self.x, self.x + self.width) and mouse_y in range(self.y, self.y + self.height):
            x, y = piece_squares[(mouse_x - self.x) // (self.square_width + self.border)].coor
            pygame.draw.rect(self.win, (102, 255, 102), (x, y, self.square_width, self.square_height), 8, 10)             

    def draw(self, is_white):

        images = self.white_images if is_white else self.black_images
        piece_squares = []

        pygame.draw.rect(self.win, (255, 255, 255), (self.x, self.y, self.width, self.height), 0, 10)

        x = self.x + self.border
        for image in images:

            self.win.blit(image, (x, self.y))
            piece_squares.append(Piece((x, self.y + self.border // 2)))
            x += self.square_width + self.border

        self.highlight_squares(piece_squares)

        pygame.display.update()

    def pop(self, is_white):

        self.run = True

        while self.run:
            self.loop()
            self.draw(is_white)

        return self.piece_index
    

        