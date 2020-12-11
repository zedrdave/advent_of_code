from ..utils import *

D = [l.strip() for l in open(input_file())]
P = {(x,y):1
     for x,Y in enumerate(D)
     for y,s in enumerate(Y) if s=='L'}

def solve(P, 𝝆, 𝝉):
    # 𝝆: radius in which to look for neighbours
    # 𝝉: number of neighbours threshold for standing up

    Δ = [-1,0,1] # directions
    neighbours = lambda x, y: sum(next(  (P[x + r*ẋ, y + r*ẏ]
                                            for r in range(1, 𝝆+1)
                                            if (x + r*ẋ, y + r*ẏ) in P),
                                        0) # next default if StopIteration
                        for ẋ in Δ for ẏ in Δ)

    while True:
        Q = { p: (neighbours(*p) <= 𝝉+1) if P[p] else (neighbours(*p) == 0)
                for p in P }
        if P == Q:
            return sum(P.values())
        P = Q

print('Part 1:', solve(P, 1, 3), '\nPart 2:', solve(P, len(D), 4))
