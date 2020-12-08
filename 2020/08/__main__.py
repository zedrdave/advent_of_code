from ..utils import input_file

𝓟 = [(l[:3], int(l[4:])) for l in open(input_file())]

def run(P, IP = 0):
    𝒜 = 0
    ℮ = set()
    while 0 <= IP < len(P):
        ℮.add(IP)
        𝒾, a = P[IP]
        if 𝒾 == 'jmp':
            IP += a-1
        if 𝒾 == 'acc':
            𝒜 += a
        IP += 1
        if IP in ℮:
            return False, 𝒜

    return IP == len(P), 𝒜

print('Part 1', run(𝓟)[1])

for l,(𝒾,a) in enumerate(𝓟):
    if 𝒾 == 'jmp':
        𝒾 = 'nop'
    elif 𝒾 == 'nop':
        𝒾 = 'jmp'
    b,𝒜 = run(𝓟[:l] + [(𝒾,a)] + 𝓟[l+1:])
    if b:
        break

print('Part 2', 𝒜)
