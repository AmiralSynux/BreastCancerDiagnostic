import sys
import numpy as np
from networkx.algorithms.tests.test_communicability import numpy
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.callbacks import ModelCheckpoint
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.utils.np_utils import to_categorical
from utils.reader import read_data_img, read_data

np.set_printoptions(threshold=sys.maxsize)


# my_tar = tarfile.open('input/all-mias.tar.gz')
# my_tar.extractall('./input/mias')  # specify which folder to extract to
# my_tar.close()
# left_right_histogram()
# diagnosis_histogram_visualization()
# resolution_graph()

# read_data_img()
def start():
    X = []
    y = []
    for el in read_data():
        matrix = el.matrix
        matrix = numpy.array(matrix)
        matrix = matrix.reshape((1, 512 * 512))
        X.append(matrix[0])
        if el.truth == 'BENIGN':
            y.append(0)
        elif el.truth == 'MALIGNANT':
            y.append(1)
        elif el.truth == 'NORM':
            y.append(2)
    X = numpy.array(X)
    y = numpy.array(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=123, shuffle=True)
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    model = Sequential()
    model.add(Dense(256, activation='relu', input_dim=512 * 512))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(3, activation='softmax'))
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(X_train, y_train, validation_split=0.2, batch_size=128, epochs=100, shuffle=True)
    pred_train = model.predict(X_train)
    scores = model.evaluate(X_train, y_train, verbose=0)
    print('Accuracy on training data: {}% \n Error on training data: {}'.format(scores[1], 1 - scores[1]))

    pred_test = model.predict(X_test)
    scores2 = model.evaluate(X_test, y_test, verbose=0)
    print('Accuracy on test data: {}% \n Error on test data: {}'.format(scores2[1], 1 - scores2[1]))


start()
