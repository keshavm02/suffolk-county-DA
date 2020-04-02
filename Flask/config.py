
from __init__ import app 




UPLOAD_FOLDER = 'uploads'
UPLOAD_JSON = 'json'
UPLOAD_FINAL = 'static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #configuration on startup
app.config['UPLOAD_JSON'] = UPLOAD_JSON
app.config['UPLOAD_FINAL'] = UPLOAD_FINAL
app.secret_key = os.urandom(24) 

