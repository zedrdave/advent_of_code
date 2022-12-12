from aocd import get_data, submit
import numpy as np
import sys
import itertools
from collections import defaultdict, Counter
import re

day = 10
year = 2022

data = get_data(day=day, year=year)

# submit(cube.sum(), part="a", day=day, year=year)

# data

cycles = 0
register = 1
signal = 0
CRT_WIDTH = 40


def draw_crt(cycle, register):
    c = '⬜️' if cycle % CRT_WIDTH in (r+register for r in (-1, 0, 1)) else '⬛️'
    end = '\n' if (cycle+1) % CRT_WIDTH == 0 else ''
    print(c, end=end)


def add_signal(cycles, register):
    return cycles*register if (cycles+20) % 40 == 0 else 0


for l in data.split("\n"):
    draw_crt(cycles, register)
    cycles += 1
    signal += add_signal(cycles, register)

    if l.startswith('addx'):
        draw_crt(cycles, register)
        cycles += 1
        signal += add_signal(cycles, register)

        register += int(l.split()[1])


print("Part 1:", signal)
