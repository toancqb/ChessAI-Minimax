
import pygame
import os.path
from define import *
from pieces import *

class Board():
    def __init__(self, screen):
        self.screen = screen
        self.color = WHITE

    def draw_board(self):
        pygame.draw.rect(self.screen, self.color, (0, 0, SCREEN_SIZE, PIECE_SIZE))
        pygame.draw.rect(self.screen, self.color, (0, 0, PIECE_SIZE, SCREEN_SIZE))
        pygame.draw.rect(self.screen, self.color, (SCREEN_SIZE-PIECE_SIZE, 0, PIECE_SIZE, SCREEN_SIZE))
        pygame.draw.rect(self.screen, self.color, (0, SCREEN_SIZE-PIECE_SIZE, SCREEN_SIZE-PIECE_SIZE, PIECE_SIZE))
        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 0:
                    self.color = WHITE
                else:
                    self.color = ORANGE
                pygame.draw.rect(
                    self.screen, self.color,
                    (PIECE_SIZE*(x+1), PIECE_SIZE*(y+1), PIECE_SIZE, PIECE_SIZE))



class Game():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        board = Board(self.screen)
        pieces = Pieces(self.screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            board.draw_board()
            pieces.move()
            pieces.draw_pieces()

            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    t = Game()
