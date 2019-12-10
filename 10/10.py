import numpy as np
import copy
from math import gcd

with open('input.txt', 'r') as fp:
    data = (np.array([list(line.strip()) for line in fp]) == '#').astype('int')

results = copy.deepcopy(data)

def dist(p1,p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

for x in range(data.shape[0]):
    for y in range(data.shape[1]):
        if not data[x][y]: continue
        # print("ORIGIN: ", y, x)
        map = copy.deepcopy(data)
        map[x][y] = 0
        for d in range(1, sum(data.shape)):
            # iterate array:
            # print("Dist: ", d)
            for x2 in range(map.shape[0]):
                for y2 in range(map.shape[1]):
                    if map[x2][y2] and dist((x,y),(x2,y2)) == d:
                        # print(y2, x2, ' d:', dist((x,y),(x2,y2)))
                        dx2, dy2 = (x2-x, y2-y)
                        dx2, dy2 = (dx2//gcd(dx2,dy2),dy2//gcd(dx2,dy2))
                        # print("dx,dy", dy2, dx2)
                        r = 1
                        while 0 <= x2+r*dx2 < map.shape[0] and 0 <= y2+r*dy2 < map.shape[1]:
                            if map[x2+r*dx2][y2+r*dy2]:
                                # print("erasing: ", y2, x2)
                                map[x2+r*dx2][y2+r*dy2] = 0
                                # print(map)
                            r += 1
        results[x][y] = sum(sum(map))
        # print(map)

print(results)

print(np.unravel_index(results.argmax(), results.shape))
print(results.max())

# < 330
