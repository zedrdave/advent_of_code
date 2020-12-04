import re

from ..utils import *

lines = ' '.join([l.strip() if l != '\n' else l for l in open(input_file())])

passports = [{f.split(':')[0]:f.split(':')[1] for f in l.strip().split()} for l in lines.split('\n')]

def check_year(y, f, t):
    return re.match('^\d{4}$', y) and f <= int(y) <= t

validators = {
    'byr': lambda x: check_year(x, 1920, 2002),
    'iyr': lambda x: check_year(x, 2010, 2020),
    'eyr': lambda x: check_year(x, 2020, 2030),
    'hgt': lambda x: (x.endswith('cm') and 150 <= int(x[:-2]) <= 193) or (x.endswith('in') and 59 <= int(x[:-2]) <= 76),
    'hcl': lambda x: re.match('^#[0-9a-f]{6}$', x),
    'ecl': lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
    'pid': lambda x: re.match('^\d{9,9}$', x),
    'cid': lambda x: True,
}

ans1 = sum([len(validators.keys() - p.keys() - set(['cid'])) == 0 for p in passports])

ans2 = sum([all(validator(p.get(k, '')) for k,validator in validators.items()) for p in passports])

print(f"Part 1: {ans1}\nPart 2: {ans2}")


# Hardened version:
ans2 = 0
for p in passports:
    try:
        if all(validator(p.get(k, '')) for k,validator in validators.items()):
            ans2 += 1
    except:
        print('Invalid format:', p)
