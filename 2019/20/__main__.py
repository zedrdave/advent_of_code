import copy
import string
import networkx as nx
import numpy as np

from ..utils import dprint, setVerbosity, inputFile
from ..graphics import snapshot, saveAnimatedGIF

arr2str = lambda a: '\n'.join([''.join([str(c) for c in line]) for line in a])
isInMap = lambda n, w, b = 0: all(0+b <= n[i] < w.shape[i]-b for i in (0,1))
isEmpty = lambda n,w: isInMap(n,w) and w[n[0],n[1]] == '.'
move = lambda n,d, a = 1: (n[0]+ a*d[0], n[1]+ a*d[1], *n[2:])

DIRS = [(0,1),(1,0),(0,-1),(-1,0)]

setVerbosity(0)

with open(inputFile()) as f:
    wallmap = f.read()

wallmap = np.array([[*l] for l in wallmap.strip('\n').split('\n')])
print(arr2str(wallmap))

def exploreWallmap(wallmap, totLevels = 1):
    portals = [{},{}]
    for idx in np.ndindex(wallmap.shape):
        C1 = wallmap[idx]
        if C1 not in string.ascii_uppercase:
            continue
        for d in DIRS[:2]:
            if not isInMap(move(idx, d),wallmap):
                continue
            C2 = wallmap[move(idx, d)]
            if C2 not in string.ascii_uppercase:
                continue
            pos = move(idx, d, -1) if isEmpty(move(idx, d, -1), wallmap) else move(idx, d, 2)
            portals[isInMap(pos, wallmap, b = 4)][C1+C2] = pos

    G = nx.Graph()
    for level in range(totLevels):
        nodes = [(*idx, level) for idx in np.ndindex(wallmap.shape)]
        G.add_nodes_from(nodes)
        G.add_edges_from((n, move(n, d)) for d in DIRS for n in nodes if isInMap(move(n, d), wallmap))
        G.remove_nodes_from((*x, level) for x in np.argwhere(wallmap != '.'))

        for k, inner in portals[1].items():
            if totLevels > 1:
                G.add_edge((*inner, level), (*portals[0][k], level+1))
                G.add_edge((*portals[0][k], level), (*inner, level-1))
            else:
                G.add_edge((*inner, 0), (*portals[0][k], 0))
                # G.add_edge((*portals[0][k], 0), (*inner, 0))

    start = (*portals[0]['AA'], 0)
    goal = (*portals[0]['ZZ'], 0)

    return next(nx.shortest_simple_paths(G, start, goal)), G, portals

# Part 1

p, G, portals = exploreWallmap(wallmap, 1)
dprint(p)
print("Part 1: ", len(p) - 1)

frame = copy.deepcopy(wallmap)

snapshot(frame, printToScreen = False, saveAnimation = True)
saveAnimatedGIF(outputFile = 'animation.gif', backgroundColour = 'white')
# Part 2

# p, G, portals = exploreWallmap(wallmap, 40)
# dprint(p)
# print("Part 2: ", len(p) - 1)
