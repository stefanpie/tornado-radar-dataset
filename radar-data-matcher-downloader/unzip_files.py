import gzip
import os
import shutil
import re
import sys


data_dir_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop', 'radar_data')
gz_match = re.compile('.gz')

total_files = 0
for root, dirs, files in os.walk(data_dir_path):
    for file in files:
        if file.endswith(".gz"):
             total_files += 1

files_processed = 0

print(total_files, " files to process")

for root, dirs, files in os.walk(data_dir_path):
    for file in files:
        if file.endswith(".gz"):

            gz_file_path = os.path.join(root, file)
            nexrad_file_path = gz_match.sub('.nexrad', gz_file_path)

            with open(gz_file_path, 'rb') as f_in, gzip.open(nexrad_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out, 512*1024)

            files_processed += 1
            percent_complete = (files_processed / total_files) *100

            print("New file written: " + nexrad_file_path)
            print("{0:.2f}".format(percent_complete) + "%")