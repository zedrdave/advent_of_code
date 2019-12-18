import sys
import copy
# from collections import defaultdict
import numpy as np
import itertools

from ..intcode.VM import VM, NeedInputException
from ..utils import loadCSVInput, dprint, setVerbosity
# from ..graphics import snapshot, saveAnimatedGIF

# Debug:
setVerbosity(False)

instructions = loadCSVInput()

# with open('2019/17/input.txt') as f:
#     instructions = [int(i.strip()) for i in f.read().split(',')]

arr2str = lambda a: '\n'.join([''.join([str(c) for c in line]) for line in a])

vm = VM(instructions)
outputStr = ''
while vm.is_running:
    for c in vm.run():
        outputStr += chr(c)
        print(chr(c), end='')


# outputStr = """.........................................
# ...................#############.........
# ...................#.....................
# ...................#.....................
# ...................#.....................
# ...................#.....................
# ...................#.....................
# ...................###########...........
# .............................#...........
# ...................#######...#...........
# ...................#.....#...#...........
# ...................#.....#...#...........
# ...................#.....#...#...........
# ...................#.....#...#...........
# ...................#.....#...#...........
# .###########.......#.....#...#...........
# .#.........#.......#.....#...#...........
# .#.........#.....#####...#...#...........
# .#.........#.....#.#.#...#...#...........
# .#.....#############.#...#...###########.
# .#.....#...#.....#...#...#.............#.
# .#.....#...#######...#...#####.........#.
# .#.....#.............#.......#.........#.
# .#.....#.............#.......#.........#.
# .#.....#.............#.......#.........#.
# .#.....#.........#######################.
# .#.....#.........#...#.......#...........
# .#.....#.......#######.#######...........
# .#.....#.......#.#.....#.................
# .#######.......#.#.....#.................
# ...............#.#.....#.................
# ...#######.....#.###########.............
# ...#.....#.....#.......#...#.............
# ...#.....#.....#####...#...#.............
# ...#.....#.........#...#...#.............
# ...#.....#.........#...#...#.............
# ...#.....#.........#...#...#.............
# ...#.....###########...#####.............
# ...#.....................................
# ...#.....................................
# ...#.....................................
# ...###########...........................
# .............#...........................
# .............#...........................
# .............#...........................
# .............#...........................
# .............#...........................
# ...^##########...........................
# ........................................."""


scaffolds = np.array([[*l] for l in outputStr.strip().split('\n')])

# Get intersections:

arr = scaffolds == '#'
intersections = np.zeros(arr.shape, 'bool')

for i,j in np.ndindex(arr.shape):
    if (0 < i < arr.shape[0]-1) and (0 < j < arr.shape[1]-1):
        if arr[i][j] and arr[i-1][j] and arr[i+1][j] and arr[i][j-1] and arr[i][j+1]:
            intersections[i][j] = True


# Extract paths:

def compress(path):
    # Turn [1,1,1] into [3] etc
    count = 0
    skipOne = False
    for i,j in zip(path,path[1:]+['Z']):
        if skipOne:
            skipOne = False
            continue
        if (i is 'R' and j is 'L') or (i is 'L' and j is 'R'):
            skipOne = True
            continue
        if i is 1:
            count += 1
        else:
            if count:
                yield str(count)
            count = 0
            yield i
    if count:
        yield str(count)


M = lambda p,d: (p[0]+DIRS[d][0],p[1]+DIRS[d][1])
R = lambda d:(d+1)%4
L = lambda d:(d-1)%4
inArray = lambda p,a: 0 <= p[0] < a.shape[0] and 0 <= p[1] < a.shape[1]
DIRS = [(-1,0),(0,1),(1,0),(0,-1)]

allIntersections = list(zip(*np.where(intersections)))

# options = [(L,'L'),(None,None),(R,'R')]
# options = [(L,'L'),(None,None)]
options = [(None,None)]

tot = len(list(itertools.product(*([options] * len(allIntersections)))))

