import matplotlib.pyplot as plt


# returns a DDSM mammogram with the outlined tumor
def show_ground_truth(image, mask):
    plt.imshow(image, 'gray')
    plt.show()
    new_image = image.copy()
    for i in range(len(image)):
        for j in range(len(image[0])):
            if mask[i][j] == 255:
                new_image[i][j] = 0
    plt.imshow(new_image, 'gray')
    plt.show()
    return new_image
