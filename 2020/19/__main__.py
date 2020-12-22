from ..utils import *
import re

rules, T = [t.split('\n') for t in open(input_file()).read().split('\n\n')]
D = { k:v for k,v in [r.split(': ') for r in rules] }

def R(r):
    if r in D: return R(D[r])
    if r[0] == '"':
        return r[1]

    x = r.split('|')
    if len(x) > 1:
        j,s = '|',' | '
    else:
        j,s = '',' '
    return '(' + j.join(R(i) for i in r.split(s)) + ')'


P = f"^{R('0')}$"
print('Part 1:', sum(1 for s in T if re.match(P, s)))

P = "^(" + '|'.join(f"{R('42')}{{{i+1},}}{R('31')}{{{i},{i}}}" for i in range(1,9)) + ")$"
print('Part 2:', sum(1 for s in T if re.match(P, s)))
