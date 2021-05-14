from glob import glob

import cv2

from analysis.dataset_analysis import read_mias
from preprocessing.process import remove_labels
from domain import ImageDTO
from utils import read_pgm, get_processed_image, processDDSMMammogram


def read_ddsm():
    benign = glob('../input/ddsm/benign/**/*MLO.jpg', recursive=True)
    malignant = glob('../input/ddsm/malignant/**/*MLO.jpg', recursive=True)
    imgs = []
    for path in benign:
        imgs.append(ImageDTO(processDDSMMammogram(path),"BENING"))
    for path in malignant:
        imgs.append(ImageDTO(processDDSMMammogram(path),"MALIGNANT"))
    return imgs


def write_data(images):
    pass


def read_data_img():
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
    imageDTOs += read_ddsm()
    write_data(imageDTOs)
    return imageDTOs


def read_data():
    pass
