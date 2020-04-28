#Route for Application for Criminal Complaint (THROW INTO DATABASECODE WHEN DONE)

#The overall objective. Add extract all information from this image and add to database under the ACC table

#Not the responsibility of this application
    #Checking if the file is actually located in this application 

#Potentially Reponsibilities
    #Security check of the individual image file itself 


def addACC(flag, Document_Image_ACC_RAW, PrevFetchedData): 
    #FLAG IS TO NOT ADD YET
    #Check the image for security purposes
    if isImageSecure(Document_Image_ACC_RAW): #put into database code, this should check the filename as well as the file itself 
        if flag:
            acc_scanned = convertRawToText(Document_Image_ACC_RAW)  #put into database code, this should do the conversion from Raw To Text
            acc_info = application_for_criminal_complaint(acc_scanned) #Extract information this returns a dictionary of the fields 
            #return [name, DOB, SSN, acc_info]
            uuid = getUser(name,DOB,SSN)
            form_upload_date = getDate() 
            acc = ACC(uuid, form_upload_date, ......, acc_scanned)
            db.session.add(acc)
            db.session.commit()
            return uuid 
    else:
        return "ACC file not secure, aborting"


"""
FOR iNSPIRATION 

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

    """