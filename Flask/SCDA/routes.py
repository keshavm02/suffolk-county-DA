import sys
sys.path.append('.././suffolk-county-DA/Flask/')
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


#http://www.programmersought.com/article/68322218798/
class JSONEncoder(json.JSONEncoder):
    def default(self, o):                # pylint: disable=E0202 
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')
    
@app.route('/upload', methods=['POST', 'GET'])
def upload_forms():
    try:
        if request.method == 'POST':
            print("POST REQUEST RECEIVED")
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
                    path = os.path.abspath("../SCDA/extract_text/extraction_tests/test_textdumps/Application for Criminal Complaint .txt")
                    doc = open(path).read()
                    acc_info = extract_application_for_criminal_complaint(doc)
                    if acc_info["Name"] == '' or acc_info["Date of Birth"] == '' or acc_info["Social Security No."] == '':
                        return "Application for criminal complaint could not be read. Please upload a clearer image."
                    else:
                        uuid = getUserID(acc_info["Name"], acc_info["Social Security No."][-4:], acc_info["Date of Birth"])
                        formTable = models.forms(uuid, form_upload_date, form_upload_date, form_upload_date, form_upload_date)
                        acc_insert = models.ACC(uuid, form_upload_date, image_path, acc_info["Summons"], acc_info["Hearing Requested"], acc_info["Court"], acc_info["Arrest Status of Accused"], acc_info["Arrest Date"], acc_info["In Custody"],acc_info["Officer ID No."],acc_info["Agency"],acc_info["Type"],acc_info["Name"],acc_info["Birth Surname"],acc_info["Address"],acc_info["Date of Birth"], acc_info["Place of Birth"], acc_info["Social Security No."], acc_info["PCF No."],acc_info["SID"],acc_info["Marital Status"],acc_info["Driver's License No."],acc_info["Driver's License State"],acc_info["Driver's License Exp. Year"],acc_info["Gender"],acc_info["Race"],acc_info["Height"],acc_info["Weight"],acc_info["Eyes"],acc_info["Hair"],acc_info["Ethnicity"],acc_info["Primary Language"],acc_info["Complexion"],acc_info["Scars/Marks/Tattoos"],acc_info["Employer Name"],acc_info["School Name"],acc_info["Day Phone"],acc_info["Mother Name"],acc_info["Mother Maiden Name"],acc_info["Father Name"],acc_info["Complainant Type"],acc_info["Police Dept."])
                        db.session.add(formTable)
                        db.session.commit()
                        db.session.add(acc_insert)
                        db.session.commit()
                cc_file = form_data['cc']
                cc_filename = cc_file.filename
                if cc_filename == "":
                    return redirect('failure')
                if isFileAllowed(cc_file):
                    cc_filename = secure_filename(cc_filename)
                    cc_file = Image.open(cc_file)
                    doc, image_path = localUploadAndExtraction(cc_filename, cc_file)
                    cc_info = extract_criminal_complaint(doc)
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
                    ir_info = extract_incident_report(doc)
                    ir_insert = models.IR(uuid, form_upload_date, image_path, ir_info["Case Number"],ir_info["CAD Incident Number"],ir_info["Report Type"],ir_info["Date / Time Occurred"],ir_info["Date / Time Reported"],ir_info["Public Narrative"])
                    db.session.add(ir_insert)
                    db.session.commit()
                else:
                    return redirect('failure')
                addOptional = addOptionalForms(form_data, uuid, formTable, form_upload_date)
                print(addOptional)
                if not addOptional:
                    return redirect('failure')
                return redirect('success')
        elif request.method == 'GET':
            print('GET request received.')
            return render_template('admin.html')
            #return 'Please send a post request with at least the following forms: Application for Criminal Complaint, Criminal Complaint, Incident Report.'
    except:
        return redirect('failure')
            
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                                filename)

