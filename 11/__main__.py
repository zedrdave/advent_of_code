import numpy as np
from collections import defaultdict
from ..intcode.VM import VM
from ..utils import loadCSVInput, dprint, asciiPrint, setVerbosity

setVerbosity(False)

instructions = loadCSVInput(__file__)

DIRS = np.array([(0,-1),(1,0),(0,1),(-1,0)])

def paint(dir = 0, pos=(0,0), hull=defaultdict(int), printOutput = False):

    robot = VM(instructions)

    while True:
        try:
            paint_color = next(robot.run(hull[tuple(pos)]))
            turn = next(robot.run())

            dprint(f"[{pos}]: {hull[tuple(pos)]} -> {paint_color}")

            hull[tuple(pos)] = paint_color
            dir = (dir + [-1,1][turn]) % 4
            pos = tuple(pos + DIRS[dir])
        except StopIteration:
            break

        dprint(f"New pos: {pos} {'^>v<'[dir]}")

    print(f"Total white: {sum(hull.values())}\nTotal painted once: {len(hull)}")
    if printOutput:
        asciiPrint(hull, transpose=True)


print("Part 1")
paint()
# paint(printOutput=True) # looks kinda cool!

print("Part 2")
paint(hull=defaultdict(int, {(0,0):1}), printOutput=True)
