import os
import tty
import termios
import sys
from collections import defaultdict
import numpy as np
import scipy.sparse

cmp = lambda a,b: (a > b) - (a < b)

def inputFile(file = 'input.txt'):
    import __main__
    return os.path.join(os.path.dirname(os.path.abspath(__main__.__file__)), file)

def loadCSVInput():
    with open(inputFile()) as f:
        return [int(i.strip()) for i in f.read().split(',')]

def loadXYZInput():
    with open(inputFile()) as f:
        return [[int(pos[2:]) for pos in l.strip()[1:-1].split(', ')] for l in f]

def setVerbosity(level):
    os.environ['VERBOSE'] = str(int(level))

def isVerbose():
    return int(os.environ.get('VERBOSE', 0)) > 0

def dprint(*pargs, **kwargs):
    if isVerbose():
        print(*pargs, **kwargs)

def sparseToDense(bitmap):
    items = list(bitmap.items())
    vs = [v for (i,j), v in items]
    ii = [i for (i,j), v in items]
    min_ii = min(ii)
    ii = [i-min_ii for i in ii] # avoid negative indices
    jj = [j for (i,j), v in items]
    min_jj = min(jj)
    jj = [i-min_jj for i in jj] # avoid negative indices
    return scipy.sparse.csr_matrix((vs, (ii, jj))).toarray()


def getChar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
