
import numpy as np
import pandas as pd
from scipy.stats import norm
import csv
import io
import requests
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()

url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"

# s=requests.get(url).content
# df=pd.read_csv(io.StringIO(s.decode('utf-8')))
df=pd.read_csv(url)
# fig,ax = plt.subplots()

x =[]
y = []
for index,row in df.iterrows():
    x.append(row["date"])
    y.append(row["deaths"])
plt.scatter(x,y)
plt.show()
