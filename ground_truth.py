import matplotlib.pyplot as plt
from numpy import array


def show_ground_truth(image ,mask):
    plt.imshow(image,'gray')
    plt.show()
    new_image = image.copy()
    for i in range(len(image)):
        for j in range(len(image[0])):
            if mask[i][j] == 255:
                new_image[i][j] = 0
    plt.imshow(new_image, 'gray')
    plt.show()
    return new_image

img = "input/COMPLETARE/cancer/0045/C_0045_1.RIGHT_MLO.jpg"
img_mask = "input/COMPLETARE/cancer/0045/C_0045_1.RIGHT_MLO_Mask.jpg"

from PIL import Image
# Open the image form working directory
image = array(Image.open(img))
image_mask = array(Image.open(img_mask))

show_ground_truth(image,image_mask)