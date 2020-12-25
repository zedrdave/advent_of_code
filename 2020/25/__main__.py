from ..utils import *

p1,p2 = [int(l) for l in open(input_file())]
def 𝓔(n, pk=0, l=-1):
    i,c = 0,1
    while True:
        c = (c*n) % 20201227
        if c == pk: return i
        elif i == l: return c
    i += 1
l1,l2 = 𝓔(7,p1),𝓔(7,p2)
assert 𝓔(p1,l=l2) == 𝓔(p1,l=l1)

print('⭐️ Merry Christmas ⭐️', 𝓔(p1, l=l2))
