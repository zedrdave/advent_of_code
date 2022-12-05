from aocd import get_data, submit
from collections import defaultdict
import numpy as np
import sys
import itertools
from collections import defaultdict, Counter

day = 3
year = 2022

data = get_data(day=day, year=year)

# submit(cube.sum(), part="a", day=day, year=year)

# data
# 
# 
P = [[ord(c) - (96 if c.islower() else 38) for c in l] for l in data.split("\n")]

sum((set(l[:len(l)//2]) & set(l[len(l)//2:])).pop() for l in P)

sum((set(P[i]) & set(P[i+1]) & set(P[i+2])).pop() for i  in range(0, len(P), 3))