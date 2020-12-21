from ..utils import *

foods = [(set(i.split()), set(a.split(', ')))
            for i,a in [l.strip()[:-1].split(' (contains ')
                            for l in open(input_file())]]

allergens = set.union(*[a for _,a in foods])

possible = {a:set.intersection(*[ings for ings,alls in foods if a in alls]) for a in allergens}

all_possible = set.union(*possible.values())
print('Part 1:', sum(len(ings - all_possible) for ings,_ in foods))

confirmed = {}
while len(confirmed) < len(possible):
    a,i = next((k,v) for k,v in possible.items() if len(v) == 1)
    confirmed[a] = [*i][0]
    possible = {k:(v-i) for k,v in possible.items()}

print('Part 2:', ','.join(v for k,v in sorted(confirmed.items())))
