from aocd import get_data, submit
import numpy as np

import re

day = 25
year = 2021

data = get_data(day=day, year=year)

# def print_grid(grid):
#     for j in range(dims[1]):
#         for i in range(dims[0]):
#             vec = grid.get((i, j), (0, 0))
#             print({(0,0):'.', (0,1):'v', (1,0):'>'}[vec], end="")
#         print()

grid = {(x, y): {'v': (0, 1), '>': (1, 0)}[c]
        for y, line in enumerate(data.splitlines())
        for x, c in enumerate(line) if c != "."}

dims = len(data.splitlines()[0]), len(data.splitlines())
def move(x, y, dx, dy): return ((x+dx) % dims[0], (y+dy) % dims[1])

# print_grid(grid)


for i in range(1, 1000):
    new_grid = grid
    for vec_ref in ((1, 0), (0, 1)):
        new_grid = {(move(*pos, *vec) if (vec == vec_ref)
                     and (move(*pos, *vec) not in new_grid) else pos): vec
                    for pos, vec in new_grid.items()}

    if grid == new_grid:
        break
    grid = new_grid

print("Solution:", i)
# print_grid(grid)
