from utils import *
data = load_int_input(3)
draws, *boards = data.split('\n\n')

draws = [int(i) for i in draws.split(',')]
boards = [[[int(i) for i in line.split()]
           for line in board.split('\n')] for board in boards]


def applyDraw(board, draw):
    return [['x' if i == draw else i for i in line] for line in board]


def hasWon(board):
    return (any(all(i == 'x' for i in line) for line in board) or
            any(all(line[idx] == 'x' for line in board) for idx in range(len(board[0]))))


def score(board, draw):
    return sum(sum(i for i in line if i != 'x') for line in board) * draw


firstWon = False
for draw in draws:
    boards = [applyDraw(board, draw) for board in boards]

    if next((board for board in boards if hasWon(board)), False):
        if not firstWon:
            print('Part 1:', score(won, draw))
            firstWon = True
        elif len(boards) == 1:
            print('Part 2:', score(boards[0], draw))
