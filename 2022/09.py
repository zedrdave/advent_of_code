from aocd import get_data, submit

day = 9
year = 2022
data = get_data(day=day, year=year)

dirs = {'R': (1, 0), 'U': (0, 1), 'L': (-1, 0), 'D': (0, -1)}
def move(X, d): return (X[0]+d[0], X[1]+d[1])


def solve(data, num_knots=10):
    K = [(0, 0)] * num_knots
    visited = set(K)

    moves = [l[0] for l in data.split("\n") for _ in range(int(l.split()[1]))]

    for dir in moves:
        K[0] = move(K[0], dirs[dir])
        for k in range(1, len(K)):
            delta = [K[k-1][i] - K[k][i] for i in (0, 1)]
            if abs(max(delta, key=abs)) > 1:
                K[k] = move(K[k], [(x > 0)-(x < 0) for x in delta])
        visited.add(K[-1])

    return len(visited)


solve(data, 2), solve(data, 10)


# Compact version:

# move = lambda X,d: (X[0]+d[0], X[1]+d[1])
# delta = lambda X,i: move(X[i-1], [-x for x in X[i]])
# absmax = lambda X: abs(max(X, key=abs))
# def solve(data, num_knots = 10):
#     K = [(0,0)] * num_knots
#     visited = set(K)

#     move_dirs = [dirs[l[0]] for l in data.split("\n") for _ in range(int(l.split()[1]))]

#     for dir in move_dirs:
#         K[0] = move(K[0], dir)
#         K[1:] = [move(K[k], [(x>0)-(x<0) for x in delta(K, k)])
#                     if absmax(delta(K, k)) > 1
#                     else K[k]
#                 for k in range(1, len(K))]
#         visited.add(K[-1])

#     return len(visited)
