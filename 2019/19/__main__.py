# import copy
import numpy as np
import math

from ..utils import loadCSVInput, dprint, setVerbosity, inputFile
from ..intcode.VM import VM


arr2str = lambda a: '\n'.join([''.join([str(c) for c in line]) for line in a])

instructions = loadCSVInput()

def getReading(i,j):
    vm = VM(instructions)
    vm.input = [i,j]
    return int(next(vm.run()))

# Part 1:
arr = np.zeros((50,50), 'int8')
for i,j in np.ndindex(arr.shape):
    arr[i,j] = getReading(i,j)
print(arr2str(arr))
print("Part 1:", np.count_nonzero(arr))


## Optional: caching…
# dim = 1200
# i = 0
# j = 0
# firstJ = 0
# lastJ = 0
# arr = np.zeros((dim,dim), 'bool')
# while i < dim:
#     if i%100 == 0:
#         print(i, j)
#     while not getReading(i, j) and j < min(dim, i*10):
#         j += 1
#     if j < min(dim, i*10):
#         firstJ = j
#     for j in range(j, lastJ):
#         arr[i,j] = True
#     while getReading(i, j) and j < dim:
#         arr[i, j] = True
#         j += 1
#         lastJ = j
#     i += 1
#     j = firstJ


# Part 2

i = j = 0
while not getReading(i+99, j):
    j += 1
    while not getReading(i, j+99):
        i += 1
dprint("4 corners:", getReading(i,j), getReading(i+99, j), getReading(i, j+99), getReading(i+99, j+99))
print("Part 2: ", i*10000 + j)


# Visualisation
#
# from PIL import Image, ImageDraw, ImageFont
#
# origFrame = arr.astype('uint8')
#
# palette = [0, 0, 0,  #black
#     211, 223, 223, #white
#     229, 39,  39,  #red
#     244, 214, 17,  #yellow
#     30, 30, 255,  #blue
# ] + [0]*(768 - 5*3)
# palette = palette + [0]*(768-len(palette))
#
#
# lastX = 0
# lastY = 0
# def computeFrame(origFrame, dim):
#     global lastX, lastY, palette
#     print("frame: ", dim)
#     x = lastX
#     y = lastY
#     while not getReading(x+dim-1, y):
#         y += 1
#         while not getReading(x, y+dim-1):
#             x += 1
#     lastX = x-1
#     lastY = y-1
#     # frame = copy.deepcopy(origFrame)
#     img = Image.fromarray(origFrame, 'P')
#     d = ImageDraw.Draw(img)
#     font = ImageFont.truetype("Arial", max(dim-2, 5))
#     d.rectangle((y,x,y+dim,x+dim), outline=2, fill=2)
#     w, h = d.textsize(str(dim), font=font)
#     d.text((y+(dim-w)/2,x+(dim-h)/2), str(dim), font=font, fill=1)
#     return img
#
# images = (computeFrame(origFrame, dim) for dim in range(3, 101))
# Image.fromarray(origFrame, 'P').save(
#     'animated.gif',
#     save_all=True,
#     append_images=images,
#     duration=100,
#     loop=0,
#     optimize=True,
#     palette=palette
# )
#
