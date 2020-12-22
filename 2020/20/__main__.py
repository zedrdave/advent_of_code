from ..utils import *


data = open(input_file()).read()

P = {int(p[5:9]): p[11:] for p in data.split('\n\n')}
Z = P.values()

edge = lambda p,i: [p[:10], p[9::11], p[-10:], p[0::11]][i]

def transform(p):
    for _ in range(4):
        yield p
        yield '\n'.join(l[::-1] for l in p.split('\n')) # flip
        p = '\n'.join(''.join(l[::-1]) for l in zip(*p.split('\n'))) # rotate

def match(p, side):
    for o in Z:
        if o in transform(p):
            continue
        for ot in transform(o):
            if edge(ot, (side+2)%4) == edge(p, side):
                return ot

corners = [k for k,v in P.items() if sum(not match(v, i) for i in range(4)) == 2]

import math
print('Part 1:', math.prod(corners))

corner_tile = next(p for p in transform(P[corners[0]]) if (match(p, 2) and match(p, 3)))

def get_line(p, side):
    R = [p]
    for _ in range(11):
        R += [match(R[-1], side)]
    return R

grid = [get_line(a, 3) for a in get_line(corner_tile, 2)]

image = '\n'.join(''.join(a[i+1:i+9] for a in B[::-1]) for B in grid for i in range(11, 99, 11))


import regex as re # Need `overlapped` option

spacing = '[.#\n]{77}'
monster = f'#.{spacing+"#....#"*3}##{spacing}.#{"..#"*5}'

for image_t in transform(image):
    m = len(re.findall(monster, image_t, overlapped=True))
    if m:
        print('Part 2:', sum(c == '#' for c in image_t) - 15*m)
        break


###################################################################
#
# print("\nVisualisation:")
#
###################################################################
#
#
# monster = '(.)#(.(?:.|\n){77})#(....)##(....)##(....)###((?:.|\n){77}.)#(..)#(..)#(..)#(..)#(..)#'
# show_monster = r'\1🐸\2🟢\3🟢🟢\4🟢🟢\5🟢🟢🟢\6🟢\7🟢\8🟢\9🟢\10🟢\11🟢'
#
# showing_monsters = re.sub(monster, show_monster, re.sub(monster, show_monster, image_t))
# print(showing_monsters.replace('.', '🟦').replace('#', '⬜️'))
# print('Num #:', sum(c == '#' for c in showing_monsters))
