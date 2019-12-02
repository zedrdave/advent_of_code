import numpy as np
m = np.loadtxt('input.txt')

def recur(x):
    f = (x//3)-2
    return 0 if f <= 0 else f + recur(f)

print(sum(map(recur, m)))
