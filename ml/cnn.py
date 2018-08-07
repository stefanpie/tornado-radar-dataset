import keras
from keras.models import Sequential
from keras.layers import Input, Dense, Activation, Conv2D, MaxPooling2D, Flatten, Dropout

import netCDF4
import random
import os
import glob
import json

import numpy as np
from matplotlib import pyplot as plt

from skimage.transform import rescale, resize, downscale_local_mean

print(keras.__version__)


def load_data_from_file(file_path):
    f = netCDF4.Dataset(file_path, 'r')
    # print(f.data_model)
    #
    # for name in f.ncattrs():
    #     print("Global attr", name, "=", getattr(f, name))
    #
    # print(f.dimensions['scanV'])
    # print(f.dimensions['gateV'])
    # print(f.dimensions['radialV'])
    #
    # print(f.variables['azimuthV'])
    # print(f.variables['distanceV'])
    # print(f.variables['elevationV'])
    # print(f.variables['numGatesV'])
    # print(f.variables['numRadialsV'])
    # print(f.variables['timeV'])
    # print(f.variables['RadialVelocity'])

    station_id = getattr(f, 'Station')
    station_name = getattr(f, 'StationName')
    time_start = getattr(f, 'time_coverage_start')
    station_lat = getattr(f, 'StationLatitude')
    station_lon = getattr(f, 'StationLongitude')

    elevation = 0

    elevation_angle = f.variables['elevationV'][elevation]
    elevation_angle = np.mean(elevation_angle)
    rounded_elevation_angle = round(elevation_angle, 2)

    spectrum_width_at_elevation = f.variables['RadialVelocity'][elevation]
    spectrum_width_at_elevation = np.array(spectrum_width_at_elevation)
    spectrum_width_at_elevation[spectrum_width_at_elevation == 0] = np.nan
    spectrum_width_at_elevation[spectrum_width_at_elevation == 1] = np.nan
    # lowest_angle = (lowest_angle + f.variables['RadialVelocity'].add_offset) * f.variables['RadialVelocity'].scale_factor
    spectrum_width_at_elevation = spectrum_width_at_elevation / f.variables['RadialVelocity'].scale_factor
    spectrum_width_at_elevation = spectrum_width_at_elevation.transpose()

    gates = np.array(f.variables['distanceV'])
    gates = gates / 1000
    # for i in range(len(gates)):
    #     gates[i] = gates[i] * math.cos(elevation_angle)
    #     if gates[i] < 0:
    #         gates[i] *= -1

    angles = np.array(f.variables['azimuthV'][elevation])
    min_index = np.argmin(angles)
    angles = np.roll(angles, min_index * -1)
    spectrum_width_at_elevation = np.roll(spectrum_width_at_elevation, min_index * -1, axis=1)

    # print(spectrum_width_at_elevation.shape)
    return spectrum_width_at_elevation


def generate_arrays_from_files(path, batch_size):
    EF1_dir = path + '/data/EF1'
    EF3_dir = path + '/data/EF3'

    EF1_paths = list()
    for root, dirs, files in os.walk(EF1_dir, topdown=False):
        for name in dirs:
            EF1_paths.append(os.path.join(root, name))

    EF3_paths = list()
    for root, dirs, files in os.walk(EF3_dir, topdown=False):
        for name in dirs:
            EF3_paths.append(os.path.join(root, name))

    random.shuffle(EF1_paths)
    random.shuffle(EF3_paths)

    data_paths = EF1_paths + EF3_paths

    random.shuffle(data_paths)

    data_len = len(data_paths)
    file_index = 0

    while True:
        inputs = []
        outputs = []

        if file_index >= data_len:
            file_index = 0

        for i in range(batch_size):
            input_file_path = glob.glob(data_paths[file_index] + "/*.nc")[0]

            input = load_data_from_file(input_file_path)

            input = np.array(resize(input, (2000, 360)))


            output_file = glob.glob(data_paths[file_index] + "/*.json")[0]

            with open(output_file) as f:
                data = json.load(f)

            output = data['TOR_F_SCALE']

            if output == 'EF3':
                output = 1
            elif output == "EF1":
                output = 0

            inputs.append(input)
            outputs.append(output)

            # yield input, output


            file_index = file_index + 1

        inputs = np.array(inputs)
        outputs = np.array(outputs)

        yield (inputs, outputs)


model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(2000, 360, 1)))

model.add(Conv2D(64, (3, 3), activation='relu'))

model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(1, activation='softmax'))

model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# model.fit_generator(generate_arrays_from_files(r'C:\Users\stefan\Desktop\radar_data', 10), steps_per_epoch=100, epochs=10, verbose=2)

# score = model.evaluate_generator(generate_arrays_from_files(r'C:\Users\stefan\Desktop\radar_data', 10), verbose=1)
#
# print('Test loss:', score[0])
# print('Test accuracy:', score[1])

g = generate_arrays_from_files(r'C:\Users\stefan\Desktop\radar_data', 10)

print(next(g)[0])