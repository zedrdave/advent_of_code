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
from ..graphics import snapshot, saveAnimatedGIF

# arr2str = lambda a: '\n'.join([''.join([str(c) for c in line]) for line in a])
# isInMap = lambda n, w, b = 0: all(0+b <= n[i] < w.shape[i]-b for i in (0,1))
# isEmpty = lambda n,w: isInMap(n,w) and w[n[0],n[1]] == '.'
# move = lambda n,d, a = 1: (n[0]+ a*d[0], n[1]+ a*d[1], *n[2:])

with open('2019/22/input.txt') as f:
    shuffles = [s for s in f.read().strip().split('\n')]

# shuffles = """deal into new stack
# cut -2
# deal with increment 7
# cut 8
# cut -4
# deal with increment 7
# cut 3
# deal with increment 9
# deal with increment 3
# cut -1"""
# shuffles = [s for s in shuffles.strip().split('\n')]
#
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
# for _ in range(5):
#     for s in shuffles:
#         for cmd,fn in cmds.items():
#             if s.startswith(cmd):
#                 if cmd[-1] == ' ':
#                     arg = int(s[len(cmd):])
#                     # print(cmd, arg)
#                     deck = fn(deck, arg)
#                 else:
#                     # print(cmd)
#                     deck = fn(deck)
#                 # assert cardPos < deckSize
#                 break
#     print(deck.index(2019))

#######

import functools

def dealInc(deckSize, n, x, a, b, rep):
    # return (cardPos*n) % deckSize
    return (a*n, b*n) # f"({cardPos}*{n})"

def cutCardsPos(deckSize, n, x, a, b, rep):
    if rep < 1 and x <= n:
        # assert rep < 1
        # return cardPos + deckSize - n
        # return f"({deckSize-n}+{cardPos})"
        return (a, b+deckSize-n)
    else:
        # return cardPos - n
        # return f"({cardPos}-{n})"
        return (a, b-n)

def cutCardsNeg(deckSize, n, x, a, b, rep):
    if rep < 1 and x >= deckSize-n:
        # assert rep < 1
        # return cardPos - deckSize + n
        # return f"({cardPos}-{deckSize-n})"
        return (a, b-deckSize+n)
    else:
        # return cardPos + n
        # return f"({cardPos}+{n})"
        return (a, b+n)

# deckSize-1 -(ax + b)
def dealNew(deckSize, x, a, b, rep):
    # return deckSize - cardPos - 1
    # return f"({deckSize-1}-{cardPos})"
    return (-a, deckSize-1-b)

cmds = {
    'deal with increment ': dealInc,
    'deal into new stack': dealNew,
    'cut -': cutCardsNeg,
    'cut ': cutCardsPos,
}

# (((s-1 - ((x*64))) - 1004) * 31) % s
# deal with increment 64
# deal into new stack
# cut 1004
# deal with increment 31


deckSize = 119315717514047
cardPos = 2020
# deckSize = 10007
# initialCardPos = cardPos = 2019

repeat = 101741582076661
# repeat = 1

shuffleCmds = []
for s in shuffles:
    for cmd,fn in cmds.items():
        if s.startswith(cmd):
            if len(s) > len(cmd):
                arg = int(s[len(cmd):])
                shuffleCmds += [functools.partial(fn, deckSize, arg)]
            else:
                shuffleCmds += [functools.partial(fn, deckSize)]
            break

a0 = 1
b0 = 0
for i,shuffleCmd in enumerate(shuffleCmds):
    a0,b0 = shuffleCmd(a0*cardPos + b0, a0, b0, 0)
    a0 = a0 % deckSize
    b0 = b0 % deckSize

print(a0,b0)
print("Res:", (a0*cardPos + b0) % deckSize)
res1 = (a0*cardPos + b0) % deckSize

a, b = 1, 0
# for rep in range(1, 5):
for i,shuffleCmd in enumerate(shuffleCmds):
    a,b = shuffleCmd('x', a, b, 1)
    a = a % deckSize
    b = b % deckSize

# x * a + b
# r = b / (1-a)
x = res1
print("a,b:", a,b)
r = b / (1-a)


n = 7
print( (
    modMult(pow(a,n,deckSize), res1, deckSize)
     + ((pow(a, n) * b // (a-1)) % deckSize)
     +  r
) % deckSize )
#
#
# print( math.ceil(
#     modMult(pow(a,n), res1, deckSize)
#      + ((pow(a, n) * b // (a-1)) % deckSize)
#      +  r
# ) % deckSize )



# n = repeat
# print( math.ceil(
#     modMult(pow(a,n), res1, deckSize) + ((pow(a,n) * b // (a-1)) % deckSize) +  r
# ) % deckSize )

# for rep in range(1, repeat):
#     if rep%10000 == 0:
#         print("#", rep, end="\r")
#     for i,shuffleCmd in enumerate(shuffleCmds):
#         cardPos = shuffleCmd(cardPos, rep)
#         if cardPos == initialCardPos:
#             print("rep:", rep, " - i:", i)
#             print(cardPos)
#             sys.exit()

# print(cardPos)

# 8502
