from collections import defaultdict, Counter

with open('./input.txt', 'r') as f:
    data = f.read()

T, _, *R = data.split('\n')
R = dict(r.split(' -> ') for r in R)

P = Counter([a+b for a, b in zip(T, T[1:])])


def polymerise(P, steps):
    for i in range(steps):
        NP = defaultdict(int)
        for pair, count in P.items():
            NP[pair[0] + R[pair]] += count
            NP[R[pair] + pair[1]] += count
        P = NP

    counts = [max(sum(count for (p1, _), count in P.items() if c == p1),
                  sum(count for (_, p2), count in P.items() if c == p2))
              for c in set(''.join(P.keys()))]

    return max(counts) - min(counts)


print('Part 1:', polymerise(P, 10), '\nPart 2:', polymerise(P, 40))