allPaths = []
foo = 0
for choice in itertools.product(*([options] * len(allIntersections))):
    foo += 1
    if foo%1000 == 0:
        print(foo, "/", tot, " | ", len(allPaths))

    interChoices = dict(zip(allIntersections,choice))

    curPos = next(zip(*np.where(scaffolds == '^')))
    curDir = 0
    # curDir = R(curDir)
    # scaffolds[M(curpos, DIRS[curDir])]

    arr = (scaffolds == '#').astype('int8') + intersections.astype('int8')
    path = []
    while np.count_nonzero(arr):
        # print(arr2str(arr))
        if curPos in interChoices:
            turn = interChoices[curPos]
            if turn[0] is not None:
                curDir = turn[0](curDir)
                path += [turn[1]]
        nextPos = M(curPos, curDir)
        if inArray(nextPos, arr) and arr[nextPos]:
            arr[nextPos] -= 1
            curPos = nextPos
            path += [1]
            continue
        else:
            nextPos = M(curPos, L(curDir))
            if inArray(nextPos, arr) and arr[nextPos]:
                curDir = L(curDir)
                path += ['L']
                continue
            else:
                nextPos = M(curPos, R(curDir))
                if inArray(nextPos, arr) and arr[nextPos]:
                    curDir = R(curDir)
                    path += ['R']
                    continue
        break

    if np.count_nonzero(arr) == 0:
        path = list(compress(path))
        # print(path)
        # print(arr2str(arr))
        allPaths += [path]

print("Found ", len(allPaths), "paths")

# Poor man's LZW:
def findProgs(path, progs = [], main = []):
    global bestProgs
    if bestProgs is None:
        bestProgs = [len(path), '', [], []]
    # print(".", end='')
    # print(len(path), ": ", len(main), " | ", [len(p) for p in progs]) #, " - ", progs)
    pathLeft = path
    newMain = []
    while True:
        found = False
        for i,prog in enumerate(progs):
            if pathLeft[:len(prog)] == prog:
                pathLeft = pathLeft[len(prog):]
                found = True
                newMain += [i]
            if len(main) + len(newMain) >= 20:
                return False
        if not found:
            break
    if len(pathLeft) == 0:
        return (progs, main + newMain)
    if len(progs) == 3:
        if len(pathLeft) < bestProgs[0]:
            bestProgs = (len(pathLeft), progs, main + newMain)
            # print(bestProgs)
        return False
    for p in range(1, len(pathLeft) + 1):
        newProg = pathLeft[0:p]
        if len(','.join([str(i) for i in compress(newProg)])) > 20:
            break
        ret = findProgs(pathLeft, progs + [newProg], main + newMain)
        if ret:
            return ret
    return False


def expand(path):
    newPath = []
    for i,j in zip(path,path[1:]+['Z']):
        newPath += [i]
        if i is 1 and j is 1:
            newPath += ['R', 'L']
    return newPath


for path in allPaths:
    bestProgs = None
    prog = findProgs(path)
    if prog:
        break
    if bestProgs[0] < 3:
        print(bestProgs)


if not prog:
    sys.exit("No solution")

assert prog

print("Found a path that can be solved: ", prog)

str = ','.join("ABC"[i] for i in prog[1]) + '\n' + '\n'.join(','.join(compress(p)) for p in prog[0]) + '\nn\n'

print("Program:\n", str)

with open('2019/17/input.txt') as f:
    instructions = [int(i.strip()) for i in f.read().split(',')]

instructions[0] = 2
vm = VM(instructions)
vm.input = [ord(c) for c in str]

while vm.is_running:
    for c in vm.run():
        # print(c)
        print(chr(c), end='')
        lastC = c

print(" Final output: ", lastC)


# INTERACTIVE:

# with open('2019/17/input.txt') as f:
#     instructions = [int(i.strip()) for i in f.read().split(',')]
#
# instructions[0] = 2
# vm = VM(instructions)
#
# while vm.is_running:
#     try:
#         for c in vm.run():
#             print(chr(c), end='')
#         # print(chr(27) + "[2J", flush=False)
#     except NeedInputException:
#         cmd = input(">")
#         # print(cmd)
#         print(list(ord(c) for c in cmd+'\n'))
#         vm.input = [ord(c) for c in cmd+'\n']
