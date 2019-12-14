import numpy as np
from ..utils import inputFile

masses = np.loadtxt(inputFile())

print("Part 1:", sum((masses//3)-2))

# with check for negative values:
print("Part 1 (safe):", sum(np.fmax(masses//3-2,0)))


def recur(x):
    f = (x//3)-2
    return 0 if f <= 0 else f + recur(f)

print("Part 2: Using regular function: ", sum(map(recur, masses)))

###########
# Lambda variation
###########

recur_lambda = lambda x: 0 if x < 9 else recur_lambda(x//3 - 2) + x//3 - 2
print("Part 2: Using lambda function: ", sum(map(recur_lambda, masses)))
