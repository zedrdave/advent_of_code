from ..utils import *

import math

data = open(input_file()).read()

P = {int(p[5:9]): p[11:] for p in data.split('\n\n')}

edge = lambda p,i: [p[:10], p[9::11], p[-10:], p[0::11]][i]

def transform(p):
    for _ in range(4):
        yield p
        yield '\n'.join(l[::-1] for l in p.split('\n')) # flip
        p = '\n'.join(''.join(l[::-1]) for l in zip(*p.split('\n'))) # rotate

def get_match(pieces, p, side):
    for o in pieces:
        if o in transform(p):
            continue
        for ot in transform(o):
            if edge(ot, (side+2)%4) == edge(p, side):
                return ot
    return 0

Z = P.values()
corners = [k for k,v in P.items() if sum(not get_match(Z, v, i) for i in range(4)) == 2]
print('Part 1:', math.prod(corners))

def get_line(pieces, p, orient):
    R = [p]
    for _ in range(11):
        R += [get_match(pieces, R[-1], orient)]
    return R

corner_tile = next(p for p in transform(P[corners[0]]) if (get_match(Z, p, 2) and get_match(Z, p, 3)))
G = [get_line(Z, a, 3) for a in get_line(Z, corner_tile, 2)]

image = '\n'.join(''.join(a[i+1:i+9] for a in B[::-1]) for B in G for i in range(11, 99, 11))

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
