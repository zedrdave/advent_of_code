from aocd import get_data, submit

data = get_data(day=1, year=2022)

cals = sorted(sum(map(int, l.split("\n"))) for l in data.split("\n\n"))
print("part 1:", cals[-1])
print("part 2:", sum(cals[-3:]))
