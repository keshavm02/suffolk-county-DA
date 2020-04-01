from flask import Flask
from pymongo import MongoClient
from app import *

app = Flask(__name__) 


IMPORT STATEMENTS
import app.py



client = MongoClient("mongodb://127.0.0.1:27017")
db = client.COURT_CASES
cases = db.cases
