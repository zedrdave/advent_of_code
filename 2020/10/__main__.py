from ..utils import *

########################################
#
# Solution using Tribonacci sequence
#
########################################

D = sorted(int(i) for i in open(input_file()))

δ = [i-j for i,j in zip(D, [0]+D)] + [3]
Δ = [1+p for p,d in enumerate(δ) if d==3]
L = [hi-lo-1 for lo,hi in zip([0] + Δ[:-1], Δ)]

T = [1, 1, 2]
while len(T) <= max(L): T += [sum(T[-3:])]
# Optional, hardcode first 6 (input chains are never longer):
# T = [1, 1, 2, 4, 7, 13]

import math
print('Part 1:', (len(δ)-len(Δ))*len(Δ),
      '\nPart 2:', math.prod(T[l] for l in L))

# 94.1 µs ± 2.24 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)


########################################
#
# Using good ol' memoization
#
########################################

D = sorted(int(i) for i in open(input_file()))
D = [0, *D, D[-1]+3]

from collections import Counter
C = Counter(j-i for i,j in zip(D,D[1:]))

from functools import lru_cache
@lru_cache
def combos(A):
    if len(A) == 2: return 1
    return combos(A[1:]) + (combos(A[0:1]+A[2:]) if A[2]-A[0] < 4 else 0)


print('Part 1:', C[3]*C[1], '\nPart 2:', combos(tuple(D)))

# 328 µs ± 4.94 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
