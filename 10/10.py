import numpy as np
import copy
from math import gcd, atan2, pi


with open('input.txt', 'r') as fp:
    data = np.array([list(line.strip()) for line in fp]) == '#'

# swap from (y,x) to (x,y):
data = np.swapaxes(data, 0, 1)

results = np.zeros(data.shape)

for ast_x in range(data.shape[0]):
    for ast_y in range(data.shape[1]):
        if not data[ast_x][ast_y]: continue

        all_dirs = set()
        for (x,y),a in np.ndenumerate(data):
            if not a: continue
            dx, dy = ast_x-x, ast_y-y
            if dx == 0 and dy == 0: continue
            dx,dy = dx//gcd(dx,dy),dy//gcd(dx,dy)
            all_dirs.update(((dx,dy),))

        results[ast_x][ast_y] = len(all_dirs)

best_pos = np.unravel_index(results.argmax(), results.shape)
print(f"Part 1: {results.max()} at pos: {best_pos}")

def angle(vector1, vector2):
    x1, y1 = vector1
    x2, y2 = vector2
    dot = x1*x2 + y1*y2
    det = x1*y2 - y1*x2
    angle = atan2(det, dot)
    return (2*pi + angle) if angle < 0 else angle

dist = lambda p1,p2: abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

ast_x, ast_y = best_pos

map = copy.deepcopy(data)

# print(ast_x, ast_y)
# map[ast_x][ast_y] = 8
# print(map.transpose())
counter = 1

while(True):
    # iterate:
    targets = set()
    all_dirs = set()
    for (x,y),a in sorted(np.ndenumerate(map), key=lambda x:dist(x[0],(ast_x,ast_y))):
        if not a: continue
        dx, dy = x-ast_x, y-ast_y
        if dx == 0 and dy == 0: continue
        # print("\n", x, y, a)
        # print("d: ", dx, dy)
        gdx,gdy = dx//gcd(dx,dy),dy//gcd(dx,dy)
        # print("d(gcd): ", gdx, gdy)
        if (gdx,gdy) in all_dirs:
            # print("skipping: ", (dx,dy))
            continue
        targets.update(((dx,dy),))
        all_dirs.update(((gdx,gdy),))

    if(len(targets) == 0):
        break

    targets = sorted(targets, key=lambda x: angle((0,-1),x))
    for i,dir in enumerate(targets):
        # print(f"#{counter+i} {ast_x+dir[0]},{ast_y+dir[1]}")
        if counter+i == 200:
            print(f"Part 2: #{counter+i} {ast_x+dir[0]},{ast_y+dir[1]} -> {100*(ast_x+dir[0]) + ast_y+dir[1]}")
        map[ast_x+dir[0]][ast_y+dir[1]] = 0
    counter += len(targets)
