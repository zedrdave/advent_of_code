from collections import defaultdict
import curses
import numpy as np
from . import sparseToDense



def initCurses():
    global win, stdscr
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    win = curses.newwin(40, 80, 0, 0)

def cursesOutput(bitmap, transpose=False, reset=True, header=""):
    global win
    if type(bitmap) is defaultdict:
        bitmap = sparseToDense(bitmap)
    else:
        bitmap = np.array(bitmap)
    if transpose:
        bitmap = bitmap.transpose()
    win.addstr(0,0, header)
    for l,line in enumerate(bitmap):
        win.addstr(l+2, 0, (''.join([" ","█","🝙","▄","●"][int(i)] for i in line)))
    win.refresh()

def cleanCurses():
    global stdscr
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
