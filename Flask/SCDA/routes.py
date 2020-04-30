import sys
sys.path.append('/Users/eloisanitorreda/suffolk-county-DA/Flask/')
import os #allows interaction with operating system and pathing files
import json #allows python dictionaries to be formatted into JSON and vice versa JSON to string
from bson import ObjectId #allows MongoDB to format data
from werkzeug.utils import secure_filename #secure file name given file name
from PIL import Image #package that allows you to give functionality to images
from SCDA import config
from .extract_text.extract_fields import *
from .extract_text.extract_text import *
import filetype
from SCDA import app, models, db
from flask import request, flash, redirect, render_template, send_from_directory
from .extract_routes.database_code import *
from datetime import datetime



ALLOWED_MIMES = {"image/gif", "image/png", "image/jpg", "image/jpeg", "application/pdf"}
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def isFileAllowed(file):
    #print(file)
    try:
        kind = filetype.guess(file)
        print('File extension: %s' % kind.extension)
        print('File MIME type: %s' % kind.mime)
        if kind is None:
            return False
        if kind.mime in ALLOWED_MIMES and kind.extension in ALLOWED_EXTENSIONS:
            return True
        else:
            return False
    except:
        return False


#http://www.programmersought.com/article/68322218798/
class JSONEncoder(json.JSONEncoder):
    def default(self, o):                # pylint: disable=E0202 
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
    
@app.route('/upload', methods=['POST'])
def upload_forms():
    if request.method == 'POST':
        print(request.files)
        form_data = request.files
        form_upload_date = datetime.now()
        uuid = -1
        checkRequiredForms = checkAllRequiredForms(form_data)
        if (not checkRequiredForms[0]):
            return checkRequiredForms[1]
        else:
            acc_file = form_data['acc']
            acc_filename = acc_file.filename
            if acc_filename == "":
                return redirect('failure')
            if isFileAllowed(acc_file):
                acc_filename = secure_filename(acc_filename)
                acc_file = Image.open(acc_file)
                doc, image_path = localUploadAndExtraction(acc_filename, acc_file)
                #FOR TESTING
                doc = open(os.path.expanduser("~/suffolk-county-DA/Flask/SCDA/extract_text/extraction_tests/test_textdumps/Application for Criminal Complaint .txt")).read()
                acc_info = application_for_criminal_complaint(doc)
                #print(acc_info)
                if acc_info["Name"] == '' or acc_info["Date of Birth"] == '' or acc_info["Social Security No."] == '':
                    return "Application for criminal complaint could not be read. Please upload a clearer image."
                else:
                    uuid = getUserID(acc_info["Name"], acc_info["Social Security No."][-4:], acc_info["Date of Birth"])
                    # print(uuid)
                    # store path or actual image?
                    formTable = models.forms(uuid, form_upload_date, form_upload_date, form_upload_date, form_upload_date)
                    acc_insert = models.ACC(uuid, form_upload_date, image_path, acc_info["Summons"], acc_info["Hearing Requested"], acc_info["Court"], acc_info["Arrest Status of Accused"], acc_info["Arrest Date"], acc_info["In Custody"],acc_info["Officer ID No."],acc_info["Agency"],acc_info["Type"],acc_info["Name"],acc_info["Birth Surname"],acc_info["Address"],acc_info["Date of Birth"], acc_info["Place of Birth"], acc_info["Social Security No."], acc_info["PCF No."],acc_info["SID"],acc_info["Marital Status"],acc_info["Driver's License No."],acc_info["Driver's License State"],acc_info["Driver's License Exp. Year"],acc_info["Gender"],acc_info["Race"],acc_info["Height"],acc_info["Weight"],acc_info["Eyes"],acc_info["Hair"],acc_info["Ethnicity"],acc_info["Primary Language"],acc_info["Complexion"],acc_info["Scars/Marks/Tattoos"],acc_info["Employer Name"],acc_info["School Name"],acc_info["Day Phone"],acc_info["Mother Name"],acc_info["Mother Maiden Name"],acc_info["Father Name"],acc_info["Complainant Type"],acc_info["Police Dept."])
                    db.session.add(formTable)
                    db.session.commit()
                    db.session.add(acc_insert)
                    db.session.commit()
                    #REMINDER: MUST HAVE FORMS TABLE BEFORE COMMITTING
                    #db.session.commit()
            cc_file = form_data['cc']
            cc_filename = cc_file.filename
            if cc_filename == "":
                return redirect('failure')
            if isFileAllowed(cc_file):
                cc_filename = secure_filename(cc_filename)
                cc_file = Image.open(cc_file)
                doc, image_path = localUploadAndExtraction(cc_filename, cc_file)
                cc_info = criminal_complaint(doc)
                #print(cc_info["court_address"])
                cc_insert = models.CC(uuid, form_upload_date, image_path, cc_info["docket"], cc_info["name"], cc_info["dob"], cc_info["doc"], 
                         cc_info["doo"], cc_info["doa"], cc_info["ned"], cc_info["obtn"], cc_info["irn"], cc_info["court_address"], 
                         cc_info["defendant_address"], cc_info["offense_codes"])
                db.session.add(cc_insert)
                db.session.commit()
            ir_file = form_data['ir']
            ir_filename = ir_file.filename
            if ir_filename == "":
                return redirect('failure')
            if isFileAllowed(ir_file):
                ir_filename = secure_filename(ir_filename)
                ir_file = Image.open(ir_file)
                doc, image_path = localUploadAndExtraction(ir_filename, ir_file)
                ir_info = incident_report(doc)
                ir_insert = models.IR(uuid, form_upload_date, image_path, ir_info["Case Number"],ir_info["CAD Incident Number"],ir_info["Report Type"],ir_info["Date / Time Occurred"],ir_info["Date / Time Reported"],ir_info["Public Narrative"])
                db.session.add(ir_insert)
                db.session.commit()
            else:
                return redirect('failure')
            #test = 1
            addOptional = addOptionalForms(form_data, uuid, formTable, form_upload_date)
            print(addOptional)
            if not addOptional:
                return redirect('failure')
            return redirect('success')
    return 'Please send a post request with at least the following forms: Application for Criminal Complaint, Criminal Complaint, Incident Report.'
            

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                                filename)

