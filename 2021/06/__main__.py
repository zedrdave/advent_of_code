with open('input.txt', 'r') as f:
    data = f.read()

from collections import deque

L = [0]*9
for i in data.split(','):
    L[int(i)] += 1


def count_fish(L, days):
    Q = deque(L)

    for i in range(days):
        spawn = Q.popleft()
        Q[-2] += spawn
        Q.append(spawn)
    return sum(Q)


print('Part 1', count_fish(L, 80))
print('Part 2', count_fish(L, 256))
