import sys
import numpy as np
from collections import defaultdict
from ..intcode.VM import VM, NeedInputException
from ..utils import loadCSVInput, dprint, asciiPrint, setVerbosity, sparseToDense

# Debug:
setVerbosity(True)

instructions = loadCSVInput()
# screen=defaultdict(int)
# vm = VM(instructions)
#
# while vm.is_running:
#     try:
#         for x,y,id in zip(*[iter(vm.run())]*3):
#             screen[x,y] = id
#     except StopIteration:
#         break
#
# screen = sparseToDense(screen)
# asciiPrint(screen, transpose=True)
# print("Part 1 - block tiles: ", sum(sum(screen == 2)))

# Part 2:

# import curses, time
#
# def input_char(message):
#     try:
#         win = curses.initscr()
#         win.addstr(0, 0, message)
#         while True:
#             ch = win.getch()
#             if ch in range(32, 127): break
#             time.sleep(0.05)
#     except: raise
#     finally:
#         curses.endwin()
#     return chr(ch)

instructions = loadCSVInput()
instructions[0] = 2
vm = VM(instructions)
screen=defaultdict(int)

import tty, termios
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

input_key = None
scores = [0,0]
brick_totals = [0,0]

while vm.is_running:
    try:
        if input_key is not None:
            x = next(vm.run(input_key))
            y = next(vm.run())
            id = next(vm.run())
            input_key = None
            if x == -1 and y == 0:
                scores += [id]
                brick_totals += [sum(sum(sparseToDense(screen) == 2))]
            else:
                screen[x,y] = id
        for x,y,id in zip(*[iter(vm.run())]*3):
            if x == -1 and y == 0:
                scores += [id]
                brick_totals += [sum(sum(sparseToDense(screen) == 2))]
            else:
                screen[x,y] = id
    except StopIteration:
        break
    except NeedInputException:
        print(f"*** Score: {scores[-1]} *** ({scores[-1]-scores[-2]})")
        asciiPrint(screen, transpose=True)
        input_key = getch()
        print("**input**:", ord(input_key))
        if ord(input_key) == 44:
            input_key = -1
        elif ord(input_key) == 46:
            input_key = 1
        elif ord(input_key) == 32:
            input_key = 0
        else:
            break
    except Exception as e:
        print(e)
        sys.exit()

# Score stored at: 386
# Incrementer stored at: 435
# Uses RB [2403+1] to increment

print(scores)
print(brick_totals)
diff_scores = [x-y for x,y in zip(scores[1:],scores[:-1])]
diff_bricks = [y-x for x,y in zip(brick_totals[1:],brick_totals[:-1])]
print(diff_scores)
print(diff_bricks)
# score_per_brick = [x/y for x,y in zip(diff_scores,diff_bricks) if y != 0]
# print(score_per_brick)
# screen = sparseToDense(screen)
# asciiPrint(screen, transpose=True)
# print("Part 1 - block tiles: ", sum(sum(screen == 2)))
