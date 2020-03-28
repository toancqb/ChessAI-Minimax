import pygame
import os.path
from copy import deepcopy
from define import *
from tools import *
from pieces_class import *

class PrevMove():
    def __init__(self):
        self.m = []
        self.len = 0

    def update(self, name, p1, p2): ## Position accord to Array ar
        self.m.append((name, p1, p2))
        self.len += 1

    def precond_en_passant(self, ar, a, b, type):  # ar[a][b] = 'bp' || 'wp'
        lst = []
        if type == 'b' and a == 4:
            if check_valid(a+2,b-1) and ar[a][b-1] == 'wp' and self.is_prev_move(ar[a][b],(a,b), 'wp',(a+2,b-1),(a,b-1)):
                lst.append((a+1,b-1))
            if check_valid(a+2,b+1) and ar[a][b+1] == 'wp' and self.is_prev_move(ar[a][b],(a,b), 'wp',(a+2,b+1),(a,b+1)):
                lst.append((a+1,b+1))

        if type == 'w' and a == 3:
            if check_valid(a-2,b-1) and ar[a][b-1] == 'bp' and self.is_prev_move(ar[a][b],(a,b), 'bp',(a-2,b-1),(a,b-1)):
                lst.append((a-1,b-1))
            if check_valid(a-2,b+1) and ar[a][b+1] == 'bp' and self.is_prev_move(ar[a][b],(a,b), 'bp',(a-2,b+1),(a,b+1)):
                lst.append((a-1,b+1))

        return lst

    def move(self, ar, a, b, c, d):
        if ar[c][d][0] == '.':
            if ar[c][d] == '...':
                if ar[a][b][0] == 'b':
                    ar[c-1][d] = '  '
                if ar[a][b][0] == 'w':
                    ar[c+1][d] = '  '
            ar[c][d] = deepcopy(ar[a][b])
            ar[a][b] = '  '
        else:
            return 0
        clean_selected(ar)
        return 1

    def is_checked(self, ar, P, type):
        p = king_position(ar, type)
        x, y = p[0], p[1]
        for i in range(8):
            for j in range(8):
                if ar[i][j] != '  ' and ar[i][j][0] != type:
                    for pos in P[ar[i][j]].a_moves(ar, (i+1,j+1), ar[i][j][0]):
                        if pos[0] == x and pos[1] == y:
                            return True
        return False

    def is_prev_move(self, piece1, p2, piece2, b1, b2):
        len = self.len - 1
        if self.m != []:
            while len >= 0:
                if self.m[len][0] == piece1 and self.m[len][2] == p2:
                    break
                if self.m[len][0] == piece2 and self.m[len][2] == b2 and self.m[len][1] == b1:
                    return True
                len -= 1
        return False

    def print_prev_move(self):
        len = self.len - 1
        if self.m != []:
            i = self.m[len]
            print("[%r]: (%r,%r) -> (%r,%r)" \
            % (i[0], i[1][0], i[1][1], i[2][0], i[2][1]))

    def print_moves(self):
        if self.m != []:
            for i in self.m:
                print("[%r]: (%r,%r) -> (%r,%r)" \
                % (i[0], i[1][0], i[1][1], i[2][0], i[2][1]))

