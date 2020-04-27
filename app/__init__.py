from flask import Flask
import csv
# import seaborn as sns
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
