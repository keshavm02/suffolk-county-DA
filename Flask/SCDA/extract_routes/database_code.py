from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import update
import sys
sys.path.append('/Users/eloisanitorreda/suffolk-county-DA/Flask/')
#SCDA = __import__('SCDA')
from SCDA import db, app
from SCDA.models import constituents, forms, ABF, PR, MF
#extract_text = __import__('suffolk-county-DA/Flask/SCDA/extract_text')
from SCDA.extract_text import *
from werkzeug.utils import secure_filename


"""
Assumptions taken: 
     There are three required documents. In the front end, the user will select a required document from the table given, scan the document that was selected. The user will do this for three documents.
     If there are extra optional documents, the user will proceed to scan those as well. When all documents are scanned, user will press the upload button that will send all documents scanned to the backend. 
     One of the required documents that should always be scanned is the ACC which contains Name, DOB, SSN. This will identify the user that we will store the information for. 
     IDEA: The backend will recieve data in a json object format. It will be a list of objects where the key will be the document name. Example:
                


                {
                    ACC: Scanned Image, 
                    CC: Scanned Image,
                    IR: Scanned Image,
                }

        This will allow us to account for the optional documents by going through the list, when we go through the list, we look at the key and match the key to a route that will handle extracting the information out of that 
        specific document. 
""" 

"""
Methods that need to implemented
3.getDate --> jus
4.addFormRow() --> Explanation can be found in routes
5.routeFunctions(6 of them) --> example can be found in example_extraction
6.convertRawToText --> similar to their code where they extract text
"""

#allowed_file adapted from http://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getUser(name, SSN, DOB):
    #User scans document
    #This function will look through the document and try to find name, date of birth, Last 4 digits of SSN
    #Ultimately return the user
    #If one or is missing ask the user to manually enter it, and then seaarch again and return user. 
    #If user is not in database add user
    # Search database for user, if not found add user
    user = db.session.query(constituents).get((name, SSN, DOB))
    if user is not None:
        return user.id
    else:
        user = constituents(name, SSN, DOB)
        db.session.add(user)
        db.session.commit()
        return user.id

def checkAllRequiredForms(form_data):
        if 'acc' not in form_data:
            return [False,"Please upload all required document(s): missing ACC"]
        elif 'cc' not in form_data:
            return [False,"Please upload all required document(s): missing CC"]
        elif 'ir' not in form_data:
            return [False,"Please upload all required document(s): missing IR"]
        else:
            return [True]
        
        


def localUploadAndExtraction(filename, file):
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image = ImageReader(image_path)
    text = ExtractText(image.image)
    #does not work well with provided test image, using premade textdump for testing purposes
    doc = text.extract_text()
    #doc = open(os.path.expanduser("~/suffolk-county-DA/Flask/SCDA/extract_text/extraction_tests/test_textdumps/Application for Criminal Complaint .txt")).read() #THIS IS FOR TESTING PURPOSES
    return doc, image_path






def addOptionalForms(form_data, uuid, formTable, form_upload_date):
    #print(uuid)
    #print(form_upload_date)
    #print(str(form_upload_date))
    #print(str(forms.form_upload_date))
    if 'abf' in form_data:
        #update the forms table
        #add abf table itself
        db.session.query(forms).filter(forms.form_upload_date==form_upload_date).update({'ABF': form_upload_date})
        #upload = db.session.query(forms).get(form_upload_date)
        #print(upload)
        abf_file = form_data['abf']
        abf_filename = abf_file.split('/')
        abf_filename = abf_filename[-1]
        if allowed_file(abf_filename):
            abf_filename = secure_filename(abf_filename)
            abf_file = Image.open(abf_file)
            doc, image_path = localUploadAndExtraction(abf_filename, abf_file)
            abf_info = arrest_booking_form(doc)
            abf_insert = ABF(uuid, form_upload_date, image_path, abf_info["Report Date"],abf_info["Booking Status"],
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
            db.session.add(abf_insert)
        else:
            return False
    if 'pr' in form_data:
        db.session.query(forms).filter(forms.form_upload_date==form_upload_date).update({'PR': form_upload_date})
        pr_file = form_data['pr']
        pr_filename = pr_file.split('/')
        pr_filename = pr_filename[-1]
        if allowed_file(pr_filename):
            pr_filename = secure_filename(pr_filename)
            pr_file = Image.open(pr_file)
            doc, image_path = localUploadAndExtraction(pr_filename, pr_file)
            pr_info = probation_form(doc)
            pr_insert = PR(uuid, form_upload_date, image_path, pr_info["PCF"],pr_info["DOB"],pr_info["Age"],pr_info["Birthplace"],pr_info["Mother"],pr_info["Father"],pr_info["Height"],pr_info["Weight"],
                                                                    pr_info["Hair"],pr_info["Eyes"],pr_info["Gender"],pr_info["Race"],pr_info["Ethnicity"],
                                                                    pr_info["DLN"],pr_info["CARI"],pr_info["Records Include"])
            db.session.add(pr_insert)
        else:
            return False
    if 'mf' in form_data:
        db.session.query(forms).filter(forms.form_upload_date==form_upload_date).update({'MF': form_upload_date})
        mf_file = form_data['mf']
        mf_filename = mf_file.split('/')
        mf_filename = mf_filename[-1]
        if allowed_file(mf_filename):
            mf_filename = secure_filename(mf_filename)
            mf_file = Image.open(mf_file)
            doc, image_path = localUploadAndExtraction(mf_filename, mf_file)
            mf_info = miranda_form(doc)
            mf_insert = MF(uuid, form_upload_date, image_path, mf_info["Booking Name"], mf_info["First"], mf_info["Middle"], mf_info["Suffix"], mf_info["Home Address"], mf_info["Report Date"], 
                                                                    mf_info["Booking Status"], mf_info["Printed By"], mf_info["Sex"], mf_info["Race"], mf_info["Date of Birth"], mf_info["District"], mf_info["Booking Number"], 
                                                                    mf_info["Arrest Date"], mf_info["Incident Number"], mf_info["Booking Date"], mf_info["Charges"], mf_info["Telephone Used"], mf_info["Breathalyzer Used"], mf_info["Examined at Hospital"], 
                                                                    mf_info["Examined by EMS"], mf_info["Visible Injuries"], mf_info["Money"], mf_info["Property Storage No"], mf_info["Property"])
            db.session.add(mf_insert)
        else:
            return False    
    db.session.commit()
    return True


if __name__ == "__main__":
    print(getUser('Test','1234','01/01/2020'))