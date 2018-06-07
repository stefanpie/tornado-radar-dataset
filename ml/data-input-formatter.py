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


def plot_radial_velocity():
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
        ax.set_title(station_id + " / " + station_name + " / " + time_start + " / " + "{:.4f}".format(
            rounded_elevation_angle) + " degrees")
        ax.set_xlabel('Azimuth angle in degrees: 0 = true north, 90 = east')
        ax.set_ylabel('Distance from radar in km')
        bar = fig.colorbar(im, ticks=range(-70, 75, 5), orientation='horizontal')
        bar.set_label('Radial velocity in m/s')

        fig.show()


def plot_high_resolution_radial_velocity():
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
        title = station_id + " / " + station_name + " / " + time_start + " / " + "{:.2f}".format(
            rounded_elevation_angle) + " degrees" + " / HR"
        ax.set_title(title)
        ax.set_xlabel('Azimuth angle in degrees: 0 = true north, 90 = east')
        ax.set_ylabel('Distance from radar in km')
        bar = fig.colorbar(im, ticks=range(-70, 75, 5), orientation='horizontal')
        bar.set_label('Radial velocity in m/s')

        fig.show()

        # filename = title
        # for c in r'[]/\;,><&*:%=+@!#^()|?^':
        #     filename = filename.replace(c, '')
        # fig.savefig(filename + ".png", dpi=2500)


def plot_high_resolution_spectrum_width():
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
        ax.set_title(station_id + " / " + station_name + " / " + time_start + " / " + "{:.2f}".format(
            rounded_elevation_angle) + " degrees" + " / HR")
        ax.set_xlabel('Azimuth angle in degrees: 0 = true north, 90 = east')
        ax.set_ylabel('Distance from radar in km')
        bar = fig.colorbar(im, ticks=range(-70, 75, 5), orientation='horizontal')
        bar.set_label('Radial velocity in m/s')

        fig.show()


def plot_cross_section(data_product_name):
    # data_products = ['RadialVelocity', 'Reflectivity', 'SpectrumWidth']
    # if data_product_name not in data_products:
    #     raise Exception(str(data_product_name) + " is not a valid data product")

    data_product_key = ''
    if data_product_name == 'RadialVelocity':
        data_product_key = 'V'
    elif data_product_name == 'Reflectivity':
        data_product_key = 'R'
    elif data_product_name == 'SpectrumWidth':
        data_product_key = 'V'
    if data_product_name == 'RadialVelocity_HI':
        data_product_key = 'V_HI'
    elif data_product_name == 'Reflectivity_HI':
        data_product_key = 'R_HI'
    elif data_product_name == 'SpectrumWidth_HI':
        data_product_key = 'V_HI'

    num_of_azimuths = f.dimensions['radial' + data_product_key].size
    for x in range(0, 360, 2):
        azimuth = x
        radar_elevation_above_sea_level = getattr(f, 'StationElevationInMeters')
        radar_tower_height = 0

        earth_radius_meters = 6378137

        elevation_angles = []
        for elevation in range(f.dimensions['scan' + data_product_key].size):
            elevation_angle = f.variables['elevation' + data_product_key][elevation]
            # angle = stats.mode((f.variables['elevationV'][elevation_index]), axis=None)[0][0]
            elevation_angle = np.mean(elevation_angle)
            elevation_angle = round(elevation_angle, 2)
            elevation_angles.append(elevation_angle)
        elevation_angles = np.array(elevation_angles)

        gates = np.array(f.variables['distance' + data_product_key])

        data_product = f.variables[data_product_name]
        data_product = np.array(data_product)
        data_product[data_product == 0] = np.nan
        data_product[data_product == 1] = np.nan
        data_product = data_product / f.variables[data_product_name].scale_factor


        data_at_elevations = []
        for elevation_index in range(f.dimensions['scan' + data_product_key].size):
            angles = np.array(f.variables['azimuth' + data_product_key][elevation_index])
            min_index = np.argmin(angles)
            offset = azimuth+min_index
            if offset >= len(angles):
                offset -= len(angles)
            data_at_elevation = data_product[elevation_index][offset]
            data_at_elevations.append(data_at_elevation)
        data_at_elevations = np.array(data_at_elevations)

        azimuth_data = np.array(f.variables['azimuth' + data_product_key])
        for i in range(f.dimensions['scan' + data_product_key].size):
            angles = azimuth_data[i]
            min_index = np.argmin(angles)
            azimuth_data[i] = np.roll(angles, min_index * -1)
        avg_azimuth_data = np.mean(azimuth_data, axis=0)



        heights = []
        distances = []
        for i in range(len(elevation_angles)):
            heights_at_angle = []
            distances_at_angle = []
            for j in range(len(gates)):
                b = (earth_radius_meters + radar_tower_height)
                c = gates[j]
                a = math.sqrt(b**2 + c**2 - (2 * b * c * math.cos(math.radians(90 + elevation_angles[i]))))
                h = a - earth_radius_meters
                heights_at_angle.append(h)

                theta_at_core = math.asin((gates[j] * math.sin(math.radians(90 + elevation_angles[i])) / a))
                distance = theta_at_core * earth_radius_meters
                distances_at_angle.append(distance)

            heights.append(heights_at_angle)
            distances.append(distances_at_angle)
        heights = np.array(heights) / 1000
        distances = np.array(distances) / 1000

        fig, ax = plt.subplots()
        ax.set_xlim(0, 200)
        ax.set_ylim(0, 30)
        ax.pcolormesh(distances, heights, data_at_elevations)
        for i in range(len(data_at_elevations)):
            ax.plot(distances[i], heights[i], label="{:.2f}".format(elevation_angles[i]), linestyle='--', linewidth = 1)
        ax.legend(loc="upper right", title="Elevation Angles", fancybox=True, ncol=2)
        ax.set_xlabel('Distance Down Range from Radar Site (km)')
        ax.set_ylabel('Perpendicular Altitude Above the Earth (km)')
        title = "Cross Section / " + "{:.2f}".format(avg_azimuth_data[azimuth]) + "° / " + str(data_product_name)
        ax.set_title(str(title))
        # fig.show()
        fig.savefig("{:.2f}".format(avg_azimuth_data[azimuth]) + '.png')
        print(azimuth)



plot_cross_section('Reflectivity')

