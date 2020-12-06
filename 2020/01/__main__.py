from ..utils import *

data = load_int_input()

ans = next(x*y for i,x in enumerate(data) for y in data[(i+1):] if x+y == 2020)

print("Part 1:", ans)

ans = next(x*y*z for i,x in enumerate(data) for j,y in enumerate(data[(i+1):]) for z in data[(i+j+1):] if x+y+z == 2020)

print("Part 2:", ans)


##### Compact (less sturdy) form:

data = [int(i) for i in open('01/input.txt')]
print("Part 1:", next(x*y for x in data for y in data if x+y == 2020))
print("Part 2:", next(x*y*z for x in data for y in data for z in data if x+y+z == 2020))
