import keras
from keras.models import Sequential
from keras.layers import Input, Dense, Activation, Conv2D, MaxPooling2D, Flatten, Dropout

import numpy as np
from matplotlib import pyplot as plt

print(keras.__version__)

np.random.seed(123)  # for reproducibility

model = Sequential()
model.add(Conv2D(32, (8, 8), activation='relu', input_shape=(224, 224, 3)))
