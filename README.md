# scdao-ios-ocr

An iOS app to built in swift to scan court documents and extract the data into a MongoDB database.
<br> Using the Tesseract OCR tool in conjuction with a flask backend, documents are scanned on the iOS device and the image
is posted to a flask server to be processed and extract data to put into the database.

# Current features

1. Scan and extract data from Criminal Complaint documents
2. View previously scanned documents for all cases, organized by docket number
3. Upload photos of documents already in camera roll to be processed
4. Scan and extract subject name and full text for application for criminal complaint documents

# How to run:

1. Install tesseract on your computer following the instructions: https://github.com/tesseract-ocr/tesseract
2. (For local testing) Install MongoDB Server and create a database called COURT_CASES
2. Clone our repository to your computer
3. Install the required python libraries: 'pip install -r requirements.txt'
4. Run app.py to run the server
5. The '/CC' route currently accepts POST requests with image files for criminal complaint forms
6. To send a post request with an image via the terminal for testing: 'curl -F "file=@{Your file} localhost:5000"


# Routes:
/CC for criminal complaint form
/ACC for application for criminal complaint form (Currently extracting name and text)