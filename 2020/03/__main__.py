import math

from ..utils import *

grid = [l.strip() for l in open(input_file())]

print("Using list comprehensions:")
# (We are assuming [0][0] is always False)

res = [sum(grid[v][right*idx % len(grid[0])] == '#' for idx,v in enumerate(range(0, len(grid), down)))
    for right, down in ([1,1], [3,1], [5,1], [7,1], [1,2])]

print(f"Part 1: {res[1]}\nPart 2: {math.prod(res)}")


print("\nUsing loops:")

def get_trees(right, down):
    h = 0
    trees = 0
    for v in range(down, len(grid), down):
        h = (h+right)%len(grid[0])
        trees += int(grid[v][h] == '#')
    return trees

res = [get_trees(r, d) for r, d in ([1,1], [3,1], [5,1], [7,1], [1,2])]
print(f"Part 1: {res[1]}\nPart 2: {math.prod(res)}")


print("\nCasual code golf:")

g=list(map(str.strip,open(input_file())))
a=[sum(g[v][r*i%len(g[0])]=='#' for i,v in enumerate(range(0,len(g),d))) for r,d in ([1,1],[3,1],[5,1],[7,1],[1,2])]
print(a[1],math.prod(a))
