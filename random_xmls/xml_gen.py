import xml.etree.cElementTree as ET
from datetime import datetime, timedelta

# "%Y-%m-%dT%H:%M:%S.0%fZ"
t = timedelta(minutes=60)
date_only = datetime.now().date()
date_only.strftime("%Y-%m-%d")
time_only = datetime.now().time()
time_only.strftime("H:%M:%S.0%fZ")
utc_time = str(date_only)+'T'+str(time_only) + 'Z'
date_list = []
date_list.append(utc_time)

for i in range(1000):

    time_obj = datetime.strptime(date_list[-1], "%Y-%m-%dT%H:%M:%S.%fZ")
    time = time_obj + t
    time_date_only = time.date()
    time_date_only.strftime("%Y-%m-%d")
    time_time_only = time.time()
    time_time_only.strftime("H:%M:%S.0%fZ")
    final_time = str(time_date_only)+'T'+str(time_time_only) + 'Z'
    date_list.append(final_time)

    root = ET.Element("ALPINE_MEASUREMENT")
    site = ET.Element("Site", name="ALPINE_KASTORIA")
    node = ET.Element("NODE", address="0013A20040A56FE9")
    register = ET.Element("REGISTER")

    site = ET.SubElement(root, "SITE", name="ALPINE_KASTORIA")
    node = ET.SubElement(site, "NODE", address="0013A20040A56FE9")
    register = ET.SubElement(node, "REGISTER")
    id = ET.SubElement(register, "ID", reg="10")

    ET.SubElement(id, "TYPE").text = "Distance_Sensor"
    ET.SubElement(id, "UNIT").text = "CM"
    ET.SubElement(id, "NAME").text = "Alpine_K81_Height"
    ET.SubElement(id, "VALUE").text = str(i+100)
    ET.SubElement(id, "VARIABLETYPE").text = "xs:double"
    ET.SubElement(id, "TIME").text = final_time

    tree = ET.ElementTree(root)
    tree.write("filename %s.xml" % i)