#route for criminal complaints
@app.route('/CC', methods=['POST'])
def Criminal_Complaint_Post():
    print("RECIEVING REQUEST 1")
    if request.method == 'POST':
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
            cc_insert = extract_criminal_complaint(doc)
            #save the image
            img_filename = os.path.join(app.config['UPLOAD_FINAL'], 'CC', cc_insert['docket']+'_CC.jpg')
            image = image.transpose(Image.ROTATE_90)
            image.save(img_filename)
            #Want to input into database
            #Way to do this without SSN?
            return cc_insert
        else:
            print('File not valid')
            print('HIT REDIRECT 3')
            return redirect('failure')
    return 'Please send a post request with your document picture'

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
            abf_info = extract_arrest_booking_form(doc)
            uuid = getUserID(abf_info["Name"], abf_info["Social Security No."][-4:], abf_info["Date of Birth"])
            formTable = models.forms(uuid, form_upload_date, form_upload_date, form_upload_date, form_upload_date)
            abf_insert = models.ABF(uuid, form_upload_date, image_path, abf_info["Report Date"],abf_info["Booking Status"],
                            abf_info["Printed By"],abf_info["District"],abf_info["UCR Code"],abf_info["OBTN"],
                            abf_info["Court of Appearance"],abf_info["Master Name"],abf_info["Age"],abf_info["Location of Arrest"],
                            abf_info["Booking Name"],abf_info["Alias"],abf_info["PAD"],abf_info["Charges"],abf_info["Booking #"],
                            abf_info["Incident #"],abf_info["CR Number"],abf_info["Booking Date"],abf_info["Arrest Date"],
                            abf_info["RA Number"],abf_info["Sex"],abf_info["Height"],abf_info["Occupation"],abf_info["Race"],
                            abf_info["Weight"],abf_info["Employer/School"],abf_info["Date of Birth"],abf_info["Build"],
                            abf_info["Emp/School Addr"],abf_info["Place of Birth"],abf_info["Eyes Color"],
                            abf_info["Social Sec. Number"],abf_info["Marital Status"],abf_info["Hair Color"],
                            abf_info["Operators License"],abf_info["Mother's Name"],abf_info["Complexion"],
                            abf_info["State"],abf_info["Father's Name"],abf_info["Phone Used"],abf_info["Scars/Marks/Tattoos"],
                            abf_info["Examined at Hospital"],abf_info["Clothing Desc"],abf_info["Breathalyzer Used"],
                            abf_info["Examined by EMS"],abf_info["Arresting Officer"],abf_info["Cell Number"],
                            abf_info["Booking Officer"],abf_info["Partner's #"],abf_info["Informed of Rights"],
                            abf_info["Unit #"],abf_info["Placed in Cell By"],abf_info["Trans Unit #"],abf_info["Searched By"],
                            abf_info["Cautions"],abf_info["Booking Comments"],abf_info["Visible Injuries"],
                            abf_info["Person Notified"],abf_info["Relationship"],abf_info["Phone"],abf_info["Address"],
                            abf_info["Juv. Prob. Officer"],abf_info["Notified By"],abf_info["Notified Date/Time"],
                            abf_info["Bail Set By"],abf_info["I Selected the Bail Comm."],abf_info["Bailed By"],abf_info["Amount"],
                            abf_info["BOP Check"],abf_info["Suicide Check"],abf_info["BOP Warrant"],abf_info["BOP Court"])
            db.session.add(formTable)
            db.session.commit()
            db.session.add(abf_insert)
            db.session.commit()
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
            acc_info = extract_application_for_criminal_complaint(doc)
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
def ir():
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
            acc_info = extract_incident_report(doc)
            #Want to input into database
            #Way to do this without SSN?
            return acc_info
        else:
            print('File not valid')
            return redirect('failure')
    return 'Please send a post request with your document picture'


#route for probation record
@app.route('/PR', methods=['POST'])
def pr():
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
            acc_info = extract_probation_form(doc)
            #Want to input into database
            #Way to do this without SSN?
            return acc_info
        else:
            print('File not valid')
            return redirect('failure')
    return 'Please send a post request with your document picture'


#route for miranda form
@app.route('/MF', methods=['POST'])
def mf():
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
            text = ExtractText(test_image.image)
            doc = text.extract_text()
            #docket number sent in the posted form since it is not on the document itself
            acc_info = extract_miranda_form(doc)
            #Want to input into database
            #Way to do this without SSN?
            return acc_info
        else:
            print('File not valid')
            return redirect('failure')
    return 'Please send a post request with your document picture'

#Web page to display all constituents
@app.route('/constituents', methods=['GET'])
def view_constituents():
    constituent_list = models.constituents.query.all()
    return render_template('constituents.html',constituent_list=constituent_list)

#web page to display all forms
@app.route('/<id_number>')
def display_forms(id_number):
    id = id_number 
    constituent_forms = db.session.query(forms).filter_by(constituent_id=id_number).all()
    return render_template('forms.html',id_number=id,form_list=constituent_forms)

#web page to display requested incident report form
@app.route('/<id_number>/IR/<upload_date>')
def display_IR(id_number, upload_date):
    IR_form = db.session.query(models.IR).filter_by(constituent_id=id_number,form_upload_date=upload_date).first()
    return render_template('IR.html',id_number=id_number,upload_date=upload_date,form=IR_form)

#web page to display requested application for criminal complaint
@app.route('/<id_number>/ACC/<upload_date>')
def display_ACC(id_number, upload_date):
    ACC_form = db.session.query(models.ACC).filter_by(constituent_id=id_number,form_upload_date=upload_date).first()
    return render_template('ACC.html',id_number=id_number,upload_date=upload_date,form=ACC_form)

#web page to display requested criminal complaint
@app.route('/<id_number>/CC/<upload_date>')
def display_CC(id_number, upload_date):
    CC_form = db.session.query(models.CC).filter_by(constituent_id=id_number,form_upload_date=upload_date).first()
    return render_template('CC.html',id_number=id_number,upload_date=upload_date,form=CC_form)

@app.route('/success')
def uploaded():
    return 'File(s) successfully uploaded'

@app.route('/failure')
def fail():
    return 'File not uploaded successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)