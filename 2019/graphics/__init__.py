import sys
import copy
import numpy as np
from PIL import Image
from collections import defaultdict

from ..utils import sparseToDense

frames = []

def snapshot(sparseDict, printToScreen = True, saveAnimation = False, update = {}):
    if not printToScreen and not saveAnimation:
        return
    frame = copy.copy(sparseDict)
    frame.update(update)
    if saveAnimation:
        global frames
        frames += [frame]
    if printToScreen:
        asciiPrint(frame, transpose = True)


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

def saveAnimatedGIF(numTiles = 41, tileSize = 10, outputFile = 'animation.gif', freq = 1, duration = 10):
    global frames

    print(f"Saving animation ({len(frames)} frames)…")
    tiles = [Image.open(f'2019/15/tiles/{i}.png').resize((tileSize,)*2) for i in range(7)]

    def frameToImage(frame, i):
        img = Image.new('RGBA', (numTiles*tileSize,)*2, 'black')
        for (x,y),v in frame.items():
            img.paste(tiles[v], ((y + numTiles//2 + 1)*tileSize, (x + numTiles//2 + 1)*tileSize))
        global saved
        print(f"saved: {i}/{len(frames)}", end="\r")
        return img

    images = (frameToImage(f,i) for i,f in enumerate(frames) if i%freq == 0)
    next(images).save(
        outputFile,
        save_all=True,
        append_images=images,
        duration=duration,
        loop=0,
        optimize=True
    )
