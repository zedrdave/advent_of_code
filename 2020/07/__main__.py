from ..utils import input_file

from collections import Counter

# List of first-level bag contents:
ℬ = {
    a+b: Counter({
        x+y: int(n)
        for n,x,y in zip(r[::4], r[1::4], r[2::4]) if n != 'no'
    })
    for a,b,_,_,*r in [l.split() for l in open(input_file())]
}

ℱ = {} # Cache
def bags_in(b, n=1):
    if b not in ℱ:
         ℱ[b] = sum([bags_in(*x) for x in ℬ[b].items()], ℬ[b])
    return Counter({c: ℱ[b][c]*n for c in ℱ[b]})

print(
    'Pt1', sum('shinygold' in bags_in(b) for b in ℬ),
    '\nPt2', sum(bags_in('shinygold').values())
)
