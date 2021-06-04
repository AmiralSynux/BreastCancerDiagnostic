import sys
from glob import glob

import matplotlib.pyplot as plt


# returns a DDSM mammogram with the outlined tumor
def show_ground_truth(image, mask):
    plt.imshow(image, 'gray')
    plt.show()
    new_image = image.copy()
    for i in range(len(image)):
        for j in range(len(image[0])):
            if mask[i][j] == 255:
                new_image[i][j] = 0
    plt.imshow(new_image, 'gray')
    plt.show()
    return new_image


def get_center(image):
    xmin = sys.maxsize
    xmax = -sys.maxsize
    ymin = sys.maxsize
    ymax = -sys.maxsize
    for i in range(len(image)):
        for j in range(len(image[0])):
            if image[i][j] == 255:
                if j < xmin:
                    xmin = j
                if j > xmax:
                    xmax = j
                if i > ymax:
                    ymax = i
                if i < ymin:
                    ymin = i
    avgx = (xmax + xmin) // 2
    avgy = (ymax + ymin) // 2
    return avgx, avgy
