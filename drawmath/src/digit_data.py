import numpy as np
import csv 
from sklearn.preprocessing import LabelBinarizer
import pathlib

"""
https://www.kaggle.com/c/digit-recognizer/data
"""

imagePath = pathlib.Path("src/testImages")

def loadData():
    X = np.zeros((42000, 784))
    y = np.zeros(42000, dtype=int)

    with open(imagePath.joinpath("train.csv")) as f:
        reader = csv.reader(f)
        #first row is the label row
        it = iter(reader)
        next(it)

        for i, line in enumerate(it):
            row = np.array(list(map(float, line[1:])))
            X[i] = row
            #first column contains label
            y[i] = int(line[0])
        
    np.save(imagePath.joinpath("trainX.npy", X))
    np.save(imagePath.joinpath("trainY.npy", y))

def readData():
    X = np.load(imagePath.joinpath("trainX.npy"))
    y = np.load(imagePath.joinpath("trainY.npy"))
    return X,y


def getData():
    """
    42000 images, 42000 labels
    => 40000 training, 2000 validation
    image_size
    #28x28 = 784
    labels are in one-hot presentation

    train_images, train_labels, test_images, test_labels
    """
    X,y = readData()

    #shuffle examples
    perm = np.arange(42000)
    np.random.shuffle(perm)
    X = X[perm]
    y = y[perm]

    X = np.multiply(X, 1.0 / 255.0)
    X = X.reshape(42000, 28,28,1)

    encoder = LabelBinarizer()
    y_one_hot = encoder.fit_transform(y)

    split = 10000
    test_images = X[:split]
    test_labels = y_one_hot[:split]

    train_images = X[split:]
    train_labels = y_one_hot[split:]

    return train_images, train_labels, test_images, test_labels


""" x,y,_,_ = getData()
import matplotlib.pyplot as plt

fig, axs = plt.subplots(4,4)

for i in range(0,4):
    for j in range(0,4):
        axs[i][j].imshow(x[i*4 + j])

plt.show() """

""" x,y,_,_ = getData()
pixels = x.flatten()
print(pixels.min())
print(pixels.max())

import matplotlib.pyplot as plt
plt.hist(pixels)
plt.show() """