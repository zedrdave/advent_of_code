import numpy as np

with open('11/input.txt', 'r') as f:
    data = f.read()

A = np.array([[int(i) for i in l] for l in data.split('\n')])

flashes = 0

for idx in range(1000):
    A += 1
    flashed = A < 0

    while True:
        flashing = A >= 10
        if not flashing.sum():
            break

        flashed |= flashing
        F = np.pad(flashing, 1).astype(int)
        A += F[0:-2, 0:-2] + F[1:-1, 0:-2] + F[2:, 0:-2] +\
            F[0:-2, 1:-1] + F[1:-1, 1:-1] + F[2:, 1:-1] +\
            F[0:-2, 2:] + F[1:-1, 2:] + F[2:, 2:]

        A[flashed] = 0

    flashes += flashed.sum()

    if idx+1 == 100:
        print('Part 1:', flashes)
    if flashed.all():
        print('Part 2:', idx+1)
        break
