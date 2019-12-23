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
    instructions = loadCSVInput('input_harold.txt')
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

bottomY = screen.shape[1]
dprint("Using screen height: ", bottomY)

# Part 2

def look_ahead(vm, moves = [0], bounces = 0):
    temp_vm = copy.deepcopy(vm)
    ball_x = -1
    ball_moves = 1
    bricks = 0
    temp_vm.input = list(moves)
    for x,y,id in zip(*[iter(temp_vm.run())]*3):
        temp_vm.input += [0]
        if x == -1 and y == 0 and id > 0: # hackish way to know a brick was hit
            bricks += 1
        elif id == 4:
            ball_moves += 1
            if y == bottomY - 3:
                if bounces:
                    bounces -= 1
                else:
                    ball_x = x
                    break

    return (ball_moves, ball_x, bricks)

# Let's begin:

instructions = loadCSVInput('input_harold.txt')
instructions[0] = 2
vm = VM(instructions)
screen=defaultdict(int)
score = 0
game_started = False

if use_curses:
    from ..utils.curses import initCurses, cursesOutput, cleanCurses
    initCurses()

key_mapping = {44:-1, 46:1, 32:0}


# def recurSolve(thisVm, movesSoFar):
#     ball_moves, ball_x, _ = look_ahead(thisVm)
#
#     return movesSoFar + ball_moves



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
            if use_curses:
                cursesOutput(screen, header=f"[Score: {score}]\n")
            else:
                snapshot(screen, printToScreen or interactive, saveAnimation, reset=True, header=f"[Score: {score}]\n")

            if interactive:
                ch = getChar()
                dprint("Key pressed: ", ord(ch))
                if ord(ch) in key_mapping:
                    vm.input = [key_mapping[ord(ch)]]
                else:
                    break
            else:
                paddle_x = [x for x,v in screen.items() if v == 3][0][0]
                num_moves, next_ball_x, _ = look_ahead(vm)
                # assert next_ball_x >= 0, "No winning move"
                print(f"Paddle: {paddle_x} | Ball (in {num_moves}): {next_ball_x} | dist: {abs(paddle_x-next_ball_x)}")
                best_moves = None
                if game_started:
                    best_bricks = 0
                    for target in [next_ball_x,next_ball_x-1,next_ball_x+1]:
                        dist = abs(paddle_x-target)
                        moves = ([cmp(target, paddle_x)] * dist + [0]*(num_moves-dist))[:num_moves]
                        nn_moves, nn_ball_x, bricks = look_ahead(vm, moves=moves, bounces=1)
                        print(f"Paddle: {paddle_x} | Ball (in {nn_moves}): {nn_ball_x} | dist: {abs(paddle_x-nn_ball_x)}")

                        if nn_ball_x >= 0 and bricks > best_bricks and (nn_moves - num_moves) >= abs(nn_ball_x-target):
                            best_bricks = bricks
                            best_moves  = moves
                if best_moves is None:
                    dist = abs(paddle_x-next_ball_x)
                    best_moves = [cmp(next_ball_x, paddle_x)] * dist + [0]*(num_moves-dist)

                vm.input = best_moves
                dprint("Next moves: ", vm.input)

            game_started = True


if use_curses:
    cleanCurses()

print("Part 2 - Final score: ", score)

if saveAnimation:
    saveAnimatedGIF(tileSize = 15, duration=1)
