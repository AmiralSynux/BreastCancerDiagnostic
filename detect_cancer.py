import cv2
import numpy as np


def get_image_after_segmentation(filename):
    image = cv2.imread(filename)

    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    k = 5
    _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)

    # flatten the labels array
    labels = labels.flatten()
    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(image.shape)

    ret, thresh = cv2.threshold(segmented_image, 125, 255, cv2.THRESH_BINARY)
    # clear the thresh
    clear(thresh)
    return thresh


# flood_fill algorithm with deep
def flood_fill(matrix, i, j, n, m, deep):
    queue = [(i, j)]
    queue = set(queue)
    while len(queue) > 0:
        indexes = queue.pop()
        i = indexes[0]
        j = indexes[1]
        if i < n and j < m and matrix[i][j][0] != 0:
            matrix[i][j] = [0, 0, 0]
            for k in range(1, deep + 1):
                queue.add((i + k, j))
                queue.add((i - k, j))
                queue.add((i, j + k))
                queue.add((i, j - k))


# clears the borders of a matrix. Higher the deep, higher the "cleaning power"
def clear(matrix, deep=3):
    n = len(matrix)
    m = len(matrix[0])
    for i in range(n):
        flood_fill(matrix, i, 0, n, m, deep)
        flood_fill(matrix, i, m - 1, n, m, deep)
    for j in range(m):
        flood_fill(matrix, 0, j, n, m, deep)
        flood_fill(matrix, n - 1, j, n, m, deep)


# used for quick testing
def work(thresh_filepath, save_filename, deep=3):
    img = cv2.imread(thresh_filepath)
    clear(img, deep)
    cv2.imwrite(save_filename, img)
