from aocd import get_data, submit
from collections import defaultdict
import numpy as np
import sys
import itertools
from collections import defaultdict, Counter
from tqdm.auto import tqdm

import re

day = 23
year = 2021

data = get_data(day=day, year=year)


# data = """#############
# #...........#
# ###D#D#C#B###
#   #D#C#B#A#
#   #D#B#A#C#
#   #B#A#A#C#
#   #########"""
  
  
def print_grid(grid):
    for j in range(max(y for _,y in grid)+1):
        for i in range(13):
            print(grid.get((i, j), '.' if (j == 1 and i not in (0,12)) or (j in (2,3) and  i in (3,5,7,9)) else '◼️'), end="")
        print("")
    print("")


def get_path(start, end):
    between = lambda a, b: range(a+1, b+1) if a < b else range(a-1, b-1, -1)
    
    if start[1] <= end[1]:
        return list(zip(between(start[0], end[0]), [start[1]]*abs(start[0]-end[0]))) \
            + list(zip([end[0]]*abs(start[1]-end[1]), between(start[1], end[1])))
    else:
        return list(zip([start[0]]*abs(start[1]-end[1]), between(start[1], end[1]))) \
            + list(zip(between(start[0], end[0]), [end[1]]*abs(start[0]-end[0])))


path_cost = lambda amphi, path: len(path) * 10 ** "ABCD".index(amphi)
cave_of = lambda c: 3 + "ABCD".index(c)*2


def explore(grid, cave_ys, energy = 0):
    
    global best_energy, grid_energy
    
    if energy >= best_energy:
        return sys.maxsize
    
    if energy > 0 and all(y >= 2 for _,y in grid):
        return energy
    
    k = tuple((p,grid[p]) for p in sorted(grid))
    if grid_energy.get(k, sys.maxsize) <= energy:
        return sys.maxsize
    grid_energy[k] = energy
    
    targets = []
    
    for (x,y), c in grid.items():
        own_cave = cave_of(c)
        
        if y == 1:
            target_x = own_cave
            if any(c != grid.get((target_x, j), c) for j in cave_ys):
                continue
            target_y = next(i for i in reversed(cave_ys) if (target_x, i) not in grid)
            path = get_path((x,y), (target_x, target_y))
            targets.append((x, y, path))   

        else:
            if (x == own_cave) and all(grid[(x, j)] == c for j in cave_ys if j >= y):
                continue
            if any(((x, j) in grid) for j in cave_ys if j < y):
                continue
                        
            target_y = 1
            for target_x in (1,2,4,6,8,10,11):
                path = get_path((x,y), (target_x, target_y))
                targets.append((x, y, path))   
                
        
    return min((explore({path[-1]: grid[(x,y)], **{p: cc for p, cc in grid.items() if p != (x,y)}}, 
                                cave_ys=cave_ys,
                                energy=energy + path_cost(grid[(x,y)], path),
                        ) for x, y, path in targets if all(p not in grid for p in path)), default=sys.maxsize)


def solve(data):
    global best_energy, grid_energy
    grid_energy = dict()
    best_energy = sys.maxsize

    grid = {(x,y): c for y, line in enumerate(data.split('\n')) for x, c in enumerate(line) if c in 'ABCD'}
    grid_ys = list(range(2, max(y for _,y in grid)+1))
    print(grid_ys)
    print_grid(grid)
    print(explore(grid, cave_ys=grid_ys))

solve(data)

new_data = data.split('\n')
new_data = '\n'.join(new_data[:3] + ["  #D#C#B#A#\n  #D#B#A#C#"] + new_data[3:])
solve(new_data)