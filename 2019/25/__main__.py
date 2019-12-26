# import copy
import numpy as np
import math
import networkx as nx
import sys
import itertools
import copy

from ..utils import loadCSVInput, dprint, setVerbosity
from ..intcode.VM import VM, NeedInputException


instructions = loadCSVInput()

OPP_DIRS = {'east':'west', 'south':'north', 'west':'east', 'north':'south'}

def processOutput(g, curPos, output):
    cmds = []

    badItems = ['molten lava', 'escape pod', 'giant electromagnet', 'photons', 'infinite loop']

    lines = output.split('\n')
    room = next(l.strip('=').strip() for l in lines if l.startswith('== '))

    print("\n***", curPos, 'aka:', room)
    nx.relabel_nodes(g, {curPos: room}, copy = False)
    curPos = room

    if room != 'Security Checkpoint':
        doorIdx =  lines.index('Doors here lead:')
        doorEndIdx = lines.index('', doorIdx)
        doorDirs = [l[2:] for l in lines[doorIdx:doorEndIdx] if l[0:1] == '-']

        print("Has dirs:", doorDirs)

        knownDirs = [d['dir'] for s,t,d in g.edges(curPos, data=True) if 'dir' in d]
        for dir in doorDirs:
            if dir in knownDirs: continue

            name = dir + ' of ' + curPos
            g.add_node(name, explored = False)
            g.add_edge(curPos, name, dir = dir)
            g.add_edge(name, curPos, dir = OPP_DIRS[dir])

    if 'Items here:' in lines:
        itemIdx =  lines.index('Items here:')
        itemEndIdx = lines.index('', itemIdx)
        items = [l[2:] for l in lines[itemIdx:itemEndIdx] if l[0:1] == '-']
        print("Has items:", items)
        cmds += ['take ' + item for item in items if item not in badItems]

    # Go to nearest unexplored spot
    paths = sorted([(t,p) for t,p in nx.single_source_shortest_path(g, curPos).items() if not g.nodes[t]['explored']], key = lambda x:len(x[1]))

    if len(paths) == 0:
        if curPos == 'Security Checkpoint':
            return g, curPos, ['inv', False]
        else:
            print("Explored everywhere: going to security checkpoint…")
            path = nx.shortest_path(g, curPos, 'Security Checkpoint')
    else:
        path = paths[0][1]

    for (u,v) in zip(path[0:],path[1:]):
        cmds += [g[u][v]['dir']]
        curPos = v
    g.nodes[curPos]['explored'] = True
    return g, curPos, cmds

# Step 1: explore ship and gather items

curPos = 'Start'
g = nx.DiGraph()
g.add_node(curPos, explored = True)
cmds = []
vm = VM(instructions)

while vm.is_running:
    try:
        output = ''
        for c in vm.run():
            output += chr(c)
            print(chr(c), end='')
    except NeedInputException:
        if len(cmds) == 0:
            g, curPos, cmds = processOutput(g, curPos, output)
            print(cmds)
        if not cmds[0]:
            break
        vm.input = [ord(c) for c in cmds.pop(0) + '\n']

# Step 2: go through checkpoint

print("Trying to pass checkpoint using items:")
items = [l[2:] for l in output.split('\n') if l[0:1] == '-']
print(items)

for r in range(0, len(items)):
    for keep in itertools.combinations(items, r):
        print("#r:", r, keep)
        drop = set(items) - set(keep)
        cmds = []
        for item in drop:
            cmds += ['drop ' + item]
        cmds += ['east']
        for item in drop:
            cmds += ['take ' + item]

        vm.input = [ord(c) for cmd in cmds for c in cmd + '\n']
        while vm.is_running:
            try:
                output = ''
                for c in vm.run():
                    output += chr(c)
            except NeedInputException:
                # if 'A loud, robotic voice says "Alert! Droids on this ship are lighter than the detected value!" and you are ejected back to the checkpoint.' in output.split('\n'):
                #     print("< ", set(keep))
                # elif 'A loud, robotic voice says "Alert! Droids on this ship are heavier than the detected value!" and you are ejected back to the checkpoint.' in output.split('\n'):
                #     print("> ", set(keep))
                break
print(output)

nx.draw(g, with_labels = True)
# plt.savefig("filename.png")
