import pandas as pd
from datetime import datetime, timedelta
import arrow
from math import radians, cos, sin, asin, sqrt
import csv


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km


with open('stations.csv') as f:
    radar_station_locations = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

print(radar_station_locations)

df = pd.read_csv('formatted-strom-event-data.csv', delimiter=',')

df.info()

for index, row in df.iterrows():

    print(row["BEGIN_DATE_TIME"], " : ",  row["STATE"], " : ", row["TOR_F_SCALE"])

    # This section is for processing the timestamps to format the date in the iso8061 format and calculate the elapsed time in minutes
    # print(row["BEGIN_DATE_TIME"], row["END_DATE_TIME"], row["CZ_TIMEZONE"])
    hour_offset = 0

    if str(row["CZ_TIMEZONE"]) == "EST":
        hour_offset = 5
    elif str(row["CZ_TIMEZONE"]) == "CST":
        hour_offset = 6
    elif str(row["CZ_TIMEZONE"]) == "MST":
        hour_offset = 7
    elif str(row["CZ_TIMEZONE"]) == "PST":
        hour_offset = 8
    elif str(row["CZ_TIMEZONE"]) == "AST":
        hour_offset = 4
    elif str(row["CZ_TIMEZONE"]) == "HST":
        hour_offset = 10

    begin = arrow.get(str(row["BEGIN_DATE_TIME"]), 'M/D/YYYY H:mm').shift(hours=hour_offset)
    begin_iso8061 = begin.format('YYYY-MM-DDTHH:mm:ss') + "Z"

    end = arrow.get(str(row["END_DATE_TIME"]), 'M/D/YYYY H:mm').shift(hours=hour_offset)
    end_iso8061 = end.format('YYYY-MM-DDTHH:mm:ss') + "Z"

    diff = end - begin
    diff_minutes = diff.seconds / 60

    df.loc[index, 'BEGIN_DATE_TIME'] = begin_iso8061
    df.loc[index, 'END_DATE_TIME'] = end_iso8061
    df.loc[index, 'ELAPSED_TIME_MINUTES'] = diff_minutes


    # This section is for finding the nearest dopplar radar station
    tor_lat = (float(row["BEGIN_LAT"]) + float(row["END_LAT"])) / 2
    tor_lon = (float(row["BEGIN_LON"]) + float(row["END_LON"])) / 2

    distances = []
    for s in radar_station_locations:
        distances.append({'distance': haversine(tor_lon, tor_lat, float(s['LONGITUDE']), float(s['LATITUDE'])), 'station': s})
    nearest_radar_station = min(distances, key=lambda x: x['distance'])['station']
    # print(tor_lat, tor_lon)
    # print(nearest_radar_station)
    df.loc[index, 'NEAREST_RADAR_STATION'] = nearest_radar_station['STATION_ID']


df.to_csv("processed_data.csv", encoding='utf-8', index=False)