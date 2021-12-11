with open('09/input.txt', 'r') as f:
    data = f.read().strip()

A = np.array([list(l) for l in data.split('\n')])
M = np.pad((A != '9'), 1)


def grow(M, pt):
    if not M[pt]:
        return 0
    M[pt] = 0
    return 1 + sum(grow(M, (pt[0]+h, pt[1]+v)) for h, v in ([-1, 0], [1, 0], [0, -1], [0, 1]))


sizes = [grow(M, (x, y)) for x in range(M.shape[0]) for y in range(M.shape[1])]
np.prod(sorted(sizes)[-3:])
