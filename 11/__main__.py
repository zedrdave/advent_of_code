import numpy as np
import os
from ..intcode.VM import VM
from ..utils import loadCSVInput, dprint, asciiPrint, setVerbosity

setVerbosity(True)

instructions = loadCSVInput(__file__)

def paint(hull, pos, dir, printOutput = False):
    dirs = np.array([(0,-1),(1,0),(0,1),(-1,0)])
    painted = set()
    pos = tuple(pos)

    robot = VM(instructions)
    while robot.is_running:
        paint_color = robot.run(hull[pos[0]][pos[1]])
        if paint_color is None:
            break
            
        dprint(f"[{pos}]: {hull[pos]} -> {paint_color}")
        hull[pos] = paint_color
        painted.update((pos,))
        dir = (dir + [-1,1][robot.run()]) % 4
        pos = tuple(pos + dirs[dir])
        dprint(f"New pos: {pos} {'^>v<'[dir]}")

    print(f"Total white: {np.count_nonzero(hull)}\nTotal painted once: {len(painted)}")
    if printOutput:
        asciiPrint(hull.transpose())

print("Part 1")
hull = np.zeros((10000,10000), 'int')
pos = [5000,5000]
dir = 0
paint(hull, pos, dir)

print("Part 2")
hull = np.zeros((45,10), 'int')
pos = [1,1]
hull[pos[0]][pos[1]] = 1
dir = 0
paint(hull, pos, dir, printOutput=True)
