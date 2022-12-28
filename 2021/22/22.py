from aocd import get_data, submit
from collections import defaultdict
import numpy as np
import sys
import itertools
from collections import defaultdict, Counter
from tqdm.auto import tqdm

import re

day = 22
year = 2021

data = get_data(day=day, year=year)


pattern = r'(on|off) x=([-\d]+)\.\.([-\d]+),y=([-\d]+)\.\.([-\d]+),z=([-\d]+)\.\.([-\d]+)'
groups = [re.match(pattern, l).groups() for l in data.split('\n')]
coords = [(g[0] == 'on', tuple(int(d) for d in g[1:])) for g in groups]


def inter(s1, e1, s2, e2):
    if s1 > s2:
        return inter(s2, e2, s1, e1)
    if e1 < s2:
        return [False]
    return (s2, min(e1, e2))


def inter3d(c1, c2):
    inter_coords = tuple(
        (*inter(*c1[:2], *c2[:2]), *inter(*c1[2:4], *c2[2:4]), *inter(*c1[4:], *c2[4:])))
    if any(i is False for i in inter_coords):
        return False
    return inter_coords


def split_segment(a1, a2, b1, b2): return ((b1, b2),) + (((a1, b1-1),)
                                                         if a1 <= b1-1 else ()) + (((b2+1, a2),) if b2+1 <= a2 else ())


def split_cube(c1, c2): return list((*a, *b, *c) for a, b, c in itertools.product(
    split_segment(*c1[:2], *c2[:2]), split_segment(*c1[2:4], *c2[2:4]), split_segment(*c1[4:], *c2[4:])))


def cubeset_diff(cs1, cs2):
    for c2 in cs2:
        new_cs1 = set()
        for c1 in cs1:
            intersection = inter3d(c1, c2)
            if intersection is False:
                new_cs1.add(c1)
            else:
                new_cs1.update(split_cube(c1, intersection)[1:])
        cs1 = new_cs1
    return cs1


all_cubes = set()
for cube_on, cube in tqdm(coords, total=len(coords)):
    if cube_on:
        all_cubes |= cubeset_diff(set([cube]), all_cubes)
    else:
        all_cubes = cubeset_diff(all_cubes, set([cube]))


def cube_vol(c): return (c[1]-c[0]+1) * (c[3]-c[2]+1) * (c[5]-c[4]+1)


sum(cube_vol(c) for c in all_cubes)

# cubeset_diff(c1, c2)
