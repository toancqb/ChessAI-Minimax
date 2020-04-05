import pygame
import random
import os.path
from copy import deepcopy
from define import *
from tools import *
from pieces_class import *

class AI():
    def __init__(self, ar, pieces):
        self.ar = ar
        self.pieces = pieces
        self.P = pieces.P
        self.ref = {
            'p': 10,
            'n': 30,
            'b': 30,
            'r': 50,
            'q': 90,
            'k': 900
        }

    def lst_pieces_available(self, ar, type):
        lst_pieces = []
        for i in range(8):
            for j in range(8):
                if ar[i][j][0] == type:
                    lst_pieces.append((ar[i][j], i, j))
        return lst_pieces

    def eval_board(self, ar):
        score = 0
        for i in range(8):
            for j in range(8):
                if ar[i][j][0] == 'b':
                    score += self.ref[ar[i][j][-1]]
                elif ar[i][j][0] == 'w':
                    score -= self.ref[ar[i][j][-1]]
        return score

    def is_checked_AI_Move(self, ar, type):
        p = king_position(ar, type)
        x, y = p[0], p[1]
        for i in range(8):
            for j in range(8):
                if ar[i][j] != '  ' and ar[i][j][0] != type:
                    for pos in self.P[ar[i][j]].a_moves(ar,(i+1,j+1),ar[i][j][0]):
                        if pos[0] == x and pos[1] == y:
                            return True
        return False

    def is_pos_not_checked_AI_Move(self, ar, p, type): #<---
        x, y = p[0]-1, p[1]-1
        for i in range(8):
            for j in range(8):
                if ar[i][j] != '  ' and ar[i][j][0] != type:
                    for pos in self.P[ar[i][j]].a_moves(ar,(i+1,j+1),ar[i][j][0]):
                        if pos[0] == x and pos[1] == y:
                            return False
        return True

    def precond_castling_AI_Move(self, ar, type, prev_move):
        res = [0,0]
        if not self.is_checked_AI_Move(ar,type) and not prev_move.is_king_moved(type):#<---
            p = king_position(ar, type)
            x, y = p[0], p[1]
            if check_valid(y+1,y+3) and ar[x][y+1] == '  ' and ar[x][y+2] == '  ' and ar[x][y+3] == type+'r':
                if self.is_pos_not_checked_AI_Move(ar, [x,y+1], type) and self.is_pos_not_checked_AI_Move(ar, [x,y+2], type):
                    res[1] = 1
            if check_valid(y-1,y-4) and ar[x][y-1] == '  ' and ar[x][y-2] == '  ' and ar[x][y-3] == '  ' and ar[x][y-4] == type+'r':
                if self.is_pos_not_checked_AI_Move(ar, [x,y-1], type) and self.is_pos_not_checked_AI_Move(ar, [x,y-2], type):
                    res[0] = 1

        return res

    def is_prevent_check_AI_Move(self, ar, a, b, c, d, m, prev_move):
        type = ar[a][b][0]
        ar[c][d] = m
        prev_move.move(ar,a,b,c,d)
        return not prev_move.is_checked(ar, self.P, type)


    def selecting_AI_Move(self, ar, p, prev_move):
        x, y = p[0]-1, p[1]-1
        type = ar[x][y][0]
        lst = self.P[ar[x][y]].a_moves(ar, p, type) # Use as independent functions
        lst_ai = []
        if ar[x][y][-1] == 'k':
            res = self.precond_castling_AI_Move(ar,type, prev_move)
            if res[0] == 1:
                lst.append((x,y-2))
            if res[1] == 1:
                lst.append((x,y+2))
        if ar[x][y][-1] == 'p':
            tmp = prev_move.precond_en_passant(ar, x, y, type)
            if tmp != []:
                for i in tmp:
                    if self.is_prevent_check_AI_Move(deepcopy(ar),x,y,i[0],i[1],'...',prev_move):
                        lst_ai.append((i[0]+1,i[1]+1,'...'))
        if lst != []:
            for i in lst:
                if ar[i[0]][i[1]] != '  ':
                    if self.is_prevent_check_AI_Move(deepcopy(ar),x,y,i[0],i[1],'.' + deepcopy(ar[i[0]][i[1]]),prev_move):
                        lst_ai.append((i[0]+1,i[1]+1,'.' + ar[i[0]][i[1]]))
                else:
                    if self.is_prevent_check_AI_Move(deepcopy(ar),x,y,i[0],i[1],'..',prev_move):
                        lst_ai.append((i[0]+1,i[1]+1,'..'))
        return lst_ai

    def move_AI_Minimax(self, ar, r, rr, prev_move):
        a, b, c, d = r[0]-1, r[1]-1, rr[0]-1, rr[1]-1
        type = ar[a][b][0]
        ar[c][d] = rr[2]
        if ar[c][d][0] == '.':
            if ar[a][b][-1] == 'k' and (b-d==2 or d-b==2):
                if b - d == 2:
                    prev_move.update(ar[a][b], (a,b), (c,d-2))
                    self.castle_move_AI(ar,(a,b),(c,d-2))
                elif d - b == 2:
                    prev_move.update(ar[a][b], (a,b), (c,d+1))
                    self.castle_move_AI(ar,(a,b),(c,d+1))
            else:
                prev_move.update(ar[a][b], (a,b), (c,d))
                if ar[c][d] == '...':
                    if type == 'b':
                        ar[c-1][d] = '  '
                    if type == 'w':
                        ar[c+1][d] = '  '
                ar[c][d] = deepcopy(ar[a][b])
                ar[a][b] = '  '
                if ar[c][d][-1] == 'p':
                    if type == 'b' and c == 7:
                        ar[c][d] = deepcopy('bq')
                    elif type == 'w' and c == 0:
                        ar[c][d] = deepcopy('wq')

        else:
            return 0
        clean_selected(ar)
        return 1

    def castle_move_AI(self, ar, k, r):
        if r[1] > k[1]:
            ar[k[0]][k[1]+2] = deepcopy(ar[k[0]][k[1]])
            ar[k[0]][k[1]+1] = deepcopy(ar[r[0]][r[1]])
            ar[k[0]][k[1]], ar[r[0]][r[1]] = '  ', '  '
        else:
            ar[k[0]][k[1]-2] = deepcopy(ar[k[0]][k[1]])
            ar[k[0]][k[1]-1] = deepcopy(ar[r[0]][r[1]])
            ar[k[0]][k[1]], ar[r[0]][r[1]] = '  ', '  '


