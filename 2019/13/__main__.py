import sys
import copy

from collections import defaultdict
from ..intcode.VM import VM, NeedInputException
from ..utils import loadCSVInput, dprint, setVerbosity, sparseToDense, getChar, cmp
from ..graphics import asciiPrint, snapshot, saveAnimatedGIF


# Debug:
setVerbosity(False)

interactive = False # use True to play with keyboard
use_curses = False # Work in progress
printToScreen = True
saveAnimation = True

# Part 1

if not interactive: # Skip in interactive mode
    instructions = loadCSVInput()
    vm = VM(instructions)
    screen=defaultdict(int)

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

# Let's begin:

instructions = loadCSVInput()
instructions[0] = 2
vm = VM(instructions)
screen=defaultdict(int)
score = 0
game_started = False

if use_curses:
    from ..utils.curses import initCurses, cursesOutput, cleanCurses
    initCurses()

key_mapping = {44:-1, 46:1, 32:0}

while vm.is_running:
    try:
        x, y, id = next(vm.run()), next(vm.run()), next(vm.run())
        if x == -1 and y == 0:
            score = id
        else:
            screen[x,y] = id
            if id == 4 and game_started:
                snapshot(screen, False, saveAnimation)
    except StopIteration:
        print("###################\n     YOU WIN!\n\n Final Score:", score, "\n###################\n")
        break
    except NeedInputException:
            game_started = True
            if use_curses:
                cursesOutput(screen, header=f"[Score: {score}]\n")
            else:
                snapshot(screen, printToScreen, saveAnimation, reset=True, header=f"[Score: {score}]\n")

            if interactive:
                ch = getChar()
                dprint("Key pressed: ", ord(ch))
                if ord(ch) in key_mapping:
                    vm.input = [key_mapping[ord(ch)]]
                else:
                    break
            else:
                paddle = [x for x,v in screen.items() if v == 3][0][0]
                num_moves, next_ball_x = look_ahead(vm)
                dprint(f"Paddle: {paddle} | Ball (in {num_moves}): {next_ball_x}")
                dist = abs(paddle-next_ball_x)
                vm.input = [cmp(next_ball_x, paddle)]*dist + [0]*(num_moves-dist)
                dprint("Next moves: ", vm.input)

if use_curses:
    cleanCurses()

print("Part 2 - Final score: ", score)

if saveAnimation:
    saveAnimatedGIF(freq=1, duration=5)

# if save_animation:
#     print("Saving animation…")
#     from PIL import Image
#     palette = [0, 0, 0,  #black
#         211, 223, 223, #white
#         229, 39,  39,  #red
#         244, 214, 17,  #yellow
#         30, 30, 255,  #blue
#     ] + [0]*(768 - 5*3)
#     palette = palette + [0]*(768-len(palette))
#     rescale = lambda img: img.resize((img.size[0]*15,img.size[1]*15))
#     images = (rescale(Image.fromarray(sparseToDense(frame).transpose().astype('uint8'), 'P')) for frame in frames)
#     next(images).save('animation.gif', save_all=True, append_images=images, duration=20, loop=0, palette=palette, optimize=True)
