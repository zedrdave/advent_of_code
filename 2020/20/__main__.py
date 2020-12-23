from ..utils import *

P = {int(p[5:9]): p[11:] for p in open(input_file()).read().split('\n\n')}

edge = lambda p,i: [p[:10], p[9::11], p[-10:], p[0::11]][i]

flip = lambda p: '\n'.join(l[::-1] for l in p.split('\n'))
rot90 = lambda p: '\n'.join(''.join(l[::-1]) for l in zip(*p.split('\n'))) # rotate

def transform(p):
    A = [p]
    for _ in range(3):
        A += [rot90(A[-1])]
    A += [flip(a) for a in A]
    return A

Z = [z for p in P.values() for z in transform(p)]

def match(p, side):
    self = transform(p)
    for o in Z:
        if o not in self and edge(o, (side+2)%4) == edge(p, side):
            return o

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
X = 12 # puzzle size: int(len(P)**.5)

# Edges:
𝑬 = lambda p,i: [p[:10], p[9::11], p[-10:], p[0::11]][i]

# Transform
def 𝑻(p):
    A = [p]
    for _ in range(3):
        A += [𝕁(𝕛(𝕣(l)) for l in zip(*A[-1].split(nl)))] # Rotate
    A += [𝕁(𝕣(l) for l in a.split(nl)) for a in A] # Flip
    return {*A}

# All pieces in all orientations
Z = {z for p in P for z in 𝑻(P[p])}

# Matching piece
𝙈 = lambda p,d: next((z for z in Z-𝑻(p) if 𝑬(z,(d+2)%4)==𝑬(p,d)), 0)

# Corners
K = [k for k,v in P.items() if sum(not 𝙈(v, i) for i in range(4)) == 2]

import math
print('Part 1:', math.prod(K))

# "Top left" corner
p = next(p for p in 𝑻(P[K[0]]) if (𝙈(p,2) and 𝙈(p,3)))

# Develop line starting from p's edge d
def 𝑳(p,d):
    A = [p]
    for _ in range(X-1): A += [𝙈(A[-1], d)]
    return A

G = 𝕁( 𝕛(b[i:i+8] for b in 𝕣(B)) # remove left-right edges
       for B in [𝑳(a,3) for a in 𝑳(p,2)] # build top row, then all columns
       for i in range(X, 90, X-1) ) # remove top-bottom edges

import regex as re
w = '[.#\n]{77}'
𝛹 = f'#.{w+"#....#"*3}##{w}.#{"..#"*5}'
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
