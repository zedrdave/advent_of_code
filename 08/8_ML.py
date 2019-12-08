################################
#           ML params          #
################################

VALIDATE = False # Set to True to validate
VERBOSE = 0 # Model fit verbosity
EPOCHS = 100

# List of available truetype font files:
FONTNAMES = ("Arial.ttf",)


################################
#                              #
#  Load & build input bitmap   #
#                              #
################################

import numpy as np

digits = [int(i) for i in open('input.txt', 'r').read().strip()]
input_shape = (6,25)
layers = np.array(digits).reshape((-1,*input_shape))
composite = np.apply_along_axis(lambda x: x[np.where(x != 2)[0][0]], axis=0, arr=layers)


##################################
#                                #
#  Split and pad each character  #
#                                #
##################################

import math

# find blank vertical lines and split along them:
vblanks = np.where(np.apply_along_axis(lambda c: all(c == 0), arr=composite, axis=0))[0]
vblanks = np.sort(np.concatenate((vblanks, vblanks+1)))
chars = [c for c in np.array_split(composite, vblanks, axis=1) if c.shape[1] > 1]

char_shape = np.array([c.shape for c in chars]).max(0)

###
# NOTE: This is just in case problems do not produce fixed-sized chars (might be superfluous)
padded_chars = [np.pad(c, [(math.floor(x),math.ceil(x)) for x in (char_shape - c.shape) / 2]) for c in chars]

# Debug check:
for c in padded_chars:
    assert((c.shape == char_shape).all())
###


#####################################
#                                   #
#  Generate synthetic training set  #
#                                   #
#####################################

import string
from PIL import Image, ImageFont, ImageDraw

# input image dimensions
img_rows, img_cols = char_shape

# Using a few font sizes to simulate variability:
min_size = max(img_cols, img_rows)
max_size = min_size + 8

images = []
labels = []
blank = Image.new('L', (max_size, max_size), color='black')
for fontname in FONTNAMES:
    for size in range(min_size, max_size):
        font = ImageFont.truetype(fontname, size)
        for i,char in enumerate(string.ascii_uppercase):
            w,h = ImageDraw.Draw(blank).textsize(text=char, font=font)
            img = Image.new('1', (max_size, max_size), color='black')
            ImageDraw.Draw(img).text(((max_size-w)/2,(max_size-h)/2), fill='white', text=char, font=font)
            arr = np.array(img)
            orig_arr = arr
            for axis in (0,1):
                x = np.where(np.apply_along_axis(lambda l: l.any(), arr=arr, axis=axis))[0]
                adj_x = max(0, 4-x[-1]+x[0])//2 # ensure min size
                arr = np.take(arr, range(x[0]-adj_x, x[-1]+adj_x+1), axis=1-axis, mode='clip')

            arr = np.array(Image.fromarray(arr.astype('int8')*255).resize((img_cols, img_rows), Image.ANTIALIAS))

            # Slightly hacky way to deal with downsampling:
            arr = arr > 64
            # DEBUG:
            # Image.fromarray(arr).resize((arr.shape[1]*10,arr.shape[0]*10)).show()
            images += [arr]
            labels += [i]

images = np.array(images)
labels = np.array(labels)


################################
#                              #
#     Train Keras model        #
#                              #
################################

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from sklearn.model_selection import train_test_split

# Following 2 lines can be commented off if your Keras install supports GPU
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

batch_size = 64

if VALIDATE:
    x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=0.05, shuffle= True)
else:
    x_train, x_test, y_train, y_test = images, images, labels, labels

if K.image_data_format() == 'channels_first':
    input_shape = (1, *char_shape)
else:
    input_shape = (*char_shape, 1)

x_train = x_train.reshape(x_train.shape[0], *input_shape)
x_test = x_test.reshape(x_test.shape[0], *input_shape)

# print('x_train shape:', x_train.shape)
# print(x_train.shape[0], 'train samples')
# print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
num_classes = len(string.ascii_uppercase)
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# build and train model
model = Sequential()
model.add(Conv2D(32, kernel_size=(2, 2),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (2, 2), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

print("Fitting model…")
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=EPOCHS,
          verbose=VERBOSE,
          validation_data=(x_test, y_test))

if VALIDATE:
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    print(' '.join(string.ascii_uppercase[c] for c in model.predict_classes(x_test[0:60])))
    print(' '.join(string.ascii_uppercase[c] for c in np.where(y_test[0:60])[1]))


################################
#                              #
#            MAGIC!            #
#                              #
################################

chars = np.array(chars)
input_chars = chars.reshape(chars.shape[0], *input_shape)*255

print("\nUsing model:\n")
print(' '.join(string.ascii_uppercase[c] for c in model.predict_classes(input_chars)))

print("\nASCII version:\n")
print("\n".join(''.join(u" ♥️"[int(i)] for i in line) for line in composite), "\n")
