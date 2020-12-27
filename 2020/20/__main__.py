from ..utils import *

P = {int(p[5:9]): p[11:] for p in open(input_file()).read().split('\n\n')}

edge = lambda p,i: [p[:10], p[9::11], p[-10:], p[0::11]][i]

flip = lambda p: '\n'.join(l[::-1] for l in p.split('\n'))
rot90 = lambda p: '\n'.join(''.join(l[::-1]) for l in zip(*p.split('\n')))

# combinations of 8 rotations/flips:
def transform(p):
    A = [p]
    for _ in range(3):
        A += [rot90(A[-1])]
    A += [flip(a) for a in A]
    return A

# All pieces in all orientations:
Z = [z for p in P.values() for z in transform(p)]

# Matches for piece p along specific side
def match(p, side):
    self = transform(p)
    for o in Z:
        if o not in self and edge(o, (side+2)%4) == edge(p, side):
            return o

corners = [k for k,v in P.items()
            if sum(not match(v, i) for i in range(4)) == 2]

import math
print('Part 1:', math.prod(corners))

corner_tile = next(p for p in transform(P[corners[0]])
                    if (match(p, 2) and match(p, 3)))

# Incrementally find row starting from piece, in given direction (side):
def get_line(p, side):
    R = [p]
    for _ in range(11):
        R += [match(R[-1], side)]
    return R

# Build row starting from corner tile, then all columns from that row:
grid = [get_line(a, 3) for a in get_line(corner_tile, 2)]

# Remove edges and join all pieces
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

𝒏 = '\n'
𝕛,𝕁 = ''.join, 𝒏.join
from itertools import accumulate as 𝒞

P = {int(p[5:9]): p[11:] for p in open(input_file()).read().split(2*𝒏)}
d = 12 # puzzle dimension: int(len(P)**.5)

# Get orientations:
def 𝑻(p):
    X = {*𝒞(4*[p], lambda x,_: 𝕁(𝕛(l[::-1]) for l in zip(*x.split(𝒏))))} # 90 rotations
    return X | {𝕁(l[::-1] for l in x.split(𝒏)) for x in X} # flips

# All pieces in all orientations
Z = {z for p in P for z in 𝑻(P[p])}

# Edges:
𝑬 = lambda p,i: [p[:10],p[9::11],p[-10:],p[0::11]][i]

# Match piece
𝙈 = lambda p,d: next((z for z in Z-𝑻(p) if 𝑬(z,(d+2)%4)==𝑬(p,d)), 0)

# get corners
K = [k for k in P if sum(not 𝙈(P[k], i) for i in range(4)) == 2]

import math
print('Part 1:', math.prod(K))

# get "Top left" corner:
p = next(p for p in 𝑻(P[K[0]]) if (𝙈(p,2) and 𝙈(p,3)))

# Develop line starting in edge d's direction:
𝑳 = lambda p,d: [*𝒞([p]+[d]*11, 𝙈)]

G = 𝕁( 𝕛(b[i:i+8] for b in B[::-1]) # remove left-right borders
    for B in [𝑳(a,3) for a in 𝑳(p,2)] # build top row, then all columns
    for i in range(d, 90, d-1) ) # remove top-bottom borders

import regex as re # need overlapping variant of findall
w = '[.#\n]{77}'
𝛹 = f'#.{w+"#....#"*3}##{w}.#{"..#"*5}' # Monster

for H in 𝑻(G):
    m = len(re.findall(𝛹,H,0,0,-1,1)) # overlapped = True
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
