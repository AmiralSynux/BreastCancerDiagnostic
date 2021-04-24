from statistics import mean, stdev

from PIL import Image
from numpy import array
from glob import glob

from utils import Plotter


def read_mias():
    mammograms = []
    with open("input/mias/groundTruth.txt", "r") as reader:
        for line in reader.readlines():
            line = line.split()
            mammograms.append(line[1])
    return mammograms


def read_ddsm():
    benign = len(glob('input/ddsm/benign/**/*Mask.jpg', recursive=True))
    malignant = len(glob('input/ddsm/malignant/**/*Mask.jpg', recursive=True))
    return benign, malignant


def histogram_visualization():
    miasMammograms = read_mias()
    benign, malignant = read_ddsm()
    benign = ['BENIGN'] * benign
    malignant = ['MALIGNANT'] * malignant
    miasMammograms += benign + malignant
    Plotter.plotHistogram(miasMammograms)


def resolution_graph():
    benign = glob('input/ddsm/benign/**/*Mask.jpg', recursive=True)
    malignant = glob('input/ddsm/malignant/**/*Mask.jpg', recursive=True)
    files = benign + malignant
    x, y = [], []
    for file in files:
        matrix = array(Image.open(file))
        x.append(len(matrix))
        y.append(len(matrix[0]))
    mias = glob('input/mias/*.pgm', recursive=True)
    for file in mias:
        matrix = array(Image.open(file))
        x.append(len(matrix))
        y.append(len(matrix[0]))
    Plotter.plotScatter(x, y)
    x = statisticalNormalisation(x)
    y = statisticalNormalisation(y)
    Plotter.plotScatter(x, y)


def statisticalNormalisation(features):
    meanValue = mean(features)
    stdDevValue = stdev(features)
    normalisedFeatures = [(feat - meanValue) / stdDevValue for feat in features]
    return normalisedFeatures


resolution_graph()
