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
