import matplotlib.pyplot as plt
import netCDF4
import numpy as np
import math
from scipy import signal

f = netCDF4.Dataset('test1.nc', 'r')
print(f.data_model)

for name in f.ncattrs():
    print("Global attr", name, "=", getattr(f, name))

print(f.dimensions['scanV'])
print(f.dimensions['gateV'])
print(f.dimensions['radialV'])

print(f.variables['azimuthV'])
print(f.variables['distanceV'])
print(f.variables['elevationV'])
print(f.variables['numGatesV'])
print(f.variables['numRadialsV'])
print(f.variables['timeV'])
print(f.variables['RadialVelocity'])

station_id = getattr(f, 'Station')
station_name = getattr(f, 'StationName')
time_start = getattr(f, 'time_coverage_start')

for elevation in range(f.dimensions['scanV'].size):
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

    fig, ax = plt.subplots()
    im = ax.pcolormesh(angles, gates, spectrum_width_at_elevation)  # if you want contour plot
    ax.set_title(station_id + " / " + station_name + " / " + time_start + " / " + "{:.4f}".format(rounded_elevation_angle) + " degrees")
    ax.set_xlabel('Azimuth angle in degrees: 0 = true north, 90 = east')
    ax.set_ylabel('Distance from radar in km')
    bar = fig.colorbar(im, ticks=range(-70, 75, 5), orientation='horizontal')
    bar.set_label('Radial velocity in m/s')

    #fig.show()

for elevation in range(f.dimensions['scanV_HI'].size):
    elevation_angle = f.variables['elevationV_HI'][elevation]
    elevation_angle = np.mean(elevation_angle)
    rounded_elevation_angle = round(elevation_angle, 2)

    spectrum_width_at_elevation = f.variables['RadialVelocity_HI'][elevation]
    spectrum_width_at_elevation = np.array(spectrum_width_at_elevation)
    spectrum_width_at_elevation[spectrum_width_at_elevation == 0] = np.nan
    spectrum_width_at_elevation[spectrum_width_at_elevation == 1] = np.nan
    # lowest_angle = (lowest_angle + f.variables['RadialVelocity'].add_offset) * f.variables['RadialVelocity'].scale_factor
    spectrum_width_at_elevation = spectrum_width_at_elevation / f.variables['RadialVelocity_HI'].scale_factor
    spectrum_width_at_elevation = spectrum_width_at_elevation.transpose()

    gates = np.array(f.variables['distanceV_HI'])
    gates = gates / 1000

    angles = np.array(f.variables['azimuthV_HI'][elevation])
    min_index = np.argmin(angles)
    angles = np.roll(angles, min_index * -1)
    spectrum_width_at_elevation = np.roll(spectrum_width_at_elevation, min_index * -1, axis=1)

    fig, ax = plt.subplots()
    im = ax.pcolormesh(angles[:], gates[:], spectrum_width_at_elevation[:])  # if you want contour plot
    title = station_id + " / " + station_name + " / " + time_start + " / " + "{:.2f}".format(rounded_elevation_angle) + " degrees" + " / HR"
    ax.set_title(title)
    ax.set_xlabel('Azimuth angle in degrees: 0 = true north, 90 = east')
    ax.set_ylabel('Distance from radar in km')
    bar = fig.colorbar(im, ticks=range(-70, 75, 5), orientation='horizontal')
    bar.set_label('Radial velocity in m/s')
    filename = title
    for c in r'[]/\;,><&*:%=+@!#^()|?^':
        filename = filename.replace(c, '')
    fig.show()
    fig.savefig(filename + ".png", dpi=2500)

for elevation in range(f.dimensions['scanV_HI'].size):
    elevation_angle = f.variables['elevationV_HI'][elevation]
    elevation_angle = np.mean(elevation_angle)
    rounded_elevation_angle = round(elevation_angle, 2)

    spectrum_width_at_elevation = f.variables['SpectrumWidth_HI'][elevation]
    spectrum_width_at_elevation = np.array(spectrum_width_at_elevation)
    spectrum_width_at_elevation[spectrum_width_at_elevation == 0] = np.nan
    spectrum_width_at_elevation[spectrum_width_at_elevation == 1] = np.nan
    # lowest_angle = (lowest_angle + f.variables['RadialVelocity'].add_offset) * f.variables['RadialVelocity'].scale_factor
    spectrum_width_at_elevation = spectrum_width_at_elevation / f.variables['SpectrumWidth_HI'].scale_factor
    spectrum_width_at_elevation = spectrum_width_at_elevation.transpose()



    gates = np.array(f.variables['distanceV_HI'])
    gates = gates / 1000

    angles = np.array(f.variables['azimuthV_HI'][elevation])
    min_index = np.argmin(angles)
    angles = np.roll(angles, min_index * -1)
    spectrum_width_at_elevation = np.roll(spectrum_width_at_elevation, min_index * -1, axis=1)


    fig, ax = plt.subplots()
    im = ax.pcolormesh(angles[:], gates[:], spectrum_width_at_elevation[:])  # if you want contour plot
    ax.set_title(station_id + " / " + station_name + " / " + time_start + " / " + "{:.2f}".format(rounded_elevation_angle) + " degrees" + " / HR")
    ax.set_xlabel('Azimuth angle in degrees: 0 = true north, 90 = east')
    ax.set_ylabel('Distance from radar in km')
    bar = fig.colorbar(im, ticks=range(-70, 75, 5), orientation='horizontal')
    bar.set_label('Radial velocity in m/s')

    fig.show()


# elevation_angle = 0
#
# data_at_elevations =  []
# for x in range(f.dimensions['scanV'].size):
#     data_at_elevation = np.array(f.variables['RadialVelocity'][x][1])
#     data_at_elevations.append(np.array(data_at_elevation))
# data_at_elevations = np.array(data_at_elevations)
#
# elevation_angles = []
# for elevation in range(f.dimensions['scanV'].size):
#     elevation_angle = f.variables['elevationV'][elevation]
#     #angle = stats.mode((f.variables['elevationV'][x]), axis=None)[0][0]
#     elevation_angle = np.mean(elevation_angle)
#     elevation_angle = round(elevation_angle, 2)
#     elevation_angles.append(elevation_angle)
# elevation_angles = np.array(elevation_angles)

