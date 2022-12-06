from aocd import get_data, submit
from collections import defaultdict
import re

day = 5
year = 2022

data = get_data(day=day, year=year)

# submit(cube.sum(), part="a", day=day, year=year)

# data

crates, instructions = data.split("\n\n")


instructions = [[int(i) for i in re.sub('[a-z]+ ', '', inst).split()]
                for inst in instructions.split("\n")]

for part in (1, 2):
    stacks = defaultdict(list)
    for row in crates.split("\n")[:-1]:
        for i in range(0, len(row)//4 + 1):
            val = row[(i*4+1):(i*4+2)]
            if val.strip():
                stacks[i+1].insert(0, val)

    for how_many, from_s, to_s in instructions:
        if part == 1:
            for _ in range(how_many):
                stacks[to_s].append(stacks[from_s].pop())
        else:
            # print(stacks[to_s])
            stacks[to_s] += stacks[from_s][-how_many:]
            stacks[from_s] = stacks[from_s][:-how_many]
            # print(stacks[to_s])
        # print("")

    print(f"Part {part}:", ''.join(stacks[i][-1]
                                   for i in range(1, len(stacks)+1)))
