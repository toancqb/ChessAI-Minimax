
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
