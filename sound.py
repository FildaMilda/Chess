import pygame

pygame.mixer.init()

class Sound:

    def __init__(self, volume):

        self.move = pygame.mixer.Sound("sounds/move.wav")
        self.capture = pygame.mixer.Sound("sounds/capture.wav")
        self.castle = pygame.mixer.Sound("sounds/castle.wav")
        self.checkmate = pygame.mixer.Sound("sounds/checkmate.wav")
        self.stalemate = pygame.mixer.Sound("sounds/stalemate.wav")
        self.check = pygame.mixer.Sound("sounds/check.wav")

        self.list = [self.move, self.capture, self.castle, self.checkmate, self.stalemate, self.check]

        self.change_volume(volume)

    def change_volume(self, volume):

        for sound in self.list:
            sound.set_volume(volume)

    def choose(self, castle, capture, checkmate, stalemate, check):

        if checkmate:
            self.checkmate.play()

        elif stalemate:
            self.stalemate.play()

        elif check:
            self.check.play()

        elif capture:
            self.capture.play()

        elif castle:
            self.castle.play()

        else:
            self.move.play()
