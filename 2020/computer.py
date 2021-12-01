code = [(l[:3], [int(i) for i in l[4:].split()]) for l in open('08/input.txt')]

def run(prog, IP = 0):
    acc = 0
    steps = []

    while 0 <= IP < len(prog):
        steps += [IP]
        cmd, (p1,) = prog[IP]

        if cmd == 'jmp':
            IP += p1
        elif cmd == 'acc':
            acc += p1
            IP += 1
        elif cmd == 'nop':
            IP += 1

        if IP in steps:
            return False, acc

    return IP == len(prog), acc

print('Part 1', run(code)[1])

# for l,(𝒾,a) in enumerate(code):
#     if 𝒾 == 'jmp':
#         𝒾 = 'nop'
#     elif 𝒾 == 'nop':
#         𝒾 = 'jmp'
#     b, 𝒜 = run(code[:l] + [(𝒾,a)] + code[l+1:])
#     if b:
#         break
#
# print('Part 2', 𝒜)
