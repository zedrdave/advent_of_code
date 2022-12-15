import numpy as np
from numba import jit
from tqdm.auto import tqdm
from aocd import get_data

day = 15
year = 2022
data = get_data(day=day, year=year)


coords = [[int(i) for i in re.match(pattern=r"[^=]+=(\-?\d+), y=(\-?\d+)[^=]+=(\-?\d+), y=(\-?\d+)",
          string=l).groups()] for l in data.split('\n')]

manhattan = lambda x1, y1, x2, y2: abs(x1 - x2) + abs(y1 - y2)
sensors = [(c[0], c[1], manhattan(*c)) for c in coords]


y = 2000000
part1 = sum(1 for x in tqdm(range(min(sx - m + sy - y for sx, sy, m in sensors), max(sx + m - sy + y for sx, sy, m in sensors)))
            if not any(((x, y) == (bx, by)) or ((x, y) == (sx, sy)) for sx, sy, bx, by in coords)
            and any(manhattan(x, y, sx, sy) <= m for sx, sy, m in sensors))

print("Part 1: ", part1)

max_c = 4000000

found = False
for y in tqdm(range(0, max_c + 1)):
    x = 0
    while (x <= max_c) and not found:
        dm = max(m - manhattan(x, y, sx, sy) for sx, sy, m in sensors)
        if dm < 0:
            found = True
            print("Part 2:", x * 4000000 + y)
            break
        x += max(1, dm)
    if found:
        break


# The fastest slowest solution:

@jit(nopython=True)
def go_fast(S):
    for y in range(0, max_c + 1):
        x = 0
        while x <= max_c:
            dm = (S[:, 2] - np.abs(x - S[:, 0]) - np.abs(y - S[:, 1])).max()
            if dm < 0:
                return x * 4000000 + y
            x += max(1, dm)


print("Part 2:", go_fast(S=np.array(sensors)))
