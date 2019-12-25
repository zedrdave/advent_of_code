# import copy
import numpy as np
import math
import networkx as nx
import sys
import itertools
import copy

from ..utils import loadCSVInput, dprint, setVerbosity, inputFile, sparseToDense
from ..intcode.VM import VM, NeedInputException


# with open('25/input.txt') as f:
#     instructions = [int(i.strip()) for i in f.read().split(',')]
instructions = loadCSVInput()

# arr2str = lambda a: '\n'.join([''.join([str(c) for c in line]) for line in a])

# , input = [ord(c) for c in moves]

# DIRS = {'east':(0,1), 'south':(1,0), 'west':(0,-1), 'north':(-1,0)}
OPP_DIRS = {'east':'west', 'south':'north', 'west':'east', 'north':'south'}
# move = lambda n,d, a = 1: (n[0]+ a*d[0], n[1]+ a*d[1], *n[2:])

def processOutput(g, curPos, output):
    cmds = []

    badItems = ['molten lava', 'escape pod', 'giant electromagnet', 'photons', 'infinite loop']
    # print(">>>>\n", output, "\n<<<<")
    lines = output.split('\n')
    try:
        room = next(l.strip('=').strip() for l in lines if l.startswith('== '))
    except:
        # print(output)
        raise

    print("\n***", curPos, 'aka:', room)

    nx.relabel_nodes(g, {curPos: room}, copy = False)
    assert room in g.nodes

    curPos = room

    if room != 'Security Checkpoint':
        if 'Doors here lead:' in lines:
            doorIdx =  lines.index('Doors here lead:')
            doorEndIdx = lines.index('', doorIdx)
            doorDirs = [l[2:] for l in lines[doorIdx:doorEndIdx] if l[0:1] == '-']
        else:
            print("No doors!\n")
            print(output)
            assert False

        print("Has dirs:", doorDirs)

        knownDirs = [d['dir'] for s,t,d in g.edges(curPos, data=True) if 'dir' in d]
        for dir in doorDirs:
            if dir in knownDirs: continue
            # if move(curPos, DIRS[dir]) not in g.edges:
            name = dir + ' of ' + curPos
            g.add_node(name, explored = False)
            g.add_edge(curPos, name, dir = dir)
            g.add_edge(name, curPos, dir = OPP_DIRS[dir])

    if 'Items here:' in lines:
        itemIdx =  lines.index('Items here:')
        itemEndIdx = lines.index('', itemIdx)
        items = [l[2:] for l in lines[itemIdx:itemEndIdx] if l[0:1] == '-']
    else:
        items = []
    for item in items:
        if item not in badItems:
            cmds += ['take ' + item]
    print("Has items:", items)
    # print(f"curPos: {curPos} [{g.nodes[curPos]['explored']}]")
    paths = sorted([(t,p) for t,p in nx.single_source_shortest_path(g, curPos).items() if not g.nodes[t]['explored']], key = lambda x:len(x[1]))
    # print([(t,p,len(p)) for t,p in nx.single_source_shortest_path(g, curPos).items() if not g.nodes[t]['explored']])
    if len(paths) == 0:
        if curPos == 'Security Checkpoint':
            return g, curPos, ['inv', False]
        else:
            print("Explored everywhere: going to security checkpoint…")
            path = nx.shortest_path(g, curPos, 'Security Checkpoint')
            print(path)
            # path += [mode(p[-1], DIRS['east'])]
    else:
        path = paths[0][1]
    # print("picked path: ", path)
    for (u,v) in zip(path[0:],path[1:]):
        cmds += [g[u][v]['dir']]
        curPos = v
    g.nodes[curPos]['explored'] = True
    return g, curPos, cmds



curPos = 'Start'
g = nx.DiGraph()
g.add_node(curPos, explored = True)
cmds = []
vm = VM(instructions)
comb = None
# vm.input = [ord(c) for c in springProg.strip() + "\nRUN\n"]
while vm.is_running:
    try:
        output = ''
        for c in vm.run():
            try:
                output += chr(c)
                print(chr(c), end='')
            except:
                print("raw: ", c)
                break
    except NeedInputException:
        if len(cmds) == 0:
            g, curPos, cmds = processOutput(g, curPos, output)
            # print(f"-> {curPos} [{g.nodes[curPos]['explored']}] ({cmds})")
        # print(list(ord(c) for c in cmd+'\n'))
            print(g.nodes)
            print(cmds)

        if not cmds[0]:
            break
        vm.input = [ord(c) for c in cmds.pop(0) + '\n']

items = [l[2:] for l in output.split('\n') if l[0:1] == '-']

print("Trying to pass checkpoint")
print(items)

for r in range(0, len(items)):
    for keep in itertools.combinations(items, r):
        print("#r:", r)
        drop = set(items) - set(keep)
        cmds = []
        for item in drop:
            cmds += ['drop ' + item]
        cmds += ['east']
        for item in drop:
            cmds += ['take ' + item]
        # print (cmds)
        # temp_vm = copy.deepcopy(vm)
        vm.input = [ord(c) for cmd in cmds for c in cmd + '\n']
        while vm.is_running:
            try:
                output = ''
                for c in vm.run():
                    output += chr(c)
                    # print(chr(c), end='')
            except NeedInputException:
                if 'A loud, robotic voice says "Alert! Droids on this ship are lighter than the detected value!" and you are ejected back to the checkpoint.' in output.split('\n'):
                    print("< ", set(keep))
                elif 'A loud, robotic voice says "Alert! Droids on this ship are heavier than the detected value!" and you are ejected back to the checkpoint.' in output.split('\n'):
                    print("> ", set(keep))
                break
print(output)
