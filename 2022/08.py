from aocd import get_data, submit
import numpy as np

day = 8
year = 2022

data = get_data(day=day, year=year)

A = np.array([[int(i) for i in l] for l in data.split("\n")])


def visible(l): return [k > max([-1, *l[:i]]) for i, k in enumerate(l)]


def view(l): return [next((j+1 for j, v in enumerate(l[i+1:])
                           if v >= l[i]), len(l)-i-1) for i in range(len(l)-1)] + [0]


def apply4sides(fn, X): return [np.rot90(np.apply_along_axis(
    fn, 1, np.rot90(X, k=k)), k=4-k) for k in range(4)]


def mprod(X): return np.prod(np.array(X), axis=0)


print("Part 1:", (sum(apply4sides(visible, A)) > 0).sum())
print("Part 2:", mprod(apply4sides(view, A)).max())
