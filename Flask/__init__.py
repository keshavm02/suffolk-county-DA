from flask import Flask
app = Flask(__name__) 

import app.py



client = MongoClient("mongodb://127.0.0.1:27017")
db = client.COURT_CASES
cases = db.cases
