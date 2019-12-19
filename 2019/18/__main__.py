import sys
import copy
from collections import defaultdict
import numpy as np
import string
import itertools

from ..utils import loadCSVInput, dprint, setVerbosity, inputFile
# from ..graphics import snapshot, saveAnimatedGIF

import networkx as nx

# Debug:
# setVerbosity(False)

with open(inputFile()) as f:
    wallmap = f.read()

arr2str = lambda a: '\n'.join([''.join([str(c) for c in line]) for line in a])
printmap = lambda m: print(arr2str(m))

DIRS = [(0,-1),(0,1),(-1,0),(1,0)]

# wallmap = """########################
# #...............b.C.D.f#
# #.######################
# #.....@.a.B.c.d.A.e.F.g#
# ########################"""

# wallmap = """#################
# #i.G..c...e..H.p#
# ########.########
# #j.A..b...f..D.o#
# ########@########
# #k.E..a...g..B.n#
# ########.########
# #l.F..d...h..C.m#
# #################"""


# wallmap = """########################
# #@..............ac.GI.b#
# ###d#e#f################
# ###A#B#C################
# ###g#h#i################
# ########################"""

# wallmap = """#############
# #g#f.D#..h#l#
# #F###e#E###.#
# #dCba@#@BcIJ#
# #############
# #nK.L@#@G...#
# #M###N#H###.#
# #o#m..#i#jk.#
# #############"""

wallmap = np.array([[*l] for l in wallmap.split()])
printmap(wallmap)

# Part 1:
# wallmaps = [wallmap]

# Part 2:
ctr = np.array(wallmap.shape)//2

replaceMap = """@#@
###
@#@"""

wallmap[(ctr[0]-1):(ctr[0]+2),(ctr[1]-1):(ctr[1]+2)] = np.array([[*l] for l in replaceMap.split()])

wallmaps = [wallmap[:(ctr[0]+1),:(ctr[1]+1)], wallmap[ctr[0]:,:(ctr[1]+1)], wallmap[:(ctr[0]+1),ctr[1]:], wallmap[ctr[0]:,ctr[1]:]]

for w in wallmaps:
    print("\n")
    printmap(w)
    print("\n")
# End part 2


def numpyToGraph(wallmap):
    G = nx.Graph()
    nodes = list(itertools.product(range(1,wallmap.shape[0]-1),range(1,wallmap.shape[1]-1)))
    G.add_nodes_from(nodes)
    for di,dj in DIRS:
        G.add_edges_from(zip(((i+di,j+dj) for i,j in nodes), nodes))
    G.remove_nodes_from(tuple(x) for x in np.argwhere(wallmap == '#'))
    return G

allGs = [numpyToGraph(w) for w in wallmaps]

print("Created graphs:", [len(G.nodes) for G in allGs])

where = lambda c,w: tuple(np.argwhere(w == c)[0])

allKeysFor = lambda wallmap: set(c for c in string.ascii_lowercase if len(np.argwhere(wallmap == c)))

def pathsFor(G, allKeys, wallmap):
    allKeysInMap = allKeysFor(wallmap)
    allDoors = set(c.upper() for keys in allKeys for c in keys)
    # print("Doors: ", allDoors)

    betweenKeys = {}
    for k1,k2 in itertools.product(['@'] + list(allKeysInMap),list(allKeysInMap)):
        if (k1,k2) not in betweenKeys:
            paths = list(nx.shortest_simple_paths(G, where(k1,wallmap), where(k2,wallmap)))
            betweenKeys[(k1,k2)] = []
            for p in paths:
                found = set(wallmap[x] for x in p if wallmap[x] != '.')
                # print(k1, k2, found, set(c.lower() for c in found & allDoors))
                betweenKeys[(k1,k2)] += [(len(p)-1, set(c.lower() for c in found & allDoors))]
            betweenKeys[(k2,k1)] = betweenKeys[(k1,k2)]
    return betweenKeys

allKeys = [allKeysFor(w) for w in wallmaps]
allBetweenKeys = [pathsFor(G, allKeys, wallmap) for G,wallmap in zip(allGs, wallmaps)]

print("Got all paths…")
print(allBetweenKeys)

bestPathLen = None
explored = {}

def recurExplore(allKeys, allBetweenKeys, pathLen = 0, curPos = '@'*len(allKeys), keys = frozenset()):
    global bestPathLen, explored
    # print(curPos)
    if bestPathLen is not None and pathLen >= bestPathLen:
        return
    if (curPos, keys) in explored and explored[(curPos, keys)] <= pathLen:
        return
    explored[(curPos, keys)] = pathLen
    if len(keys) == sum(len(a) for a in allKeys):
        bestPathLen = pathLen
        print("Got best length so far:", pathLen)
        return
    # print("Got keys: ", keys)
    for i,allKeysForSubgraph in enumerate(allKeys):
        for k in allKeysForSubgraph - keys:
            for pathLenBetween, doorsBetween in allBetweenKeys[i][ (curPos[i],k) ]:
                # print(f"submap: {i}, curPos: {curPos[i]}, target: {k}, path len: {pathLenBetween}, doors: {doorsBetween}")
                if doorsBetween - keys:
                    continue
                recurExplore(allKeys, allBetweenKeys,
                    pathLen = pathLen + pathLenBetween,
                    curPos = curPos[:i] + k + curPos[i+1:],
                    keys = keys | set(k)
                )

recurExplore(allKeys, allBetweenKeys)
