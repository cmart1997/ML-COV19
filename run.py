
import numpy as np
import pandas as pd
from scipy.stats import norm
import csv
import seaborn as sns
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
df=pd.read_csv(url)

the_date =[]
total_deaths = []
percentage = []
cases = []
total_cases=[]
differences = []
current,current_counts = 0, 0
row_iterator= df.iterrows()

for index,row in row_iterator:
    the_date.append(row["date"])
    total_deaths.append(row["deaths"])
    cases.append(row["cases"] - current_counts)
    differences.append(row["deaths"] - current)
    if current == 0:
        difference = 0
    else:
        difference = ((row["deaths"] - current)/current)*100
    percentage.append(difference)
    current = row["deaths"]
    current_counts = row["cases"]

for i in range(0,len(the_date)):
    print(f"On {the_date[i]}, {cases[i]} new cases, {differences[i]} new death(s).")
    print(f"There has now been a total of {total_deaths[i]} deaths in the USA")
    print(f"Which is {'%.2f' % percentage[i]}% more deaths than the day before. \n")

plt.scatter(range(0,len(total_deaths)),total_deaths)
plt.show()
