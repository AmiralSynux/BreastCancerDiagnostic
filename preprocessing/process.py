import copy


def compute_pixel_sums(thresh):
    sum_1 = 0
    for i in range(len(thresh)):
        for j in range(len(thresh[0]) // 2):
            if thresh[i][j] == 255:
                sum_1 += 255

    sum_2 = 0
    for i in range(len(thresh)):
        for j in range(len(thresh[0]) // 2, len(thresh[0])):
            if thresh[i][j] == 255:
                sum_2 += 255
    return sum_1, sum_2


def remove_labels(thresh):
    sum_1, sum_2 = compute_pixel_sums(thresh)
    processed_thresh = copy.deepcopy(thresh)
    if sum_1 < sum_2:
        for i in range(len(thresh)):
            begin = 0
            end = 0
            for j in range(len(thresh[0]) // 2 - 1):
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
        for i in range(len(thresh)):
            begin = 0
            end = 0
            for j in range(len(thresh[0]) - 1, len(thresh[0]) // 2 - 1, -1):
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


def add_black(matrix):
    zeros = []
    for i in range(2800):
        line = []
        for j in range(3100):
            line.append(0)
        zeros.append(line)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            zeros[i][j] = matrix[i][j]
    return zeros
