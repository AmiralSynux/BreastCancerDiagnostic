from glob import glob

import cv2

from analysis.dataset_analysis import read_mias
from preprocessing.process import remove_labels
from domain import ImageDTO
from utils import read_pgm, get_processed_image


def read_data():
    imageDTOs = []
    mias_gt = read_mias()
    i=0
    for img in glob('../input/mias/*.pgm', recursive=True):
        img = read_pgm(img)
        ret, thresh = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)
        processed_thresh = remove_labels(thresh)
        processed_img = get_processed_image(processed_thresh, img)
        imageDTO = ImageDTO(processed_img, mias_gt[i])
        imageDTOs.append(imageDTO)
        i+=1
        print(i)
    print(imageDTOs[0])


read_data()