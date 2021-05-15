import copy
import sys
from typing import Any
import matplotlib.pyplot as plt
import numpy as np
import re
from glob import glob
import cv2
from PIL import Image
from preprocessing.process import remove_labels

np.set_printoptions(threshold=sys.maxsize)


# a function that reads a pgm file
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


# returns the mammogram from a specified image index in the mias db
def print_original_image(index):
    img = read_pgm(glob('../input/mias/*.pgm', recursive=True)[index])
    plt.imshow(img, cmap='bone')
    plt.show()
    return img


# returns the binary mammogram from a specified image index, after the process of thresholding
def print_binary_image(index):
    img = read_pgm(glob('../input/mias/*.pgm', recursive=True)[index])
    ret, thresh = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)
    plt.imshow(thresh, 'gray')
    plt.show()
    return thresh


# returns the processed mammogram (without any labels or artifacts) given the original and the thresh image
def print_processed_image(processed_thresh, img):
    processed_img = get_processed_image(processed_thresh, img)
    plt.imshow(processed_img, cmap='bone')
    plt.show()


def processMiasMammogram(index):
    img = print_original_image(index)
    thresh = print_binary_image(index)
    processed_thresh = remove_labels(thresh)
    print_processed_image(processed_thresh, img)


def processDDSMMammogram(fileName, resize=-1):
    image = np.array(Image.open(fileName))
    if resize != -1:
        image = cv2.resize(image, (resize, resize))
    ret, thresh = cv2.threshold(image, 15, 255, cv2.THRESH_BINARY)
    processed_thresh = remove_labels(thresh)
    # print_processed_image(processed_thresh, image)
    return processed_thresh


def get_processed_image(processed_thresh, img):
    processed_img = copy.deepcopy(img)
    for i in range(len(img)):
        for j in range(len(img[0])):
            if processed_thresh[i][j] == 0:
                processed_img[i][j] = 0
    return processed_img


class Plotter:
    @staticmethod
    def plotPlot(x: Any, y: Any, x1: Any, y1: Any, title):
        plt.plot(x, y, 'g^', label="Mias")
        plt.plot(x1, y1, 'ro', label="DDSM")
        plt.legend()
        plt.xlabel("Width")
        plt.ylabel("Height")
        plt.title(title)
        plt.show()

    @staticmethod
    def plotHistogram(*args: Any, title, nrOfbins, colors, labels, rotation):
        fig, ax = plt.subplots()
        N, bins, patches = ax.hist(args, bins=nrOfbins, edgecolor='white', linewidth=1)
        for i in range(nrOfbins):
            patches[i].set_facecolor(colors[i])
        plt.xticks(rotation=rotation)
        plt.xlabel(labels[0])
        plt.ylabel(labels[1])
        plt.title(title)
        plt.show()
