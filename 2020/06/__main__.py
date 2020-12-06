from ..utils import input_file

from collections import Counter

data = [
    (Counter(l.replace('\n', '')), len(l.split('\n')))
    for l in open(input_file()).read().split('\n\n')
]

print(
'Pt 1:',
    sum(len(g[0]) for g in data),
'\nPt 2:',
    sum(v == g[1] for g in data for v in g[0].values())
)
