import os
basedir = os.path.abspath('uploads')
#print(basedir)
#from SCDA import app


UPLOAD_FOLDER = os.path.abspath('uploads')
UPLOAD_JSON = 'json'
UPLOAD_FINAL = os.path.abspath('static')
app.config['DEBUG'] = True

#https://docs.sqlalchemy.org/en/13/core/engines.html
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@localhost/constituents"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #configuration on startup
app.config['UPLOAD_JSON'] = UPLOAD_JSON
app.config['UPLOAD_FINAL'] = UPLOAD_FINAL

app.secret_key = os.urandom(24)
