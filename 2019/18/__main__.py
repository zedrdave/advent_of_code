import sys
import copy
from collections import defaultdict
import numpy as np
import string
import itertools

from ..utils import loadCSVInput, dprint, setVerbosity, inputFile
from ..graphics import snapshot, saveAnimatedGIF

import networkx as nx

# Debug:
setVerbosity(False)

with open(inputFile()) as f:
# with open('2019/18/input.txt') as f:
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
replaceMap = "@#@\n###\n@#@"

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

explored = {}
# bestPathLen = None
bestPathLen = 1733 # DEBUG CHEAT

def recurExplore(allKeys, allBetweenKeys, pathLen = 0, curPos = '@'*len(allKeys), keys = frozenset()):
    global explored, bestPathLen
    # print(curPos)
    if bestPathLen is not None and pathLen >= bestPathLen:
        return False
    if (curPos, keys) in explored and explored[(curPos, keys)] <= pathLen:
        return False
    explored[(curPos, keys)] = pathLen
    if len(keys) == sum(len(a) for a in allKeys):
        bestPathLen = pathLen
        print("Got best length so far:", pathLen)
        return [curPos]
    # print("Got keys: ", keys)
    bestPath = False
    for i,allKeysForSubgraph in enumerate(allKeys):
        for k in allKeysForSubgraph - keys:
            for pathLenBetween, doorsBetween in allBetweenKeys[i][ (curPos[i],k) ]:
                # print(f"submap: {i}, curPos: {curPos[i]}, target: {k}, path len: {pathLenBetween}, doors: {doorsBetween}")
                if doorsBetween - keys:
                    continue
                ret = recurExplore(allKeys, allBetweenKeys,
                    pathLen = pathLen + pathLenBetween,
                    curPos = curPos[:i] + k + curPos[i+1:],
                    keys = keys | set(k),
                )
                if ret:
                    # print(ret)
                    bestPath = [curPos] + ret
    return bestPath


keyPaths = recurExplore(allKeys, allBetweenKeys)

print(keyPaths)

# Visualisation

from itertools import zip_longest

EMPTY = 1
DRONE = 6
OPEN_DOOR = 9

frame = copy.deepcopy(wallmap)
frame[frame == '#'] = 2
frame[frame == '.'] = EMPTY
frame[frame == '@'] = DRONE
for c in string.ascii_lowercase:
    frame[frame == c] = 7
for c in string.ascii_uppercase:
    frame[frame == c] = 8

G = numpyToGraph(wallmap)

curPos = None
initPos = [tuple(ctr+adj) for adj in [(-1,-1),(1,-1),(-1,1),(1,1)]]

for step in keyPaths:
    print(step)
    stepPos = [initPos[i] if c == '@' else where(c, wallmap) for i,c in enumerate(step)]
    print(stepPos)
    if curPos:
        print(curPos, stepPos)
        paths = [next(nx.shortest_simple_paths(G, f, t)) for f,t in zip(curPos,stepPos)]
        print(paths)
        for nextPos in zip_longest(*paths, fillvalue=None):
            for p in curPos:
                frame[p] = EMPTY
            curPos = [n if n else p for p,n in zip(curPos,nextPos)]
            print(curPos)
            for p in curPos:
                if wallmap[p] in string.ascii_lowercase:
                    print("Opening: ", wallmap[p].upper())
                    frame[where(wallmap[p].upper(), wallmap)] = OPEN_DOOR
                frame[p] = DRONE
            snapshot(frame, printToScreen = True, saveAnimation = True, transpose = False)
        # print(paths)
        break
    else:
        curPos = stepPos

saveAnimatedGIF(backgroundColour='black', skipTile=1)
