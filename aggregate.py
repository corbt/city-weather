import pandas as pd
import numpy as np
import re

data = None

for typ in ["tavg","tmin","tmax"]:
    typ_data = pd.read_csv("data/csv/"+typ+".csv")
    if data is None:
        data = typ_data
    else:
        data = pd.merge(data, typ_data, on=['year','id'])

data.replace(-99.99,np.NaN,inplace=True)
data = data.groupby(by='id').mean().drop('year',axis=1)

index = pd.read_csv("data/csv/tavg-inv.csv")
data = pd.merge(data.reset_index(), index, on=['id']).set_index('id')

# Write file to disk
data.to_csv("data/csv/data.csv")