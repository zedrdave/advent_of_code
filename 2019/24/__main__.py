import copy
import string
import networkx as nx
import numpy as np

from ..utils import dprint, setVerbosity, inputFile
from ..graphics import snapshot, saveAnimatedGIF

arr2str = lambda a: '\n'.join([''.join(["#" if c else '.' for c in line]) for line in a])
isInMap = lambda n, w, b = 0: all(0+b <= n[i] < w.shape[i]-b for i in (0,1))
isEmpty = lambda n,w: isInMap(n,w) and w[n[0],n[1]] == '.'
move = lambda n,d, a = 1: (n[0]+ a*d[0], n[1]+ a*d[1], *n[2:])

DIRS = [(0,1),(1,0),(0,-1),(-1,0)]

setVerbosity(0)

with open(inputFile()) as f:
    wallmap = f.read()

# wallmap = """....#
# #..#.
# #.?##
# ..#..
# #...."""

wallmap = np.array([[*l] for l in wallmap.strip('\n').split('\n')])

wallmap = wallmap == '#'
print(arr2str(wallmap))

saved = set()
while True:
    if tuple(wallmap.flatten().tolist()) in saved:
        print("Repeat:")
        print(arr2str(wallmap))
        break
    saved.add(tuple(wallmap.flatten().tolist()))
    newMap = copy.deepcopy(wallmap)
    for x in np.ndindex(wallmap.shape):
        neigh = sum(wallmap[move(x,d)] for d in DIRS if isInMap(move(x,d), wallmap))
        print(neigh)
        if neigh == 1 or (neigh == 2 and not wallmap[x]):
            newMap[x] = True
        else:
            newMap[x] = False
    wallmap = newMap

val = [x * 2**i for i,x in enumerate(wallmap.flat)]
print("Part 1 - ", sum(val))

levels = {0: wallmap}
for time in range(200):
    dprint("\nTime: ", time)
    levels[min(levels.keys())-1] = np.zeros(wallmap.shape, 'bool')
    levels[max(levels.keys())+1] = np.zeros(wallmap.shape, 'bool')
    newLevels = copy.deepcopy(levels)
    for level,w in levels.items():
        for x in np.ndindex(w.shape):
            if x == (2,2):
                continue
            neigh = sum(w[move(x,d)] for d in DIRS if isInMap(move(x,d), w))
            if level+1 in levels:
                if x == (1,2):
                    neigh += sum(levels[level+1][0,:])
                elif x == (3,2):
                    neigh += sum(levels[level+1][-1,:])
                elif x == (2,1):
                    neigh += sum(levels[level+1][:,0])
                elif x == (2,3):
                    neigh += sum(levels[level+1][:,-1])
            if level-1 in levels:
                if x[0] == 0:
                    neigh += levels[level-1][1,2]
                elif x[0] == 4:
                    neigh += levels[level-1][3,2]
                if x[1] == 0:
                    neigh += levels[level-1][2,1]
                elif x[1] == 4:
                    neigh += levels[level-1][2,3]
            if neigh == 1 or (neigh == 2 and not newLevels[level][x]):
                newLevels[level][x] = True
            else:
                newLevels[level][x] = False
    levels = newLevels

totBugs = 0
for level,w in levels.items():
    totBugs += w.sum()
print("Part 2 -", totBugs)




# x > 2032
