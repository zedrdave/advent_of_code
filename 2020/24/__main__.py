from ..utils import *

data = open(input_file())

D = {'w': (-1,0), 'nw': (0,-1), 'ne': (1,-1), 'e': (1,0), 'se': (0,1), 'sw': (-1,1)}

move = lambda x,y,dx,dy: (x+dx,y+dy)

BT = set()

for l in data:
    pos = (0,0)
    while len(l.strip()):
        if l[:2] in D:
            pos = move(*pos,*D[l[:2]])
            l = l[2:]
        else:
            pos = move(*pos, *D[l[0]])
            l = l[1:]
    if pos in BT:
        BT.remove(pos)
    else:
        BT.add(pos)

print(f"Part 1: {len(BT)}")

neighbours = lambda x,y: sum(move(x,y,*d) in BT for d in D.values())

for day in range(100):
    newBT = {*BT}
    xr, yr = (min(BT)[0]-1, max(BT)[0]+2), (min(x[1] for x in BT)-1, max(x[1] for x in BT)+2)
    for x in range(*xr):
        for y in range(*yr):
            if (x,y) in BT and neighbours(x,y) not in (1,2):
                newBT.remove((x,y))
            elif (x,y) not in BT and neighbours(x,y) == 2:
                newBT.add((x,y))

#     print(f"Day {day+1}: {len(newBT)}")
    BT = newBT

print(f"Part 2: {len(newBT)}")
