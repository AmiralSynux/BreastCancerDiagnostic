# import os
# from glob import glob
#
# import pandas
# import torch
# from torch import optim, nn
# from torchvision import models, transforms
#
# model = models.vgg16(pretrained=True)
# import cv2
# from torch import nn
#
#
# class FeatureExtractor(nn.Module):
#     def __init__(self, model):
#         super(FeatureExtractor, self).__init__()
#         # Extract VGG-16 Feature Layers
#         self.features = list(model.features)
#         self.features = nn.Sequential(*self.features)
#         # Extract VGG-16 Average Pooling Layer
#         self.pooling = model.avgpool
#         # Convert the image into one-dimensional vector
#         self.flatten = nn.Flatten()
#         # Extract the first part of fully-connected layer from VGG16
#         self.fc = model.classifier[0]
#
#     def forward(self, x):
#         # It will take the input 'x' until it returns the feature vector called 'out'
#         out = self.features(x)
#         out = self.pooling(out)
#         out = self.flatten(out)
#         out = self.fc(out)
#         return out
#
#
# from tqdm import tqdm
# import numpy as np
#
# # Initialize the model
# model = models.vgg16(pretrained=True)
# new_model = FeatureExtractor(model)
#
# # Change the device to GPU
# device = torch.device('cuda:0' if torch.cuda.is_available() else "cpu")
# new_model = new_model.to(device)
# # Transform the image, so it becomes readable with the model
# transform = transforms.Compose([
#     transforms.ToPILImage(),
#     transforms.ToTensor()
# ])
#
#
# def readFile(filename):
#     with open(filename, "r") as reader:
#         lines = reader.readlines()
#         lines.pop(0)
#         truth = lines.pop()[:-1]
#         image = []
#         for line in lines:
#             line = line.strip(' \n')
#             line = line.split(',')
#             line.pop()
#             row = []
#             for el in line:
#                 elems = [int(el), int(el), int(el)]
#                 row.append(elems)
#             image.append(row)
#         return image, truth


def readData():
    with open("all_features.csv", "r") as reader:
        data = []
        lines = reader.readlines()
        lines.pop(0)
        for line in lines:
            line = line.split(",")
            row = []
            for el in line:
                row.append(float(el))
            data.append(row)
    with open("all_truths.csv", "r") as reader:
        truths = []
        lines = reader.readlines()
        for line in lines:
            line = line.strip(" \n")
            if line == "NORM":
                truths.append(1)
            else:
                truths.append(0)
    return data, truths
#
# features = []
# truths = []
# nr = 0
#
# for i in range(415):
#     file = "input/mammos/mammo" + str(i) + ".txt"
#     print(nr)
#     image, truth = readFile(file)
#     img = np.array(image, dtype=np.uint8)
#     img = transform(img)
#     img = img.reshape(1, 3, len(image), len(image[0]))
#     img = img.to(device)
#     with torch.no_grad():
#         feature = new_model(img)
#     features.append(feature.cpu().detach().numpy().reshape(-1))
#     truths.append(truth)
#     nr += 1
#
# dataframe = pandas.DataFrame(features)
# dataframe.to_csv('all_features.csv', index=False)
#
# dataframe = pandas.DataFrame(truths)
# dataframe.to_csv('all_truths.csv', index=False)
