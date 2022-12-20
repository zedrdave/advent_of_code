from aocd import get_data, submit
import numpy as np
import sys
import itertools
from collections import defaultdict, Counter
import re

day = 18
year = 2022

data = get_data(day=day, year=year)

cubes = {tuple([int(i) for i in l.split(',')]) for l in data.split()}

faces = len(cubes) * 6
faces -= sum(tuple(cc + d * pp for cc, pp in zip(c, p)) in cubes
             for c in cubes for d in (-1, 1) for p in ((1, 0, 0), (0, 1, 0), (0, 0, 1)))

print("Part 1:", faces)


m = max(max(cubes, key=lambda x: x[i])[i] for i in range(3))

steam = set(
    [(a, b, c) for a in (-1, m + 2)
     for b in range(-1, m + 2) for c in range(-1, m + 2)]
    + [(b, c, a) for a in (-1, m + 2)
        for b in range(-1, m + 2) for c in range(-1, m + 2)]
    + [(c, a, b) for a in (-1, m + 2)
        for b in range(-1, m + 2) for c in range(-1, m + 2)]
)

expanded = True
while expanded:
    expanded = False
    for x in range(0, m + 1):
        for y in range(0, m + 1):
            for z in range(0, m + 1):
                if (x, y, z) in cubes or (x, y, z) in steam:
                    continue
                for d in (-1, 1):
                    if (x + d, y, z) in steam or (x, y + d, z) in steam or (x, y, z + d) in steam:
                        steam.add((x, y, z))
                        expanded = True
                        break

cooling = {(x, y, z)
           for x in range(0, m + 1)
           for y in range(0, m + 1)
           for z in range(0, m + 1)
           if (x, y, z) not in steam}

faces = len(cubes) * 6
faces -= sum(tuple(cc + d * pp for cc, pp in zip(c, p)) in cooling
             for c in cubes for d in (-1, 1) for p in ((1, 0, 0), (0, 1, 0), (0, 0, 1)))


print("Part 2:", faces)
