from ..utils import *

def play(C, n):

    # Linked list or successors:
    LL = {k:v for k,v in zip(C, C[1:]+C[:1])}
    LL[0] = 0

    c = C[0]
    for _ in range(n):
        x = LL[c]
        y = LL[x]
        z = LL[y]
        LL[c] = LL[z]
        d = c-1
        while d in (x,y,z,0):
            d = d-1 if d else len(C)
        LL[z] = LL[d]
        LL[d] = x
        c = LL[c]
    return LL


C = [int(i) for i in open(input_file()).read()]
LL = play(C, 100)
c,s = LL[1],''
while c != 1:
    s += str(c)
    c = LL[c]
print('Part 1:', s)

n = 1000000
C += range(max(C)+1, n+1)
LL = play(C, 10*n)
print('Part 2:', LL[1]*LL[LL[1]])
