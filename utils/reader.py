import threading
from glob import glob

import cv2
from chronometer import Chronometer

from analysis.dataset_analysis import read_mias
from preprocessing.process import remove_labels
from utils.domain import ImageDTO
from utils.utils import read_pgm, get_processed_image, processDDSMMammogram


def read_ddsm_data(imgs, resize=-1):
    benign = glob('input/ddsm/benign/**/*MLO.jpg', recursive=True)
    malignant = glob('input/ddsm/malignant/**/*MLO.jpg', recursive=True)
    for path in benign:
        imgs.append(ImageDTO(processDDSMMammogram(path, resize), "BENIGN"))
    print("---------###    BENIGN Finished    ###---------")
    for path in malignant:
        imgs.append(ImageDTO(processDDSMMammogram(path, resize), "MALIGNANT"))
    print("---------###    MALIGNANT Finished    ###---------")
    print("-- DDSM FINISHED --")


def read_one_image(res, path, start, end, mias_gt, resize=-1):
    t_ = "Thread: " + str(start) + " - " + str(end - 1) + " read: #"
    for i in range(start, end):
        img = read_pgm(path[i])
        if resize != -1:
            img = cv2.resize(img, (resize, resize))
        ret, thresh = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)
        processed_thresh = remove_labels(thresh)
        processed_img = get_processed_image(processed_thresh, img)
        imageDTO = ImageDTO(processed_img, mias_gt[i])
        res.append(imageDTO)
        print(t_ + str(i - start + 1) + " out of " + str(end - start))
    print("### Thread: " + str(start) + " - " + str(end) + " Finished  ###")


def read_mias_data(imageDTOs, resize=-1):
    mias_gt = read_mias()
    res = []
    no_t = 3
    threads = []
    paths = glob('input/mias/*.pgm', recursive=True)
    paths_n = len(paths)
    count = paths_n // no_t
    for i in range(no_t):
        r = []
        t = threading.Thread(target=read_one_image, args=(r, paths, i * count, i * count + count, mias_gt, resize))
        res.append(r)
        t.start()
        threads.append(t)
        i += 1
    if paths_n % no_t != 0:
        r = []
        t = threading.Thread(target=read_one_image,
                             args=(r, paths, paths_n - (paths_n % no_t), paths_n, mias_gt, resize))
        res.append(r)
        t.start()
        t.join()
    for thread in threads:
        thread.join()
    result = []
    for r in res:
        result += r
    for r in result:
        imageDTOs.append(r)
    print("-- MIAS FINISHED --")


def write_data(images):
    print("Writing...")
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
    print("-- Writing finished --")
    # k = 0
    # for imageDTO in images:
    #     name = "mammo" + str(k)
    #     with open("input/mammos/" + name, "w") as writer:
    #         matrix = imageDTO.matrix
    #         writer.write(str(len(matrix)) + "," + str(len(matrix[0])) + "\n")
    #         for i in range(len(matrix)):
    #             for j in range(len(matrix[0])):
    #                 writer.write(str(matrix[i][j]) + ",")
    #             writer.write("\n")
    #         writer.write(imageDTO.truth + "\n")
    #     k += 1


# Reads mias & ddsm and if the resize parameter is given, the read images are resized
# Returns the read images
def read_data_img(resize=-1):
    with Chronometer() as cr:
        mias = []
        ddsm = []
        t = threading.Thread(target=read_mias_data, args=(mias, resize,))
        t2 = threading.Thread(target=read_ddsm_data, args=(ddsm, resize,))
        t2.start()
        t.start()
        t.join()
        t2.join()
        imageDTOs = mias + ddsm
    print('Reading done..\nElapsed time: {:.3f} seconds\nTotal length: {}'.format(float(cr), len(imageDTOs)))
    write_data(imageDTOs)
    return imageDTOs


def read_threaded(imageDTOs, start, end):
    print("#Start - " + str(start) + " " + str(end))
    for i in range(start, end):
        path = "input/mammos/mammo" + str(i)
        with open(path, "r") as reader:
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
    print("#END - " + str(start) + " " + str(end))


def read_scattered_data(n=382, nr_t=-1):
    if n > 382:
        n = 382
    if nr_t == -1:
        nr_t = n // 15
    threads = []
    rez = []
    count = n // nr_t
    for i in range(nr_t):
        r = []
        t = threading.Thread(target=read_threaded, args=(r, i * count, i * count + count))
        rez.append(r)
        t.start()
        threads.append(t)
    if n % nr_t != 0:
        r = []
        t = threading.Thread(target=read_threaded, args=(r, n - (n % nr_t), n))
        rez.append(r)
        t.start()
        t.join()
    for thread in threads:
        thread.join()
    result = []
    for r in rez:
        result += r
    print("READING FINISHED")
    return result


# returns the data out of truth.txt
# the data caps out at 382
# if no n is given, it will read all data
def read_data(n=382):
    with Chronometer() as cr:
        k = 1
        imageDTOs = []
        with open("input/truth.txt", "r") as reader:
            length = int(reader.readline())
            if n < length:
                length = n
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
                if k % 5 == 0:
                    print("#" + str(k))
                k += 1
    print('Reading done..\nElapsed time: {:.3f} seconds\nTotal length: {}'.format(float(cr), len(imageDTOs)))
    return imageDTOs
