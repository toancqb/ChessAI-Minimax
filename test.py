
ar = [[0 for i in range(8)] for i in range(8)]
ar[0][3] = 1
for i in ar:
    print(i)


    def init_pieces(self):
        self.Black = [
            Rook(B['rook'], self.cal_rect(1, 1)),
            Knight(B['knight'], self.cal_rect(2, 1)),
            Bishop(B['bishop'], self.cal_rect(3, 1)),
            Queen(B['queen'], self.cal_rect(4, 1)),
            King(B['king'], self.cal_rect(5, 1)),
            Bishop(B['bishop'], self.cal_rect(6, 1)),
            Knight(B['knight'], self.cal_rect(7, 1)),
            Rook(B['rook'], self.cal_rect(8, 1)),
        ]
        for i in range(1, 9):
            self.Black.append(Pawn(B['pawn'], self.cal_rect(i, 2)))
        self.White = [
            Rook(W['rook'], self.cal_rect(1, 8)),
            Knight(W['knight'], self.cal_rect(2, 8)),
            Bishop(W['bishop'], self.cal_rect(3, 8)),
            Queen(W['queen'], self.cal_rect(4, 8)),
            King(W['king'], self.cal_rect(5, 8)),
            Bishop(W['bishop'], self.cal_rect(6, 8)),
            Knight(W['knight'], self.cal_rect(7, 8)),
            Rook(W['rook'], self.cal_rect(8, 8)),
        ]
        for i in range(1, 9):
            self.White.append(Pawn(W['pawn'], self.cal_rect(i, 7)))

def draw_pieces(self):
    for p in self.Black:
        self.screen.blit(p.surf, p.rect)
    for p in self.White:
        self.screen.blit(p.surf, p.rect)

def init_surf_pieces(self):
    self.P = {
        'br': Rook(B['rook'], self.cal_rect(1, 1)),
        'bn':Knight(B['knight'], self.cal_rect(2, 1)),
        'bb':Bishop(B['bishop'], self.cal_rect(3, 1)),
        'bq':Queen(B['queen'], self.cal_rect(4, 1)),
        'bk':King(B['king'], self.cal_rect(5, 1)),
        'bp':Pawn(B['pawn'], self.cal_rect(1, 2)),

        'wr':Rook(W['rook'], self.cal_rect(1, 8)),
        'wn':Knight(W['knight'], self.cal_rect(2, 8)),
        'wb':Bishop(W['bishop'], self.cal_rect(3, 8)),
        'wq':Queen(W['queen'], self.cal_rect(4, 8)),
        'wk':King(W['king'], self.cal_rect(5, 8)),
        'wp':Pawn(W['pawn'], self.cal_rect(1, 7)),

        '  ': None
    }


# class Queen(pygame.sprite.Sprite):
#
#     def __init__(self, surf, rect):
#         super(Queen, self).__init__()
#         self.surf = surf
#         self.surf.set_colorkey(BLACK, RLEACCEL)
#         self.surf = pygame.transform.scale(self.surf, (PIECE_SIZE, PIECE_SIZE))
#         self.rect = rect
#
# class Rook(pygame.sprite.Sprite):
#
#     def __init__(self, surf, rect):
#         super(Rook, self).__init__()
#         self.surf = surf
#         self.surf.set_colorkey(BLACK, RLEACCEL)
#         self.surf = pygame.transform.scale(self.surf, (PIECE_SIZE, PIECE_SIZE))
#         self.rect = rect
#
# class Bishop(pygame.sprite.Sprite):
#
#     def __init__(self, surf, rect):
#         super(Bishop, self).__init__()
#         self.surf = surf
#         self.surf.set_colorkey(BLACK, RLEACCEL)
#         self.surf = pygame.transform.scale(self.surf, (PIECE_SIZE, PIECE_SIZE))
#         self.rect = rect
#
# class Knight(pygame.sprite.Sprite):
#
#     def __init__(self, surf, rect):
#         super(Knight, self).__init__()
#         self.surf = surf
#         self.surf.set_colorkey(BLACK, RLEACCEL)
#         self.surf = pygame.transform.scale(self.surf, (PIECE_SIZE, PIECE_SIZE))
#         self.rect = rect
#
# class Pawn(pygame.sprite.Sprite):
#
#     def __init__(self, surf, rect):
#         super(Pawn, self).__init__()
#         self.surf = surf
#         self.surf.set_colorkey(BLACK, RLEACCEL)
#         self.surf = pygame.transform.scale(self.surf, (PIECE_SIZE, PIECE_SIZE))
#         self.rect = rect
def a_moves(self, ar, p, type):
    x, y, lst = p[0]-1, p[1]-1, []
    for py in range(1, 8):
        if check_valid(x, y-py):
            if ar[x][y-py] == '  ':
                lst.append((x, y-py))
            if ar[x][y-py] != '  ':
                if type != ar[x][y-py][0]:
                    lst.append((x, y-py))
                break
        else:
            break
    for py in range(1, 8):
        if check_valid(x, y+py):
            if ar[x][y+py] == '  ':
                lst.append((x, y+py))
            else:
                if type != ar[x][y+py][0]:
                    lst.append((x, y+py))
                break
        else:
            break
    for px in range(1, 8):
        if check_valid(x-px, y):
            if ar[x-px][y] == '  ':
                lst.append((x-px, y))
            else:
                if type != ar[x-px][y][0]:
                    lst.append((x-px, y))
                break
        else:
            break
    for px in range(1, 8):
        if check_valid(x+px, y):
            if ar[x+px][y] == '  ':
                lst.append((x+px, y))
            else:
                if type != ar[x+px][y][0]:
                    lst.append((x+px, y))
                break
        else:
            break
