import numpy as np
with open('input.txt', 'r') as f:
    data = f.read()

data = [int(i) for i in data.split(',')]


def fuel(p): return sum(abs(i-p) for i in data)
def fuel2(p): return sum(abs(i-p)*(abs(i-p)+1)//2 for i in data)


print('Part 1:', min(fuel(i) for i in range(max(data))))
print('Part 2:', min(fuel2(i) for i in range(max(data))))


print('Part 1:', fuel(np.median(data)))

m = np.mean(data)
print('Part 2:', min(fuel2(np.ceil(m)), fuel2(np.floor(m))))
