
import numpy as np
import pandas as pd
from flask import Flask, render_template, make_response
import csv
import matplotlib.pyplot as plt
from datetime import datetime
import io
from app import app
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

@app.route('/')
def index():
    return render_template('index.html')

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

    return_string = '''<center> <h1> <a href="/caseplot.png">PLOT IMAGE OF CASE DATA BELOW</a></h1> </center> <br>
    <center> <h1> <a href="/deathplot.png">PLOT IMAGE OF DEATH DATA BELOW</a></h1> </center>  <br> <br> 
    '''
    for i in range(0,len(the_date)):
        return_string += '<center> <h1>On {}, {} new cases, {} new deaths</h1> </center> \n'.format(the_date[i], cases[i], differences[i])

    return return_string

@app.route('/caseplot.png')
def display(): 
    the_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    df=pd.read_csv(the_url)

    total_cases = []
    row_iterator= df.iterrows()
    last = reversed(df["cases"])

    for index,row in row_iterator:
        if row["cases"] > 20000:
            total_cases.append(row["cases"] / 10) 

    fig = Figure()
    fig.suptitle('Total Cases In USA (COV-19)', fontsize=18)
    axis = fig.add_subplot(1, 1, 1)

    x = range(0,len(total_cases))
    y = total_cases
    # xp = np.linspace(0, 7, 100000)
    # p3 = np.poly1d(np.polyfit(x, y, 3))

    axis.scatter(x, y)   
    # m, b = np.polyfit(x, y, 1)

    # axis.plot(range(0,len(y)), p3(y), c='r')
    # axis.plot(x, m*x + b)
    axis.set_xlabel('nth day since 20,000 cases first reported', fontsize=9)
    axis.set_ylabel('total amount of cases (multiply by 10)', fontsize=9)
    # plt.xlim(xmin=20)
    
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


@app.route('/deathplot.png')
def show(): 
    the_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    df=pd.read_csv(the_url)

    total_deaths = []
    the_date =[]
    row_iterator= df.iterrows()
    last = reversed(df["deaths"])

    for index,row in row_iterator:
        if row["deaths"] > 100:
            the_date.append(row["date"])
            total_deaths.append(row["deaths"]) 

    fig = Figure()
    fig.suptitle('Total Deaths In USA (COV-19)', fontsize=27)
    axis = fig.add_subplot(1, 1, 1)

    x = range(0,len(total_deaths))
    y = total_deaths
    # xp = np.linspace(0, 7, 100000)
    # p3 = np.poly1d(np.polyfit(x, y, 3))

    axis.scatter(x, y)   
    # m, b = np.polyfit(x, y, 1)

    # axis.plot(range(0,len(y)), p3(y), c='r')
    # axis.plot(x, m*x + b)
    axis.set_xlabel('nth day since the 100th death', fontsize=18)
    axis.set_ylabel('total amount of deaths', fontsize=16)
    # plt.xlim(xmin=20)
    
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response