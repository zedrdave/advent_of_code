import numpy as np
import itertools
import os
import math
# from collections import defaultdict
# from ..intcode.VM import VM
from ..utils import loadCSVInput, dprint, asciiPrint, setVerbosity

# Debug:
setVerbosity(True)

# data = loadCSVInput()
inputFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt')
with open(inputFile) as f:
    data = [line.strip()[1:-1] for line in f]

positions = np.array([[int(pos[2:]) for pos in line] for line in [line.split(', ') for line in data]]).transpose()

velocities = np.zeros(positions.shape)

print("velocities: \n", velocities)
print("positions: \n", positions)

past_pos = [{},{},{}]
periodicity = np.array([0,0,0])

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

for step in range(0,1000000):
    for axis in range(0,3):
        if periodicity[axis]: continue
        state = tuple(positions[axis]) + tuple(velocities[axis])
        # print(state)
        if state in past_pos[axis]:
            print("\n*** Found periodicity for axis: ", axis, "\nStep:", step, ", state:\n", state)
            print("same as step: ", past_pos[axis][state])
            print("velocities: \n", velocities)
            print("positions: \n", positions)
            periodicity[axis] = step
        else:
            past_pos[axis][state] = step
    if np.count_nonzero(periodicity) == 3:
        break
    for i,j in itertools.combinations(range(0,len(velocities[0])),2):
        for axis,axis_positions in enumerate(positions):
            if axis_positions[i] < axis_positions[j]:
                velocities[axis][i] += 1
                velocities[axis][j] -= 1
            elif axis_positions[i] > axis_positions[j]:
                velocities[axis][i] -= 1
                velocities[axis][j] += 1
    positions = positions + velocities

print(periodicity)
print(lcm(lcm(periodicity[0], periodicity[1]), periodicity[2]))
# pot = np.sum(abs(positions), axis=0)
# kin = np.sum(abs(velocities), axis=0)
# total = sum(pot * kin)
# print("\nstep: ", step+1)
# print("velocities: \n", velocities)
# print("positions: \n", positions)
# print(total)
