from define import *

def cal_rect(bool, rect0, rect1):
    if bool:
        return (rect1 * PIECE_SIZE, rect0 * PIECE_SIZE, )
    else:
        return (rect1 * PIECE_SIZE + PIECE_SIZE//2, rect0 * PIECE_SIZE + PIECE_SIZE//2, )

def rev_rect(pos):
    return (pos[1] // PIECE_SIZE, pos[0] // PIECE_SIZE)

def eq(a, b):
    if a[0] == b[0] and a[1] == b[1]:
        return True
    return False

def check_valid(n, m):
    if (n >= 0 and n <= 7) and (m >= 0 and m <= 7):
        return True
    return False

def print_ar(ar):
    print("==================================")
    for i in ar:
        print(i)
    print("==================================")
