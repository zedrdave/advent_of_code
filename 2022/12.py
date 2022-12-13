from aocd import get_data
from collections import defaultdict
import sys

day = 12
year = 2022
data = get_data(day=day, year=year)

grid = {(i, j): ord(c) - ord('a')
        for j, l in enumerate(data.split('\n')) for i, c in enumerate(l)}
end, start = [next(k for k, v in grid.items() if v == i) for i in (-28, -14)]
grid[end] = 25
grid[start] = 0

add = lambda x, d: (x[0] + d[0], x[1] + d[1])
neighbours = lambda c: [add(c, dir)
                        for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

dists = defaultdict(lambda: sys.maxsize)
dists[end] = 0
stack = [end]

while len(stack):
    coords = stack.pop()
    for neigh in neighbours(coords):
        if (neigh in grid) and (dists[neigh] > dists[coords] + 1) and (grid[neigh] >= grid[coords] - 1):
            dists[neigh] = dists[coords] + 1
            stack.append(neigh)

print('Part 1:', dists[start])
print('Part 2:', min(dists[k] for k, v in grid.items() if v == 0))
