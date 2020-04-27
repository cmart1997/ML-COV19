import numpy as np
import pandas as pd
from flask import Flask
from scipy.stats import norm
import csv
# import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
