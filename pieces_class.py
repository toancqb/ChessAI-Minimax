import pygame
import random
from define import *
from tools import *


class King(pygame.sprite.Sprite):

    def __init__(self, surf, rect, type, p):
        super(King, self).__init__()
        self.surf = surf
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (PIECE_SIZE, PIECE_SIZE))
        self.rect = rect
        self.type = type
        self.is_moved = False
        self.k_pos = p

    def a_moves(self, ar, p, type):
        x, y, lst = p[0]-1, p[1]-1, []
        index = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
        for i in index:
            nx, ny = x+i[0], y+i[1]
            if check_valid(nx, ny):
                if ar[nx][ny] == '  ' or ar[x][y][0] != ar[nx][ny][0]:
                    lst.append((nx, ny))
        return lst

    def update_kpos(self, p):
        self.is_moved = True
        self.k_pos = p

class Queen(King):
    def __init__(self, surf, rect, type, p):
        super(Queen, self).__init__(surf, rect, type, p)

    def a_moves(self, ar, p, type):
        x, y, lst = p[0]-1, p[1]-1, []
        index = [(-1,-1), (-1,1), (1,-1), (1,1), (0,-1), (0,1), (-1,0), (1,0)]
        for i in index:
            for pxy in range(1, 8):
                kx, ky = x + i[0]*pxy, y + i[1]*pxy
                if check_valid(kx, ky):
                    if ar[kx][ky] == '  ':
                        lst.append((kx, ky))
                    else:
                        if type != ar[kx][ky][0]:
                            lst.append((kx, ky))
                        break
                else:
                    break

        return lst


class Bishop(King):
    def __init__(self, surf, rect, type, p):
        super(Bishop, self).__init__(surf, rect, type, p)

    def a_moves(self, ar, p, type):
        x, y, lst = p[0]-1, p[1]-1, []
        index = [(-1,-1), (-1,1), (1,-1), (1,1)]
        for i in index:
            for pxy in range(1, 8):
                kx, ky = x + i[0]*pxy, y + i[1]*pxy
                if check_valid(kx, ky):
                    if ar[kx][ky] == '  ':
                        lst.append((kx, ky))
                    else:
                        if type != ar[kx][ky][0]:
                            lst.append((kx, ky))
                        break
                else:
                    break

        return lst

class Rook(King):
    def __init__(self, surf, rect, type, p):
        super(Rook, self).__init__(surf, rect, type, p)
        self.is_moved = False

    def a_moves(self, ar, p, type):
        x, y, lst = p[0]-1, p[1]-1, []
        index = [(0,-1), (0,1), (-1,0), (1,0)]
        for i in index:
            for pxy in range(1, 8):
                kx, ky = x + i[0]*pxy, y + i[1]*pxy
                if check_valid(kx, ky):
                    if ar[kx][ky] == '  ':
                        lst.append((kx, ky))
                    else:
                        if type != ar[kx][ky][0]:
                            lst.append((kx, ky))
                        break
                else:
                    break

        return lst

    def update_kpos(self, p):
        self.is_moved = True

class Knight(King):
    def __init__(self, surf, rect, type, p):
        super(Knight, self).__init__(surf, rect, type, p)

    def a_moves(self, ar, p, type):
        x, y, lst = p[0]-1, p[1]-1, []
        index = [(-1,-2), (-1,2), (1,-2), (1,2)]
        for i in index:
            nx, ny = x+i[0], y+i[1]
            if check_valid(nx, ny):
                if ar[nx][ny] == '  ' or type != ar[nx][ny][0]:
                    lst.append((nx, ny))
            nx, ny = x+i[1], y+i[0]
            if check_valid(nx, ny):
                if ar[nx][ny] == '  ' or type != ar[nx][ny][0]:
                    lst.append((nx, ny))
        return lst

class Pawn(King):
    def __init__(self, surf, rect, type, p):
        super(Pawn, self).__init__(surf, rect, type, p)
        self.is_jumped = False

    def a_moves(self, ar, p, type):
        x, y, lst = p[0]-1, p[1]-1, []
        if type == 'b':
            i_start, odd_type, sign = 1, 'w', 1
        else:   #type = 'w'
            i_start, odd_type, sign = 6, 'b', -1

        if x == i_start:
            if check_valid(x+sign*2, y):
                if ar[x+sign*1][y] == '  ' and ar[x+sign*2][y] == '  ':
                    lst.append((x+sign*2, y))

        if check_valid(x+sign*1, y) and ar[x+sign*1][y] == '  ':
            lst.append((x+sign*1, y))
        if check_valid(x+sign*1, y-1) and ar[x+sign*1][y-1][0] == odd_type:
            lst.append((x+sign*1, y-1))
        if check_valid(x+sign*1, y+1) and ar[x+sign*1][y+1][0] == odd_type:
            lst.append((x+sign*1, y+1))

        return lst

    def update_pawn(self, a, c):
        if self.type == 'b':
            cond = a < c - 1
        else:
            cond = a > c + 1
        if cond:
            self.is_jumped = True
        else:
            self.is_jumped = False

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(os.path.join("img","cloud.png")).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_SIZE+20, SCREEN_SIZE+100),
                random.randint(0, SCREEN_SIZE),
            )
        )
        self.speed = 4

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
