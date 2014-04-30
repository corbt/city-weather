import os, sys, json
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
import pandas as pd

data = pd.read_csv("data/csv/categories.csv")


kml = KML.kml(KML.Document(KML.Style(KML.LabelStyle(KML.scale(6)), id="big_label")))

cat_colors = ['ff1400BE','ff14F01E','ffB41E14','ff0A78F0','ff7800F0','ffB4FF14','ff14F0FF','ff143C82','ffffffff','ff143C0A']
for category,color in zip(data['category'].unique(),cat_colors):
    kml.Document.append(
        KML.Style(
            KML.IconStyle(
                KML.color(color),
                KML.scale(4),
                KML.Icon(KML.href("http://maps.google.com/mapfiles/kml/pal2/icon18.png"))
            ),
        id=str(category)))

for index,row in data.iterrows():
    # print row['name']
    kml.Document.append(
        KML.Placemark(
            KML.name(row['name']),
            KML.styleUrl("#"+str(row['category'])),
            KML.Point(
                KML.coordinates('{0},{1},0'.format(row['long'],row['lat'])))))

with open('/media/sf_virtual_share/stations.kml', 'w') as f:
    f.write(etree.tostring(etree.ElementTree(kml),pretty_print=True))

print "{0} placemarks".format(len(data))