from ..utils import *

# Solution using Tribonacci sequence
D = sorted(int(i) for i in open(input_file()))

δ = [i-j for i,j in zip(D, [0]+D)] + [3]
Δ = [1+p for p,d in enumerate(δ) if d==3]
L = [hi-lo-1 for lo,hi in zip([0] + Δ[:-1], Δ)]

# Optional, hardcode:
# T = [1, 1, 2, 4, 7, 13]
T = [1, 1, 2]
while len(T) <= max(L): T += [sum(T[-3:])]

import math
print('Part 1:', (len(δ)-len(Δ))*len(Δ),
      '\nPart 2:', math.prod(T[l] for l in L))
