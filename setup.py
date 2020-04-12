from flask import Flask, request, redirect, url_for, flash, render_template 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from setuptools import setup

setup(
    name='Flask',
    packages=['Flask'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)

'''
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
'''