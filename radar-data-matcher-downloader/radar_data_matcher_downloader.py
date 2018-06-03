import csv
import datetime
import json
import os

import nexradaws

base_dir = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop', 'radar_data')
print(base_dir)

conn = nexradaws.NexradAwsInterface()

if not os.path.exists(base_dir + '/data/'):
    os.makedirs(base_dir + '/data/')

if not os.path.exists(base_dir + '/data/EF5'):
    os.makedirs(base_dir + '/data/EF5')

if not os.path.exists(base_dir + '/data/EF4'):
    os.makedirs(base_dir + '/data/EF4')

if not os.path.exists(base_dir + '/data/EF3'):
    os.makedirs(base_dir + '/data/EF3')

if not os.path.exists(base_dir + '/data/EF2'):
    os.makedirs(base_dir + '/data/EF2')

if not os.path.exists(base_dir + '/data/EF1'):
    os.makedirs(base_dir + '/data/EF1')

if not os.path.exists(base_dir + '/data/F5'):
    os.makedirs(base_dir + '/data/F5')

if not os.path.exists(base_dir + '/data/F4'):
    os.makedirs(base_dir + '/data/F4')

if not os.path.exists(base_dir + '/data/F3'):
    os.makedirs(base_dir + '/data/F3')

if not os.path.exists(base_dir + '/data/F2'):
    os.makedirs(base_dir + '/data/F2')

if not os.path.exists(base_dir + '/data/F1'):
    os.makedirs(base_dir + '/data/F1')

with open('processed_data.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    for i, row in enumerate(reader):
        begin = datetime.datetime.strptime(row['BEGIN_DATE_TIME'], "%Y-%m-%dT%H:%M:%SZ")
        end = datetime.datetime.strptime(row['END_DATE_TIME'], "%Y-%m-%dT%H:%M:%SZ")
        radar = row['NEAREST_RADAR_STATION']
        strength = row['TOR_F_SCALE']
        print(begin, " : ", end, " : ", radar, " : ", strength)
        scans = []
        if strength in 'F1 F2 F3 F4 F5 EF1 EF2 EF3 EF4 EF5':
            print(begin, " : ", end, " : ", radar, " : ", strength)
            if radar in conn.get_avail_radars(begin.strftime('%Y'), begin.strftime('%m'), begin.strftime('%d')):
                scans = conn.get_avail_scans_in_range(begin, end, radar)
            print(scans)
            if scans:
                path = base_dir + '/data/' + strength + '/' + row['EVENT_ID'] + '/'
                if not os.path.exists(path):
                    os.makedirs(path)
                    with open(path + row['EVENT_ID'] + '.json', 'w') as outfile:
                        json.dump(row, outfile)
                    results = conn.download(scans, path)
                    print(results)
            print()
