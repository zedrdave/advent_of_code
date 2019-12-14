import math
from collections import defaultdict
from ..utils import dprint, setVerbosity, inputFile

# Debug:
setVerbosity(False)

with open(inputFile("input.txt")) as f:
    reactions = [[[
        (int(e.split()[0]), e.split()[1])
            for e in s.split(", ")]
                for s in l.strip().split(' => ')]
                    for l in f]

reactions = { r[1][0][1]: (int(r[1][0][0]),r[0]) for r in reactions }

def orePerFuel(fuel):
    need = defaultdict(int, {'FUEL': fuel})
    while True:
        try:
            need_e, need_n = next((e,n) for e,n in need.items() if n > 0 and e != 'ORE')
        except: break
        prod_n, reactants = reactions[need_e]
        mult_reac = math.ceil(need_n/prod_n)
        for coef,reactant in reactants:
            need[reactant] += mult_reac * coef
        need[need_e] -= mult_reac*prod_n
    return need['ORE']

print(f"Part 1 - For 1 FUEL, need: {orePerFuel(1)} ORE")
# 504284

have_ore = 1000000000000

min_f = have_ore//orePerFuel(1)
max_f = 2*min_f

while max_f > min_f+1:
    prod_fuel = min_f + (max_f - min_f) // 2
    dprint(f"[{max_f}, {min_f}]: prod_fuel")
    if orePerFuel(prod_fuel) > have_ore:
        max_f = prod_fuel
    else:
        min_f = prod_fuel

print(f"Part 2 - With {have_ore} ORE, can produce: {min_f} FUEL")
# 2690795
