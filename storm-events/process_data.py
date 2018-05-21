"""
This script porcesses NOAA Strom Event Details data (csv) files to extact only tornado and waterspout events.
The script outputs the processed data as new csv files.

Author: Stefan Abi-Karam
"""


import os
import pandas as pd


input_dir= "./"

data = []

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.csv'):
            data.append(file)

print(data)

for x in data:
    df = pd.read_csv(x)
    df = df[((df.EVENT_TYPE == "Tornado") | (df.EVENT_TYPE == "Waterspout"))]
    year = df['YEAR'].iloc[0]
    print(year)
    df.to_csv(str(year)+".csv", encoding='utf-8', index=False)