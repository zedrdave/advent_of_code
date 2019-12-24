import itertools
import asyncio
from collections import deque

from ..intcode.VM import VM
from ..utils import loadCSVInput, dprint, setVerbosity

# Debug:
setVerbosity(True)

instructions = loadCSVInput()

max_output = 0
for phases in itertools.permutations([5,6,7,8,9]):
    dprint("Phases: ", phases)
    machines = [VM(instructions, phase=phase) for phase in phases]
    iter = 0
    in_out = 0 # first input
    while True:
        try:
            dprint(f"\n*** iter {iter} ***")
            for machine in machines:
                in_out = next(machine.run([in_out]))
            iter += 1
        except StopIteration:
            break
    max_output = max(max_output, in_out)

print(f"max output: {max_output}")
# 1047153
