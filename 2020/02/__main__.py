from ..utils import *
import re

lines = [re.split('[: \-]', l) for l in open(input_file())]

lines = [(int(p1), int(p2), [c == ch for c in pwd]) for p1, p2, ch, _, pwd in lines]

ans = sum(n1 <= sum(matches) <= n2 for n1, n2, matches in lines)
print("Part 1:", ans)

ans = sum(matches[p1-1] ^ matches[p2-1] for p1, p2, matches in lines)
print("Part 2:", ans)
