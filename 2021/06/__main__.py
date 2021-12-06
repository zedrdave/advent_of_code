with open('input.txt', 'r') as f:
    data = f.read()

from collections import deque

L = [0]*9
for i in data.split(','):
    L[int(i)] += 1


def count_fish_deque(L, days):
    Q = deque(L)

    for i in range(days):
        spawn = Q.popleft()
        Q[-2] += spawn
        Q.append(spawn)
    return sum(Q)


def count_fish_list(L, days):
    cur_idx = 0

    for i in range(days):
        L[cur_idx-2] += L[cur_idx]
        cur_idx = (cur_idx+1) % len(L)
    return sum(L)


print('Part 1', count_fish_deque(L, 80))
print('Part 2', count_fish_deque(L, 256))

assert count_fish_deque(L, 256) == count_fish_list(L, 256)
