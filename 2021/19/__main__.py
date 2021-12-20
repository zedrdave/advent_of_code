from itertools import product
from collections import deque

import numpy as np
from numpy.linalg import matrix_power

rot90_x = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
rot90_y = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
rot90_z = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

# 24 rotations:
rots = [rot1@rot2
        for rot1 in [matrix_power(rot90_x, i) for i in range(4)]
        for rot2 in [matrix_power(rot90_y, i) for i in range(4)] + [matrix_power(rot90_z, i) for i in [1, 3]]]

# Manhattan distance


def dist(a, b): return sum(abs(aa-bb) for aa, bb in zip(a, b))


def align(s1, s2):
    matches = [(b1, b2) for b1 in s1 for b2 in s2
               if len({dist(b1, b) for b in s1} & {dist(b2, b) for b in s2}) >= 12]

    if len(matches) == 0:
        return False

    scanner_rot = next(rot for rot in rots
                       if len({tuple(b1 - (b2 @ rot)) for b1, b2 in matches}) == 1)
    scanner_pos = matches[0][0] - matches[0][1] @ scanner_rot

    return [tuple((s @ scanner_rot) + scanner_pos) for s in s2], scanner_pos


with open('19/input.txt', 'r') as f:
    data = f.read()

scanners = data.split('\n\n')
scanners = [[list(map(int, l.split(',')))
             for l in s.split('\n')[1:]] for s in scanners]

aligned_scanners = [scanners[0]]
other_scanners = deque(scanners[1:])
scanner_positions = [(0, 0, 0)]

while len(other_scanners):
    s = other_scanners.popleft()
    for ref_s in aligned_scanners:
        res = align(ref_s, s)
        if res:
            aligned_scanners += [res[0]]
            scanner_positions += [res[1]]
            print(len(other_scanners), end='… ')
            break

    if not res:
        other_scanners.append(s)

print('\nPart 1:', len({tuple(b) for s in aligned_scanners for b in s}))
print('Part 2:', max(dist(s1, s2)
      for s1 in scanner_positions for s2 in scanner_positions))
