with open('input.txt', 'r') as f:
    parents = dict( reversed(orbit.split(')')) for orbit in f.read().splitlines() )

ancestors = lambda n: ancestors(parents[n]).union([parents[n]]) if n in parents else set()

# Part 1:
print("Part 1:", sum(len(ancestors(n)) for n in parents))

# Part 2:
print("Part 2:", len(ancestors('YOU') ^ ancestors('SAN')))
