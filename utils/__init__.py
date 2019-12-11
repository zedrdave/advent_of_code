import os
from collections import defaultdict
import numpy as np
import scipy.sparse

def loadCSVInput():
    import __main__
    inputFile = os.path.join(os.path.dirname(os.path.abspath(__main__.__file__)), 'input.txt')
    with open(inputFile) as f:
        data = [int(i.strip()) for i in f.read().split(',')]
    return data

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


def asciiPrint(bitmap, transpose=False):
    if type(bitmap) is defaultdict:
        bitmap = sparseToDense(bitmap)
    else:
        bitmap = np.array(bitmap)
    if transpose:
        bitmap = bitmap.transpose()
    if bitmap.shape[0] > 500 or bitmap.shape[1] > 500:
        raise(Exception(f"Bitmap too large to be printed: {np.array(bitmap).shape}"))
    print("\n".join(''.join([u"⬛️",u"⬜️"][int(i)] for i in line) for line in bitmap))
