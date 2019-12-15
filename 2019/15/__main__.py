import sys
import copy
from collections import defaultdict

from ..intcode.VM import VM, NeedInputException
from ..utils import loadCSVInput, dprint, setVerbosity
from ..graphics import snapshot, saveAnimatedGIF

# Debug:
setVerbosity(False)

# Options:
printToScreen = False
saveAnimation = True

instructions = loadCSVInput()

vm = VM(instructions)

UNKNOWN = 0
EMPTY = 1
WALL = 2
OXYGEN = 5
ROBOT = 6

DIRS = [(0,-1),(0,1),(-1,0),(1,0)]
move = lambda pos, dir: (pos[0]+dir[0], pos[1]+dir[1])

def path_to(orig, dest, wallmap, prev_pos = None):
    for dir_idx,dir in enumerate(DIRS):
        neighbour = move(orig, dir)
        if neighbour == prev_pos:
            continue
        if neighbour == dest:
            return [dir_idx]
        if wallmap[neighbour] == EMPTY:
            add_path = path_to(neighbour, dest, wallmap, prev_pos = orig)
            if len(add_path):
                return [dir_idx] + add_path
    return []

cur_pos = (0,0)
wallmap = defaultdict(int)
wallmap[cur_pos] = EMPTY
explore = [(1,0)]

while len(explore) > 0:
    next_dest = explore.pop()
    next_path = path_to(cur_pos, next_dest, wallmap)
    dprint(f"Cur pos: {cur_pos}\nNext dest: {next_dest}\nPath: {['NSWE'[d] for d in next_path]}")
    for dir_idx in next_path:
        vm.input = [dir_idx+1]
        status = next(vm.run())
        next_pos = move(cur_pos, DIRS[dir_idx])
        dprint(f"Moved: {'NSWE'[dir_idx]} -> {next_pos}({status})")

        if status == 0:
            wallmap[next_pos] = WALL
        else:
            cur_pos = next_pos

            if wallmap[cur_pos] == UNKNOWN:
                explore += [p for p in [move(cur_pos, dir) for dir in DIRS] if wallmap[p] == UNKNOWN]
            if status == 2:
                wallmap[cur_pos] = OXYGEN
                path = path_to((0,0), cur_pos, wallmap)
                dprint("Found oxygen at: ", cur_pos, " | path: ", path)
                print("Part 1 -", len(path))
            else:
                wallmap[cur_pos] = EMPTY

        snapshot(wallmap, printToScreen, saveAnimation, {cur_pos: ROBOT})

# Part 2

time = 0
while time == 0 or len(empty_neighbours) > 0:
    oxy_pos = [p for p,s in wallmap.items() if s == OXYGEN]
    empty_neighbours = [move(p,dir) for p in oxy_pos for dir in DIRS if wallmap[move(p,dir)] == EMPTY]
    for p in empty_neighbours:
        wallmap[p] = OXYGEN
    time += 1
    snapshot(wallmap, printToScreen, saveAnimation)

print("Part 2: took ", time)

if saveAnimation:
    saveAnimatedGIF(freq=10)
