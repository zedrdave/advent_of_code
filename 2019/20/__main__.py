# import sys
import copy
from collections import defaultdict
import numpy as np
import string
import itertools

# from ..utils import loadCSVInput, dprint, setVerbosity, inputFile
# from ..graphics import snapshot, saveAnimatedGIF

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

# with open(inputFile()) as f:
with open('2019/20/input_test.txt') as f:
    wallmap = f.read()

# for l in wallmap.strip('\n').split('\n'):
#     print(len(l))

wallmap = np.array([[*l] for l in wallmap.strip('\n').split('\n')])
print(wallmap)
printmap(wallmap)


def numpyToGraph(wallmap):
    G = nx.DiGraph()
    nodes = list(itertools.product(range(1,wallmap.shape[0]-1),range(1,wallmap.shape[1]-1)))
    G.add_nodes_from(nodes)
    for di,dj in DIRS:
        for i,j in nodes:
            if 0 <= i+di < wallmap.shape[0] and 0 <= j+dj < wallmap.shape[1]:
                G.add_edge((i+di,j+dj),(i,j), weight = 1)
                G.add_edge((i,j),(i+di,j+dj), weight = 1)
    G.remove_nodes_from(tuple(x) for x in np.argwhere(wallmap != '.'))
    return G

G = numpyToGraph(wallmap)

isInMap = lambda i,j,w: 0 <= i < w.shape[0] and 0 <= j < w.shape[1]
isEmpty = lambda i,j,w: isInMap(i,j,w) and w[i,j] == '.'
isCentral = lambda i,j,w: 4 <= i < w.shape[0]-4 and 4 <= j < w.shape[1]-4

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
                        if isCentral(*pos, wallmap):
                            assert not isCentral(*tunnels[C1+C2], wallmap)
                            G.add_edge(tunnels[C1+C2], pos, weight = 10000)
                            G.add_edge(pos, tunnels[C1+C2], weight = -10000)
                        else:
                            assert isCentral(*tunnels[C1+C2], wallmap)
                            G.add_edge(tunnels[C1+C2], pos, weight = -10000)
                            G.add_edge(pos, tunnels[C1+C2], weight = 10000)
                    else:
                        tunnels[C1+C2] = pos

start = tunnels['AA']
goal = tunnels['ZZ']

p = next(nx.shortest_simple_paths(G, start, goal, weight = 'weight'))
print(p)
print(len(p) - 1)


# x > 678
