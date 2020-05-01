# Suffolk Country District Attorney's Office

### We have two parts to our app, and both are connected.
- An iOS app built in Swift to scan court documents and extract the data into a SQLite database.
- A Flask app built in Python to process the documents uploaded with the help of the Tesseract OCR tool.
  - In our Flask app, we also have an admin portal, where our client can upload scanned documents directly from their computer's web browser.

# Current features

1. Scan and extract data from all possible documents as following:
  - Criminal Complaint
  - Application for Criminal Complaint
  - Incident Report
  - Arrest Booking Form
  - Miranda Form
  - Probation Record
2. View previously scanned documents for all cases, organized by constituents
3. In the iOS app, the user can upload photos of documents from their camera roll or by taking a new picture with their phone.
4. An admin portal on the Flask web app to upload clearly scanned documents that belong to the same person in bulk.

# How to run and use the Flask app (primarily our backend):
1. Install tesseract on your computer following the instructions: https://github.com/tesseract-ocr/tesseract
2. Clone this repository to your computer:
  - `git clone https://github.com/keshavm02/suffolk-county-DA/`
3. Install the required python libraries in your virtual environment: `pip install -r requirements.txt`
4. (For local testing) Assuming presence of SQLite, initialize the local database with the following commands:
  - `cd Flask/`
  - `python3 manager.py create_db`
  - `python3 manager.py db init`
  - `python3 manager.py migrate`
5. After successfully initializing the db, run the Flask app with the following commands:
  - `cd Flask/SCDA/`
  - `export FLASK_APP=routes.py`
  - `flask run`
6. On the "/admin" route, choose the files to upload according to the labels, and then click the submit button to have it processed. At the very least, the following required documents must be uploaded in order to process your request:
  - Criminal Complaint
  - Application for Criminal Complaint
  - Incident Report

# Routes:
- "/admin" to choose and upload images of documents as needed.
- "/constituents" to view the processed data of previously uploaded documents in a tabular form.
  - You can see here a list of all people in the database.
  - Clicking on a person will redirect you to "/<id_number>" where a list of forms related to the constituent can be viewed.
  - Clicking on an entry in the table will redirect you to "/<id_number>/<document_type>/<upload_date>" where the data requested can be viewed.
- "/upload" takes in a POST request with the at least the 3 required document types to be processed.
- "/<document_type>" takes in a POST request with the document pertaining to the type mentioned. Types are:
  - "/CC"
  - "/ACC"
  - "/IR"
  - "/ABF"
  - "/MF"
  - "/PR"
- "/uploads/<file_name>" displays the image pertaining to the file name mentioned in the route.


# Limitations:
