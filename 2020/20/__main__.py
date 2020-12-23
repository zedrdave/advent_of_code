from ..utils import *

P = {int(p[5:9]): p[11:] for p in open(input_file()).read().split('\n\n')}
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

image = '\n'.join(''.join(a[i:i+8] for a in B[::-1]) for B in grid for i in range(12, 99, 11))


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
print("\nCompact version:")
#
###################################################################

nl = '\n'
𝕛 = ''.join
𝕁 = nl.join
𝕣 = lambda l:l[::-1]

P = {int(p[5:9]): p[11:] for p in open(input_file()).read().split(nl*2)}
Z = P.values()

𝑬 = lambda p,i: [p[:10], p[9::11], p[-10:], p[0::11]][i]

def 𝑻(p):
    for _ in range(4):
        yield p; yield 𝕁(𝕣(l) for l in p.split(nl))
        p = 𝕁(𝕛(𝕣(l)) for l in zip(*p.split(nl)))

𝙈 = lambda p,d: next((r for q in Z for r in 𝑻(q) if q not in 𝑻(p) and 𝑬(r,(d+2)%4)==𝑬(p,d)), 0)
K = [k for k,v in P.items() if sum(not 𝙈(v, i) for i in range(4)) == 2]

import math
print('Part 1:', math.prod(K))

p = next(p for p in 𝑻(P[K[0]]) if (𝙈(p,2) and 𝙈(p,3)))

def 𝑳(p, o):
    R = [p]
    for _ in range(11):
        R += [𝙈(R[-1], o)]
    return R

G = 𝕁( 𝕛(b[i:i+8] for b in 𝕣(B))
       for B in [𝑳(a, 3) for a in 𝑳(p, 2)]
       for i in range(12, 99, 11) )


import regex as re
w = '[.#\n]{77}'
𝛹 = f'#.{w+"#....#"*3}##{w}.#{"..#"*5}'
for Ğ in 𝑻(G):
    m = len(re.findall(𝛹, Ğ,  overlapped=True))
    if m: print('Part 2:', sum(c == '#' for l in G for c in l) - 15*m)

###################################################################
#
# print("\nVisualisation:")
#
###################################################################
#
#
# monster = '(.)#(.(?:.|\n){77})#(....)##(....)##(....)###((?:.|\n){77}.)#(..)#(..)#(..)#(..)#(..)#'
# show_monster = r'\1🐲\2🟢\3🟢🟢\4🟢🟢\5🟢🟢🟢\6🟢\7🟢\8🟢\9🟢\10🟢\11🟢'
#
# showing_monsters = re.sub(monster, show_monster, re.sub(monster, show_monster, image_t))
# print(showing_monsters.replace('.', '🟦').replace('#', '⬜️'))
# print('Num #:', sum(c == '#' for c in showing_monsters))
