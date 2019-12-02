import numpy as np
masses = np.loadtxt('input.txt')

def recur(x):
    f = (x//3)-2
    return 0 if f <= 0 else f + recur(f)

print("Using regular function: ", sum(map(recur, masses)))

###########
# Lambda variation
###########

recur_lambda = lambda x: 0 if x < 9 else recur_lambda(x//3 - 2) + x//3 - 2
print("Using lambda function: ", sum(map(recur_lambda, masses)))
