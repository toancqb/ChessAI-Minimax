import pygame
import os.path


from pygame.locals import (
    MOUSEBUTTONDOWN,
    RLEACCEL,
    QUIT,
)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN_SIZE = 500
PIECE_SIZE = 50
CIRCLE_RADIUS = 7

BLACK = (0, 0, 0)
ORANGE = (181, 101, 29)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (135, 206, 250)
RED = (255, 0, 0)

B = {
        'king': pygame.image.load(os.path.join("img", "black_king.png")),
        'queen': pygame.image.load(os.path.join("img", "black_queen.png")),
        'rook': pygame.image.load(os.path.join("img", "black_rook.png")),
        'bishop': pygame.image.load(os.path.join("img", "black_bishop.png")),
        'knight': pygame.image.load(os.path.join("img", "black_knight.png")),
        'pawn': pygame.image.load(os.path.join("img", "black_pawn.png")),
    }

W = {
        'king': pygame.image.load(os.path.join("img", "white_king.png")),
        'queen': pygame.image.load(os.path.join("img", "white_queen.png")),
        'rook': pygame.image.load(os.path.join("img", "white_rook.png")),
        'bishop': pygame.image.load(os.path.join("img", "white_bishop.png")),
        'knight': pygame.image.load(os.path.join("img", "white_knight.png")),
        'pawn': pygame.image.load(os.path.join("img", "white_pawn.png")),
    }
