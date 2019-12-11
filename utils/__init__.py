import os
import numpy as np

def loadCSVInput(curFile):
    inputFile = os.path.join(os.path.dirname(os.path.abspath(curFile)), 'input.txt')
    with open(inputFile) as f:
        data = [int(i.strip()) for i in f.read().split(',')]
    return data

def setVerbosity(level):
    os.environ['VERBOSE'] = str(int(level))

def dprint(*pargs, **kwargs):
    if int(os.environ.get('VERBOSE', 0)) > 0:
        print(*pargs, **kwargs)

def asciiPrint(bitmap):
    if len(bitmap) > 500 or len(bitmap[0]) > 100:
        raise(Exception(f"Bitmap too large to be printed: {np.array(bitmap).shape}"))
    print("\n".join(''.join([u"⬛️",u"⬜️"][int(i)] for i in line) for line in bitmap))
