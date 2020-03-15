import pygame
import os.path
from define import *


class Pieces(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Pieces, self).__init__()
        self.screen = screen
        self.init_array_pieces()
        self.init_surf_pieces()

    def init_array_pieces(self):
        self.ar = [['  ' for i in range(8)] for i in range(8)]
        for i in (0, 7):
            if i == 0:
                bw = 'b'
            else:
                bw = 'w'
            self.ar[i][0] = bw + 'r'
            self.ar[i][1] = bw + 'n'
            self.ar[i][2] = bw + 'b'
            self.ar[i][3] = bw + 'q'
            self.ar[i][4] = bw + 'k'
            self.ar[i][5] = bw + 'b'
            self.ar[i][6] = bw + 'n'
            self.ar[i][7] = bw + 'r'
        for i in range(8):
            self.ar[1][i] = 'bp'
            self.ar[6][i] = 'wp'

    def init_surf_pieces(self):
        self.P = {
            'br': Rook(B['rook'], (0, 0)),
            'bn': Knight(B['knight'], (0, 0)),
            'bb': Bishop(B['bishop'], (0, 0)),
            'bq': Queen(B['queen'], (0, 0)),
            'bk': King(B['king'], (0, 0)),
            'bp': Pawn(B['pawn'], (0, 0)),

            'wr': Rook(W['rook'], (0, 0)),
            'wn': Knight(W['knight'], (0, 0)),
            'wb': Bishop(W['bishop'], (0, 0)),
            'wq': Queen(W['queen'], (0, 0)),
            'wk': King(W['king'], (0, 0)),
            'wp': Pawn(W['pawn'], (0, 0)),

            '  ': None
        }

    def draw_pieces(self):
        for i in range(8):
            for j in range(8):
                if self.P[self.ar[i][j]] != None:
                    self.screen.blit(self.P[self.ar[i][j]].surf, self.cal_rect(i+1,j+1))

    def move(self):
        self.ar[6][4] = '  '
        self.ar[4][4] = 'wp'

    def cal_rect(self, rect0, rect1):
        return (rect1 * PIECE_SIZE, rect0 * PIECE_SIZE, )

class King(pygame.sprite.Sprite):

    def __init__(self, surf, rect):
        super(King, self).__init__()
        self.surf = surf
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (PIECE_SIZE, PIECE_SIZE))
        self.rect = rect


class Queen(pygame.sprite.Sprite):

    def __init__(self, surf, rect):
        super(Queen, self).__init__()
        self.surf = surf
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (PIECE_SIZE, PIECE_SIZE))
        self.rect = rect

class Rook(pygame.sprite.Sprite):

    def __init__(self, surf, rect):
        super(Rook, self).__init__()
        self.surf = surf
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (PIECE_SIZE, PIECE_SIZE))
        self.rect = rect

class Bishop(pygame.sprite.Sprite):

    def __init__(self, surf, rect):
        super(Bishop, self).__init__()
        self.surf = surf
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (PIECE_SIZE, PIECE_SIZE))
        self.rect = rect

class Knight(pygame.sprite.Sprite):

    def __init__(self, surf, rect):
        super(Knight, self).__init__()
        self.surf = surf
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (PIECE_SIZE, PIECE_SIZE))
        self.rect = rect

class Pawn(pygame.sprite.Sprite):

    def __init__(self, surf, rect):
        super(Pawn, self).__init__()
        self.surf = surf
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (PIECE_SIZE, PIECE_SIZE))
        self.rect = rect
