import numpy as np
import copy
import math

with open('input.txt', 'r') as fp:
    data = np.array([list(line.strip()) for line in fp]) == '#'

data = np.swapaxes(data, 0, 1) # swap coords from (y,x) to (x,y):

# Part 1

indices = [np.array(a) for a in zip(*np.nonzero(data))]

# One-line list comprehension, because why not…
result = {
    tuple(ast): len(set([
        tuple(x//math.gcd(*x))
        for x in ast-indices
        if np.count_nonzero(x)
    ]))
    for ast in indices
}

base = max(result.keys(), key=lambda k:result[k])
print(f"Part 1: {result[base]} at pos: {base}")

# Part 2

base = np.array(base)

def angle(vector1, vector2):
    x1, y1 = vector1
    x2, y2 = vector2
    dot = x1*x2 + y1*y2
    det = x1*y2 - y1*x2
    angle = math.atan2(det, dot)
    return (2*math.pi + angle) if angle < 0 else angle

dist = lambda p1,p2: abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

counter = 1
while(True):
    targets = {}
    indices = [np.array(a) for a in zip(*np.nonzero(data))]

    for ast in sorted(indices, key=lambda x:dist(x,base)):
        dir = ast - base
        if not np.count_nonzero(dir): continue

        g = math.gcd(*dir)
        gdir = dir//g

        if tuple(gdir) in targets:
            continue
        targets[tuple(gdir)] = ast

    for k in sorted(targets.keys(), key=lambda dir: angle((0,-1), dir)):
        target = targets[k]
        # Pew pew!
        data[target[0]][target[1]] = 0
        if counter == 200:
            print(f"Part 2: #{counter} {target} -> {100*(target[0]) + target[1]}")
        counter += 1

    if len(targets) == 0:
        break;
