from aocd import get_data, submit

data = get_data(day=2, year=2022)

d = {'A': 0, 'B': 1, 'C': 2, 'X': 0, 'Y': 1, 'Z': 2}
turns = [[d[x] for x in l.split()] for l in data.split("\n")]

print("Part 1:", sum(b+1 + ((b+1-a)%3)*3 for a, b in turns))
print("Part 2:", sum((a+b-1)%3 + 1 + (b)*3 for a, b in turns))