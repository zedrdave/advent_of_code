

with open('../input.txt', 'r') as f:
    data = f.read().strip()

A = np.array([[int(i) for i in l] for l in data.split('\n')])

M = (A < 9)

r1 = (slice(None,-1), slice(None))
r2 = (slice(1, None), slice(None))
M[r1] &= A[r1] < A[r2]
M[r2] &= A[r2] < A[r1]
r1 = r1[::-1]
r2 = r2[::-1]
M[r1] &= A[r1] < A[r2]
M[r2] &= A[r2] < A[r1]

(A+1)[M].sum()


with open('../input.txt', 'r') as f:
    data = f.read().strip()

A = np.array([list(l) for l in data.split('\n')])
M = np.pad((A != '9'), 1)

def grow(M, pt):
    if not M[pt]: return 0
    M[pt] = 0
    return 1 + sum(grow(M, (pt[0]+h, pt[1]+v)) for h,v in ([-1,0],[1,0],[0,-1],[0,1]))

sizes = [grow(M, (x,y)) for x in range(M.shape[0]) for y in range(M.shape[1])]
np.prod(sorted(sizes)[-3:])