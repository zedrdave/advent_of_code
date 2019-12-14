import numpy as np
xmin = 273025
xmax = 767253

count = 0
for x in range(xmin, xmax+1):
    s = [int(d) for d in str(x)]
    s.insert(0, 0)
    s = np.array(s)
    s = np.sign(s[1:] - s[:-1])
    if any(s < 0) or all(s > 0):
        continue
    count += 1

print("Part 1 - ", count)

count = 0
for x in range(xmin, xmax+1):
    s = [int(d) for d in str(x)]
    s.insert(0, 0)
    s = np.array(s)
    s = np.sign(s[1:] - s[:-1])
    if any(s < 0) or all(s > 0):
        continue
    s2 = np.append(s, 1)
    for i in range(0, len(s2-3)):
        if np.array_equal(s2[i:(i+3)], [1,0,1]):
            count += 1
            break

print("Part 2 - ", count)
