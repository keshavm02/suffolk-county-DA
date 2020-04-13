from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__) 

from SCDA import routes,config

db = SQLAlchemy(app)
migrate = Migrate(app,db)


class temporaryModel(db.Model):
    __tablename__ = 'TEST'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Constituent {self.name}>"




