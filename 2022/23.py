
from aocd import get_data
from collections import Counter

day = 23
year = 2022

data = get_data(day=day, year=year)

add = lambda a, b: (a[0] + b[0], a[1] + b[1])

dirs = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
dirs.update({a + b: add(dirs[a], dirs[b]) for a in 'NS' for b in 'EW'})
dirs.update({b + a: add(dirs[a], dirs[b]) for a in 'NS' for b in 'EW'})  # Dirty but works…

elves = {(i, j) for j, l in enumerate(data.split('\n')) for i, v in enumerate(l) if v == '#'}
next_dirs = 'NSWE'

for r in range(1, 10000):
    moves = dict()
    for elf in elves:
        if all(add(elf, d) not in elves for d in dirs.values()):
            moves[elf] = elf
            continue
        moves[elf] = next((add(elf, dirs[d1])
                           for d1 in next_dirs
                           if all(add(elf, dirs[d1 + d2]) not in elves
                                  for d2 in (('W', 'E', '') if d1 in 'NS' else ('N', 'S', '')))), elf)

    if all(k == v for k, v in moves.items()):
        bounds_i = min(i for i, _ in grid), max(i for i, _ in grid) + 1
        bounds_j = min(j for _, j in grid), max(j for _, j in grid) + 1
        empty_ground = sum((i, j) not in grid for j in range(*bounds_j) for i in range(*bounds_i))
        print(f"Part 2: {empty_ground}")
        break

    next_dirs = next_dirs[1:] + next_dirs[0]
    counts = Counter(moves.values())
    elves = {prev_pos if counts[next_pos] > 1 else next_pos for prev_pos, next_pos in moves.items()}

    if r == 10:
        print("Part 1:", empty_ground(elves))
