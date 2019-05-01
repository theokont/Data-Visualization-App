import re
import xml.etree.ElementTree as ET


class Parser:

    def __init__(self, file_name):

        self.tree = ET.parse(file_name)
        self.root = self.tree.getroot()

    def fetch_values(self):

        for sensor_unit in self.root.iter('UNIT'):
            self.unit = sensor_unit.text
            # return self.id
            # print(self.unit)
        for value in self.root.iter('VALUE'):
            self.val = value.text
            # self.int_val = int(self.val)
            # return self.val
            # print(self.int_val)
        for el in self.root.iter('TIME'):
            self.time_stamp = el.text
            self.re_compiled = re.compile(r"(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})")
            self.re_result = self.re_compiled.match(self.time_stamp)
            self.date = self.re_result.group(1)
            self.time = self.re_result.group(2)
            # return self.time_stamp
            # print('Date: {}, Time: {}'.format(self.date, self.time))

        # for table_name in self.root.iter('Site'):
        #     self.name = table_name.attrib['NAME']
        #     # return self.name
        #     print(self.name)

        return self.unit, self.val, self.time_stamp


# if __name__ == '__main__':
#     prs = Parser('dummy.xml')
#     example = prs.fetch_values()
#     print(example)
