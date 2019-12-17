import sys
import copy
from collections import defaultdict
import numpy as np

from ..intcode.VM import VM, NeedInputException
from ..utils import loadCSVInput, dprint, setVerbosity
from ..graphics import snapshot, saveAnimatedGIF

# Debug:
setVerbosity(False)

with open('2019/17/input.txt') as f:
    instructions = [int(i.strip()) for i in f.read().split(',')]

# instructions = loadCSVInput()

# vm = VM(instructions)
#
# str = ''
# while vm.is_running:
#     for c in vm.run():
#         str += chr(c)
#         print(chr(c), end='')
#
# arr = np.array([[*l] for l in str.strip().split('\n')]) != '.'
# inter = np.zeros(arr.shape, 'bool')
#
# for i,j in np.ndindex(arr.shape):
#     print(i, j)
#     if (0 < i < arr.shape[0]-1) and (0 < j < arr.shape[1]-1):
#         print('.')
#         if arr[i][j] and arr[i-1][j] and arr[i+1][j] and arr[i][j-1] and arr[i][j+1]:
#             inter[i][j] = True
#
# print(sum(i*j for i,j in zip(*np.where(inter))))

with open('2019/17/input.txt') as f:
    instructions = [int(i.strip()) for i in f.read().split(',')]

instructions[0] = 2
vm = VM(instructions)

while vm.is_running:
    try:
        for c in vm.run():
            print(chr(c), end='')
        # print(chr(27) + "[2J", flush=False)
    except NeedInputException:
        cmd = input(">")
        # print(cmd)
        print(list(ord(c) for c in cmd+'\n'))
        vm.input = [ord(c) for c in cmd+'\n']

# A,B,C
# R,8,L,12,
# R,8,R,12,
# L,8,R,10,
# R,12,L,10,
# R,10,R,10,
# L,12,R,8,
# R,8,L,8
# n
#
# R,4,L
# R,4,L
# 2,L,
#
#
# R,4,L
# R,4,L
# 2,L
# R,4,L
# R,4,L
# 2,L
#
#
# R,4,
# 4,L,6
# 6,R,4
# 4,R,6
# 6,L,4
# 4,R,6/4
#
###########..
#############
###########
#########
