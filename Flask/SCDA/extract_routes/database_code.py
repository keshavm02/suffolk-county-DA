from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
sys.path.append('/Users/eloisanitorreda/suffolk-county-DA/Flask/')
#SCDA = __import__('SCDA')
from SCDA import db
from SCDA.models import constituents
#extract_text = __import__('suffolk-county-DA/Flask/SCDA/extract_text')
from SCDA.extract_text import *

"""
Assumptions taken: 
     There are three required documents. In the front end, the user will select a required document from the table given, scan the document that was selected. The user will do this for three documents.
     If there are extra optional documents, the user will proceed to scan those as well. When all documents are scanned, user will press the upload button that will send all documents scanned to the backend. 
     One of the required documents that should always be scanned is the ACC which contains Name, DOB, SSN. This will identify the user that we will store the information for. 
     IDEA: The backend will recieve data in a json object format. It will be a list of objects where the key will be the document name. Example:
                 {
                     forms: [
                         {
                             ACC: Scanned Image
                         },
                         {
                             CC: Scanned Image
                         },
                         {
                             IR: Scanned Image
                         },
                         {
                             Some Optional Form: Scanned Image
                         }
                     ]
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

 


if __name__ == "__main__":
    print(getUser('Test','1234','01/01/2020'))