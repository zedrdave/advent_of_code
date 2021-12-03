from utils import *
data = load_int_input(3)

data = data.split('\n')

bits = [sum(1 for l in data if l[i] == '1') >
        len(data)/2 for i in range(len(data[0]))]


def count(most): return sum((b ^ most) * 2 **
                            i for (i, b) in enumerate(reversed(bits)))


print('Part 1:', count(True)*count(False))


def sieve(most):
    arr = data
    for i in range(len(arr[0])):
        bit_criteria = (
            sum(1 for l in arr if l[i] == '1') >= len(arr)/2) ^ most
        arr = [l for l in arr if int(l[i]) == bit_criteria]

        if len(arr) == 1:
            return int(arr[0], 2)


print('Part 2: ', sieve(True) * sieve(False))
