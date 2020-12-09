from ..utils import *

N = [int(n) for n in open(input_file())]
p = 25

def is_ok(P, n):
    S = sorted(P)
    for i, a in enumerate(S):
        if a > n//2:
            break
        if n-a in S[i+1:]:
            return True

x = next(n for i,n in enumerate(N[p:]) if not is_ok(N[i:i+p], n))
print('Part 1:', x)

C = []
for n in N:
    C += [n]
    while sum(C) > x:
        C.pop(0)
    if len(C) > 1 and sum(C) == x:
        break

print('Part 2:', min(C)+max(C))


#####################################
#
print("\nCompact code:")
#
#####################################

p,N,C = 25, [int(n) for n in open(input_file())], []

is_ok = lambda n, S: any(1 for j in range(p) if n-S[j] in S[j+1:])

x = next(n for i,n in enumerate(N[p:]) if not is_ok(n, sorted(N[i:i+p])))

for n in N:
    C += [n]
    while sum(C) > x: C.pop(0)
    if len(C) > 1 and sum(C) == x: print('Part 1:', x, '\nPart 2:', min(C)+max(C))
