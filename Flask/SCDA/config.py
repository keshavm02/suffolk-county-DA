import os
basedir = os.path.abspath(os.path.dirname(__file__))
#print(basedir)
from SCDA import app


#UPLOAD_FOLDER = os.path.abspath('Flask/SCDA/uploads')
UPLOAD_FOLDER = os.path.relpath('uploads')
UPLOAD_JSON = 'json'
#UPLOAD_FINAL = os.path.abspath('Flask/SCDA/static')
UPLOAD_FINAL = os.path.relpath('static')
#print(UPLOAD_FINAL)


app.config['DEBUG'] = True
#https://docs.sqlalchemy.org/en/13/core/engines.html
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///constituents"
# In future: app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///constituents"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #configuration on startup
app.config['UPLOAD_JSON'] = UPLOAD_JSON
app.config['UPLOAD_FINAL'] = UPLOAD_FINAL

app.secret_key = os.urandom(24)
app.config['DEBUG'] = True
#https://docs.sqlalchemy.org/en/13/core/engines.html
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///constituents"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #configuration on startup
app.config['UPLOAD_JSON'] = UPLOAD_JSON
app.config['UPLOAD_FINAL'] = UPLOAD_FINAL

app.secret_key = os.urandom(24)
app.config['DEBUG'] = True
#https://docs.sqlalchemy.org/en/13/core/engines.html
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///constituents"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #configuration on startup
app.config['UPLOAD_JSON'] = UPLOAD_JSON
app.config['UPLOAD_FINAL'] = UPLOAD_FINAL

app.secret_key = os.urandom(24)
app.config['DEBUG'] = True
#https://docs.sqlalchemy.org/en/13/core/engines.html
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///constituents"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #configuration on startup
app.config['UPLOAD_JSON'] = UPLOAD_JSON
app.config['UPLOAD_FINAL'] = UPLOAD_FINAL

app.secret_key = os.urandom(24)
