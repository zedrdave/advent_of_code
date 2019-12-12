import numpy as np
import string
import os

class CharPredictor:
    """
    Init with character dimensions, then use predict(chars), where <chars> is an array of bitmaps.
    """


    ################################
    #           ML params          #
    ################################

    VALIDATION_RATIO = 0.1
    EPOCHS = 500

    VERBOSITY = 0 # verbosity (2: show model fit progression)

    # List of truetype font files:
    FONTNAMES = [os.path.join(os.path.dirname(__file__), 'fonts', f) for f in ("Anonymous_Pro.ttf", "Anonymous_Pro_B.ttf")]
    # Optional: only use built-in:
    # FONTNAMES = ("Arial.ttf", "SFNSMono.ttf")

    def __init__(self, char_shape, verbosity = None):

        if verbosity is not None:
            self.VERBOSITY = verbosity

        from PIL import Image, ImageFont, ImageDraw

        import keras
        from keras.datasets import mnist
        from keras.models import Sequential
        from keras.layers import Dense, Dropout, Flatten
        from keras.layers import Conv2D, MaxPooling2D
        from keras import backend as K
        from sklearn.model_selection import train_test_split

        #####################################
        #                                   #
        #  Generate synthetic training set  #
        #                                   #
        #####################################
        if self.VERBOSITY:
            print("Building training set…")

        # input image dimensions
        img_rows, img_cols = char_shape

        # Using a few font sizes to simulate variability:
        min_size = max(img_cols, img_rows)
        max_size = min_size + 7

        images = []
        labels = []
        blank = Image.new('L', (max_size*2, max_size*2), color='black')
        for fontname in self.FONTNAMES:
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
                        adj_x = max(0, 4-x[-1]+x[0])//2 # ensure min size of 4
                        arr = np.take(arr, range(x[0]-adj_x, x[-1]+adj_x+1), axis=1-axis, mode='clip')
                    # jiggle to the right, jiggle to the left
                    for r in (0,1):
                        arr = np.array(Image.fromarray(arr.astype('uint8')*255).resize((img_cols-r, img_rows), Image.ANTIALIAS))
                        arr = np.pad(arr, ((0,0),(0,r)))
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

        # Following 2 lines can be commented off if your Keras install supports GPU
        import os
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        batch_size = 128

        if self.VALIDATION_RATIO > 0:
            x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=self.VALIDATION_RATIO, shuffle= True)
        else:
            x_train, x_test, y_train, y_test = images, images, labels, labels

        if K.image_data_format() == 'channels_first':
            self.self.input_shape = (1, *char_shape)
        else:
            self.input_shape = (*char_shape, 1)

        x_train = x_train.reshape(x_train.shape[0], *self.input_shape)
        x_test = x_test.reshape(x_test.shape[0], *self.input_shape)

        # print('x_train shape:', x_train.shape)
        # print(x_train.shape[0], 'train samples')
        # print(x_test.shape[0], 'test samples')
        # print(x_train[0])

        # convert class vectors to binary class matrices
        num_classes = len(string.ascii_uppercase)
        y_train = keras.utils.to_categorical(y_train, num_classes)
        y_test = keras.utils.to_categorical(y_test, num_classes)

        # build and train model
        self.model = Sequential()
        self.model.add(Conv2D(32, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=self.input_shape))
        self.model.add(Conv2D(64, (2, 2), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))
        self.model.add(Flatten())
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(num_classes, activation='softmax'))

        self.model.compile(loss=keras.losses.categorical_crossentropy,
                      optimizer=keras.optimizers.Adadelta(),
                      metrics=['accuracy'])

        if self.VERBOSITY:
            print("Fitting model…")
        self.model.fit(x_train, y_train,
                  batch_size=batch_size,
                  epochs=self.EPOCHS,
                  verbose=self.VERBOSITY > 1,
                  validation_data=(x_test, y_test))

        if self.VALIDATION_RATIO and self.VERBOSITY:
            score = self.model.evaluate(x_test, y_test, verbose=self.VERBOSITY > 1)
            print('Test loss:', score[0])
            print('Test accuracy:', score[1])
            # Debug:
            # print(' '.join(string.ascii_uppercase[c] for c in self.model.predict_classes(x_test[0:60])))
            # print(' '.join(string.ascii_uppercase[c] for c in np.where(y_test[0:60])[1]))


    def predict(self, chars):
        chars = np.array(chars)
        input_chars = chars.reshape(chars.shape[0], *self.input_shape)*255

        predicted = [string.ascii_uppercase[c] for c in self.model.predict_classes(input_chars)]
        return predicted
