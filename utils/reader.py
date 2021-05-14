import threading
from glob import glob

import cv2

from analysis.dataset_analysis import read_mias
from preprocessing.process import remove_labels
from utils.domain import ImageDTO
from utils.utils import read_pgm, get_processed_image, processDDSMMammogram


def read_ddsm_data(imgs):
    benign = glob('input/ddsm/benign/**/*MLO.jpg', recursive=True)[:10]
    malignant = glob('input/ddsm/malignant/**/*MLO.jpg', recursive=True)[:10]
    for path in benign:
        imgs.append(ImageDTO(processDDSMMammogram(path), "BENING"))
    print("---------    benign finished    ---------")
    for path in malignant:
        imgs.append(ImageDTO(processDDSMMammogram(path), "MALIGNANT"))
    print("---------    malignant finished    ---------")


def read_mias_data(imageDTOs):
    mias_gt = read_mias()
    i = 0
    for img in glob('input/mias/*.pgm', recursive=True)[:10]:
        img = read_pgm(img)
        ret, thresh = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)
        processed_thresh = remove_labels(thresh)
        processed_img = get_processed_image(processed_thresh, img)
        imageDTO = ImageDTO(processed_img, mias_gt[i])
        imageDTOs.append(imageDTO)
        print("#" + str(i))
        i += 1


def write_data(images):
    with open("input/truth.txt", "w") as writer:
        writer.write(str(len(images)) + "\n")
        for imageDTO in images:
            matrix = imageDTO.matrix
            writer.write(str(len(matrix)) + "," + str(len(matrix[0])) + "\n")
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    writer.write(str(matrix[i][j]) + ",")
                writer.write("\n")
            writer.write(imageDTO.truth + "\n")
    k = 0
    for imageDTO in images:
        name = "mamo" + str(k)
        with open("input/mamos/" + name, "w") as writer:
            matrix = imageDTO.matrix
            writer.write(str(len(matrix)) + "," + str(len(matrix[0])) + "\n")
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    writer.write(str(matrix[i][j]) + ",")
                writer.write("\n")
            writer.write(imageDTO.truth + "\n")
        k += 1


def read_data_img():
    mias = []
    ddsm = []
    t = threading.Thread(target=read_mias_data, args=(mias,))
    t.start()
    t2 = threading.Thread(target=read_ddsm_data, args=(ddsm,))
    t2.start()
    t.join()
    t2.join()
    imageDTOs = mias + ddsm
    write_data(imageDTOs)
    return imageDTOs


def read_data():
    imageDTOs = []
    with open("input/truth.txt", "r") as reader:
        length = int(reader.readline())
        for _ in range(length):
            n = reader.readline()
            n = n.split(",")
            m = int(n[1])
            n = int(n[0])
            matrix = []
            for line in range(n):
                matrix_line = []
                line = reader.readline()
                line = line.split(",")
                for j in range(m):
                    matrix_line.append(int(line[j]))
                matrix.append(matrix_line)
            truth = reader.readline()
            truth = truth[:-1]
            imageDTOs.append(ImageDTO(matrix, truth))
            print(len(imageDTOs))
    return imageDTOs
