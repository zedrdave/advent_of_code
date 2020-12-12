from ..utils import *

ℳ = lambda x,y,dx,dy,d: (x+d*dx, y+d*dy)

cos = [1,0,-1,0]
sin = [0,1,0,-1]
ℛ = lambda x,y,t: (x*cos[t]-y*sin[t], x*sin[t]+y*cos[t])

def s(W=[1,0], pt=1):
    P = [0,0]

    for i in open(input_file()):
        c,n= i[0],int(i[1:])
        if c == 'F':
            P = ℳ(*P,*W,n)
        elif c == 'R':
            W = ℛ(*W,-n//90%4)
        elif c == 'L':
            W = ℛ(*W,n//90)
        else:
            r = ℛ(1,0,'ENWS'.index(c))
            if pt-1:
                W = ℳ(*W, *r, n)
            else:
                P = ℳ(*P, *r, n)

    print(f'Part {pt}:', abs(P[0]) + abs(P[1]))

s()
s([10,1],2)
