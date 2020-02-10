import os
import json
from bson import ObjectId
from pymongo import MongoClient
from extract_text.extract_text import *
from extract_text.extract_fields import *
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = 'uploads'
UPLOAD_JSON = 'json'
UPLOAD_FINAL = 'static'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_JSON'] = UPLOAD_JSON
app.config['UPLOAD_FINAL'] = UPLOAD_FINAL
app.secret_key = os.urandom(24)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.COURT_CASES
cases = db.cases

#allowed_file adapted from http://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

#route for criminal complaints
@app.route('/CC', methods=['POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        print(request.headers)
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            print('file not in request.files')
            return redirect('/failure')
        file = request.files['file']
        #print(file)
        if file.filename == '':
            flash('/failure')
            print('no file name')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            test_image = ImageReader(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            #images come in oriented wrong, so the following code rotates it the correct way
            image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = image.transpose(Image.ROTATE_270)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],'file_rotated.png'))
            final_image = ImageReader(os.path.join(app.config['UPLOAD_FOLDER'],'file_rotated.png'))

            text = ExtractText(final_image.image)
            doc = text.extract_text()
            print(doc)
            docket_num = find_docket_number(doc)
            subject_name = find_full_name(doc)
            dates = find_dates(doc)
            #the following date variables assume all dates were recorded properly by the scan -- need to fix that assumption
            if(0<len(dates)):
                date_of_birth = dates[0]
            else:
                date_of_birth = 'Not found'
            #date of issued complaint
            if(1<len(dates)):
                complaint_issued = dates[1]
            else:
                complaint_issued = 'Not found'
            #date of offense
            if(2<len(dates)):
                doo = dates[2]
            else:
                doo = 'Not found'
            if(3<len(dates)):
                arrest_date = dates[3]
            else:
                arrest_date = 'Not found'
            if(4<len(dates)):
                next_event_date = dates[4]
            else:
                next_event_date = 'Not found'
            #obtn number
            obtn = find_obtn(doc)
            #address
            address = find_addresses(doc)
            offense_codes = find_codes(doc)
            #incident report number
            irn = str(find_indicent_report(doc))
            print("docket:", docket_num)
            print("name:", subject_name)
            print("obtn:", obtn)
            print("dob:", date_of_birth)
            print("doc:", complaint_issued)
            print("doo:",doo)
            print("doa:", arrest_date)
            print("irn:", irn)
            print("court address:", address['court'])
            print('defendant address:', address['defendant'])
            print('offense codes:', str(offense_codes))
            fields = {'_id': docket_num,'docket': docket_num, 'name': subject_name, 'dob': date_of_birth,'doc':complaint_issued,'doo':doo, 'doa':arrest_date, 'obtn': obtn, 'text': doc, 'irn': irn,
            'court_address':address['court'], 'defendant_address':address['defendant'], 'offense_codes':offense_codes}
            #save the image
            img_filename = os.path.join(app.config['UPLOAD_FINAL'], 'CC', fields['docket']+'_CC.jpg')
            image = image.transpose(Image.ROTATE_90)
            image.save(img_filename)
            fields['img'] = img_filename
            fields_package = json.dumps(fields)
            #check if there is an already existing record, and simply update with the new info
            #set unique case incident report number, and obtn to the scanned values and embed all scanned fields into new document under the case with this docket #
            cases.update_one({'docket':docket_num}, { "$set": {'irn': irn, 'obtn': obtn, 'CC': fields}}, upsert=True)
            #create a new db document if one does not already exist
            return fields_package
        else:
            print('File not valid')
            return redirect('failure')
    return 'Please send a post request with your document picture'

