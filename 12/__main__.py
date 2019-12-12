import numpy as np
import itertools
import os
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

for step in range(0,1000):
    for i,j in itertools.combinations(range(0,len(velocities[0])),2):
        for axis,axis_positions in enumerate(positions):
            if axis_positions[i] < axis_positions[j]:
                velocities[axis][i] += 1
                velocities[axis][j] -= 1
            elif axis_positions[i] > axis_positions[j]:
                velocities[axis][i] -= 1
                velocities[axis][j] += 1

    positions = positions + velocities

pot = np.sum(abs(positions), axis=0)
kin = np.sum(abs(velocities), axis=0)
total = sum(pot * kin)
print("\nstep: ", step+1)
print("velocities: \n", velocities)
print("positions: \n", positions)
print(total)
