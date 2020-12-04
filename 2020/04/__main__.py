import re

from ..utils import *

passports = [{f.split(':')[0]:f.split(':')[1] for f in l.split()}
             for l in open(input_file()).read().strip().split('\n\n')]

def check_year(y, f, t):
    return re.match('^\d{4}$', y) and f <= int(y) <= t

validators = {
    'byr': lambda x: check_year(x, 1920, 2002),
    'iyr': lambda x: check_year(x, 2010, 2020),
    'eyr': lambda x: check_year(x, 2020, 2030),
    'hgt': lambda x: (x.endswith('cm') and 150 <= int(x[:-2]) <= 193) or (x.endswith('in') and 59 <= int(x[:-2]) <= 76),
    'hcl': lambda x: re.match('^#[0-9a-f]{6}$', x),
    'ecl': lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
    'pid': lambda x: re.match('^\d{9}$', x),
    'cid': lambda x: True,
}

ans1 = sum([len(validators.keys() - p.keys() - set(['cid'])) == 0 for p in passports])

ans2 = sum([all(validator(p.get(k, '')) for k,validator in validators.items()) for p in passports])

print(f"Part 1: {ans1}\nPart 2: {ans2}")


###############################################
#
# Variant with functools.partial:
#
###############################################

from functools import partial

def check_year(f, t, y):
    return re.match('^\d{4}$', y) and f <= int(y) <= t

validators = {
    'byr': partial(check_year, 1920, 2002),
    'iyr': partial(check_year, 2010, 2020),
    'eyr': partial(check_year, 2020, 2030),
    'hgt': lambda x: (x.endswith('cm') and 150 <= int(x[:-2]) <= 193) or (x.endswith('in') and 59 <= int(x[:-2]) <= 76),
    'hcl': partial(re.match, '^#[0-9a-f]{6}$'),
    'ecl': lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
    'pid': partial(re.match, '^\d{9}$'),
    'cid': lambda x: True,
}

ans2 = sum([all(validator(p.get(k, '')) for k,validator in validators.items()) for p in passports])

print(f"Part 2 (using functools.partial): {ans2}")

###############################################
#
# Hardened version (will work on any values):
#
###############################################

ans2 = 0
for p in passports:
    try:
        if all(validator(p.get(k, '')) for k,validator in validators.items()):
            ans2 += 1
    except:
        print('Invalid format:', p)

print(f"Part 2 (with exception catching): {ans2}")
