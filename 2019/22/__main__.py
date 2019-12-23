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


with open(inputFile()) as f:
    shuffles = [s for s in f.read().strip().split('\n')]

# Part 1: The age of innocence

deck = list(range(0, 10007))

def dealInc(deck, n):
    newDeck = [-1] * len(deck)
    i = 0
    while len(deck):
        newDeck[i % len(newDeck)] = deck.pop(0)
        i += n
    assert not any(i == -1 for i in newDeck)
    return newDeck

cmds = {
    'deal with increment ': dealInc,
    'deal into new stack': (lambda x: x[::-1]),
    'cut ': (lambda x,n: x[n:] + x[:n])
}

for s in shuffles:
    for cmd,fn in cmds.items():
        if s.startswith(cmd):
            if cmd[-1] == ' ':
                arg = int(s[len(cmd):])
                deck = fn(deck, arg)
            else:
                deck = fn(deck)
            # assert card < m
            break
print("Part 1 - card 2019 is at: ", deck.index(2019))

# Part 2: Number Theory Chainsaw Massacre

    # m = 119315717514047
    # n = 101741582076661
    # pos = 2020
    # shuffles = { 'deal with increment ': lambda x,m,a,b: (a*x %m, b*x %m),
    #          'deal into new stack': lambda _,m,a,b: (-a %m, (m-1-b)%m),
    #          'cut ': lambda x,m,a,b: (a, (b-x)%m) }
    # a,b = 1,0
    # with open('2019/22/input.txt') as f:
    #   for s in f.read().strip().split('\n'):
    #     for name,fn in shuffles.items():
    #       if s.startswith(name):
    #         arg = int(s[len(name):]) if name[-1] == ' ' else 0
    #         a,b = fn(arg, m, a, b)
    #         break
    # r = (b * pow(1-a, m-2, m)) % m
    # print(f"Card at #{pos}: {((pos - r) * pow(a, n*(m-2), m) + r) % m}")
    #
    # sys.exit()

import functools

cmds = {
    'deal with increment ': lambda x,m,a,b: (a*x %m, b*x %m),
    'deal into new stack': lambda _,m,a,b: (-a %m, (m-1-b)%m),
    'cut ': lambda x,m,a,b: (a, (b-x)%m),
}

shuffleSeq = []
for s in shuffles:
    for cmd,fn in cmds.items():
        if s.startswith(cmd):
            arg = int(s[len(cmd):]) if cmd[-1] == ' ' else 0
            shuffleSeq += [functools.partial(fn, arg)]
            break

def modularComp(shuffleSeq, m, n, card = None, pos = None):
    """
    # After 1 set of shuffles:
    # pos = card * a + b  <-- composition of affine transformations
    # card = (pos - b) * inv_a

    # With:
    # inv_a (= a^-1) = a^(phi_m - 1) = a^(m-2) <-- phi: Euler function
    # phi_m = m-1 <-- since m is prime
    # inv_a = a^(m-2)

    # After n sets of shuffles:
    # pos = (card - r) * a^n + r  <-- arithmetico-geometric series
    # card = (pos - r) * inv_a^n + r

    # With:
    # inv_a^n = a^(n * (m-2))
    # r = b * (1-a)^-1
    #   = b * (1-a)^(phi_m - 1)
    """

    a,b = 1,0
    for shuffleCmd in shuffleSeq:
        a,b = shuffleCmd(m, a, b)
    dprint("a =", a, " | b =", b)

    r = (b * pow(1-a, m-2, m)) % m

    if card:
        calcPos = ((card - r) * pow(a, n, m) + r) % m
        dprint(f"{card} is at pos: {calcPos}")

    if pos:
        calcCard = ((pos - r) * pow(a, n*(m-2), m) + r) % m
        dprint(f"Card at #{pos}: {calcCard}\n")

    if pos and card:
        assert pos == calcPos, "Calculated position incorrect"
        assert card == calcCard, "Calculated card incorrect"

    return (calcCard if pos else card, calcPos if card else pos)

### Random tests:

dprint("Testing with part 1 result:")
modularComp(shuffleSeq, m = 10007, n = 1, card = 2019, pos = 8502)

dprint("Testing iteratively:")
m = 119315717514047
card = 2020

a,b = 1,0
cardPos = []
for i in range(100):
    dprint(f"#{i} ({a},{b}): {(a*card + b) % m}")
    cardPos += [((a*card + b) % m, a, b)]
    for shuffleCmd in shuffleSeq:
        a,b = shuffleCmd(m, a, b)

for n, (pos, a, b) in enumerate(cardPos):
    dprint(f"{n}: {pos}")
    inv_a = pow(a, m-2, m)
    dprint(f"[iterative] Card at {pos}: ", ((pos - b)%m * inv_a) % m)
    modularComp(shuffleSeq, m, n, card = card, pos = pos)

### End tests

card, pos = modularComp(shuffleSeq, m = 119315717514047, n = 101741582076661, pos = 2020)
print(f"Part 2 - card at position {pos}: {card}")
