import copy
import matplotlib.pyplot as plt


def compute_pixel_sums(thresh):
    sum_1 = 0
    for i in range(1024):
        for j in range(512):
            if thresh[i][j] == 255:
                sum_1 += 255

    sum_2 = 0
    for i in range(1024):
        for j in range(512, 1024):
            if thresh[i][j] == 255:
                sum_2 += 255
    return sum_1, sum_2


def remove_labels(thresh):
    sum_1, sum_2 = compute_pixel_sums(thresh)
    processed_thresh = copy.deepcopy(thresh)
    if sum_1 < sum_2:
        for i in range(1024):
            begin = 0
            end = 0
            for j in range(511):
                if thresh[i][j] == 255 and begin == 0:
                    begin = j
                if thresh[i][j] == 255 and thresh[i][j + 1] == 0:
                    end = j
                if end != 0:
                    for k in range(begin, end + 1):
                        processed_thresh[i][k] = 0
                    begin = 0
                    end = 0
    else:
        for i in range(1024):
            begin = 0
            end = 0
            for j in range(1023, 511, -1):
                if thresh[i][j] == 255 and begin == 0:
                    begin = j
                if thresh[i][j] == 255 and thresh[i][j - 1] == 0:
                    end = j
                if end != 0:
                    for k in range(begin, end - 1, -1):
                        processed_thresh[i][k] = 0
                    begin = 0
                    end = 0
    return processed_thresh
