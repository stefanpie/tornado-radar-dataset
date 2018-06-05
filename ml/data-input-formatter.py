import matplotlib.pyplot as plt
import netCDF4
import numpy as np

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

for x in range(f.dimensions['scanV'].size):
    # TODO figure out how to calculate the right angle of elevation from netcdf file
    angle = np.median(f.variables['elevationV'][x])

    lowest_angle = f.variables['RadialVelocity'][x]
    lowest_angle = np.array(lowest_angle)
    lowest_angle[lowest_angle == 0] = np.nan
    lowest_angle[lowest_angle == 1] = np.nan
    # lowest_angle = (lowest_angle + f.variables['RadialVelocity'].add_offset) * f.variables['RadialVelocity'].scale_factor
    lowest_angle = lowest_angle.transpose()

    gates = np.array(f.variables['distanceV'])
    # angles = np.linspace(0, f.dimensions['radialV'].size-1, f.dimensions['radialV'].size)
    angles = np.array(f.variables['azimuthV'][x])
    min_index = np.argmin(angles)

    angles = np.roll(angles, min_index * -1)
    lowest_angle = np.roll(lowest_angle, min_index * -1, axis=1)

    fig, ax = plt.subplots()
    im = ax.pcolormesh(angles, gates, lowest_angle)  # if you want contour plot
    ax.set_title(station_id + " / " + station_name + " / " + time_start + " / " + "{:.4f}".format(angle) + " degrees")
    ax.set_xlabel('Azimuth angle in degrees: 0 = true north, 90 = east')
    ax.set_ylabel('Distance from radar in meters')
    bar = fig.colorbar(im, ticks=range(-35, 40, 5), orientation='horizontal')
    bar.set_label('Radial velocity in m/s')

    fig.show()