#route for criminal complaint confirmation
@app.route('/confirm_CC', methods=['POST'])
def confirm_CC():
    if request.method == 'POST':
        data = request.form['data']
        print(data)
        img = request.files['image']
        json_name = 'data'
        img_name = secure_filename(img.filename)
        data.save(os.path.join(app.config['UPLOAD_JSON'],json_name))
        with open(os.path.join(app.config['UPLOAD_JSON'], json_name)) as f:
            fields = json.loads(f.read())
            img_filename = os.path.join(app.config['UPLOAD_FINAL'], 'CC', fields['docket']+'_CC.jpg')
            #set unique case incident report number, and obtn to the scanned values and embed all scanned fields into new document under the case with this docket #
            fields['image'] = img_filename
            img.save(img_filename)
            cases.update_one({'docket':fields['docket']},{'$set':{'irn':fields['irn'],'obtn':fields['obtn'],'CC':fields}}, upsert=True)
        os.remove(os.path.join(app.config['UPLOAD_JSON'],json_name))
        #fields = json.loads(data)
        #img_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'CC', fields['docket']+'_CC.jpg')
        #set unique case incident report number, and obtn to the scanned values and embed all scanned fields into new document under the case with this docket #
        #fields['image'] = img_filename
        #img.save(img_filename)
        #cases.update_one({'docket':fields['docket']},{'$set':{'irn':fields['irn'],'obtn':fields['obtn'],'CC':fields}}, upsert=True)
        return json.dumps({'status':'success'})



@app.route('/ABF', methods=['POST'])
def abf():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            print('file not in request.files')
            return redirect('/failure')
        file = request.files['file']
        if file.filename == '':
            flash('/failure')
            print('no file name')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            test_image = ImageReader(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #images come in oriented wrong, so the following code rotates it the correct way
            image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = image.transpose(Image.ROTATE_270)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],'file_rotated.png'))
            final_image = ImageReader(os.path.join(app.config['UPLOAD_FOLDER'],'file_rotated.png'))
            text = ExtractText(final_image.image)
            doc = text.extract_text()
            data = arrest_booking_form(doc)
            print(data)
            cases.update_one({'obtn':data['OBTN']}, { "$set": {'abf':data}}, upsert=True)
            return json.dumps(data)
        else:
            print('File not valid')
            return redirect('failure')
    return 'Please send a post request with your document picture'
#route for application for criminal complaints
@app.route('/ACC', methods=['POST'])
def acc():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            print('file not in request.files')
            return redirect('/failure')
        file = request.files['file']
        #print(file)        
        if file.filename == '':
            flash('/failure')
            print('no file name')
            return redirect(request.url)        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            test_image = ImageReader(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            text = ExtractText(test_image.image)
            doc = text.extract_text()
            #docket number sent in the posted form since it is not on the document itself
            docket_num = request.form.get('docket')
            subject_name = find_name_ACC(doc)
            print(subject_name)
            dates = find_dates(doc)
            #the following date variables assume all dates were recorded properly by the scan -- need to fix that assumption
            #date_of_birth = dates[0]
            print("docket:", docket_num)
            print("name:", subject_name)
            #print("dob:", date_of_birth)
            fields = {'_id': docket_num,'docket': docket_num, 'name': subject_name, 'text': doc}
            fields_package = json.dumps(fields)
            #check if there is an already existing record, and simply update with the new info
            cases.update_one({'docket':docket_num}, { "$set": {'name': subject_name, 'text':doc}}, upsert=True)
            #create a new db document if one does not already exist
            return fields_package
        else:
            print('File not valid')
            return redirect('failure')
    return 'Please send a post request with your document picture'

@app.route('/dockets', methods=['GET'])
def dockets():
    case_list = cases.find({})
    dockets = []
    for case in case_list:
        print(case)
        dockets.append(case['docket'])
    return json.dumps({'dockets': dockets})

#returns a 'master json' which contains all cases keyed by docket number and within each case has all documents
@app.route('/master')
def get_master():
    master_list = list(cases.find({}))
    case_list = {}
    for case in master_list:
        case_list[case['docket']] = case
    return JSONEncoder().encode(case_list)

#web page to display all documents
@app.route('/all_cases')
def case_page():
    master_list = list(cases.find({}))
    case_list = {}
    for case in master_list:
        case_list[case['docket']] = case
    return render_template('case_page.html',case_list=case_list)

#web page to display documents for a specific case
@app.route('/<docket_number>')
def display_doc(docket_number):
    docket = docket_number 
    document = dict(cases.find_one({'docket':docket}))
    return render_template('display_doc.html',document=document,docket=docket)
    


@app.route('/success')
def uploaded():
    return 'File successfully uploaded'

@app.route('/failure')
def fail():
    return 'File not uploaded successfully'

if __name__ == '__main__':
    #app.run(host='0.0.0.0', ssl_context=('/home/eric/cert.pem', '/home/eric/key.pem'))
    app.run(host='0.0.0.0')