from aocd import get_data, submit
import numpy as np

day = 11
year = 2022
data = get_data(day=day, year=year)


def solve(blocks, tot_rounds, extra_op=''):
    monkeys = [([int(i) for i in start.split(", ")],        # Object list
                op_str.split(' = ')[1],                     # Operation str
                [int(t.split()[-1]) for t in test_args])    # Test args
               for start, op_str, *test_args in blocks]

    # Perform all operations modulo [prod of all test values]:
    extra_op += f" % {np.prod([m[2][0] for m in monkeys])}"

    def op(op_str, old): return eval(f"({op_str}){extra_op}")
    def test(div_by, t, f, val): return f if val % div_by else t

    inspections = [0]*len(monkeys)

    for _ in range(tot_rounds):
        for i, (objects, op_str, test_args) in enumerate(monkeys):
            inspections[i] += len(objects)
            for obj in objects:
                obj = op(op_str, obj)
                monkeys[test(*test_args, obj)][0].append(obj)
            objects[:] = []

    return np.prod(sorted(inspections)[-2:])


blocks = [[l.split(': ')[1]
           for l in block.split("\n")[1:]] for block in data.split("\n\n")]

print("Part 1:", solve(blocks, tot_rounds=20, extra_op=' // 3'))
print("Part 2:", solve(blocks, tot_rounds=10000))
