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
        print(request.data)
        form_data = request.get_json()
        form_upload_date = datetime.now()
        uuid = -1
        checkRequiredForms = checkAllRequiredForms(form_data)
        if (not checkRequiredForms[0]):
            return checkRequiredForms[1]
        else:
            acc_file = form_data['acc']
            acc_filename = acc_file.split('/')
            acc_filename = acc_filename[-1]
            # Replace with better security
            if allowed_file(acc_filename):
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
                    uuid = getUser(acc_info["Name"], acc_info["Social Security No."][-4:], acc_info["Date of Birth"])
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
            else:
                return redirect('failure')
            cc_file = form_data['cc']
            cc_filename = cc_file.split('/')
            cc_filename = cc_filename[-1]
            if allowed_file(cc_filename):
                cc_filename = secure_filename(cc_filename)
                cc_file = Image.open(cc_file)
                doc, image_path = localUploadAndExtraction(cc_filename, cc_file)
                cc_info = criminal_complaint(doc)
                print(cc_info["court_address"])
                cc_insert = models.CC(uuid, form_upload_date, image_path, cc_info["docket"], cc_info["name"], cc_info["dob"], cc_info["doc"], 
                         cc_info["doo"], cc_info["doa"], cc_info["ned"], cc_info["obtn"], cc_info["irn"], cc_info["court_address"], 
                         cc_info["defendant_address"], cc_info["offense_codes"])
                db.session.add(cc_insert)
                db.session.commit()
            ir_file = form_data['ir']
            ir_filename = ir_file.split('/')
            ir_filename = ir_filename[-1]
            if allowed_file(ir_filename):
                ir_filename = secure_filename(ir_filename)
                ir_file = Image.open(ir_file)
                doc, image_path = localUploadAndExtraction(ir_filename, ir_file)
                ir_info = incident_report(doc)
                ir_insert = models.IR(uuid, form_upload_date, image_path, ir_info["Case Number"],ir_info["CAD Incident Number"],ir_info["Report Type"],ir_info["Date / Time Occurred"],ir_info["Date / Time Reported"],ir_info["Public Narrative"])
                db.session.add(ir_insert)
                db.session.commit()
            else:
                return redirect('failure')
            
        #Adding the forms table and individual forms
            #add forms table
            
            """
            #add required forms --> Criminal Complaint
            cc_file = form_data['cc']
            cc_filename = cc_file.split('/')
            cc_filename = cc_filename[-1]
            cc_filename = secure_filename(cc_filename)
            cc_file = Image.open(cc_file)
            doc, image_path = localUploadAndExtraction(cc_filename, cc_file)
            cc_info = criminal_complaint(doc)
            cc_insert = models.CC(uuid, form_upload_date, image_path, cc_info["docket"], cc_info["name"], cc_info["dob"], cc_info["doc], 
                         cc_info["doo"], cc_info["doa"], cc_info["obtn"], cc_info["text"], cc_info["irn"], cc_info["court_address"], 
                         cc_info["defendant_address"], cc_info["offense_codes"])

            #add required forms --> Incident Report
            ir_file = form_data['ir']
            ir_filename = ir_file.split('/')
            ir_filename = ir_filename[-1]
            ir_filename = secure_filename(ir_filename)
            ir_file = Image.open(ir_file)
            doc, image_path = localUploadAndExtraction(ir_filename, ir_file)
            ir_info = incident_report(doc)
            ir_insert = models.IR(uuid, form_upload_date, image_path, ir_info["Case Number"],ir_info["CAD Incident Number"],ir_info["Report Type"],ir_info["Date / Time Occured"],ir_info["Date / Time Reported"],ir_info["Public Narrative"])


            
            """
            """

            #add optional forms
            #miranda form 
            mf_file = form_data['ir']
            mf_filename = mf_file.split('/')
            mf_filename = mf_filename[-1]
            mf_filename = secure_filename(mf_filename)
            mf_file = Image.open(mf_file)
            doc, image_path = localUploadAndExtraction(mf_filename, mf_file)
            mf_info = incident_report(doc)
            mf_insert = models.MF(uuid, form_upload_date, image_path, mf_info["Booking Name"], mf_info["First"], mf_info["Middle"], mf_info["Suffix"], mf_info["Home Address"], mf_info["Report Date"], 
                                                                    mf_info["Booking Status"], mf_info["Printed By"], mf_info["Sex"], mf_info["Race"], mf_info["Date of Birth"], mf_info["District"], mf_info["Booking Number"], 
                                                                    mf_info["Arrest Date"], mf_info["Incident Number"], mf_info["Booking Date"], mf_info["Charges"], mf_info["Telephone Used"], mf_info["Breathalyzer Used"], mf_info["Examined at Hospital"], 
                                                                    mf_info["Examined by EMS"], mf_info["Visibile Injuries"], mf_info["Money"], mf_info["Property Storage No"], mf_info["Property"])

            #probation record
            pr_file = form_data['pr']
            pr_filename = pr_file.split('/')
            pr_filename = pr_filename[-1]
            pr_filename = secure_filename(pr_filename)
            pr_file = Image.open(pr_file)
            doc, image_path = localUploadAndExtraction(pr_filename, pr_file)
            pr_info = incident_report(doc)
            pr_insert = models.PR(uuid, form_upload_date, image_path, pr_info["PCF"],pr_info["DOB"],pr_info["Age"],pr_info["Birthplace"],pr_info["Mother"],pr_info["Father"],pr_info["Height"],pr_info["Weight"],
                                                                    pr_info["Hair"],pr_info["Eyes"],pr_info["Gender"],pr_info["Race"],pr_info["Ethnicity"],
                                                                    pr_info["DLN"],pr_info["CARI"],pr_info["Records Include"])
            
            

            #abf
            abf_file = form_data['abf']
            abf_filename = abf_file.split('/')
            abf_filename = abf_filename[-1]
            abf_filename = secure_filename(abf_filename)
            abf_file = Image.open(abf_file)
            doc, image_path = localUploadAndExtraction(abf_filename, abf_file)
            abf_info = arrest_booking_form(doc)
            abf_insert = models.PR(uuid, form_upload_date, image_path, abf_info["Report Date"],abf_info["Booking Status"],abf_info["Printed By"],abf_info["District"],abf_info["UCR Code"],abf_info["OBTN"],abf_info["Court of Appearance"],
                                                                       abf_info["Master Name"],abf_info["Age"],abf_info["Location of Arrest"],abf_info["Booking Name"],abf_info["Alias"],abf_info["PAD"],abf_info["Charges"],abf_info["Booking #"],abf_info["Incident #"],
                                                                       abf_info["CR Number"],abf_info["Booking Date"],abf_info["Arrest Date"],abf_info["RA Number"],abf_info["Sex"],abf_info["Height"],abf_info["Occupation"],abf_info["Race"],abf_info["Weight"],
                                                                       abf_info["Employer/School"],abf_info["Date of Birth"],abf_info["Build"],abf_info["Emp/School Addr"],abf_info["Place of Birth"],abf_info["Eyes Color"],abf_info["Social Sec. Number"],abf_info["Marital Status"],abf_info["Hair Color"],
                                                                       abf_info["Operators License"],abf_info["Mother's Name"],abf_info["Complexion"],abf_info["State"],abf_info["Father's Name"],abf_info["Phone Used"],abf_info["Scars/Marks/Tattoos"],abf_info["Examiend at Hospital"],abf_info["Clothing Desc"],
                                                                       abf_info[""Breathalyzer Used],abf_info["Examined by EMS"],abf_info["Arresting Officer"],abf_info["Cell Number"],abf_info["Booking Officer"],abf_info["Parther's #"],abf_info["Informaed of Rights"],abf_info["Unit #"],abf_info["Placed in Cell by"],
                                                                       abf_info["Trans Unit #"],abf_info["Searched by"],abf_info["Cautions"],abf_info["Booking Comments"],abf_info["Visibile Injuries"],abf_info["Person Notified"],abf_info["Relationship"],abf_info["Phone"],abf_info["Address"],abf_info["Juv. Prob. Officer"],
                                                                       abf_info["Notified By"],abf_info["Notified Date/Time"],abf_info["Bail Set By"],abf_info["I selected the Bail Comm."],abf_info["Bailed By"],abf_info["Amount"],abf_info["BOP Check"],abf_info["Suicide Check"],abf_info["BOP Warrant"],
                                                                       abf_info["BOP Court"])
                                                                       
           
            #test = 3               
            #addOptional = addOptionalForms(form_data, uuid, formTable, form_upload_date)

"""
            #test = 1
            addOptional = addOptionalForms(form_data, uuid, formTable, form_upload_date)
            if not addOptional:
                return redirect('failure')
            return "All good!"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                                filename)


    #recieve the json object and possibily convert it
    #the upload should be in json format by this point, see format in database code.py 
    #also at this point, the json should hold a key called forms which contains a list of objects where each object is keyed by their form title
    #extract forms such that there is a variable call it forms that is equal to the list of objects
    #Go through the list and find ACC which is required.
        #If ACC is in the list
                #Constiutents table
                    #User = add_acc(RAW_ACC_Document), at this point we get the UUID
                    #GetUser(Name,DOB,SSN), this getUser should return the unique id number
                        #If GetUser returns no user found, else call AddUser which also returns the newly made uuid number
                    #Set a variable User = GetUser() 
                #At this point, we have a user we want to add our forms to.
                #At this point we are finished with the constituents table
    #At this point, Constituents table is properly filled out
                #Forms Table
                    #Given their UUID
                    #Get the FormUploadDate = getDate()
                    #Call addFormRow(UUID,FormUploadDate, List Variable Forms)
                        #this should add a new row with consitutuent UUID, Form upload date, all the forms in list set to upload date. 
                        #this function should return a reference to the new row in the forms table so that we can add the actual forms later
                    #Set variable formRow = addFormRow()
    #At this point, Forms Table is properly filled out.
    #Six if in conditions, but if ACC pass, example https://stackoverflow.com/questions/9371114/check-if-list-of-objects-contain-an-object-with-a-certain-attribute-value. 
                #Individual Document Tables 
                    #Example: Do this for all 6 forms,
                    #Route ACC Table
                        #Call addACCForm(ACC Image)
                            #The ultimate goal of this function is to add a row to their respective tables in the Postgres database. 
                            #This should return success or failure depending if the form was successfully extracted and tested

                

        #If ACC is not in list, send error "Please upload all required document(s): missing ACC"
    pass


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
        #print(file)
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
            #print(fields_package)            
            #Input into database
            #Check if there is an existing record, if so just update. 
            #If no such records exist, create an entry.
            #set unique case incident report number, and obtn to the scanned values and embed all scanned fields into new document under the case with this docket #
        
            #create a new db document if one does not already exist
            return fields_package
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
        if file and isFileAllowed(file):
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