
import numpy as np
import pandas as pd
from flask import Flask
from flask import render_template 
from flask import make_response
from scipy.stats import norm
import csv
import matplotlib.pyplot as plt
from datetime import datetime
import io
import base64
from app import app
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

@app.route('/')
def index():
    return '''<center> <h1> <a href="/stats">COV-19 Deaths in the United States</a></h1> </center>'''

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

    return_string = '''<center> <h1> <a href="/plot.png">PLOT IMAGE OF DATA BELOW</a></h1> </center> '''
    for i in range(0,len(the_date)):
        return_string += '<center> <h1>On {}, {} new cases, {} new deaths</h1> </center> \n'.format(the_date[i], cases[i], differences[i])

    return return_string

@app.route('/plot.png')
def display(): 
    the_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    df=pd.read_csv(the_url)

    total_deaths = []
    row_iterator= df.iterrows()

    for index,row in row_iterator:
        total_deaths.append(row["deaths"])
        
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    axis.plot(range(0,len(total_deaths)),total_deaths)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
