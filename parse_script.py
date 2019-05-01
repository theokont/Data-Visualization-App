"script me to opoio tha kanw parse ola ta xml arxeia kai insert"
from create_db import Database
from parse_data import Parser
import os
from datetime import date, time, datetime
import pprint


dir_path = os.path.dirname(os.path.realpath(__file__))
data = []
db = Database("sensor_data.db")

for subdir, dirs, files in os.walk(dir_path):
    for file in files:
        filepath = subdir + os.path.sep + file

        if filepath.endswith(".xml"):
            prs = Parser(filepath)
            data.append(prs.fetch_values())


data.sort(key=lambda date: datetime.strptime(date[2], "%Y-%m-%dT%H:%M:%S.0%fZ"))
pp = pprint.PrettyPrinter(indent=2)
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
