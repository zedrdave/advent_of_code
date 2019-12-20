import sys
import copy
from collections import defaultdict
import numpy as np
import string
import itertools

from ..utils import loadCSVInput, dprint, setVerbosity, inputFile
from ..graphics import snapshot, saveAnimatedGIF

import networkx as nx

arr2str = lambda a: '\n'.join([''.join([str(c) for c in line]) for line in a])
printmap = lambda m: print(arr2str(m))

DIRS = [(0,-1),(0,1),(-1,0),(1,0)]


# wallmap = """         A#########
#          A#########
#   #######.#########
#   #######.........#
#   #######.#######.#
#   #######.#######.#
#   #######.#######.#
#   #####  B    ###.#
# BC...##  C    ###.#
#   ##.##       ###.#
#   ##...DE  F  ###.#
#   #####    G  ###.#
#   #########.#####.#
# DE..#######...###.#
#   #.#########.###.#
# FG..#########.....#
#   ###########.#####
#              Z#####
#              Z#####"""

with open(inputFile()) as f:
# with open('2019/18/input.txt') as f:
    wallmap = f.read()

# for l in wallmap.strip('\n').split('\n'):
#     print(len(l))

wallmap = np.array([[*l] for l in wallmap.strip('\n').split('\n')])
print(wallmap)
printmap(wallmap)


def numpyToGraph(wallmap):
    G = nx.Graph()
    nodes = list(itertools.product(range(1,wallmap.shape[0]-1),range(1,wallmap.shape[1]-1)))
    G.add_nodes_from(nodes)
    for di,dj in DIRS:
        for i,j in nodes:
            if 0 <= i+di < wallmap.shape[0] and 0 <= j+dj < wallmap.shape[1]:
                G.add_edge((i+di,j+dj),(i,j))
    G.remove_nodes_from(tuple(x) for x in np.argwhere(wallmap != '.'))
    return G

G = numpyToGraph(wallmap)

isInMap = lambda i,j,w: 0 <= i < w.shape[0] and 0 <= j < w.shape[1]
isEmpty = lambda i,j,w: isInMap(i,j,w) and w[i,j] == '.'

tunnels = {}
for i,j in np.ndindex(wallmap.shape):
    C1 = wallmap[i,j]
    if C1 in string.ascii_uppercase:
        for di,dj in [(0,1),(1,0)]:
            if isInMap(i+di,j+dj,wallmap):
                C2 = wallmap[i+di, j+dj]
                if C2 in string.ascii_uppercase:
                    if isEmpty(i+2*di,j+2*dj,wallmap):
                        pos = (i+2*di,j+2*dj)
                    else:
                        assert isEmpty(i-di,j-dj,wallmap)
                        pos = (i-di,j-dj)
                    print(C1, C2, pos)
                    if C1+C2 in tunnels:
                        print("Adding tunnel:", tunnels[C1+C2],pos)
                        G.add_edge(tunnels[C1+C2],pos)
                    else:
                        tunnels[C1+C2] = pos

start = tunnels['AA']
goal = tunnels['ZZ']

p = next(nx.shortest_simple_paths(G, start, goal))

print(len(p) - 1)
