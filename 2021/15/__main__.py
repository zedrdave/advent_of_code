import numpy as np

with open('15/input.txt', 'r') as f:
    data = f.read()

data = [[int(i) for i in l] for l in data.split('\n')]
dists = np.array(data)

# Part 2:
dists = np.concatenate([((dists + i - 1) % 9)+1 for i in range(5)], axis=0)
dists = np.concatenate([((dists + i - 1) % 9)+1 for i in range(5)], axis=1)

M = dists.shape[0]
min_paths = np.ones(dists.shape) * 100000
min_paths[0, 0] = 0

frontier = {(0, 0)}

while len(frontier):
    x, y = frontier.pop()
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if (x+dx < 0) or (y+dy < 0) or (x+dx >= M) or (y+dy >= M):
            continue
        neigh = (x + dx, y + dy)
        d = min_paths[x, y] + dists[neigh]
        if d < min_paths[neigh]:
            min_paths[neigh] = d
            frontier |= {neigh}

print(min_paths[M-1, M-1])

# min_paths[:17,:10]
