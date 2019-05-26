import xml.etree.ElementTree as ET


class Parser:

    def __init__(self, file_name):

        self.tree = ET.parse(file_name)
        self.root = self.tree.getroot()

    def fetch_values(self):

        for sensor_unit in self.root.iter('UNIT'):
            self.unit = sensor_unit.text

        for value in self.root.iter('VALUE'):
            self.val = value.text

        for el in self.root.iter('TIME'):
            self.time_stamp = el.text

        return self.unit, self.val, self.time_stamp

    def fetch_name(self):
        for sensor_name in self.root.iter('NAME'):
            self.name = sensor_name.text
        return self.name
