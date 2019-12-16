import sys
import copy
import numpy as np
from PIL import Image
from collections import defaultdict

from ..utils import sparseToDense

frames = []

def snapshot(sparseDict, printToScreen = True, saveAnimation = False, update = {}, **kwargs):
    if not printToScreen and not saveAnimation:
        return
    frame = copy.copy(sparseDict)
    frame.update(update)
    if saveAnimation:
        global frames
        frames += [frame]
    if printToScreen:
        asciiPrint(frame, transpose = True, **kwargs)


def asciiPrint(bitmap, transpose=False, reset=False, header=""):
    if type(bitmap) is defaultdict:
        bitmap = sparseToDense(bitmap)
    else:
        bitmap = np.array(bitmap)
    if transpose:
        bitmap = bitmap.transpose()
    if bitmap.shape[0] > 500 or bitmap.shape[1] > 500:
        raise(Exception(f"Bitmap too large to be printed: {np.array(bitmap).shape}"))
    if reset:
        print(chr(27) + "[2J", flush=False)
    print(header, flush=False)
    print("\n".join(''.join([u"⬛️",u"⬜️",u"🟥",u"🟨", u"🔵",u"🟦",u"🤖"][int(i)] for i in line) for line in bitmap), flush=False)
    sys.stdout.flush()

def saveAnimatedGIF(tileSize = 10, outputFile = 'animation.gif', freq = 1, duration = 10):
    global frames
    if len(frames) == 0:
        return

    print(f"Saving animation ({len(frames)} frames)…")
    tiles = [Image.open(f'2019/15/tiles/{i}.png').resize((tileSize,)*2) for i in range(7)]

    dims = sparseToDense(frames[-1]).shape
    minY = min(y for _,y in frames[-1])
    minX = min(x for x,_ in frames[-1])

    def frameToImage(frame, i):
        img = Image.new('RGBA', (dims[0]*tileSize, dims[1]*tileSize), 'black')
        for (y,x),v in frame.items():
            img.paste(tiles[v], ((y - minY)*tileSize, (x - minX)*tileSize))
        print(f"saved: {i}/{len(frames)}", end="\r")
        return img.convert('P', palette=Image.ADAPTIVE)

    images = (frameToImage(f,i) for i,f in enumerate(frames) if i%freq == 0)
    next(images).save(
        outputFile,
        save_all=True,
        append_images=images,
        duration=duration,
        loop=0,
        optimize=True
    )
