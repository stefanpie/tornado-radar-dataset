import csv
import nexradaws
import datetime

conn = nexradaws.NexradAwsInterface()

with open('processed_data.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	
	for i, row in enumerate(reader):
		begin = datetime.datetime.strptime(row['BEGIN_DATE_TIME'], "%Y-%m-%dT%H:%M:%SZ")
		end = datetime.datetime.strptime(row['END_DATE_TIME'], "%Y-%m-%dT%H:%M:%SZ")
		radar = row['NEAREST_RADAR_STATION']
		strength = row['TOR_F_SCALE']
		# print(begin, " : ", end, " : ", radar, " : ", strength)
		scans = []

		if (strength in "F4 F5 EF4 EF5"):
			print(begin, " : ", end, " : ", radar, " : ", strength)
			if (radar in conn.get_avail_radars(begin.strftime("%Y"), begin.strftime("%m"), begin.strftime("%d"))):
				scans = conn.get_avail_scans_in_range(begin, end, radar)
			print(scans)
			print()