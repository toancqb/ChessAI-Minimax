
import pygame
import os.path
from copy import deepcopy
from define import *
from pieces import *
from tools import *


class Board():
    def __init__(self, screen):
        self.screen = screen
        self.color = BLUE

    def draw_board(self):
        pygame.draw.rect(self.screen, BLUE, (0, 0, SCREEN_SIZE, PIECE_SIZE))
        pygame.draw.rect(self.screen, BLUE, (0, 0, PIECE_SIZE, SCREEN_SIZE))
        pygame.draw.rect(self.screen, BLUE, (SCREEN_SIZE-PIECE_SIZE, 0, PIECE_SIZE, SCREEN_SIZE))
        pygame.draw.rect(self.screen, BLUE, (0, SCREEN_SIZE-PIECE_SIZE, SCREEN_SIZE-PIECE_SIZE, PIECE_SIZE))
        # pygame.draw.line(self.screen, GREEN, (PZ-WL, PZ-WL), (PZ-WL, SZ+WL), 2*WL)
        # pygame.draw.line(self.screen, GREEN, (PZ-WL, PZ-WL), (SZ+WL, PZ-WL), 2*WL)
        # pygame.draw.line(self.screen, GREEN, (SZ+WL, PZ-WL), (SZ+WL, SZ+WL), 2*WL)
        # pygame.draw.line(self.screen, GREEN, (PZ-WL, SZ+WL), (SZ+WL, SZ+WL), 2*WL)
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
        self.clock = pygame.time.Clock()
        board = Board(self.screen)
        pieces = Pieces(self.screen)

        # player 0 for white
        #        1 for black
        cplayer = ['w', 'b']
        player, cl, st, cmate = 0, -1, [], -1
        running = True
        while running:
            pos_clicked = ()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        pos_clicked = rev_rect(pygame.mouse.get_pos())
                        cl += 1
                        if not pieces.precond(pos_clicked, player) and cl == 0:
                            cl -= 1
                            continue

            if pos_clicked != () and cl == 0:
                pieces.selecting(pos_clicked)
                st.append(pos_clicked)
                print_ar(pieces.ar)
            if pos_clicked != () and cl == 1:
                if eq(st[0], pos_clicked):
                    cl -= 1
                    continue
                if pieces.switch_piece(st[0], pos_clicked):
                    cl, st = -1, []
                    pieces.clean_selected()
                    continue
                if not pieces.move(st[0], pos_clicked):
                    cl -= 1
                    continue
                player, cl, st = 1 - player, -1, []
                print_ar(pieces.ar)
                print("Is Checked ? ", pieces.is_checked(cplayer[player]))
                print("White King's Position:", pieces.P['wk'].k_pos)
                print("Black King's Position:", pieces.P['bk'].k_pos)


            board.draw_board()
            pieces.draw_pieces()

            pygame.display.flip()
            self.clock.tick(20)

        pygame.quit()

if __name__ == '__main__':
    t = Game()
