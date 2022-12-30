from aocd import get_data, submit
from collections import defaultdict
import numpy as np
import sys
import itertools
from collections import defaultdict, Counter
from tqdm.auto import tqdm

import re

day = 24
year = 2021

data = get_data(day=day, year=year)

digits = [l.split('\n') for l in data.split('inp w')[1:]]

params = []
for insts in zip(*[all_insts for all_insts in zip(*digits) if len(set(all_insts)) > 1]):
    a,b,c  = ([i.split(' ')[-1] for i in insts])
    params += [(int(a), int(b), int(c))]

div_prod = [np.prod([a for a,_,_ in params][i:]) for i in range(len(params))]


run_1 = lambda z,b,w: int((z % 26) + b != w)
run_2 = lambda z,a,x,c,w: (z // a) * (1 + (25 * x)) + (w + c) * x

def solve(part, z=0, step=0, digits = []):    
    if step == 14:
        if z == 0:
            print(f"Part {part}:", "".join(str(i) for i in digits))
            return True
        return False
    
    if z > div_prod[step]:
        return False
    
    a,b,c = params[step]
    
    if part == 1:
        R = range(9, 0, -1)
    else:
        R = range(1, 10, 1)
        
    if step == 0:
        R = tqdm(R)
        
    for w in R:
        x = run_1(z,b,w)
        next_z = run_2(z,a,x,c,w)
        
        res = solve(part, next_z, step+1, digits + [w])
        if res is True:
            return res

    return False
    
solve(part=1)
solve(part=2)