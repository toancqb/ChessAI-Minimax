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

    def lst_pieces_available(self, ar, pieces, type):
        lst_pieces = []
        for i in range(8):
            for j in range(8):
                if ar[i][j][0] == type:
                    lst_pieces.append((ar[i][j], i, j))
        return lst_pieces

class AI_simple(AI):
    def __init__(self, ar, pieces):
        self.ar = ar
        self.pieces = pieces

class AI_stupid(AI):
    def __init__(self, ar, pieces):
        self.ar = ar
        self.pieces = pieces

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
