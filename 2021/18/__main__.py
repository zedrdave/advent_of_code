import re
import math
from collections import Counter


def explode(line):
    m = None
    for m in re.finditer(r"\[(\d*),(\d*)\]", line):
        counts = Counter(line[:m.span()[1]])
        if counts['['] - counts[']'] >= 4:
            break
        else:
            m = None

    if not m:
        return None

    a, b = m.groups()
    left = line[0:m.span()[0]]
    right = line[m.span()[1]:]

    m = re.search(r"(.*[^\d])(\d+)([^\d]*)", left)
    if m:
        l1, l2, l3 = m.groups()
        left = l1 + str(int(l2) + int(a)) + l3

    m = re.search(r"([^\d]*)(\d+)([^\d].*)", right)
    if m:
        r1, r2, r3 = m.groups()
        right = r1 + str(int(r2) + int(b)) + r3

    return left + '0' + right


def split(line):
    m = re.search(r"\d\d", line)
    if not m:
        return None
    num = int(m.group())
    return (line[0:m.span()[0]]
            + f"[{math.floor(num/2)},{math.ceil(num/2)}]"
            + line[m.span()[1]:])


def reduce(line):
    while True:
        new_line = explode(line)
        if new_line is None:
            new_line = split(line)
        if new_line is None:
            break
        line = new_line
    return line


def magnitude(num):
    try:
        return int(num)
    except:
        num = num[1:-1]
        pars = 0
        for midsep in range(0, len(num)):
            if num[midsep] == ',' and pars == 0:
                break
            if num[midsep] == '[':
                pars += 1
            elif num[midsep] == ']':
                pars -= 1
        return 3*magnitude(num[:midsep]) + 2*magnitude(num[(midsep+1):])


def process(lines):
    num, *lines = lines

    while len(lines):
        line, *lines = lines
        num = reduce(f"[{num},{line}]")

    return num


with open('18/input.txt', 'r') as f:
    data = f.read()

lines = data.split('\n')

print('Part 1:', magnitude(process(lines)))

max_magnitude = 0
for left in lines:
    for right in lines:
        max_magnitude = max(max_magnitude, magnitude(process([left, right])))

print('Part 2:', max_magnitude)
