# Suffolk Country District Attorney's Office

### We have two parts to our app, and both are connected.
- An iOS app built in Swift to scan court documents and send them to our backend Flask app to be processed.
- A Flask app built in Python which extracts text from the documents received with the help of the Tesseract OCR tool.
  - In our Flask app, we also have an admin portal, where our client can upload scanned documents directly from their computer's web browser, in order to avoid the hassle of uploading an unclear picture from the iOS app.

# Current features

1. Scan and extract data from all possible documents as following:
    - Criminal Complaint
    - Application for Criminal Complaint
    - Incident Report
    - Arrest Booking Form
    - Miranda Form
    - Probation Record
2. View previously processed documents for all cases, organized by constituents.
3. In the iOS app, the user can upload photos of documents from their camera roll or take a new picture with their phone.
4. An admin portal on the Flask web app to upload clearly scanned documents that belong to the same person in bulk, avoiding the hassle of the iOS app.
5. State of the art security implemented, mitigating any file extension attacks through the upload file feature.

# How to run and use the Flask app with Database (primarily our backend):
1. Install tesseract on your computer following the instructions: https://github.com/tesseract-ocr/tesseract
2. Clone this repository to your computer:
    - `git clone https://github.com/keshavm02/suffolk-county-DA/`
3. Install the required python libraries in your virtual environment: `pip install -r requirements.txt`
4. (For local testing) Assuming presence of SQLite on your machine, initialize the local database with the following commands:
    - `cd Flask/`
    - `python3 manager.py create_db`
    - `python3 manager.py db init`
    - `python3 manager.py migrate`
5. After successfully initializing the db, run the Flask app with the following commands in the root directory:
    - `cd Flask/SCDA/`
    - `export FLASK_APP=routes.py`
    - `flask run`
6. On the "/admin" route, choose the files to upload according to the labels, and then click the submit button to have it processed. At the very least, the following required documents must be uploaded in order to process your request:
    - Criminal Complaint
    - Application for Criminal Complaint
    - Incident Report

# How to run and use the Swift app for iOS:
1. Go to the "Swift/swift_test/" directory.
2. Open "test.xcodeproj" on a Mac with Xcode installed.
3. Run the app with Command+R.
4. Follow the instructions in the app, and before pressing the upload button, make sure the Flask app is running on port 5000 of the same machine. If it is, then a successful POST request would be made to the approriate route with the document image to be processed. 

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


# Current limitations of the iOS app:
1. iOS Log In and Sign Up buttons are non-functional for now, as our client Nasser requested that we concentrate our time only on the backend after the iOS app was up to the standard he desired.
2. After the upload button is pressed, regardless of success or failure, a success screen is displayed to the user. This should be turned into a dynamic screen which displays a message based on the actual status of the upload.
3. The app cannot currently bundle up all documents for the same person and send them together to the "/upload" route as this is a new feature in the backend. Nasser had asked us to stop further work on the iOS app as it was almost ready, and wouldn't be much use without the backend resources actually working.
4. We are only a team of 3 students, hence development progress is not that of a 5 person team.

# Current limitations of the Flask app:
1. No authentication implemented yet, but it should not be a problem for the client in the near future as he will be the only person using the portal to upload documents and store the processed data in his local db.
2. The three optional documents do not translate into an HTML table yet, as the code for that would have taken some more time. However, they are all absolutely still getting processed and their extracted data can be viewed in the console with a simple database query and a print statement.
3. In the individual routes for document types (eg. "/acc", "/mf", etc.), we can currently only store data for Application for Criminal Complaint and Arrest Booking Form in the routes /acc and /abf respectively. The others are still a work in progress. However, we did not prioritize this since you can just send all documents together to the "/upload" route and have it all processed together.
4. We currently cannot process certain data fields in the Arrest Booking Form due to the fact that they are on a different physcial line from their associated label with no clear distinction between two labels placed closely. Hence, the OCR is unable to distinguish between the two, and fails miserably.
5. We currently have a barebones frontend user interface on the web portal, due to the fact that only one techincal person would be using it in the foreseeable future. He specifically asked us not to waste time prettying web pages up for him.
6. We are currently using SQLite, which is not the first choice database for most people. We tried implementing PostgreSQL but it was being extremely inconsistent and unstable in different environments, so we decided to switch to SQLite.
7. The OCR processing produces absolute gibberish when it comes to extracting data from even slightly unclear or blurred images, which would have been perfectly readble by human eyes. This is out of our control for now, and we cannot help how well the OCR performs. We chose Tesseract, which is currently one of the most popular open source Python frameworks for OCR.
