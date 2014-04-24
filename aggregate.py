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

# The following code reverses the year for the southern hemisphere.
# This allows northern and southern climates to be compared
cols = data.columns
first_months = [col for col in cols if re.match('[1-6]_', col)]
last_months = [col for col in cols if re.match('\d+_', col) and col not in first_months]

south_data = data[data.lat < 0]
first_months_data = south_data[first_months]
south_data[first_months] = south_data[last_months]
south_data[last_months] = first_months_data

data.loc[south_data.index] = south_data

# Write file to disk
data.to_csv("data/csv/data.csv")