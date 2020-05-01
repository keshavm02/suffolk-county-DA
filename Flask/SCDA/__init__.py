from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__) 

from SCDA import config 

db = SQLAlchemy(app)
database_name = 'constituents'
migrate = Migrate(app,db)

from SCDA import models, routes


