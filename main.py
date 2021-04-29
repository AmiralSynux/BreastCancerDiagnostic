import sys
import numpy as np
from analysis.dataset_analysis import *

np.set_printoptions(threshold=sys.maxsize)

# my_tar = tarfile.open('input/all-mias.tar.gz')
# my_tar.extractall('./input/mias')  # specify which folder to extract to
# my_tar.close()
left_right_histogram()
diagnosis_histogram_visualization()
resolution_graph()
