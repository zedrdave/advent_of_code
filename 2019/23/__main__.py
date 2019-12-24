# import copy
import numpy as np
import math

from ..utils import loadCSVInput, dprint, setVerbosity, inputFile
from ..intcode.VM import VM, NeedInputException

setVerbosity(False)

vms = []

for i in range(50):
    instructions = loadCSVInput()
    vms += [VM(instructions, input=[i])]

print("Starting…")
NAT = None
lastY = None
while True:
    active = False
    for i,vm in enumerate(vms):
        print("Running VM", i)
        vm.input += [-1]
        while True:
            try:
                address,x,y = next(vm.run()),next(vm.run()),next(vm.run())
                print(address,x,y)
                active = True
                if address == 255:
                    NAT = [x,y]
                else:
                    vms[address].input += [x,y]
            except NeedInputException:
                break
            except StopIteration:
                break
            # except Exception as e:
    if not active:
        vms[0].input = NAT
        if lastY == NAT[1]:
            print("Sending ", NAT[1], "for second time in a row")
            break
        lastY = NAT[1]
print("Done")
