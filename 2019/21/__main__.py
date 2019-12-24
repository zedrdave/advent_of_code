# import copy
import numpy as np
import math

from ..utils import loadCSVInput, dprint, setVerbosity, inputFile
from ..intcode.VM import VM


# arr2str = lambda a: '\n'.join([''.join([str(c) for c in line]) for line in a])

# !A | !B | !C  & D & (E | H)
# !(A & B & C) & D &

springProg = """OR A T
AND B T
AND C T
NOT T T
AND D T
OR T J
AND E T
OR H T
AND T J
"""

for s in range(1):
    instructions = loadCSVInput()
    vm = VM(instructions)
    vm.input = [ord(c) for c in springProg.strip() + "\nRUN\n"]
    floor = []
    start = None
    for i,c in enumerate(vm.run()):
        # print(c)
        try:
            print(chr(c), end='')
            if not start and chr(c) == '@':
                start = i
            if start and start + 17 < i < start + 35:
                floor += [chr(c)]
        except:
            print("raw: ", c)
            break
    floor = np.array(floor)
    print(floor)
