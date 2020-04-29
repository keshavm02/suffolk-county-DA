from flask import Flask
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
    if 'pr' in form_data:
        db.session.query(forms).filter(forms.form_upload_date==form_upload_date).update({'PR': form_upload_date})
    if 'mf' in form_data:
        db.session.query(forms).filter(forms.form_upload_date==form_upload_date).update({'MF': form_upload_date})
    db.session.commit()


if __name__ == "__main__":
    print(getUser('Test','1234','01/01/2020'))