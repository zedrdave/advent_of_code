from aocd import get_data

day = 13
year = 2022
data = get_data(day=day, year=year)


packets = [[eval(x) for x in l.split('\n')] for l in data.split("\n\n")]

cmp = lambda a, b: (a < b) - (a > b)


def is_ordered(l, r):
    l_i, r_i = isinstance(l, int), isinstance(r, int)
    if l_i and r_i:
        return cmp(l, r)
    if l_i:
        l = [l]
    if r_i:
        r = [r]

    arr = (is_ordered(a, b) for a, b in zip(l, r))
    return next((o for o in arr if o != 0), cmp(len(l), len(r)))


print("Part 1:", sum(i + 1 for i, p in enumerate(packets) if is_ordered(*p) > 0))

dividers = [[[2]], [[6]]]
sorted_packets = sorted([p for pair in packets for p in pair] + dividers,
                        key=cmp_to_key(is_ordered), reverse=True)

from functools import cmp_to_key  # noqa

d1, d2 = [i + 1 for i, p in enumerate(sorted_packets) if p in dividers]
print("Part 2:", d1 * d2)


# print("Using Python 3.10 (match/case):")

# from functools import cmp_to_key

# packets = [[eval(x) for x in l.split('\n')] for l in data.split("\n\n")]

# cmp = lambda a,b: (a < b) - (a > b)

# def is_ordered(l, r):
#     match l, r:
#         case int(), int():
#             return cmp(l, r)
#         case int(), list():
#             l = [l]
#         case list(), int():
#             r = [r]
#     arr = (is_ordered(a, b) for a,b in zip(l,r))
#     return next((o for o in arr if o != 0), cmp(len(l), len(r)))

# print("Part 1:", sum(i+1 for i,p in enumerate(packets) if is_ordered(*p) > 0))

# dividers = [[[2]], [[6]]]
# sorted_packets = sorted([p for pair in packets for p in pair] + dividers,
#                         key=cmp_to_key(is_ordered), reverse=True)

# d1, d2 = [i+1 for i,p in enumerate(sorted_packets) if p in dividers]
# print("Part 2:", d1*d2)
