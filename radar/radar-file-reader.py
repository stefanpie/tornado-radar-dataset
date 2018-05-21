import matplotlib.pyplot as plt
import pyart

# open the file, create the displays and figure
filename = 'KAMX19970512_175328.gz'
radar = pyart.io.read_nexrad_archive(filename)
display = pyart.graph.RadarDisplay(radar)
fig = plt.figure(figsize=(6, 5))