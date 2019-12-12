with open('input.txt') as f:
    d = [int(n) for n in f.read().split(',')]

d[1] = 12
d[2] = 2
ip = 0
while d[ip] != 99:
    if d[ip] == 1:
        val = d[d[ip+1]] + d[d[ip+2]]
    elif d[ip] == 2:
        val = d[d[ip+1]] * d[d[ip+2]]
    else:
        print("error")
        break
    d[d[ip+3]] = val
    ip += 4

print(f"Final state d[0]: {d[0]}")
# 5098658
