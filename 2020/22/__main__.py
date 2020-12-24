from ..utils import *

def 𝓟(p, q, P1=0):
    S={0}
    while p and q:
        h = {(*p,0,*q)}
        if h & S:
            return [1]
        S |= h
        c, d = p.pop(0), q.pop(0)
        if P1 or c > len(p) or d > len(q):
            w = c > d
        else:
            w = 𝓟(p[:c],q[:d])[0]
        if w:
            p += (c,d)
        else:
            q += (d,c)
    return (p,q)

for part in (1,2):
    p,q = [[int(i) for i in p[10:].split('\n')]
           for p in open(input_file()).read().split('\n\n')]

    p,q = 𝓟(p,q, part==1)

    print(f'Part {part}:', sum((i+1)*c for i,c in enumerate((p+q)[::-1])))
