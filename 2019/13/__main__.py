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
    bak_mem = copy.deepcopy(vm.mem)
    bak_RB = vm.RB
    bak_IP = vm.IP

    # ball = [x for x,v in screen.items() if v == 4][0]
    ball = (0,0)
    while vm.is_running:
        try:
            x = next(vm.run(0))
            y = next(vm.run())
            id = next(vm.run())
            if id == 4 and y == 17:
                ball = (x,y)
                break
        except StopIteration:
            break
    vm.mem = bak_mem
    vm.RB = bak_RB
    vm.IP = bak_IP
    return ball

instructions = loadCSVInput()

score = 0
input_key = None
instructions[0] = 2
brick_count = None

vm = VM(instructions)
screen=defaultdict(int)
auto_pilot = True

while vm.is_running:
    try:
        x = next(vm.run(input_key))
        y = next(vm.run())
        id = next(vm.run())
        if x == -1 and y == 0:
            score = id
        else:
            screen[x,y] = id
        input_key = None
    except StopIteration:
        print("################\n     YOU WIN!\n\n  Final Score:", score, "\n################\n")
        break
    except NeedInputException:
        print(f"[Score: {score}]")
        asciiPrint(screen, transpose=True)
        if auto_pilot:
            paddle = [x for x,v in screen.items() if v == 3][0][0]
            ball = [x for x,v in screen.items() if v == 4][0]
            if ball[1] == 17:
                next_ball = ball[0]
            else:
                next_ball = look_ahead(vm)[0]
            dprint(f"Paddle: {paddle} | Ball: {ball} -> {next_ball}")
            if paddle < next_ball:
                move = 1
            elif paddle > next_ball:
                move = -1
            else:
                move = 0
            dprint("Move paddle: ", move)
            input_key = move
        else:
            input_key = getch()
            dprint("key press: ", ord(input_key))
            if ord(input_key) == 44:
                input_key = -1
            elif ord(input_key) == 46:
                input_key = 1
            elif ord(input_key) == 32:
                input_key = 0
            else:
                break

# Disassembly:
#  Score stored at: 386
#  Incrementer stored at: 435
#  Uses RB [2403+1] to increment

print("Part 2 - Final score: ", score)