#route for criminal complaints
@app.route('/CC', methods=['POST'])
def Criminal_Complaint_Post():
    print("RECIEVING REQUEST 1")
    if request.method == 'POST':
        #print(request)
        #print(request.form)
        #print(request.headers)
        print(request.files)
        print(request.data)
        if 'file' not in request.files:
            flash('No file part')
            print('file not in request.files')
            print('REDIRECT LINK')
            return redirect('/failure')
        file = request.files['file']
        if file.filename == '':
            flash('/failure')
            print('no file name')
            print('HIT REDIRECT LINK 2')
            return redirect(request.url)
        if file and isFileAllowed(file):
            print("RECEIVING IMAGE")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))     
            test_image = ImageReader(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #this allows you to see image
            
            #images come in oriented wrong, so the following code rotates it the correct way
            image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = image.transpose(Image.ROTATE_270)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],'file_rotated.png'))
            final_image = ImageReader(os.path.join(app.config['UPLOAD_FOLDER'],'file_rotated.png'))
            text = ExtractText(final_image.image)
            doc = text.extract_text()
            #print(doc)
            cc_insert = criminal_complaint(doc)
            #save the image
            img_filename = os.path.join(app.config['UPLOAD_FINAL'], 'CC', cc_insert['docket']+'_CC.jpg')
            image = image.transpose(Image.ROTATE_90)
            image.save(img_filename)
            #print(fields_package)            
            #Want to input into database
            #Way to do this without SSN?
            return cc_insert
        else:
            print('File not valid')
            print('HIT REDIRECT 3')
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
        if file and isFileAllowed(file):
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
            #Want to input into database
            #Way to do this without SSN?
            return data
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
        if file and isFileAllowed(file):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            test_image = ImageReader(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            text = ExtractText(test_image.image)
            doc = text.extract_text()
            #docket number sent in the posted form since it is not on the document itself
            acc_info = application_for_criminal_complaint(doc)
            #check if there is an already existing record, and simply update with the new info
            uuid = getUserID(acc_info["Name"], acc_info["Social Security No."][-4:], acc_info["Date of Birth"])
            formTable = models.forms(uuid, form_upload_date, form_upload_date, form_upload_date, form_upload_date)
            acc_insert = models.ACC(uuid, form_upload_date, image_path, acc_info["Summons"], acc_info["Hearing Requested"], acc_info["Court"], acc_info["Arrest Status of Accused"], acc_info["Arrest Date"], acc_info["In Custody"],acc_info["Officer ID No."],acc_info["Agency"],acc_info["Type"],acc_info["Name"],acc_info["Birth Surname"],acc_info["Address"],acc_info["Date of Birth"], acc_info["Place of Birth"], acc_info["Social Security No."], acc_info["PCF No."],acc_info["SID"],acc_info["Marital Status"],acc_info["Driver's License No."],acc_info["Driver's License State"],acc_info["Driver's License Exp. Year"],acc_info["Gender"],acc_info["Race"],acc_info["Height"],acc_info["Weight"],acc_info["Eyes"],acc_info["Hair"],acc_info["Ethnicity"],acc_info["Primary Language"],acc_info["Complexion"],acc_info["Scars/Marks/Tattoos"],acc_info["Employer Name"],acc_info["School Name"],acc_info["Day Phone"],acc_info["Mother Name"],acc_info["Mother Maiden Name"],acc_info["Father Name"],acc_info["Complainant Type"],acc_info["Police Dept."])
            db.session.add(formTable)
            db.session.commit()
            db.session.add(acc_insert)
            db.session.commit()
            return acc_info
        else:
            print('File not valid')
            return redirect('failure')
    return 'Please send a post request with your document picture'

#route for incident reports
@app.route('/IR', methods=['POST'])
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
        if file and isFileAllowed(file):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            test_image = ImageReader(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            text = ExtractText(test_image.image)
            doc = text.extract_text()
            #docket number sent in the posted form since it is not on the document itself
            acc_info = incident_report(doc)
            #Want to input into database
            #Way to do this without SSN?
            return acc_info
        else:
            print('File not valid')
            return redirect('failure')
    return 'Please send a post request with your document picture'


#route for probation record
@app.route('/PR', methods=['POST'])
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
        if file and isFileAllowed(file):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            test_image = ImageReader(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            text = ExtractText(test_image.image)
            doc = text.extract_text()
            #docket number sent in the posted form since it is not on the document itself
            acc_info = probation_form(doc)
            #Want to input into database
            #Way to do this without SSN?
            return acc_info
        else:
            print('File not valid')
            return redirect('failure')
    return 'Please send a post request with your document picture'


#route for miranda form
@app.route('/MF', methods=['POST'])
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
        if file and isFileAllowed(file):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            test_image = ImageReader(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            text = ExtractText(test_image.image)
            doc = text.extract_text()
            #docket number sent in the posted form since it is not on the document itself
            acc_info = miranda_form(doc)
            #Want to input into database
            #Way to do this without SSN?
            return acc_info
        else:
            print('File not valid')
            return redirect('failure')
    return 'Please send a post request with your document picture'

#FINISH THIS
@app.route('/constituents', methods=['GET'])
def constituents():
    sql = "SELECT * FROM constituents;"
    """
    case_list = constituents.find({})
    dockets = []
    for case in case_list:
        print(case)
        dockets.append(case['docket'])
    return json.dumps({'dockets': dockets})
    """

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