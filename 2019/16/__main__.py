import math
import numpy as np
from collections import defaultdict
from ..utils import dprint, setVerbosity, inputFile

# Debug:
setVerbosity(False)

with open(inputFile("input.txt")) as f:
    digits = f.readline().strip()

# Part 1: (slow method)

# Test:
# digits = '69317163492948606335995924319873'

pattern = [0, 1, 0, -1]

for phase in range(100):
    new_digits = ''
    for n in range(len(digits)):
        pn_pattern = [i for i in pattern for _ in range(n+1)]
        checksum = sum([int(d)*pn_pattern[(i+1)%len(pn_pattern)] for i,d in enumerate(digits)])
        new_digits += str(checksum)[-1]
        # print(str(checksum)[-1])
    digits = new_digits

print("Part 1 - ", digits[:8])

# Part 2 (optimised)
# Test:
# digits = '02935109699940807407585447034323'

with open(inputFile("input.txt")) as f:
    digits = f.readline().strip()

skip = int(digits[0:7])
digits = [int(i) for i in digits] * 10000

# confirm that only the first 2 elements of the pattern will be used:
assert(len(digits) < 2*skip - 1)

for phase in range(100):
    # n first digits only affected by n first digits of checksum
    # and all pattern positions after `skip` are `1`:
    checksum = 0
    new_digits = []
    for n in range(1,len(digits)-skip+1):
        checksum += digits[-n]
        new_digits += [int(str(checksum)[-1])]
    digits = [0]*skip + list(reversed(new_digits))
    dprint(f"Phase {phase+1}: {digits[skip:(skip+8)]}")

print("Part 2 - ", ''.join(str(i) for i in digits[skip:(skip+8)]))
