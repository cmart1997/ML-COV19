import numpy as np
import pandas as pd
from flask import Flask
from scipy.stats import norm
import csv
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__) #create flask app

@app.route('/')
def index():
    return '''<h1> <a href="/stats">COV-19 Deaths in the United States</a></h1>'''

@app.route('/stats')
def print_stats(): 
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

    return_string = ''' '''
    for i in range(0,len(the_date)):
        return_string += '<h1>On {}, {} new cases, {} new deaths</h1> \n'.format(the_date[i], cases[i], differences[i])

    # plt.scatter(range(0,len(total_deaths)),total_deaths)
    # plt.show()
    return return_string

if __name__ == '__main__':
    app.run(debug=True) 
