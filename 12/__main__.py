import numpy as np
import itertools
import os
import math
from ..utils import loadXYZInput, dprint, setVerbosity

# Debug:
setVerbosity(True)

data = loadXYZInput()

pos = np.array(data).transpose()
vel = np.zeros(pos.shape)

dprint("Initial positions: \n", pos)
dprint("Initial velocities: \n", vel)

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)
def cmp(a, b):
    return (a > b) - (a < b)

# Part 1:

for step in range(1,1001):
    for axis in range(len(pos)):
        for i,j in itertools.combinations(range(0,len(vel[0])),2):
            dir = cmp(int(pos[axis][i]), int(pos[axis][j]))
            vel[axis][i] -= dir
            vel[axis][j] += dir
        pos[axis] = pos[axis] + vel[axis]

dprint("Velocities at step", step, ":\n", vel)
dprint("positions at step:", step, ":\n", pos)

total = int(sum(np.sum(abs(pos), axis=0) * np.sum(abs(vel), axis=0)))
print(f"Part 1 - Total energy at step {step}: {total}")

# Part 2:

periodicity = [0,0,0]

for axis in range(len(pos)):
    initial_state = tuple(pos[axis]) + tuple(vel[axis])
    for step in range(1,1000000):
        for i,j in itertools.combinations(range(0,len(vel[0])),2):
            dir = cmp(int(pos[axis][i]), int(pos[axis][j]))
            vel[axis][i] -= dir
            vel[axis][j] += dir
        pos[axis] = pos[axis] + vel[axis]

        if initial_state == tuple(pos[axis]) + tuple(vel[axis]):
            dprint("Periodicity for axis", axis, ":", step)
            periodicity[axis] = step
            break

dprint("Periodicities: ", periodicity)
print("Part 2 -  Pediodicity: ", lcm(lcm(periodicity[0], periodicity[1]), periodicity[2]))

# 319290382980408
