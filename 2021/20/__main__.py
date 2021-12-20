from functools import reduce

with open('20/input.txt', 'r') as f:
    data = f.read()
algo, A = data.split('\n\n')
algo = algo.replace('\n', '')

A = np.array([[c == '#' for c in l] for l in A.split('\n')], dtype=int)
algo = np.array([c == '#' for c in algo], dtype=int)

defaults = [algo[0], algo[511] if algo[0] else algo[0]]


def enhance(A, times):
    for it in range(times):
        A = np.pad(A, 2, constant_values=defaults[(it + 1) % 2])
        B = np.ones(A.shape, dtype=int) * default[it % 2]

        for i in range(1, A.shape[0]-1):
            for j in range(1, A.shape[1]-1):
                B[i, j] = algo[reduce(lambda x, t: x*2+t,
                                      A[(i-1):(i+2), (j-1):(j+2)].flat)]

        A = B

    return A


print('Part 1:', enhance(A, 2).sum())
print('Give me a hard copy right there:', enhance(A, 50).sum())
