import copy
import sys
from typing import Any
import matplotlib.pyplot as plt
import numpy as np
import re
from glob import glob
import cv2

np.set_printoptions(threshold=sys.maxsize)


def read_pgm(filename, byteorder='>'):
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    return np.frombuffer(buffer,
                         dtype='u1' if int(maxval) < 256 else byteorder + 'u2',
                         count=int(width) * int(height),
                         offset=len(header)
                         ).reshape((int(height), int(width)))


def print_original_image(index):
    img = read_pgm(glob('**/*.pgm', recursive=True)[index])
    plt.imshow(img, cmap='bone')
    plt.show()
    return img


def print_binary_image(index):
    img = read_pgm(glob('**/*.pgm', recursive=True)[index])
    ret, thresh = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)
    plt.imshow(thresh, 'gray')
    plt.show()
    return thresh


def print_processed_image(processed_thresh, img):
    processed_img = copy.deepcopy(img)
    for i in range(len(img)):
        for j in range(len(img[0])):
            if processed_thresh[i][j] == 0:
                processed_img[i][j] = 0
    plt.imshow(processed_img, cmap='bone')
    plt.show()
    return processed_img


class Plotter:
    @staticmethod
    def plotHistogram(*args: Any):
        plt.hist(args, bins=3, rwidth=0.8, align='mid', color='pink')
        plt.show()

    @staticmethod
    def plotScatter(x: Any, y: Any):
        plt.scatter(x, y)
        plt.show()
