import pygame
import random
import os.path
from copy import deepcopy
from define import *
from tools import *
from pieces_class import *

class AI_stupid():
    def __init__(self, ar, pieces):
        self.ar = ar
        self.pieces = pieces

    def find_pos(self, ar, pieces, type):
        # lst1 = random.shuffle([0,1,2,3,4,5,6,7])
        # lst2 = random.shuffle([0,1,2,3,4,5,6,7])
        # lst = [0,1,2,3,4,5,6,7]
        # random.shuffle(lst)
        # for i in lst:
        #     for j in lst:
        #         if ar[i][j][0] == type:
        #             lst_ai = pieces.selecting_AI((i+1,j+1))
        #             if lst_ai == []:
        #                 continue
        #             random.shuffle(lst_ai)
        #             return ((i+1,j+1), lst_ai[0])
        for i in range(8):
            for j in range(8):
                if ar[i][j][0] == type:
                    lst_ai = pieces.selecting_AI((i+1,j+1))
                    if lst_ai == []:
                        continue
                    random.shuffle(lst_ai)
                    return ((i+1,j+1), lst_ai[0])
        return ()
