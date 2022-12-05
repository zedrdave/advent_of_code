from aocd import get_data, submit

day = 4
year = 2022
data = get_data(day=day, year=year)

D = [[[int(i) for i in p.split('-')] for p in l.split(",")] for l in data.split("\n")]

𝓛 = lambda p: p[1]+1-p[0]

def overlap(p1, p2):
    if p1[0] > p2[0]:
        return overlap(p2, p1)
    if p1[1] < p2[0]:
        return 0
    return 𝓛([p2[0], min(p1[1], p2[1])])

print("Part 1:", sum(overlap(*l) == min(𝓛(l[0]), 𝓛(l[1])) for l in D))

print("Part 2:", sum(overlap(*l) > 0 for l in D))


# Using Regex:

import re
L = data.split("\n")

inter_lens = [eval(re.sub(r"(\d+)\-(\d+),(\d+)\-(\d+)", 
            r"len(set(range(\1,\2+1)).intersection(set(range(\3,\4+1))))", l)) for l in L]

min_lens = [eval(re.sub(r"(\d+)\-(\d+),(\d+)\-(\d+)", 
            r"min(len(set(range(\1,\2+1))), len(set(range(\3,\4+1))))", l)) for l in L]


sum(a == b for a,b in zip(inter_lens, min_lens))
sum(a > 0 for a in inter_lens)

