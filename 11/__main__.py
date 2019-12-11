import numpy as np
from collections import defaultdict
from ..intcode.VM import VM
from ..utils import loadCSVInput, dprint, asciiPrint, setVerbosity, sparseToDense
from ..utils.OCR import CharPredictor

# Debug:
# setVerbosity(True)

instructions = loadCSVInput(__file__)

DIRS = np.array([(0,-1),(1,0),(0,1),(-1,0)])

def paint(dir = 0, pos=(0,0), hull=defaultdict(int)):
    robot = VM(instructions)
    while True:
        try:
            paint_color = next(robot.run(hull[tuple(pos)]))
            turn = next(robot.run())
            dprint(f"[{pos}]: {hull[tuple(pos)]} -> {paint_color}")
            hull[tuple(pos)] = paint_color
            dir = (dir + [-1,1][turn]) % 4
            pos = tuple(pos + DIRS[dir])
            dprint(f"New pos: {pos} {'^>v<'[dir]}")
        except StopIteration:
            break
    print(f"Total white: {sum(hull.values())}\nTotal painted once: {len(hull)}")
    return hull

print("Part 1")
paint()

print("Part 2")
bitmap = paint(hull=defaultdict(int, {(0,0):1}))
asciiPrint(bitmap, transpose=True)

###################################
# OPTIONAL:
print("Upping the ante:")

# Segmenting the bitmap (cheating a bit with the cropping):
NUM_CHARS = 8
bitmap = sparseToDense(bitmap).transpose()[:,1:(1+NUM_CHARS*5)]
chars = [c for c in np.split(bitmap, NUM_CHARS, axis=1)]

# Using ML to predict each char:
predictor = CharPredictor(chars[0].shape)
predicted = predictor.predict(chars)
print("*** OCR prediction: ***\n", " ".join(predicted))
