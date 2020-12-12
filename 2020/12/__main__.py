from ..utils import *

# Moving:
ℳ = lambda x,y,dx,dy,d: (x+d*dx, y+d*dy)

cos = [1,0,-1,0]
sin = [0,1,0,-1]
# Rotation:
ℛ = lambda x,y,t: (x*cos[t]-y*sin[t], x*sin[t]+y*cos[t])

def solve(W, pt):
    P = [0, 0]
    A = {'L': 90, 'R': -90}

    for i in open(input_file()):
        c, n = i[0], int(i[1:])

        if c == 'F': # Move P by n in W's direction
            P = ℳ(*P, *W, n)
        elif c in A: # Rotate W +/- 90 degrees
            W = ℛ(*W, n//A[c] %4)
        else: # Move P (in pt 1) or W (in pt 2)
            dir = ℛ(1, 0, 'ENWS'.index(c))
            if pt == 1:
                P = ℳ(*P, *dir, n)
            else:
                W = ℳ(*W, *dir, n)

    print(f'Part {pt}:', abs(P[0]) + abs(P[1]))

solve([1,0], 1)
solve([10,1], 2)
