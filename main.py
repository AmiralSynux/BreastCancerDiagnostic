import sys
from glob import glob
import cv2
import numpy as np
from sklearn.metrics import jaccard_score
from detect_cancer import get_image_after_segmentation
from solver_classification import classifyMammograms
from utils.reader import read_scattered_data

np.set_printoptions(threshold=sys.maxsize)

# left_right_histogram()
# diagnosis_histogram_visualization()
# resolution_graph()
# read_data_img()

# classifyMammograms()


def detect_tumors():
    images = read_scattered_data()
    print(len(images))
    for i in range(len(images)):
        img = get_image_after_segmentation(images[i].matrix)
        cv2.imwrite("tumors/tumor" + str(i) + ".jpg", img)


def make_tumor_mask_white(matrix):
    for i in range(len(matrix)):
        for j in range(1, len(matrix[0])):
            if matrix[i][j][0] != 255 and matrix[i][j - 1][0] != 0:
                matrix[i][j] = [255, 255, 255]
            elif matrix[i][j][0] != 0 and matrix[i][j - 1][0] != 0:
                break


def calculate_jaccard():
    masks = glob('input/ddsm/**/*_Mask.jpg', recursive=True)
    sum_jac = 0
    for i in range(30):
        print(i)
        img1 = cv2.imread("tumors/tumor"+str(i)+".jpg").flatten().tolist()
        img2 = cv2.imread(masks[i])
        ret, thresh = cv2.threshold(img2, 15, 255, cv2.THRESH_BINARY)
        make_tumor_mask_white(thresh)
        thresh = thresh.flatten().tolist()
        sum_jac += jaccard_score(thresh, img1, average='micro')
    return sum_jac / 30


print(calculate_jaccard())
