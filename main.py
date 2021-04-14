import sys
import numpy as np
from utils import print_original_image, print_binary_image, print_processed_image
from process import remove_labels
np.set_printoptions(threshold=sys.maxsize)

# my_tar = tarfile.open('input/all-mias.tar.gz')
# my_tar.extractall('./input/mammograms')  # specify which folder to extract to
# my_tar.close()

img = print_original_image(3)
thresh = print_binary_image(3)
processed_thresh = remove_labels(thresh)
print_processed_image(processed_thresh, img)


img2 = print_original_image(2)
thresh2 = print_binary_image(2)
processed_thresh2 = remove_labels(thresh2)
print_processed_image(processed_thresh2, img2)


