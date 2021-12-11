import numpy as np

with open('input.txt', 'r') as f:
    data = f.read().split('\n')

pairs = {'(': ')', '[': ']', '<': '>', '{': '}'}
scoring_1 = {')': 3, ']': 57, '}': 1197, '>': 25137}
score_1 = 0
scoring_2 = '([{<'
scores_2 = []

for line in data:
    stack = []
    for c in line:
        if c in pairs.keys():
            stack.append(c)
        elif c != pairs[stack.pop()]:
            score_1 += scoring_1[c]
            stack = []
            break
    if len(stack):
        score_2 = 0
        for s in (scoring_2.index(c) + 1 for c in reversed(stack)):
            score_2 = score_2*5 + s
        scores_2 += [score_2]

print('Part 1:', score_1)
print('Part 2:', int(np.median(scores_2)))

# 318081
# 4361305341