class AI_Minimax(AI):
    def __init__(self, ar, pieces):
        super().__init__(ar,pieces)

    def minimax(self,ar,pieces,type,alpha,beta,depth, last_move,prev_move):
        if depth == 0:
            return [self.eval_board(ar),last_move[0],last_move[1]]
        if type == 'b': # Maximal Player
            max_s = [-1000000000, None, None]
            ps = self.lst_pieces_available(ar, type)
            random.shuffle(ps)
            for piece in ps:
                x, y = piece[1], piece[2]
                lst_ai = self.selecting_AI_Move(ar, (x+1, y+1),prev_move)
                if lst_ai == []:
                    continue
                for pos in lst_ai:
                    img = deepcopy(ar[x][y])
                    cp_ar = deepcopy(ar)
                    cp_prev_move = deepcopy(prev_move)
                    self.move_AI_Minimax(cp_ar, (x+1,y+1),pos, cp_prev_move)
                    score = self.minimax(cp_ar,pieces,'w',alpha,beta,depth-1, ((x+1,y+1),pos),cp_prev_move)
                    score[0] += Score_init[img][pos[0]-1][pos[1]-1]
                    if score[0] >= max_s[0]:
                        max_s = [score[0],(x+1,y+1),pos]
                    if alpha < max_s[0]:
                        alpha = max_s[0]
                    if alpha >= beta:
                        break
            return max_s
        else: # Minimal Player
            min_s = [1000000000, None, None]
            ps = self.lst_pieces_available(ar, type)
            random.shuffle(ps)
            for piece in ps:
                x, y = piece[1], piece[2]
                lst_ai = self.selecting_AI_Move(ar, (x+1, y+1),prev_move)
                if lst_ai == []:
                    continue
                for pos in lst_ai:
                    img = deepcopy(ar[x][y])
                    cp_ar = deepcopy(ar)
                    cp_prev_move = deepcopy(prev_move)
                    self.move_AI_Minimax(cp_ar, (x+1,y+1),pos,cp_prev_move)
                    score = self.minimax(cp_ar,pieces,'b',alpha,beta,depth-1, ((x+1,y+1),pos),cp_prev_move)
                    score[0] += Score_init[img][pos[0]-1][pos[1]-1]
                    if score[0] <= min_s[0]:
                        min_s = [score[0],(x+1,y+1),pos]
                    if beta > min_s[0]:
                        beta = min_s[0]
                    if alpha >= beta:
                        break
            return min_s


class AI_stupid(AI):
    def __init__(self, ar, pieces):
        super().__init__(ar,pieces)

    def find_pos_random(self, ar, pieces, type):
        lst_pieces = self.lst_pieces_available(ar, pieces, type)
        if lst_pieces != []:
            random.shuffle(lst_pieces)
            for p in lst_pieces:
                lst_ai = pieces.selecting_AI((p[1]+1, p[2]+1))
                if lst_ai == []:
                    continue
                random.shuffle(lst_ai)
                return ((p[1]+1,p[2]+1), lst_ai[0])
