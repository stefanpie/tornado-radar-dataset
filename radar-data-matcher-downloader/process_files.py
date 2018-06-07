import os
import re
import subprocess

data_dir_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop', 'radar_data')
netcdf_tools_jar_file_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop', 'toolsUI-4.6.jar')

gz_match = re.compile('.gz')
gz_decompress_command_template = "7z elevation_index {} -so > {}"
netcdf_convert_command_template = "java -classpath {} ucar.nc2.FileWriter -in {} -out {}"
netcdf_compressor_command_template = "nccopy -d1 {} {}"

with open("processed_files.txt", "r") as f:
    file_list = f.read()

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
            if not os.path.isfile((gz_match.sub('.nc', os.path.join(root, file)))):
                gz_file_path = os.path.join(root, file)
                nexrad_file_path = gz_match.sub('.nexrad', gz_file_path)

                command = gz_decompress_command_template.format(gz_file_path, nexrad_file_path)
                print(command)
                os.system(command)

                # process = subprocess.call(command)
                # print(process)

                # with gzip.open(gz_file_path, 'rb') as f_in:
                #     with open(nexrad_file_path, 'wb') as f_out:
                #         shutil.copyfileobj(f_in, f_out, length=8*1024)

                print("Unzipped data to: ", nexrad_file_path)
                nc3_file_path = gz_match.sub('.nc3', gz_file_path)

                command = netcdf_convert_command_template.format(netcdf_tools_jar_file_path, nexrad_file_path,
                                                                 nc3_file_path)
                print(command)
                process = subprocess.call(command)
                print(process)

                os.remove(nexrad_file_path)

                nc4_file_path = gz_match.sub('.nc', gz_file_path)

                command = netcdf_compressor_command_template.format(nc3_file_path, nc4_file_path)
                print(command)
                process = subprocess.call(command)
                print(process)

                os.remove(nc3_file_path)

                print("New file processed: " + nc4_file_path)

                with open("processed_files.txt", "a+") as f:
                    f.write(str(file))
                    f.write("\n")

            files_processed += 1
            percent_complete = (files_processed / total_files) * 100
            print("{0:.2f}".format(percent_complete) + "%")
            print()
            print()

f.close()
print("Done")
