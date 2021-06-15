import numpy
from keras import initializers
from networkx.drawing.tests.test_pylab import plt
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.utils.np_utils import to_categorical
from tensorflow.python.ops.init_ops import he_normal
from extract_features import readData


def classifyMammograms():
    X, y = readData()
    X = numpy.array(X)
    y = numpy.array(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=123, shuffle=True)
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    model = Sequential()
    model.add(Dense(128, activation='relu', input_dim=len(X[0]), kernel_regularizer='l2', kernel_initializer=he_normal(seed=None)))
    model.add(Dense(128))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(32))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(16))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(4))
    model.add(Dense(2, activation='sigmoid'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    filepath = "model.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    earlystopping = EarlyStopping(monitor='loss', patience=20, restore_best_weights=True)
    desired_callbacks = [checkpoint, earlystopping]
    # history = model.fit(X_train, y_train, validation_split=0.2, batch_size=50, epochs=1000, shuffle=True,
    #                     callbacks=desired_callbacks)
    # plt.plot(history.history['loss'])
    # plt.plot(history.history['val_loss'])
    # plt.title('model loss')
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='upper left')
    # plt.savefig("loss.jpg")
    model = load_model("model.hdf5")
    model.summary()
    scores = model.evaluate(X_train, y_train, verbose=0)
    print('Accuracy on training data: {}% \n Error on training data: {}'.format(scores[1], 1 - scores[1]))

    scores2 = model.evaluate(X_test, y_test, verbose=0)
    print('Accuracy on test data: {}% \n Error on test data: {}'.format(scores2[1], 1 - scores2[1]))
