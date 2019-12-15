import sys
import copy
from collections import defaultdict

from ..intcode.VM import VM, NeedInputException
from ..utils import loadCSVInput, dprint, setVerbosity
from ..graphics import snapshot, saveAnimatedGIF

# Debug:
setVerbosity(False)

# Options:
printToScreen = True
saveAnimation = True

instructions = loadCSVInput()

vm = VM(instructions)

UNKNOWN = 0
EMPTY = 1
WALL = 2
EXPLORE = 3
OXYGEN = 5
ROBOT = 6

DIRS = [(0,-1),(0,1),(-1,0),(1,0)]
move = lambda pos, dir: (pos[0]+dir[0], pos[1]+dir[1])

def path_to(orig, dest, prevPos = None):
    path = None
    for dirIdx,dir in enumerate(DIRS):
        neighbour = move(orig, dir)
        if neighbour == prevPos:
            continue
        if dest == neighbour:
            return [dirIdx]
        if wallmap[neighbour] == EMPTY or wallmap[neighbour] == OXYGEN:
            newPath = path_to(neighbour, dest, prevPos = orig)
            if newPath is not None and (path is None or len(newPath) < len(path)):
                path = [dirIdx] + newPath
    return path

# Part 1

curPos = (0,0)
wallmap = defaultdict(int)
wallmap[curPos] = EMPTY
explore = [(1,0)]


while len(explore) > 0:
    nextDest = explore.pop()
    nextPath = path_to(curPos, nextDest)
    dprint(f"Cur pos: {curPos}\nNext dest: {nextDest}\nPath: {['NSWE'[d] for d in nextPath]}")
    assert wallmap[nextDest] == UNKNOWN
    for dirIdx in nextPath:
        vm.input = [dirIdx+1]
        status = next(vm.run())
        nextPos = move(curPos, DIRS[dirIdx])
        dprint(f"Moved: {'NSWE'[dirIdx]} -> {nextPos}({status})")

        explore = [p for p in explore if p != nextPos]

        if status == 0:
            wallmap[nextPos] = WALL
        else:
            curPos = nextPos
            if wallmap[curPos] == UNKNOWN:
                explore += [p for p in [move(curPos, dir) for dir in DIRS] if wallmap[p] == UNKNOWN]
            if status == 2:
                wallmap[curPos] = OXYGEN
                path = path_to((0,0), curPos)
                dprint("Found oxygen at: ", curPos, " | path: ", path)
                print("Part 1 -", len(path))
            else:
                wallmap[curPos] = EMPTY

        snapshot(wallmap, printToScreen, saveAnimation, {curPos: ROBOT, **{p:EXPLORE for p in explore}})

# Part 2

time = 0
while time == 0 or len(emptyNeighbours) > 0:
    oxy_pos = [p for p,s in wallmap.items() if s == OXYGEN]
    emptyNeighbours = [move(p,dir) for p in oxy_pos for dir in DIRS if wallmap[move(p,dir)] == EMPTY]
    for p in emptyNeighbours:
        wallmap[p] = OXYGEN
    time += 1
    snapshot(wallmap, printToScreen, saveAnimation)

print("Part 2: took ", time)

if saveAnimation:
    saveAnimatedGIF(freq=2, duration=5)
