import numpy as np

m = np.loadtxt('input.txt')
print(sum((m//3)-2))

# with check for negative values:
print(sum(np.fmax(m//3-2,0)))
