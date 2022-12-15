from aocd import get_data
day = 14
year = 2022
data = get_data(day=day, year=year)


def r_range(s, e):
    if (s[0] > e[0]) or (s[1] > e[1]):
        return r_range(e, s)
    if s[0] == e[0]:
        return [(s[0], i) for i in range(s[1], e[1] + 1)]
    else:
        return [(i, s[1]) for i in range(s[0], e[0] + 1)]


rocks = [[list(map(int, c.split(','))) for c in l.split(" -> ")]
         for l in data.split("\n")]
rock_set = set(x for l in rocks for s, e in zip(
    l, l[1:]) for x in r_range(s, e))


def print_cave(rock_set, sand_set=set()):
    bottom = max(y for _, y in rock_set | sand_set)
    for j in range(0, bottom + 1):
        for i in range(min(x for x, _ in rock_set | sand_set),
                       max(x for x, _ in rock_set | sand_set) + 1):
            if (j == bottom) or (i, j) in rock_set:
                print('#', end='')
            elif (i, j) in sand_set:
                print('o', end='')
            else:
                print('.', end='')
        print('')
    print('')


move = lambda x, y: ((x + dx, y + dy) for dx, dy in ((0, 1), (-1, 1), (1, 1)))

# print_cave(rock_set=rock_set)
bottom = max(y for _, y in rock_set)
reached_the_void = False
sand_set = set()
while not reached_the_void:
    sand = (500, 0)
    while not reached_the_void:
        next_sand = next(
            (s for s in move(*sand) if (s not in rock_set) and (s not in sand_set)), None)
        if next_sand is None:
            sand_set.add(sand)
            break
        if next_sand[1] > bottom:
            reached_the_void = True
            break
        sand = next_sand

# print_cave(rock_set=rock_set, sand_set=sand_set)
print('Part 1:', len(sand_set))

bottom = max(y for _, y in rock_set) + 2
reached_the_top = False
sand_set = set()
while not reached_the_top:
    sand = (500, 0)
    while not reached_the_top:
        next_sand = next(
            (s for s in move(*sand) if (s not in rock_set) and (s not in sand_set)), None)
        if next_sand is None or next_sand[1] >= bottom:
            sand_set.add(sand)
            if sand == (500, 0):
                reached_the_top = True
            break
        sand = next_sand

# print_cave(rock_set=rock_set, sand_set=sand_set)
print('Part 2:', len(sand_set))
