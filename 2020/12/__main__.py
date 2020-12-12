from ..utils import *

P,W = [0,0],[1,0]

ℳ = lambda x,y,dx,dy,d: (x+d*dx, y+d*dy) # Move

cos, sin = [1,0,-1,0], [0,1,0,-1] # by increments of 90
ℛ = lambda x,y,t: (x*cos[t]-y*sin[t], x*sin[t]+y*cos[t]) # Rotate

for i in open(input_file()):
    c,n = i[0], int(i[1:])

    if c == 'F': P = ℳ(*P, *W, n)
    elif c == 'R': W = ℛ(*W, -n//90 % 4)
    elif c == 'L': W = ℛ(*W, n//90)
    else: P = ℳ(*P, *ℛ(1, 0, 'ENWS'.index(c)), n)

print('Part 1:', abs(P[0]) + abs(P[1]))

P,W = [0,0],[10,1]

for i in open(input_file()):
    c,n = i[0], int(i[1:])

    if c == 'F': P = ℳ(*P, *W, n)
    elif c == 'R': W = ℛ(*W, -n//90 % 4)
    elif c == 'L': W = ℛ(*W, n//90)
    else: W = ℳ(*W, *ℛ(1, 0, 'ENWS'.index(c)), n)

print('Part 2:', abs(P[0]) + abs(P[1]))
