from ..utils import inputFile

with open(inputFile()) as f:
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

print(f"Part 1 - Final state d[0]: {d[0]}")
# 5098658

# Part 2:

def search(target):
    for noun in range(0, 100):
        for verb in range(0, 100):
            with open(inputFile()) as f:
                d = [int(n) for n in f.read().split(',')]
            d[1] = noun
            d[2] = verb
            ip = 0
            while d[ip] != 99:
                if d[ip] == 1:
                    val = d[d[ip+1]] + d[d[ip+2]]
                elif d[ip] == 2:
                    val = d[d[ip+1]] * d[d[ip+2]]
                else:
                    break
                d[d[ip+3]] = val
                ip += 4
            if d[0] == target:
                return(noun, verb)
    return false

res = search(19690720)
if res:
    print(f"Part 2 - {res} -> {res[0] * 100 + res[1]}")

# 5098658
