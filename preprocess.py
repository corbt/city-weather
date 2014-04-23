from __future__ import division
from glob import glob
import csv,re

for name in glob('data/raw/*.dat'):
    label = name[15:19]
    with open(name) as in_file:
        with open("data/csv/"+label+".csv",'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(["id","year","type","jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"])

            for line in in_file:
                if int(line[11:15]) < 2000:
                    continue
                components = [line[0:11],line[11:15],line[15:19]]
                components += [int(line[19+x*8:24+x*8])/100 for x in range(12)]
                writer.writerow(components)

def title(name):
    return re.sub("([a-z])'([A-Z])", lambda m: m.group(0).lower(), name.title())

cc_file = open('data/raw/country-codes')
ccodes = {l[:3]:title(l[4:].strip()) for l in cc_file}

for name in glob('data/raw/*.inv'):
    label = name[15:19]
    with open(name) as in_file:
        with open("data/csv/"+label+"-inv.csv",'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(["id","lat","long","name","country"])
            for line in in_file:
                if not line[74:79].strip().isdigit() or int(line[74:79]) < 100:
                    continue
                name = title(line[38:68])
                name = name[:name.find("  ")].strip()
                components = [line[0:11],line[12:20],line[21:30],name,ccodes[line[:3]]]
                writer.writerow(components)
