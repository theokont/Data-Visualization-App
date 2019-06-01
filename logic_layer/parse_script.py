from data_layer.create_db import DatabaseInteraction
from logic_layer.parse_data import Parser
import os
from datetime import datetime


class XMLImporter:

    def __init__(self, db_name, path):
        self.path = path
        self.db = DatabaseInteraction(db_name)

    def import_xml(self):

        dir_path = self.path
        db = DatabaseInteraction(self.db.name)
        db.create_table("sensor")
        data = []
        mode = 0

        # Searches the current directory and every one below for every file that ends with .xml and parses it

        for subdir, dirs, files in os.walk(dir_path):
            for file in files:
                filepath = subdir + os.path.sep + file

                if filepath.endswith(".xml"):
                    prs = Parser(filepath)
        # Adds only the files that have UNIT = CM because the file with xmls contains more data from other
        # sensors while it shouldn't, also fixes timestamp to isoformat (will be removed later probably)
                    if len(prs.fetch_values()[2]) == 28:
                        mode = 1
                        datetime_fixed = prs.fetch_values()[2][0:20] + prs.fetch_values()[2][21:28]
                        fetched_values = [prs.fetch_values()[0], prs.fetch_values()[
                            1], datetime_fixed]
                        data.append(fetched_values)
                    elif len(prs.fetch_values()[2]) == 27:
                        mode = 2
                        data.append(prs.fetch_values())
                    else:
                        pass

        if mode == 1:
            data.sort(key=lambda x: datetime.strptime(x[2], "%Y-%m-%dT%H:%M:%S.0%fZ"))
        elif mode == 2:
            data.sort(key=lambda x: datetime.strptime(x[2], "%Y-%m-%dT%H:%M:%S.%fZ"))
        else:
            print("ERROR : datetime format is not correct")
        if len(data) == 0:
            return False

        for values in data:
            db.insert_values("sensor", values)

        return True
