import numpy as np
import pandas as pd
import re
from sklearn.cluster import MiniBatchKMeans

def reverse_south(dataset):
    # The following code reverses the year for the southern hemisphere.
    # This allows northern and southern climates to be compared
    cols = dataset.columns
    first_months = [col for col in cols if re.match('[1-6]_', col)]
    last_months = [col for col in cols if re.match('\d+_', col) and col not in first_months]

    south_data = dataset[dataset.lat < 0]
    first_months_data = south_data[first_months]
    south_data[first_months] = south_data[last_months]
    south_data[last_months] = first_months_data

    dataset.loc[south_data.index] = south_data
    return dataset


data = pd.read_csv("data/csv/data.csv").set_index('id')

data = reverse_south(data)
prediction_data = data.drop(['lat','long','name','country'],axis=1).fillna(20)

d = MiniBatchKMeans(n_clusters=10).fit(prediction_data)

data['category'] = d.predict(prediction_data)

data = reverse_south(data)

data.to_csv("data/csv/categories.csv")