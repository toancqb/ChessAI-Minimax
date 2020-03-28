
import pygame
import os.path
import random
from copy import deepcopy
from define import *
from pieces import *
from tools import *
from AI import *


class Board():
    def __init__(self, screen):
        self.screen = screen
        self.color = BLUE

    def draw_board(self, C):
        pygame.draw.rect(self.screen, C, (0, 0, SCREEN_SIZE, PIECE_SIZE))
        pygame.draw.rect(self.screen, C, (0, 0, PIECE_SIZE, SCREEN_SIZE))
        pygame.draw.rect(self.screen, C, (SCREEN_SIZE-PIECE_SIZE, 0, PIECE_SIZE, SCREEN_SIZE))
        pygame.draw.rect(self.screen, C, (0, SCREEN_SIZE-PIECE_SIZE, SCREEN_SIZE-PIECE_SIZE, PIECE_SIZE))
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
        self.font = pygame.font.SysFont("comicsansms", 35)
        self.font2 = pygame.font.SysFont("comicsansms", 72)
        board = Board(self.screen)
        pieces = Pieces(self.screen)

        option = self.Menu()
        if option == 1:
            cmate = self.Game_player_vs_player(board, pieces)
        elif option == 2:
            cmate = self.Game_player_vs_AI(board, pieces)
        self.Game_Over(board, pieces, cmate)

        pygame.quit()

    def Menu(self):
        self.screen.fill(BLUE)

        txt = self.font2.render("-= Chess Game =-", True, RED)
        txt_center = (
            SCREEN_SIZE/2 - txt.get_width() // 2,
            SCREEN_SIZE/2 - txt.get_height() // 2
        )

        txt2 = self.font.render("Press <Space> to Play", True, GREEN)
        txt2_center = (
            SCREEN_SIZE/2 - txt2.get_width() // 2,
            SCREEN_SIZE/2 + 30
        )

        ADDCLOUD = pygame.USEREVENT + 3
        pygame.time.set_timer(ADDCLOUD, 2000)

        clouds_decor = pygame.sprite.Group()
        clouds_decor.add(Cloud())
        clouds_decor.add(Cloud())
        option = -1
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        option = 1
                        running = False
                    if event.key == K_UP:
                        option = 2
                        running = False
                elif event.type == QUIT:
                    running = False
                elif event.type == ADDCLOUD:
                    new_cloud = Cloud()
                    clouds_decor.add(new_cloud)

            clouds_decor.update()
            self.screen.fill(BLUE)

            self.screen.blit(txt, txt_center)
            self.screen.blit(txt2, txt2_center)

            for entity in clouds_decor:
                self.screen.blit(entity.surf, entity.rect)

            pygame.display.flip()
            self.clock.tick(30)

        return option


    def Game_player_vs_player(self, board, pieces):
        # player 0 for white
        #        1 for black
        cplayer = ['w', 'b']
        C = [BLUE, BLACK]
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
                    clean_selected(pieces.ar)
                    continue
                if not pieces.move(st[0], pos_clicked):
                    cl -= 1
                    continue
                player, cl, st = 1 - player, -1, []
                print_ar(pieces.ar)
                print("Is Checked ? ", pieces.is_checked(cplayer[player]))
                print("Is CheckMate ? ", pieces.is_checkmate(cplayer[player]))
                if pieces.is_checked(cplayer[player]):
                    if pieces.is_checkmate(cplayer[player]):
                        cmate = 1-player
                        running = False

            board.draw_board(C[player])
            pieces.draw_pieces()

            pygame.display.flip()
            self.clock.tick(30)
        return cmate

    def Game_player_vs_AI(self, board, pieces):
        cplayer = ['w', 'b']
        C = [BLUE, BLACK]
        player, cl, st, cmate = 0, -1, [], -1
        AI = AI_stupid(pieces.ar, pieces)
        running = True
        while running:
            pos_clicked = ()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    if player == 0 and pygame.mouse.get_pressed()[0]:
                        pos_clicked = rev_rect(pygame.mouse.get_pos())
                        cl += 1
                        if not pieces.precond(pos_clicked, player) and cl == 0:
                            cl -= 1
                            continue
            if player == 0:
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
                        clean_selected(pieces.ar)
                        continue
                    if not pieces.move(st[0], pos_clicked):
                        cl -= 1
                        continue
                    player, cl, st = 1 - player, -1, []
                    print_ar(pieces.ar)
                    if pieces.is_checked(cplayer[player]):
                        if pieces.is_checkmate(cplayer[player]):
                            cmate = 1-player
                            running = False
            else: # player(AI) = 1
                pos = AI.find_pos_optimal(pieces.ar, pieces, 'b')
                pieces.move(pos[0], pos[1])
                print_ar(pieces.ar)
                player = 1 - player
                if pieces.is_checked(cplayer[player]):
                    if pieces.is_checkmate(cplayer[player]):
                        cmate = 1-player
                        running = False
            board.draw_board(C[player])
            pieces.draw_pieces()

            pygame.display.flip()
            self.clock.tick(30)
        return cmate

    def Game_Over(self, board, pieces, cmate):
        if cmate == -1:
            txt = "-= Never Give Up =-"
        else:
            txt = "-= PLAYER "+str(cmate+1)+" WON! =-"
        txt = self.font.render(txt, True, GREEN)
        txt_center = (
            SCREEN_SIZE/2 - txt.get_width() // 2,
            50/2 - txt.get_height() // 2
        )
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            board.draw_board(BLUE)
            pieces.draw_pieces()
            self.screen.blit(txt, txt_center)

            pygame.display.flip()
            self.clock.tick(30)



if __name__ == '__main__':
    t = Game()
