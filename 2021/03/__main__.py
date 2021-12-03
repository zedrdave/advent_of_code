from utils import *
data = load_int_input(3)

data = data.split('\n')

tots = [sum(1 for l in data if l[i] == '1') for i in range(len(data[0]))]


def fn(cmp): return int(''.join(str(int(cmp(i))) for i in tots), 2)


print('Part 1: ', fn(lambda x: x >= len(data)/2)
      * fn(lambda x: x < len(data)/2))

arr = data


def sieve(arr, fn):
    for i in range(len(arr[0])):
        tot = sum(1 for l in arr if l[i] == '1')
        bit_criteria = str(int(tot < len(arr)/2))
        arr = [l for l in arr if l[i] == bit_criteria]
        if len(arr) == 1:
            return int(arr[0], 2)


print('Part 2: ', sieve(data, lambda tot, arr: tot <= len(arr)/2)
      * sieve(data, lambda tot, arr: tot >= len(arr)/2))
