import pygame
import os.path
from copy import deepcopy
from define import *
from tools import *


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
            'br': Rook(B['rook'], None, 'b', None),
            'bn': Knight(B['knight'], None, 'b', None),
            'bb': Bishop(B['bishop'], None, 'b', None),
            'bq': Queen(B['queen'], None, 'b', None),
            'bk': King(B['king'], None, 'b', [1,5]),
            'bp': Pawn(B['pawn'], None, 'b', None),

            'wr': Rook(W['rook'], None, 'w', None),
            'wn': Knight(W['knight'], None, 'w', None),
            'wb': Bishop(W['bishop'], None, 'w', None),
            'wq': Queen(W['queen'], None, 'w', None),
            'wk': King(W['king'], None, 'w', [8,5]),
            'wp': Pawn(W['pawn'], None, 'w', None),

            '  ': None
        }

    def draw_pieces(self):
        for i in range(8):
            for j in range(8):
                if self.ar[i][j] != '  ':
                    if self.ar[i][j] == '..':
                        pygame.draw.circle(self.screen, RED, cal_rect(0, i+1, j+1), CIRCLE_RADIUS)
                    elif self.ar[i][j][0] == '.':
                        self.P[self.ar[i][j][1:]].rect = cal_rect(1, i+1,j+1)
                        self.screen.blit(self.P[self.ar[i][j][1:]].surf, cal_rect(1, i+1,j+1))
                    else:
                        self.P[self.ar[i][j]].rect = cal_rect(1, i+1,j+1)
                        self.screen.blit(self.P[self.ar[i][j]].surf, cal_rect(1, i+1,j+1))

    def selecting(self, p):
        x, y = p[0]-1, p[1]-1
        lst = self.available_moves(self.ar[x][y], p, self.ar[x][y][0])
        if self.ar[x][y][-1] == 'k':
            res = self.precond_castling(self.ar[x][y][0])
            if res[0] == 1:
                lst.append((x,y-2))
            if res[1] == 1:
                lst.append((x,y+2))
        if lst != []:
            for i in lst:
                if self.ar[i[0]][i[1]] != '  ':
                    self.ar[i[0]][i[1]] = '.' + self.ar[i[0]][i[1]]
                else:
                    self.ar[i[0]][i[1]] = '..'

    def available_moves(self, pc, p, type):
        return self.P[pc].a_moves(self.ar, p, type)

    def clean_selected(self):
        for i in range(8):
            for j in range(8):
                if self.ar[i][j] == '..':
                    self.ar[i][j] = '  '
                if self.ar[i][j][:2] == '.w' or self.ar[i][j][:2] == '.b':
                    self.ar[i][j] = self.ar[i][j][1:]

    def move(self, r, rr):
        a, b, c, d = r[0]-1, r[1]-1, rr[0]-1, rr[1]-1
        if self.ar[a][b][-1] == 'k' or self.ar[a][b][-1] == 'r':
            self.P[self.ar[a][b]].update_kpos([rr[0], rr[1]])

        if self.ar[c][d][0] == '.':
            if self.ar[a][b][-1] == 'k' and (b-d==2 or d-b==2):
                if b - d == 2:
                    self.castle_move((a,b),(c,d-2))
                elif d - b == 2:
                    self.castle_move((a,b),(c,d+1))
            else:
                self.ar[c][d] = deepcopy(self.ar[a][b])
                self.ar[a][b] = '  '
        else:
            return 0
        self.clean_selected()
        return 1

    # def precond_castling(self, type):
    #     res = [0,0]
    #     if not self.is_checked(type) and not self.P[type+'k'].is_moved:
    #         p = self.P[type+'k'].k_pos
    #         x, y = p[0]-1, p[1]-1
    #         if self.ar[x][y+1] == '  ' and self.ar[x][y+2] == '  ' and self.ar[x][y+3] == type+'r':
    #             if self.is_pos_checked([x,y+1], type) and self.is_pos_checked([x,y+2], type):
    #                 res[1] = 1
    #         if self.ar[x][y-1] == '  ' and self.ar[x][y-2] == '  ' and self.ar[x][y-4] == type+'r':
    #             if self.is_pos_checked([x,y-1], type) and self.is_pos_checked([x,y-2], type):
    #                 res[0] = 1
    #
    #     return res
    def precond_castling(self, type):
        res = [0,0]
        if not self.is_checked(type) and not self.P[type+'k'].is_moved:
            p = self.P[type+'k'].k_pos
            x, y = p[0]-1, p[1]-1
            if self.ar[x][y+1] == '  ' and self.ar[x][y+2] == '  ' and self.ar[x][y+3] == type+'r':
                    res[1] = 1
            if self.ar[x][y-1] == '  ' and self.ar[x][y-2] == '  ' and self.ar[x][y-4] == type+'r':
                    res[0] = 1

        return res


    def castle_move(self, k, r):
        if r[1] > k[1]:
            self.ar[k[0]][k[1]+2] = deepcopy(self.ar[k[0]][k[1]])
            self.ar[k[0]][k[1]+1] = deepcopy(self.ar[r[0]][r[1]])
            self.ar[k[0]][k[1]], self.ar[r[0]][r[1]] = '  ', '  '
        else:
            self.ar[k[0]][k[1]-2] = deepcopy(self.ar[k[0]][k[1]])
            self.ar[k[0]][k[1]-1] = deepcopy(self.ar[r[0]][r[1]])
            self.ar[k[0]][k[1]], self.ar[r[0]][r[1]] = '  ', '  '

    def is_checked(self, type):
        p = self.P[type+'k'].k_pos
        x, y = p[0]-1, p[1]-1
        for i in range(8):
            for j in range(8):
                if self.ar[i][j] != '  ' and self.ar[i][j][0] != type:
                    for pos in self.available_moves(self.ar[i][j], (i+1,j+1), self.ar[i][j][0]):
                        if pos[0] == x and pos[1] == y:
                            return True
        return False

    def is_checkmate(self, type):
        pass

    def is_pos_checked(self, p, type):
        x, y = p[0]-1, p[1]-1
        for i in range(8):
            for j in range(8):
                if self.ar[i][j] != '  ' and self.ar[i][j][0] != type:
                    for pos in self.available_moves(self.ar[i][j], (i+1,j+1), self.ar[i][j][0]):
                        if pos[0] == x and pos[1] == y:
                            return True
        return False

    def switch_piece(self, a, b):
        x, y = a[0]-1, a[1]-1
        kx, ky = b[0]-1, b[1]-1
        if self.ar[x][y][0] == self.ar[kx][ky][0]:
            return True
        return False

    def precond(self, p, player):
        if player == 0:
            player = 'w'
        else:
            player = 'b'
        if self.ar[p[0]-1][p[1]-1] != '  ' and self.ar[p[0]-1][p[1]-1][0] == player:
            return True
        return False

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

    def a_moves(self, ar, p, type):
        x, y, lst = p[0]-1, p[1]-1, []
        if type == 'b':
            i_start, odd_type, sign = 1, 'w', 1
        else:   #type = 'w'
            i_start, odd_type, sign = 6, 'b', -1

        if x == i_start:
            if check_valid(x+sign*2, y) and ar[x+sign*2][y] == '  ':
                lst.append((x+sign*2, y))
        if check_valid(x+sign*1, y) and ar[x+sign*1][y] == '  ':
            lst.append((x+sign*1, y))
        if check_valid(x+sign*1, y-1) and ar[x+sign*1][y-1][0] == odd_type:
            lst.append((x+sign*1, y-1))
        if check_valid(x+sign*1, y+1) and ar[x+sign*1][y+1][0] == odd_type:
            lst.append((x+sign*1, y+1))

        return lst
