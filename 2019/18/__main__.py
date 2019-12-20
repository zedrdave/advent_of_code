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
dprint(allBetweenKeys)

explored = {}
bestPathLen = None

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

# keyPaths = ['@@@@', '@s@@', '@d@@', '@de@', '@dn@', '@dnu', '@dno', '@dnx', 'qdnx', 'bdnx', 'fdnx', 'fdnm', 'fdni', 'fdnw', 'ftnw', 'fynw', 'fync', 'fyzc', 'fyzk', 'fyrk', 'fygk', 'fyak', 'fyjk', 'fyhk', 'fylk', 'fypk', 'fyvk']

print(keyPaths)

# Visualisation

EMPTY = '1'
WALL = '0'
DRONE = '6'
OPEN_DOOR = '9'
CLOSED_DOOR = '2'
KEY = '7'

frame = copy.deepcopy(wallmap)
frame[frame == '#'] = WALL
frame[frame == '.'] = EMPTY
frame[frame == '@'] = DRONE
for c in string.ascii_lowercase:
    frame[frame == c] = KEY
for c in string.ascii_uppercase:
    frame[frame == c] = CLOSED_DOOR

snapshot(frame, printToScreen = True, saveAnimation = True, transpose = False)

G = numpyToGraph(wallmap)
initPos = [tuple(ctr+adj) for adj in [(-1,-1),(1,-1),(-1,1),(1,1)]]

paths = []
for i in range(4):
    stops = [initPos[i] if k[i] == '@' else where(k[i], wallmap) for k in keyPaths]
    paths += [[p for f,t in zip(stops[:-1],stops[1:]) for p in next(nx.shortest_simple_paths(G, f, t))]]

# print(len(paths))
# print([len(p) for p in paths])

lastPos = [None] * 4
while any(len(p) for p in paths):
    updates = {}
    for i in range(4):
        if not len(paths[i]):
            continue
        c = wallmap[paths[i][0]]
        if c in string.ascii_lowercase:
            updates[where(c.upper(), wallmap)] = OPEN_DOOR
        if frame[paths[i][0]] == CLOSED_DOOR:
            continue
        p = paths[i].pop(0)
        if lastPos[i]:
            updates[lastPos[i]] = EMPTY
        updates[p] = DRONE
        lastPos[i] = p
    for p,v in updates.items():
        frame[p] = v
    snapshot(frame, printToScreen = False, saveAnimation = True, transpose = False)

for _ in range(10):
    snapshot(frame, printToScreen = False, saveAnimation = True, transpose = False)
saveAnimatedGIF(backgroundColour=(217,217,217), duration = 70)
