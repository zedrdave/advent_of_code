
from aocd import get_data, submit
import numpy as np
import sys
import itertools
from collections import defaultdict, Counter
import re
from tqdm.auto import tqdm

day = 22
year = 2022

data = get_data(day=day, year=year)

grid, insts = data.split("\n\n")

insts = re.split(r"([A-Z])", insts)
grid = {(i, j): v for j, l in enumerate(grid.split('\n')) for i, v in enumerate(l) if v != ' '}


rotations = np.array((
    ((1, 0, 0),
     (0, 0, -1),
        (0, 1, 0)),

    ((0, 0, 1),
        (0, 1, 0),
        (-1, 0, 0)),

    ((0, -1, 0),
        (1, 0, 0),
        (0, 0, 1))
))

faces = {(ii, jj) for ii in range(4) for jj in range(4) if (ii * face_dim, jj * face_dim) in grid}

dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))

move3d = lambda u, dir: (next(r.T if o == 1 else r
                              for o, r in zip(dir, rotations)
                              if o != 0) @ u.T).T


def rotate_match(axes, target):
    if (axes == target).all():
        return 0
    for i in range(1, 4):
        axes = move3d(axes, axes[0])
        if (axes == target).all():
            return i
    return False


def search_face(faces, cur_face, axes, target_axes, prev_face=None):
    r = rotate_match(axes, target_axes)
    if r is not False:
        return r, cur_face
    directions = (axes[1] - axes[0], axes[2] - axes[0], axes[0] - axes[1], axes[0] - axes[2])
    for i, dir in enumerate(dirs):
        next_face = tuple(a + b for a, b in zip(cur_face, dir))
        # print(next_face)
        if (next_face == prev_face) or (next_face not in faces):
            continue
        r, face = search_face(faces, next_face, move3d(axes, directions[i]), target_axes, cur_face)
        if r is not False:
            return r, face
    return False, False


def neighbour(faces, face_from, dir):
    axes = np.array(((0, 0, 1), (1, 0, 1), (0, 1, 1)))
    directions = (axes[1] - axes[0], axes[2] - axes[0], axes[0] - axes[1], axes[0] - axes[2])
    target = move3d(axes, directions[dir])
    return search_face(faces, face_from, axes, target)


print(neighbour(faces, face_from=(2, 0), dir=0))
print(neighbour(faces, face_from=(0, 1), dir=2))

# (2, (1, 2))
# (1, (0, 3))


tiles = {'.': '⬜️', '#': '🟥', ' ': '⬛️'}


def print_grid(grid, curpos=None, curdir=4, bounds_i=None, bounds_j=None):
    if bounds_i is None:
        bounds_i = 0, max(i for i, _ in grid) + 1
    if bounds_j is None:
        bounds_j = 0, max(j for _, j in grid) + 1

    for j in range(*bounds_j):
        for i in range(*bounds_i):
            if curpos is not None and curpos == (i, j):
                if grid.get(curpos, False) != '.':
                    print("?", end="")
                    continue
                    # print("ERROR: curpos not empty:", curpos, grid.get(curpos, False))
                    # print_grid(grid)
                # assert grid.get(curpos) == '.', (curpos, grid.get(curpos), grid)
                print(["⏩", "🔽", "⏪", "🔼", "🤓"][curdir], end="")
                # print("🤓", end="")
            else:
                print(tiles[grid.get((i, j), ' ')], end="")
        print("")
    print("")


rot_ij_90 = lambda i, j: (face_dim - 1 - j, i)
rot_ij = lambda i, j, r: rot_ij(*rot_ij_90(i, j), r - 1) if r > 0 else (i, j)


move = lambda p, d: ((p[0] + d[0]), (p[1] + d[1]))

curdir = 0
curpos = min(p for p in grid if p[1] == 0)

# print_grid(grid , curpos, curdir)

for i, inst in enumerate(insts):
    if inst in 'RL':
        curdir = (curdir + (1 if inst == "R" else -1)) % 4
    else:
        inst = int(inst)

        for _ in range(inst):
            nextpos = move(curpos, dirs[curdir])
            if nextpos not in grid:
                p = (curpos[0] // face_dim, curpos[1] // face_dim)
                r, face = neighbour(faces, p, curdir)
                nextpos = rot_ij(nextpos[0] % face_dim, nextpos[1] % face_dim, 4 - r)
                nextpos = (face[0] * face_dim + nextpos[0], face[1] * face_dim + nextpos[1])
                if grid[nextpos] != '#':
                    curdir = (curdir - r) % 4
            if grid[nextpos] == '#':
                break
            curpos = nextpos

print('Part 2:', 1000 * (curpos[1] + 1) + 4 * (curpos[0] + 1) + curdir)
