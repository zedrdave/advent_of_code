from aocd import get_data, submit

day = 17
year = 2022
data = get_data(day=day, year=year)

# data = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

rocks = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##""".split("\n\n")

rocks = [set((x, y)
             for y, l in enumerate(reversed(r.split("\n"))) for x, c in enumerate(l) if c == '#')
         for r in rocks]


cave_width = 7

move = lambda r, d: {(x + d[0], y + d[1]) for x, y in r}
jets = {'<': (-1, 0), '>': (1, 0)}

height = lambda s: max(y for _, y in s)
is_valid = lambda rock, cave: all(
    0 <= x < cave_width for x, _ in rock) and (len(rock & cave) == 0)


def print_cave(cave, rock={}):
    for y in reversed(range(0, height(cave | rock) + 1)):
        print('|', end='')
        for x in range(cave_width):
            print('#' if (x, y) in cave else (
                '@' if (x, y) in rock else '.'), end='')
        print('|')
    print("")


def play_game(tot_rocks,
              cycle_height_start=False, cycle_height_len=False):
    cave = set([(x, 0) for x in range(cave_width)])

    true_cycle_start = False
    skipped_cycles = 0
    cycle_rocks_len = 0

    j = 0
    for num_rocks in range(tot_rocks):
        h = height(cave)

        # Skip cycles if any:
        if cycle_height_start:
            if num_rocks == tot_rocks - skipped_cycles * cycle_rocks_len:
                print(f"Reached {num_rocks} rocks + {skipped_rocks} skipped -> ",
                      f"{num_rocks + skipped_rocks}")

                real_height = h + skipped_cycles * cycle_height_len
                print(f"Height: {h} + {skipped_cycles*cycle_height_len} = ",
                      f"{real_height}")
                return cave, real_height

            if not true_cycle_start:
                if (h > cycle_height_start):
                    print(f"Cycle starts at: {num_rocks} rocks | height: {h}")
                    true_cycle_start = h
                    cycle_rocks_start = num_rocks
            elif not skipped_cycles and (h - true_cycle_start == cycle_height_len):
                print(f"Full cycle at: {num_rocks} rocks | height: {h}")
                cycle_rocks_len = num_rocks - cycle_rocks_start
                skipped_cycles = (tot_rocks - num_rocks) // cycle_rocks_len
                skipped_rocks = skipped_cycles * cycle_rocks_len

                print(f"Cycle length in rocks: {cycle_rocks_len}")
                print(f"Skipping {skipped_cycles} cycles: ",
                      f"{skipped_rocks} rocks | {skipped_cycles*cycle_height_len} height")

        rock = move(rocks[num_rocks % len(rocks)], (2, h + 4))

        while rock:
            jet = jets[data[j % len(data)]]
            j += 1
            new_pos = move(rock, jet)
            if is_valid(new_pos, cave):
                rock = new_pos
            new_pos = move(rock, (0, -1))
            if is_valid(new_pos, cave):
                rock = new_pos
            else:
                cave |= rock
                rock = set()

    return cave, height(cave)


cave, part1 = play_game(2022)
print("Part 1:", part1, "\n")


cave, _ = play_game(5000)  # need to be big enough to find cycle…

marker_x_pos = range(1, cave_width)  # (0, 7) works with real data but not test
markers = sorted({y for _, y in cave if all(
    (x, y) in cave for x in marker_x_pos)})
print(f"Found {len(markers)} markers")

cycle_height_start = False
for i, y2 in enumerate(markers):
    for y1 in markers[i + 1:]:
        # if y2-y1 < 10:
        #     continue
        y3 = 2 * y2 - y1
        if y3 not in markers:
            continue
        block1 = {(x, y - y2) for x, y in cave if y2 <= y < y1}
        block2 = {(x, y - y3) for x, y in cave if y3 <= y < y2}
        if block1 == block2:
            print(y1, y2, y3)
            assert y1 - y2 == y2 - y3
            cycle_height_len = y1 - y2
            cycle_height_start = y3
            print("Cycle start:", cycle_height_start)
            print("Cycle len:", cycle_height_len)
            break
    if cycle_height_start:
        break

assert cycle_height_start

_, h = play_game(1000000000000,
                 cycle_height_start=cycle_height_start,
                 cycle_height_len=cycle_height_len)

print("\nPart 2:", h)
