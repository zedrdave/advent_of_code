
from aocd import get_data, submit
import numpy as np
import sys
import itertools
from collections import defaultdict, Counter
import re
from tqdm.auto import tqdm

day = 24
year = 2022

data = get_data(day=day, year=year)

dirs = ((1, 0), (0, 1), (-1, 0), (0, -1), (0, 0))
dirs_letters = dict(zip(">v<^", dirs))

lines = data.split('\n')
blizards = {(x, y): {dirs_letters[v]} for y, l in enumerate(lines[1:-1]) for x, v in enumerate(l[1:-1]) if v != '.'}
dims = len(lines[0]) - 2, len(lines) - 2

all_blizards = [blizards]
for i in range(1, np.lcm(*dims)):
    new_bliz = defaultdict(set)
    for (x, y), b_dirs in all_bliz[-1].items():
        for dx, dy in b_dirs:
            new_bliz[((x + dx) % dims[0], (y + dy) % dims[1])].add((dx, dy))
    all_blizards.append(new_bliz)


def shortest_path(all_blizards, dims, start_min, start_pos, end_pos):
    cur_nodes = {start_pos}

    for minute in range(start_min + 1, 10000):
        next_nodes = {(x, y)
                      for x in range(dims[0]) for y in range(dims[1])
                      if (x, y) not in all_bliz[minute % len(all_bliz)]}
        next_nodes.add(start_pos)

        cur_nodes = {(x + dx, y + dy) for x, y in cur_nodes for dx, dy in dirs
                     if (x + dx, y + dy) in next_nodes}

        if end_pos in cur_nodes:
            # print(f"Reached {n} in {minute} minutes. Solution: {minute+1}")
            return minute + 1


t1 = shortest_path(all_blizards, dims=dims, start_min=0, start_pos=(0, -1), end_pos=(dims[0] - 1, dims[1] - 1))
print("Part 1:", t1)

t2 = shortest_path(all_blizards, dims=dims, start_min=t1, start_pos=(dims[0] - 1, dims[1]), end_pos=(0, 0))
t3 = shortest_path(all_blizards, dims=dims, start_min=t2, start_pos=(0, -1), end_pos=(dims[0] - 1, dims[1] - 1))

print("Part 2:", t3)
