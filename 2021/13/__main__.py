with open('./input.txt', 'r') as f:
    data = f.read()

coords, folds = data.split('\n\n')

coords = [[int(c.split(',')[0]), int(c.split(',')[1])]
          for c in coords.split('\n')]
M = np.array(coords).max(axis=0) + 1

A = np.zeros(M, dtype=bool)

for c in coords:
    A[tuple(c)] = True

folds = [(f[11] == 'y', int(f[13:])) for f in folds.split('\n')]

for axis, fold in folds:
    if axis:
        A = A[:, :fold] | np.flip(A[:, (fold+1):], axis=1)
    else:
        A = A[:fold, :] | np.flip(A[(fold+1):, :], axis=0)
    print(A.sum())
    # break

for l in A.transpose():
    print(''.join(" ◼️"[c] for c in l*1))


########
#
# No numpy:
#
########

coords, folds = data.split('\n\n')
coords = [list(map(int, c.split(','))) for c in coords.split('\n')]
folds = [(f[11] == 'y', int(f[13:])) for f in folds.split('\n')]

for axis, fold in folds:
    coords = {tuple(c) if c[axis] < fold else ((c[0], 2*fold-c[1]) if axis else (2*fold-c[0], c[1]))
              for c in coords}

M = max(max(c) for c in coords)
for y in range(M):
    l = ''.join('*' if (x, y) in coords else ' ' for x in range(M))
    if l != ' ' * M:
        print(l)
