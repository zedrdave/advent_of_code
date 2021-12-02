from utils import *
data = load_int_input(2)

lines = [line.split() for line in data.split('\n')]
cmds = [(cmd[0], int(val)) for cmd, val in lines]


def sum_cmds(l): return sum(val for cmd, val in cmds if cmd == l)


print('Part 1:', sum_cmds('f') * (sum_cmds('d') - sum_cmds('u')))

aim, horiz, depth = 0, 0, 0

for cmd, val in cmds:
    if cmd == 'f':
        horiz += val
        depth += aim*val
    else:
        aim += val if cmd == 'd' else -val

print('Part 2:', horiz * depth)
