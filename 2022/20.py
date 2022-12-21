from aocd import get_data, submit
import numpy as np
import sys
import itertools
from collections import defaultdict, Counter
import re

day = 20
year = 2022

data = get_data(day=day, year=year)


def solve(data, rounds, key):
    numbers = [(i, int(n) * key) for i, n in enumerate(data.split("\n"))]

    for _ in range(rounds):
        for i in range(len(numbers)):
            cur_idx = next(cur_idx for cur_idx, (idx, _)
                           in enumerate(numbers) if idx == i)
            idx, num = numbers.pop(cur_idx)
            numbers.insert((cur_idx + num) % len(numbers), (idx, num))

    zero_idx = next(cur_idx for cur_idx, (_, n)
                    in enumerate(numbers) if n == 0)
    return sum(numbers[(zero_idx + (shift * 1000)) % len(numbers)][1] for shift in range(1, 4))


print("Part 1:", solve(data, rounds=1, key=1))
print("Part 2:", solve(data, rounds=10, key=811589153))
