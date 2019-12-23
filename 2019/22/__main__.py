import math
import copy
import string
import sys
import copy
from collections import defaultdict
import itertools
import networkx as nx
import numpy as np

from ..utils import dprint, setVerbosity, inputFile
# from ..graphics import snapshot, saveAnimatedGIF


with open(inputFile()) as f:
    shuffles = [s for s in f.read().strip().split('\n')]

# Part 1: The age of innocence

# deck = list(range(0, 10007))
#
# def dealInc(deck, n):
#     newDeck = [-1] * len(deck)
#     i = 0
#     while len(deck):
#         newDeck[i % len(newDeck)] = deck.pop(0)
#         i += n
#     assert not any(i == -1 for i in newDeck)
#     return newDeck
#
# cmds = {
#     'deal with increment ': dealInc,
#     'deal into new stack': (lambda x: x[::-1]),
#     'cut ': (lambda x,n: x[n:] + x[:n])
# }
#
# for s in shuffles:
#     for cmd,fn in cmds.items():
#         if s.startswith(cmd):
#             if cmd[-1] == ' ':
#                 arg = int(s[len(cmd):])
#                 deck = fn(deck, arg)
#             else:
#                 deck = fn(deck)
#             # assert card < m
#             break
# print("Part 1 - card 2019 is at: ", deck.index(2019))

# Part 2: Number Theory Chainsaw Massacre

import functools

cmds = {
    'deal with increment ': lambda x,m,a,b: (a*x %m, b*x %m),
    'deal into new stack': lambda _,m,a,b: (-a %m, (m-1-b)%m),
    'cut -': lambda x,m,a,b: (a, (b-m+x)%m),
    'cut ': lambda x,m,a,b: (a, (b+m-x)%m),
}

shuffleSeq = []
for s in shuffles:
    for cmd,fn in cmds.items():
        if s.startswith(cmd):
            # if len(s) > len(cmd):
            arg = int(s[len(cmd):]) if len(s) > len(cmd) else 0
            shuffleSeq += [functools.partial(fn, arg)]
            break

def modularComp(shuffleSeq, m, n, card = None, pos = None):
    a,b = 1,0
    for shuffleCmd in shuffleSeq:
        a,b = shuffleCmd(m, a, b)
        a = a % m
        b = b % m

    # pos = card * a + b
    # card = (pos - b) * inv_a

    # pos = (card - r) * a**n + r
    # card = (pos - r) * inv_a**n + r

    # r = b / (1-a)
    #   = b * ((1-a) ** (phi_m - 1))

    print("a =", a, " | b =", b)
    phi_m = m - 1 # m is prime
    inv_a = pow(a, phi_m - 1, m)
    r = (b * pow(1-a, phi_m - 1, m)) % m

    if card:
        calcPos = ((card - r) * pow(a, n, m) + r) % m
        print(f"{card} is at pos: {calcPos}")

    if pos:
        calcCard = ((pos - r) * pow(inv_a, n, m) + r) % m
        print(f"Card at #{pos}: {calcCard}\n")

    if pos and card:
        assert pos == calcPos, "Calculated position incorrect"
        assert card == calcCard, "Calculated card incorrect"


print("testing with part 1 result:")
modularComp(shuffleSeq, m = 10007, n = 1, card = 2019, pos = 8502)

print("testing iteratively:")
m = 119315717514047
card = 2020

a,b = 1,0
cardPos = []
for i in range(100):
    print(f"#{i} ({a},{b}): {(a*card + b) % m}")
    cardPos += [((a*card + b) % m, a, b)]
    for shuffleCmd in shuffleSeq:
        a,b = shuffleCmd(m, a, b)

for n, (pos, a, b) in enumerate(cardPos):
    print(f"{n}: {pos}")
    phi_m = m - 1
    inv_a = pow(a, phi_m - 1, m)
    print(f"[iterative] Card at {pos}: ", ((pos - b)%m * inv_a) % m)
    modularComp(shuffleSeq, m, n, card = card, pos = pos)

print("Part 2")
modularComp(shuffleSeq, m = 119315717514047, n = 101741582076661, pos = 2020)
