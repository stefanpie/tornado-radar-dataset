import csv
import nexradaws
import datetime

conn = nexradaws.NexradAwsInterface()
# print(conn.get_avail_years())
# print(conn.get_avail_months('2013'))
# print(conn.get_avail_days('2013', '05'))
# print(conn.get_avail_radars('2013', '05', '31'))
# print(conn.get_avail_scans('2013', '05', '31', 'KTLX'))

# from datetime import datetime
# radarid = 'KAMX'
# start = datetime(2015,1,30,00,00)
# end = datetime(2015,1,30,1,00)
# print(conn.get_avail_scans_in_range(start, end, radarid))

with open('processed_data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):

        begin = datetime.datetime.strptime(row['BEGIN_DATE_TIME'], "%Y-%m-%dT%H:%M:%SZ")
        end = datetime.datetime.strptime(row['END_DATE_TIME'], "%Y-%m-%dT%H:%M:%SZ")
        radar = row['NEAREST_RADAR_STATION']
        strength = row['TOR_F_SCALE']
        print(begin, " : ", end, " : ", radar, " : ", strength)
        scans = []
        if(radar in conn.get_avail_radars(begin.strftime("%Y"), begin.strftime("%m"), begin.strftime("%d"))):
            scans = conn.get_avail_scans_in_range(begin, end, radar)

        print(scans)
        print()

        if (i >= 100):
            break
