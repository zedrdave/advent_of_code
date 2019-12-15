import sys
import copy
from collections import defaultdict

from ..intcode.VM import VM, NeedInputException
from ..utils import loadCSVInput, dprint, asciiPrint, setVerbosity, sparseToDense, getChar, cmp

# Debug:
setVerbosity(False)

# Options:
print_to_screen = False
save_animation = True

instructions = loadCSVInput()

vm = VM(instructions)

UNKNOWN = 0
EMPTY = 1
WALL = 2
OXYGEN = 5
ROBOT = 6

DIR_NAMES = "NSWE"
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
explore = [(-1,0),(1,0),(0,1),(0,-1)]

frames = []
def printAndStore(wallmap, update = {}):
    if not print_to_screen and not save_animation:
        return
    printmap = copy.copy(wallmap)
    printmap.update(update)
    if save_animation:
        global frames
        frames += [printmap]
    if print_to_screen:
        asciiPrint(printmap, transpose = True)


while len(explore) > 0:
    next_dest = explore.pop()
    next_path = path_to(cur_pos, next_dest, wallmap)
    dprint(f"Cur pos: {cur_pos}\nNext dest: {next_dest}\nPath: {[DIR_NAMES[d] for d in next_path]}")
    vm.input = next_path
    for dir_idx in next_path:
        vm.input = [dir_idx+1]
        status = next(vm.run())
        next_pos = move(cur_pos, DIRS[dir_idx])
        dprint(f"Moved: {DIR_NAMES[dir_idx]} -> {next_pos}({status})")

        if status == 0:
            wallmap[next_pos] = WALL
        else:
            cur_pos = next_pos

            if wallmap[cur_pos] == UNKNOWN:
                for dir in DIRS:
                    if wallmap[move(cur_pos, dir)] == UNKNOWN:
                        explore += [move(cur_pos, dir)]

            if status == 2:
                wallmap[next_pos] = OXYGEN
                path = path_to((0,0), next_pos, wallmap)
                dprint("Found oxygen at: ", next_pos, " | path: ", path)
                print("Part 1 -", len(path))
            else:
                wallmap[next_pos] = EMPTY

        printAndStore(wallmap, {cur_pos: ROBOT})

# Part 2

time = 0
while time == 0 or len(empty_neighbours) > 0:
    oxy_pos = [p for p,s in wallmap.items() if s == OXYGEN]
    empty_neighbours = [move(p,dir) for p in oxy_pos for dir in DIRS if wallmap[move(p,dir)] == EMPTY]
    for p in empty_neighbours:
        wallmap[p] = OXYGEN
    time += 1
    printAndStore(wallmap)

print("Part 2: took ", time)
# Visualisation: print animation

if len(frames):
    print(f"Saving animation ({len(frames)} frames)…")

    from PIL import Image

    tileSize = 10
    numTiles = 41
    tiles = [Image.open(f'2019/15/tiles/{i}.png').resize((tileSize,)*2) for i in range(7)]

    def frameToImage(frame, i):
        img = Image.new('RGBA', (numTiles*tileSize,)*2, 'black')
        for (x,y),v in frame.items():
            img.paste(tiles[v], ((y + numTiles//2 + 1)*tileSize, (x + numTiles//2 + 1)*tileSize))
        global saved
        print(f"saved: {i}/{len(frames)}", end="\r")
        return img

    images = (frameToImage(f,i) for i,f in enumerate(frames))
    next(images).save(
        'animation.gif',
        save_all=True,
        append_images=images,
        duration=10,
        loop=0,
        optimize=True
    )
