

def pr(lst):
    for i in lst:
        print(i)
    print("\n")

Score_init_BQ1 = [
    [  -2,  -1,  -1,-0.5,-0.5,  -1,  -1,  -2],
    [  -1,   0, 0.5,   0,   0,   0,   0,  -1],
    [  -1, 0.5, 0.5, 0.5, 0.5, 0.5,   0,  -1],
    [   0,   0, 0.5, 0.5, 0.5, 0.5,   0,-0.5],
    [-0.5,   0, 0.5, 0.5, 0.5, 0.5,   0,-0.5],
    [  -1,   0, 0.5, 0.5, 0.5, 0.5,   0,  -1],
    [  -1,   0,   0,   0,   0,   0,   0,  -1],
    [  -2,  -1,  -1,-0.5,-0.5,  -1,  -1,  -2]
]

Score_init_BQ = [i[::-1] for i in Score_init_BQ1]
# Score_init_BQ = []
# for lst in Score_init_BQ1:
#     lst.reverse()
#     Score_init_BQ.append(lst)

pr(Score_init_BQ1)
pr(Score_init_BQ)

# a = [[1, 2, 3]]
# a.reverse()
# for x in a:
#     x.reverse()
#
# print(a)
