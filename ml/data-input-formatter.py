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

for x in range(len(f.variables['RadialVelocity'])):
    lowest_angle = f.variables['RadialVelocity'][x]

    lowest_angle = np.array(lowest_angle)
    print(lowest_angle)

    lowest_angle = lowest_angle.transpose()

    lowest_angle[lowest_angle == 0] = np.nan
    lowest_angle[lowest_angle == 1] = np.nan

    gates = f.variables['distanceV']
    angles = np.linspace(0, 360, 360)
    # angles = f.variables['azimuthV'][x]

    lowest_angle[lowest_angle == 0] = np.nan
    lowest_angle[lowest_angle == 1] = np.nan

    r, theta = np.meshgrid(gates, angles)
    print(theta)

    plt.pcolormesh(angles, gates, lowest_angle, polar=True)
    plt.colorbar()  # need a color bar to show the intensity scale
    plt.show()  # boom
