import sys
import numpy as np
from collections import defaultdict
from ..intcode.VM import VM, NeedInputException
from ..utils import loadCSVInput, dprint, asciiPrint, setVerbosity, sparseToDense

# Debug:
setVerbosity(False)

# Part 1

instructions = loadCSVInput()
screen=defaultdict(int)
vm = VM(instructions)

while vm.is_running:
    try:
        for x,y,id in zip(*[iter(vm.run())]*3):
            screen[x,y] = id
    except StopIteration:
        break

screen = sparseToDense(screen)
asciiPrint(screen, transpose=True)
print("Part 1 - total number of block tiles: ", sum(sum(screen == 2)))

# Part 2

import tty, termios
import copy

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def look_ahead(vm):
    temp_vm = copy.deepcopy(vm)

    ball_x = 0
    ball_moves = 1
    temp_vm.input = [0]
    for x,y,id in zip(*[iter(temp_vm.run())]*3):
        temp_vm.input = [0]
        if id == 4:
            ball_moves += 1
            if y == 17:
                ball_x = x
                break

    return (ball_moves, ball_x)

cmp = lambda a,b: (a > b) - (a < b)


# Let's begin:
demo_mode = True

instructions = loadCSVInput()
instructions[0] = 2
vm = VM(instructions)

score = 0
screen=defaultdict(int)

key_mapping = {44:-1, 46:1, 32:0}

while vm.is_running:
    try:
        x, y, id = next(vm.run()), next(vm.run()), next(vm.run())
        if x == -1 and y == 0:
            score = id
            print(f"[Score: {score}]")
        else:
            screen[x,y] = id
    except StopIteration:
        print("###################\n     YOU WIN!\n\n Final Score:", score, "\n###################\n")
        break
    except NeedInputException:
            asciiPrint(screen, transpose=True)
            if demo_mode:
                paddle = [x for x,v in screen.items() if v == 3][0][0]
                num_moves, next_ball_x = look_ahead(vm)
                dprint(f"Paddle: {paddle} | Ball (in {num_moves}): {next_ball_x}")
                dist = abs(paddle-next_ball_x)
                vm.input = [cmp(next_ball_x, paddle)]*dist + [0]*(num_moves-dist)
                dprint("Next moves: ", vm.input)
            else:
                ch = getch()
                dprint("Key pressed: ", ord(ch))
                if ord(ch) in key_mapping:
                    vm.input = [key_mapping[ord(ch)]]
                else:
                    break

# Disassembly:
#  Score stored at: 386
#  Incrementer stored at: 435
#  Uses RB [2403+1] to increment

print("Part 2 - Final score: ", score)
