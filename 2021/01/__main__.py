from utils import *

data = load_int_input(1)


def fn(d): return sum(b > a for a, b in zip(d, d[1:]))


print('Part 1:', fn(data))
print('Part 2:', fn([sum(x) for x in zip(data, data[1:], data[2:])]))
