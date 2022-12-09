from aocd import get_data, submit

day = 9
year = 2022
data = get_data(day=day, year=year)

dirs = {'R': (1, 0), 'U': (0, 1), 'L': (-1, 0), 'D': (0, -1)}
def move(X, d): return (X[0]+d[0], X[1]+d[1])


def solve(data, num_knots=10):
    K = [(0, 0)] * num_knots
    visited = set(K)

    for l in data.split("\n"):
        dir, steps = l.split()
        for _ in range(int(steps)):
            K[0] = move(K[0], dirs[dir])
            for k in range(1, len(K)):
                delta = [K[k-1][i] - K[k][i] for i in (0, 1)]
                if abs(max(delta, key=abs)) > 1:
                    K[k] = move(K[k], [x//(abs(x) or 1) for x in delta])
            visited.add(K[-1])

    return len(visited)


print("Part 1:", solve(data, 2))
print("Part 2:", solve(data, 10))
