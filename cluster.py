import numpy as np
import pandas as pd
import re

from sklearn.cluster import MiniBatchKMeans
# from sklearn import metrics
# from sklearn.preprocessing import StandardScaler


data = pd.read_csv("data/csv/data.csv").set_index('id')

# print pd.isnull(data.drop(['lat','long','name','country'],axis=1)).any(1).nonzero()[0]

prediction_data = data.drop(['lat','long','name','country'],axis=1).fillna(20)

d = MiniBatchKMeans(n_clusters=10).fit(prediction_data)

data['category'] = d.predict(prediction_data)

data.to_csv("data/csv/categories.csv")