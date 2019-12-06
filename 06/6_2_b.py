with open('input.txt', 'r') as f:
    parents = dict( reversed(orbit.split(')')) for orbit in f.read().splitlines() )

# Part 1:
dist_to_root = lambda n: 1+dist_to_root(parents[n]) if n in parents else 0
print(sum(dist_to_root(n) for n in parents))

# Part 2:
ancestors = lambda n: ancestors(parents[n]).union([parents[n]]) if n in parents else set()
print(len(ancestors('YOU') ^ ancestors('SAN')))
