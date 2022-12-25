
from aocd import get_data, submit

day = 25
year = 2022
data = get_data(day=day, year=year)


def snafu_to_dec(n):
    tot = 0
    for d in n:
        tot = tot * 5 + ({'=': -2, '-': -1}.get(d, 0) or int(d))
    return tot


def dec_to_snafu(n):

    r = n
    s = []
    while r:
        s += [r % 5]
        r //= 5

    for i in range(len(s)):
        if s[i] >= 3:
            if s[i] == 3:
                s[i] = '='
            elif s[i] == 4:
                s[i] = '-'
            else:
                s[i] = 0

            if i + 1 < len(s):
                s[i + 1] += 1
            else:
                s += [1]

    return "".join(f"{i}" for i in reversed(s))


dec_to_snafu(sum(snafu_to_dec(n) for n in data.split('\n')))