class Pieces(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Pieces, self).__init__()
        self.screen = screen
        self.prev_move = PrevMove()
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
                    if self.ar[i][j] == '..' or self.ar[i][j] == '...':
                        pygame.draw.circle(self.screen, RED, cal_rect(0, i+1, j+1), CIRCLE_RADIUS)
                    elif self.ar[i][j][0] == '.':
                        self.P[self.ar[i][j][1:]].rect = cal_rect(1, i+1,j+1)
                        self.screen.blit(self.P[self.ar[i][j][1:]].surf, cal_rect(1, i+1,j+1))
                    else:
                        self.P[self.ar[i][j]].rect = cal_rect(1, i+1,j+1)
                        self.screen.blit(self.P[self.ar[i][j]].surf, cal_rect(1, i+1,j+1))

    def is_prevent_check(self, ar, a, b, c, d, m):
        type = ar[a][b][0]
        ar[c][d] = m
        self.prev_move.move(ar,a,b,c,d)
        return not self.prev_move.is_checked(ar, self.P, type)

    def selecting(self, p):
        x, y = p[0]-1, p[1]-1
        type = self.ar[x][y][0]
        if self.is_checked(type):
            lst = self.available_moves(self.ar[x][y], p, type)
            if self.ar[x][y][-1] == 'p':
                tmp = self.prev_move.precond_en_passant(self.ar, x, y, self.ar[x][y][0])
                if tmp != []:
                    for i in tmp:
                        if self.is_prevent_check(deepcopy(self.ar),x,y,i[0],i[1],'...'):
                            self.ar[i[0]][i[1]] = '...'
            if lst != []:
                for i in lst:
                    if self.ar[i[0]][i[1]] != '  ':
                        if self.is_prevent_check(deepcopy(self.ar),x,y,i[0],i[1],'.' + deepcopy(self.ar[i[0]][i[1]])):
                            self.ar[i[0]][i[1]] = '.' + self.ar[i[0]][i[1]]
                    else:
                        if self.is_prevent_check(deepcopy(self.ar),x,y,i[0],i[1],'..'):
                            self.ar[i[0]][i[1]] = '..'
        else:
            lst = self.available_moves(self.ar[x][y], p, type)
            if self.ar[x][y][-1] == 'k':
                res = self.precond_castling(type)
                if res[0] == 1:
                    lst.append((x,y-2))
                if res[1] == 1:
                    lst.append((x,y+2))
            if self.ar[x][y][-1] == 'p':
                tmp = self.prev_move.precond_en_passant(self.ar, x, y, type)
                if tmp != []:
                    for i in tmp:
                        self.ar[i[0]][i[1]] = '...'
            if lst != []:
                for i in lst:
                    if self.ar[i[0]][i[1]] != '  ':
                        if self.is_prevent_check(deepcopy(self.ar),x,y,i[0],i[1],'.' + deepcopy(self.ar[i[0]][i[1]])):
                            self.ar[i[0]][i[1]] = '.' + self.ar[i[0]][i[1]]
                    else:
                        if self.is_prevent_check(deepcopy(self.ar),x,y,i[0],i[1],'..'):
                            self.ar[i[0]][i[1]] = '..'

    def available_moves(self, pc, p, type):
        return self.P[pc].a_moves(self.ar, p, type)

    def move(self, r, rr):
        a, b, c, d = r[0]-1, r[1]-1, rr[0]-1, rr[1]-1
        type = self.ar[a][b][0]
        if self.ar[a][b][-1] == 'k' or self.ar[a][b][-1] == 'r':
            self.P[self.ar[a][b]].update_kpos([rr[0], rr[1]])

        if self.ar[c][d][0] == '.':
            if self.ar[a][b][-1] == 'k' and (b-d==2 or d-b==2):
                if b - d == 2:
                    self.prev_move.update(self.ar[a][b], (a,b), (c,d-2))
                    self.castle_move((a,b),(c,d-2))
                elif d - b == 2:
                    self.prev_move.update(self.ar[a][b], (a,b), (c,d+1))
                    self.castle_move((a,b),(c,d+1))
            else:
                self.prev_move.update(self.ar[a][b], (a,b), (c,d))
                if self.ar[c][d] == '...':
                    if type == 'b':
                        self.ar[c-1][d] = '  '
                    if type == 'w':
                        self.ar[c+1][d] = '  '
                self.ar[c][d] = deepcopy(self.ar[a][b])
                self.ar[a][b] = '  '
                if self.ar[c][d][-1] == 'p':
                    if type == 'b' and c == 7:
                        self.ar[c][d] = deepcopy('bq')
                    elif type == 'w' and c == 0:
                        self.ar[c][d] = deepcopy('wq')

        else:
            return 0
        clean_selected(self.ar)
        return 1

    def precond_castling(self, type):
        res = [0,0]
        if not self.is_checked(type) and not self.P[type+'k'].is_moved:
            p = self.P[type+'k'].k_pos
            x, y = p[0]-1, p[1]-1
            if self.ar[x][y+1] == '  ' and self.ar[x][y+2] == '  ' and self.ar[x][y+3] == type+'r':
                if self.is_pos_not_checked([x,y+1], type) and self.is_pos_not_checked([x,y+2], type):
                    res[1] = 1
            if self.ar[x][y-1] == '  ' and self.ar[x][y-2] == '  ' and self.ar[x][y-4] == type+'r':
                if self.is_pos_not_checked([x,y-1], type) and self.is_pos_not_checked([x,y-2], type):
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
        count = 0
        if self.is_checked(type):
            for x in range(8):
                for y in range(8):
                    if self.ar[x][y][0] == type:
                        lst = self.available_moves(self.ar[x][y], (x+1,y+1), type)
                        if self.ar[x][y][-1] == 'p':
                            tmp = self.prev_move.precond_en_passant(self.ar, x, y, type)
                            if tmp != []:
                                for i in tmp:
                                    if self.is_prevent_check(deepcopy(self.ar),x,y,i[0],i[1],'...'):
                                        count += 1
                        if lst != []:
                            for i in lst:
                                if self.ar[i[0]][i[1]] != '  ':
                                    if self.is_prevent_check(deepcopy(self.ar),x,y,i[0],i[1],'.' + deepcopy(self.ar[i[0]][i[1]])):
                                        count += 1
                                else:
                                    if self.is_prevent_check(deepcopy(self.ar),x,y,i[0],i[1],'..'):
                                        count += 1
            if count == 0:
                return True
        return False

    def is_pos_not_checked(self, p, type):
        x, y = p[0]-1, p[1]-1
        for i in range(8):
            for j in range(8):
                if self.ar[i][j] != '  ' and self.ar[i][j][0] != type:
                    for pos in self.available_moves(self.ar[i][j], (i+1,j+1), self.ar[i][j][0]):
                        if pos[0] == x and pos[1] == y:
                            return False
        return True

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


    def selecting_AI(self, p):
        x, y = p[0]-1, p[1]-1
        type = self.ar[x][y][0]
        lst_ai = []
        if self.is_checked(type):
            lst = self.available_moves(self.ar[x][y], p, type)
            if self.ar[x][y][-1] == 'p':
                tmp = self.prev_move.precond_en_passant(self.ar, x, y, self.ar[x][y][0])
                if tmp != []:
                    for i in tmp:
                        if self.is_prevent_check(deepcopy(self.ar),x,y,i[0],i[1],'...'):
                            self.ar[i[0]][i[1]] = '...'
                            lst_ai.append((i[0]+1,i[1]+1))
            if lst != []:
                for i in lst:
                    if self.ar[i[0]][i[1]] != '  ':
                        if self.is_prevent_check(deepcopy(self.ar),x,y,i[0],i[1],'.' + deepcopy(self.ar[i[0]][i[1]])):
                            self.ar[i[0]][i[1]] = '.' + self.ar[i[0]][i[1]]
                            lst_ai.append((i[0]+1,i[1]+1))
                    else:
                        if self.is_prevent_check(deepcopy(self.ar),x,y,i[0],i[1],'..'):
                            self.ar[i[0]][i[1]] = '..'
                            lst_ai.append((i[0]+1,i[1]+1))
        else:
            lst = self.available_moves(self.ar[x][y], p, type)
            if self.ar[x][y][-1] == 'k':
                res = self.precond_castling(type)
                if res[0] == 1:
                    lst.append((x+1,y-1))
                if res[1] == 1:
                    lst.append((x+1,y+3))
            if self.ar[x][y][-1] == 'p':
                tmp = self.prev_move.precond_en_passant(self.ar, x, y, type)
                if tmp != []:
                    for i in tmp:
                        self.ar[i[0]][i[1]] = '...'
                        lst_ai.append((i[0]+1,i[1]+1))
            if lst != []:
                for i in lst:
                    if self.ar[i[0]][i[1]] != '  ':
                        if self.is_prevent_check(deepcopy(self.ar),x,y,i[0],i[1],'.' + deepcopy(self.ar[i[0]][i[1]])):
                            self.ar[i[0]][i[1]] = '.' + self.ar[i[0]][i[1]]
                            lst_ai.append((i[0]+1,i[1]+1))
                    else:
                        if self.is_prevent_check(deepcopy(self.ar),x,y,i[0],i[1],'..'):
                            self.ar[i[0]][i[1]] = '..'
                            lst_ai.append((i[0]+1,i[1]+1))
        return lst_ai
