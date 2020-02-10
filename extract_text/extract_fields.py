import re

#criminal complaint
def find_docket_number(document):
    docket = re.search("[0-9]{4}[A-Z]{2}[0-9]{5}", document)
    if(docket != None):
        return docket.group()
    return "Docket number not found"

def find_full_name(document):
    name = re.search("[A-Z][a-z]*\s[A-Z]\s[A-Z][a-z]*", document)
    if(name != None):
        return name.group()
    return "Name not found"

def find_dates(document):
    dates = re.findall("[0-9]{2}/[0-9]{2}/[0-9]{4}", document)
    if(dates != None):
        return dates
    return "No dates found"

def find_obtn(document):
    obtn = re.search("[A-Z]{4}[0-9]{9}", document)
    if (obtn != None):
        return obtn.group()
    return "obtn not found"

def find_indicent_report(document):
    irn = re.search("[0-9]{3}\s[0-9]{3}\s[0-9]{3}",document)
    if(irn != None):
        return irn.group()
    return "Police Incident report number not found"

def find_addresses(document):
    street = re.findall('[0-9][0-9]*\s[A-Z][a-z]*\s[A-Z][a-z]+',document)
    city_state = re.findall('[A-Z][a-z]+[,]\s[A-Z]{2}\s[0-9]{5}',document)
    if len(street) == 2 and len(city_state)== 2:
        return {'court':street[1]+' ' + city_state[1], 'defendant':street[0]+' '+city_state[0]}
    return {'court':'Not found', 'defendant':'Not found'}

def find_codes(document):
    codes = re.findall('[1-9][0-9]*/[0-9]+[A-Z]*(/[0-9]*[A-Z]*)?',document)
    return codes

#data extracted from arrest booking form by finding the key words for the fields and adding the corresponding key, value pair to dictionary
def arrest_booking_form(raw_document):
    header = ['Boston Police Department', 'Arrest Booking Form']
    document = raw_document
    for phrase in header:
        document = document.replace(phrase, '')
    #list of keywords
    block_list = ["Report Date", "Booking Status", "Printed By", "District", "UCR Code", "OBTN", "Court of Appearance", "Master Name", "Age", "Location of Arrest",
            "Booking Name", "Alias", "Address", "Charges", "Booking#", "Incident#", "CR Number", "Booking Date", "Arrest Date", "RA Number", "Sex", "Height", "Occupation",
            "Race", "Weight", "Employer/School", "Date of Birth", "Build, Emp/School Addr", "Place of birth", "Eyes color", "Social Sec. Number", "Marital Status", 
            "Hair color", "Operators License", "Mother's Name", "Complexion", "State", "Father's Name","Phone Used", "Scars/Marks/Tattos", "Examined at Hospital",
            "Clothing Desc", "Breathalyzer Used", "Examined by EMS", "Arresting Officer", "Cell Number", "Booking Officer", "Partner's","Informed of Rights", "Unit#",
            "Placed in Cell By", "Trans Unit#", "Searched By", "Cautions", "Booking Comments","Visible Injuries", "Person Notified", "Relationship","Phone","Address",
            "Juv.Prob.Officer","Notified By","Notified Date/Time","Bail Set By", "I Selected the Bail Comm.","Bailed By","Amount","BOP Check",
            "Suicide Check","BOP Warrant", "BOP Court"]
    fields = {}
    for field in block_list:
        find = field+': '
        value = ''
        if find in document:
            temp_doc = document[document.index(find) + len(find):]
            if ':' in temp_doc:
                #temporarily erase keywords and use the index of : to know when to end the string
                for word in block_list:
                    temp_doc = temp_doc.replace(word,'')
                value = temp_doc[:temp_doc.index(':')].replace('\n','').strip()
            else:
                #if no : in the remaining document, end current field with next space or newline
                value = temp_doc[:re.search('\s|\n',temp_doc).start()]
        fields[field] = value
    return fields
        
#application for criminal complaint
def find_name_ACC(document):
    name = re.search("[a-z]*\s[A-Z][a-z]*[,]\s[A-Z][a-z]*", document)
    return name