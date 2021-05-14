from PIL import Image
from numpy import array
from glob import glob
from utils import Plotter


# a function that reads the ground truth for the mias db(NORM,MALIGNANT,BENIGN)
def read_mias():
    mammograms = []
    with open("../input/mias/groundTruth.txt", "r") as reader:
        for line in reader.readlines():
            line = line.split()
            mammograms.append(line[1])
    return mammograms


# a function that reads the ground truth for the ddsm db
# returns the numbers of each benign, malignant mammograms
def read_ddsm():
    benign = len(glob('input/ddsm/benign/**/*Mask.jpg', recursive=True))
    malignant = len(glob('input/ddsm/malignant/**/*Mask.jpg', recursive=True))
    benign = ['BENIGN'] * benign
    malignant = ['MALIGNANT'] * malignant
    return benign, malignant


# displays a histogram of the number of each type of diagnosis(NORM,MALIGNANT,BENIGN)
def diagnosis_histogram_visualization():
    miasMammograms = read_mias()
    ddsmBenign, ddsmMalignant = read_ddsm()
    allMammograms = miasMammograms + ddsmBenign + ddsmMalignant
    Plotter.plotHistogram(allMammograms, title="Diagnosis histogram", nrOfbins=3,
                          colors=['darkgrey', 'black', 'lightgrey'], labels=['Diagnosis', 'Number of cases'],
                          rotation=None)


# displays a plot with the resolutions corresponding to mammograms
def resolution_graph():
    benign = glob('input/ddsm/benign/**/*Mask.jpg', recursive=True)
    malignant = glob('input/ddsm/malignant/**/*Mask.jpg', recursive=True)
    files = benign + malignant
    xDdsm, yDdsm = [], []
    for file in files:
        matrix = array(Image.open(file))
        xDdsm.append(len(matrix))
        yDdsm.append(len(matrix[0]))
    mias = glob('input/mias/*.pgm', recursive=True)
    xMias, yMias = [], []
    for file in mias:
        matrix = array(Image.open(file))
        xMias.append(len(matrix))
        yMias.append(len(matrix[0]))
    Plotter.plotPlot(xMias, yMias, xDdsm, yDdsm, title="Resolution plot")


def left_right_histogram():
    leftM, leftN, leftB, rightM, rightN, rightB = [], [], [], [], [], []
    leftB = len(glob('input/ddsm/benign/**/*LEFT_MLO_Mask.jpg', recursive=True))
    rightB = len(glob('input/ddsm/benign/**/*RIGHT_MLO_Mask.jpg', recursive=True))
    rightM = len(glob('input/ddsm/malignant/**/*RIGHT_MLO_Mask.jpg', recursive=True))
    leftM = len(glob('input/ddsm/malignant/**/*LEFT_MLO_Mask.jpg', recursive=True))
    leftB = ['LEFT_BENIGN'] * leftB
    leftM = ['LEFT_MALIGNANT'] * leftM
    rightB = ['RIGHT_BENIGN'] * rightB
    rightM = ['RIGHT_MALIGNANT'] * rightM
    mias = read_mias()
    for index in range(len(mias) - 1):
        if (index + 1) % 2 == 0 and mias[index] == 'NORM':
            leftN.append('LEFT_NORM')
        elif (index + 1) % 2 == 1 and mias[index] == 'NORM':
            rightN.append('RIGHT_NORM')
        elif (index + 1) % 2 == 0 and mias[index] == 'BENIGN':
            leftB.append('LEFT_BENIGN')
        elif (index + 1) % 2 == 1 and mias[index] == 'BENIGN':
            rightB.append('RIGHT_BENIGN')
        elif (index + 1) % 2 == 0 and mias[index] == 'MALIGNANT':
            leftM.append('LEFT_MALIGNANT')
        elif (index + 1) % 2 == 1 and mias[index] == 'MALIGNANT':
            rightM.append('RIGHT_MALIGNANT')
    allMammograms = leftM + leftN + leftB + rightM + rightN + rightB
    Plotter.plotHistogram(allMammograms, title="Left and right mammogram diagnosis", nrOfbins=6,
                          colors=['yellowgreen', 'olivedrab', 'goldenrod', 'gold', 'forestgreen', 'limegreen'],
                          labels=['', 'Number of cases'], rotation=10)
