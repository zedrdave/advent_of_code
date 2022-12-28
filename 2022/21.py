from aocd import get_data, submit
import numpy as np
import sys
import itertools
from collections import defaultdict, Counter
import re

day = 21
year = 2022

data = get_data(day=day, year=year)

ops = {l.split(': ')[0]: l.split(': ')[1].split() for l in data.split('\n')}
ops


def recur_solve(ops, op):
    if len(ops[op]) == 1:
        return int(ops[op][0])
    return eval(f"{recur_solve(ops, ops[op][0])} {ops[op][1]} {recur_solve(ops, ops[op][2])}")


# def recur_solve(ops, op):
#     """Safer, faster, without eval"""
#     next_ops = ops[op]
#     if len(next_ops) == 1:
#         return int(next_ops[0])
#     vals = [recur_solve(ops, next_ops[0]), recur_solve(ops, next_ops[2])]
#     if next_ops[1] == '+':
#         return vals[0] + vals[1]
#     if next_ops[1] == "-":
#         return vals[0] - vals[1]
#     if next_ops[1] == '*':
#         return vals[0] * vals[1]
#     if next_ops[1] == '/':
#         return vals[0] / vals[1]


print("Part 1:", int(recur_solve(ops, 'root')))


def inv_search(ops, start, end, sign=None):
    step = (end - start) // 10
    # print("inv_search", start, end, step)

    for humn in range(start, end + step, step):
        ops['humn'] = [humn]
        diff = recur_solve(ops, ops["root"][2]) - recur_solve(ops, ops["root"][0])
        if diff == 0:
            print("Part 2:", humn)
            break
        if sign is None:
            sign = (diff > 0) - (diff < 0)
        if diff * sign < 0:
            inv_search(ops, start=humn - step, end=humn, sign=sign)
            break


inv_search(ops, start=0, end=int(1e13))
