import random
from copy import deepcopy
from AI import AI
from define_sunfish import Score_initsf, piece_eval


class AI_Sunfish(AI):
    def __init__(self, ar, pieces):
        super().__init__(ar,pieces)

    def eval_board(self, ar):
        score = 0
        for i in range(8):
            for j in range(8):
                if ar[i][j][0] == 'b':
                    score += piece_eval[ar[i][j][-1]]
                elif ar[i][j][0] == 'w':
                    score -= piece_eval[ar[i][j][-1]]
        return score

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
                    if self.is_checkmate_AI_Move(cp_ar, 'w',prev_move):
                        score = [10000000000000,(x+1,y+1),pos]
                    else:
                        score = self.minimax(cp_ar,pieces,'w',alpha,beta,depth-1, ((x+1,y+1),pos),cp_prev_move)
                        score[0] += Score_initsf[img][pos[0]-1][pos[1]-1]
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
                    if self.is_checkmate_AI_Move(cp_ar, 'b', prev_move):
                        score = [-10000000000000,(x+1,y+1),pos]
                    else:
                        score = self.minimax(cp_ar,pieces,'b',alpha,beta,depth-1, ((x+1,y+1),pos),cp_prev_move)
                        score[0] += Score_initsf[img][pos[0]-1][pos[1]-1]
                    if score[0] <= min_s[0]:
                        min_s = [score[0],(x+1,y+1),pos]
                    if beta > min_s[0]:
                        beta = min_s[0]
                    if alpha >= beta:
                        break
            return min_s