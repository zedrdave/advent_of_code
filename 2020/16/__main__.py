from ..utils import *

import re
import math

rules, my_ticket, other_tickets = [g.split('\n') for g in open(input_file()).read().split('\n\n')]
my_ticket, *other_tickets = [[int(i) for i in l.split(',')] for l in (my_ticket[1:] + other_tickets[1:])]

rules = [re.split(':| or |-', r) for r in rules]
valid_dict = {field: set([*range(int(a),int(b)+1), *range(int(c),int(d)+1)]) for field,a,b,c,d in rules}

valid_set = set.union(*valid_dict.values())
print('Part 1:', sum(n for t in other_tickets for n in t if n not in valid_set))

valid_tickets = [t for t in other_tickets if all(n in valid_set for n in t)]

field_translate = {}

while len(valid_dict):
    for i in range(len(my_ticket)):
        fields = [n for n,r in valid_dict.items() if all(v[i] in r for v in valid_tickets)]
        if len(fields) == 1:
            field_translate[fields[0]] = i
            del valid_dict[fields[0]]

print('Part 2:', math.prod([my_ticket[field_translate[f]] for f in field_translate if f.startswith('dep')]))
