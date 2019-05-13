"script me to opoio tha kanw parse ola ta xml arxeia kai insert"
from create_db import Database
from parse_data import Parser
import os
from datetime import date, time, datetime
import pprint
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
data = []
db = Database("sensor_data.db")
db.clear_table("sensor")
mode = 0
# sensor_name = None
# Searches the current directory and every one below for every file that ends with .xml and parses it

for subdir, dirs, files in os.walk(dir_path):
    for file in files:
        filepath = subdir + os.path.sep + file

        if filepath.endswith(".xml"):
            prs = Parser(filepath)
# Adds only the files that have UNIT = CM because the file with xmls contains more data from other
# sensors while it shouldn't, also fixes timestamp to isoformat (will be removed later probably) prs.fetch_values()[0] == "CM"
            if len(prs.fetch_values()[2]) == 28:
                mode = 1
                datetime_fixed = prs.fetch_values()[2][0:20] + prs.fetch_values()[2][21:28]
                fetched_values = [prs.fetch_values()[0], prs.fetch_values()[1], datetime_fixed]
                data.append(fetched_values)
            elif len(prs.fetch_values()[2]) == 27:
                mode = 2
                data.append(prs.fetch_values())
            else:
                pass
            # if prs.fetch_values()[0] == "CM" and not sensor_name:
            #     sensor_name = prs.fetch_name()

if mode == 1:
    data.sort(key=lambda x: datetime.strptime(x[2], "%Y-%m-%dT%H:%M:%S.0%fZ"))
elif mode == 2:
    data.sort(key=lambda x: datetime.strptime(x[2], "%Y-%m-%dT%H:%M:%S.%fZ"))
else:
    print("ERROR : datetime format is not correct")
# pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(data)

for values in data:
    db.insert_values("sensor", values)

# sensor_date = "2015-10-26T11:40:33.0000000Z"

# T%H:%M:S.0%fZ datetime.datetime.strptime("2008-09-03T20:56:35.450686Z", "%Y-%m-%dT%H:%M:%S.%fZ")
# # not official iso format, exei 7 digits gia ta microseconds anti gia 6..
# new = datetime.strptime(sensor_date, "%Y-%m-%dT%H:%M:%S.0%fZ")
# print(new)

# new = datetime.fromisoformat(sensor_date)
# print(new)
#
# new1 = datetime.now().isoformat()
# print(new1)
#
# new2 = datetime.strptime(new1, "%Y-%m-%dT%H:%M:%S.%f")
# print(new2)
