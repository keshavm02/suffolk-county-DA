from SCDA import db
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, ForeignKey, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class constituents(db.Model):
    __tablename__ = 'constituents'

    uuid = db.Column(db.Integer, unique =True, nullable = False)
    name = db.Column(db.String(), primary_key = True, nullable = False)
    SSN = db.Column(db.String(), nullable = False) #we should hash, or only display last 4
    DOB = db.Column(db.String(), nullable = False)
  
    

    def __init__(self, uuid, name, SSN, DOB):
        self.uuid = uuid
        self.name = name
        self.SSN = SSN
        self.DOB = DOB

    def __repr__(self):
        return f"<Constituent {self.name}>"


class forms(db.Model):
    __tablename__ = 'forms'

    constituent_id = db.Column(db.Integer, ForeignKey('constituents.uuid'), unique = True)
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_upload_date = db.Column(db.String(), primary_key= True)
    #The information that should be added here is the date they uploaded, the forms could be null except for the mandatory

    #Mandatory
    IR = db.Column(db.String(), nullable = False)
    ACC = db.Column(db.String(), nullable = False)
    CC = db.Column(db.String(), nullable = False)
    #Optional
    ABF = db.Column(db.String())
    MF = db.Column(db.String())
    PR = db.Column(db.String())

    def __init__(self, IR, ACC, CC, ABF, MF, PR):
        self.IR = IR
        self.ACC = ACC
        self.CC = CC
        self.ABF = ABF
        self.MF = MF
        self.PR = PR

    


   
    
class IR(db.Model):
    __tablename__ = 'incident report'
    constituent_id = db.Column(db.Integer, ForeignKey('constituents.uuid'), primary_key = True, unique=True)
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_upload_date = db.Column(db.String(),ForeignKey('forms.form_upload_date'))

    case_number = db.Column(db.String())
    CAD_incident_num = db.Column(db.String())
    report_type = db.Column(db.String())
    date_time_occured = db.Column(db.String())
    date_time_reported = db.Column(db.String())
    public_narrative = db.Column(db.String())



class ACC(db.Model):
    __tablename__ = 'application for criminal complaint'
    constituent_id = db.Column(db.Integer, ForeignKey('constituents.uuid'), primary_key = True)
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_upload_date = db.Column(db.String(),ForeignKey('forms.form_upload_date'))

    summons = db.Column(db.String())
    hearing_requested = db.Column(db.String())
    court = db.Column(db.String())
    arrest_status_of_accused = db.Column(db.String())
    arrest_date = db.Column(db.String())
    in_custody = db.Column(db.String())
    officer_id_num = db.Column(db.String())
    agency = db.Column(db.String())
    type = db.Column(db.String())
    name = db.Column(db.String())
    birth_surname = db.Column(db.String())
    address = db.Column(db.String())
    date_of_birth = db.Column(db.String())
    place_of_birth = db.Column(db.String())
    ssn = db.Column(db.String())
    pcs_num = db.Column(db.String())
    sid = db.Column(db.String())
    marital_status = db.Column(db.String())
    driver_license_num = db.Column(db.String())
    driver_license_state = db.Column(db.String())
    driver_license_exp = db.Column(db.String())
    gender = db.Column(db.String())
    race = db.Column(db.String())
    height = db.Column(db.String())
    weight = db.Column(db.String())
    eyes = db.Column(db.String())
    hair = db.Column(db.String())
    ethnicity = db.Column(db.String())
    primary_language = db.Column(db.String())
    complexion = db.Column(db.String())
    scars_marks_tattoos = db.Column(db.String())
    employer_name = db.Column(db.String())
    school_name = db.Column(db.String())
    day_phone = db.Column(db.String())
    mother_name = db.Column(db.String())
    mother_maiden_name = db.Column(db.String())
    father_name = db.Column(db.String())
    complainant_type = db.Column(db.String())
    police_department = db.Column(db.String())


class CC(db.Model):
    __tablename__ = 'criminal complaint'
    constituent_id = db.Column(db.Integer, ForeignKey('constituents.uuid'), primary_key = True)
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_date = db.Column(db.String(),ForeignKey('forms.form_upload_date'))

    docket_number = db.Column(db.String())
    full_name = db.Column(db.String())
    date_of_birth = db.Column(db.String())
    date_of_issued_complaint = db.Column(db.String())
    date_of_offense = db.Column(db.String())
    date_of_arrest = db.Column(db.String())
    next_event_date = db.Column(db.String())
    obtn_num = db.Column(db.String())
    incident_report_num = db.Column(db.String())
    court_address = db.Column(db.String())
    defendant_address = db.Column(db.String())
    offense_code = db.Column(db.String())


class ABF(db.Model):
    __tablename__ = 'arrest booking form'
    constituent_id = db.Column(db.Integer, ForeignKey('constituents.uuid'), primary_key = True)
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_date = db.Column(db.String(),ForeignKey('forms.form_upload_date'))

    report_date = db.Column(db.String())
    booking_status = db.Column(db.String())
    printed_by = db.Column(db.String())
    district = db.Column(db.String())
    ucr_code = db.Column(db.String())
    obtn = db.Column(db.String())
    court_of_appearance = db.Column(db.String())
    master_name = db.Column(db.String())
    age = db.Column(db.String())
    location_of_arrest = db.Column(db.String())
    booking_name = db.Column(db.String())
    alias = db.Column(db.String())
    pad = db.Column(db.String())
    charges = db.Column(db.String())
    booking_num = db.Column(db.String())
    incident_report_num = db.Column(db.String())
    cr_num = db.Column(db.String())
    booking_date = db.Column(db.String())
    arrest_date = db.Column(db.String())
    ra_num = db.Column(db.String())
    sex = db.Column(db.String())
    height = db.Column(db.String())
    occupation = db.Column(db.String())
    race = db.Column(db.String())
    weight = db.Column(db.String())
    employer_school = db.Column(db.String())
    date_of_birth = db.Column(db.String())
    build = db.Column(db.String())
    employer_school_address = db.Column(db.String())
    place_of_birth = db.Column(db.String())
    eye_color = db.Column(db.String())
    ssn = db.Column(db.String())
    marital_status = db.Column(db.String())
    hair_color = db.Column(db.String())
    operators_license = db.Column(db.String())
    mothers_name = db.Column(db.String())
    complexion = db.Column(db.String())
    state = db.Column(db.String())
    fathers_name = db.Column(db.String())
    phone_used = db.Column(db.String())
    scars_marks_tattoos = db.Column(db.String())
    examined_at_hospital = db.Column(db.String())
    clothing_description = db.Column(db.String())
    breathalyzer_used = db.Column(db.String())
    examined_by_ems = db.Column(db.String())
    arresting_officer = db.Column(db.String())
    cell_number = db.Column(db.String())
    booking_officer = db.Column(db.String())
    partners_number = db.Column(db.String())
    informed_of_rights = db.Column(db.String())
    unit_number = db.Column(db.String())
    placed_in_cell_by = db.Column(db.String())
    trans_unit_num = db.Column(db.String())
    searched_by = db.Column(db.String())
    cautions = db.Column(db.String())
    booking_comments = db.Column(db.String())
    visibile_injuries = db.Column(db.String())
    person_notified = db.Column(db.String())
    relationship = db.Column(db.String())
    phone = db.Column(db.String())
    address = db.Column(db.String())
    juv_prob_officer = db.Column(db.String())
    notified_by = db.Column(db.String())
    notified_date_time = db.Column(db.String())
    bail_set_by = db.Column(db.String())
    I_selected_the_bail_comm = db.Column(db.String())
    bailed_by = db.Column(db.String())
    amount = db.Column(db.String())
    bop_check = db.Column(db.String())
    suicide_check = db.Column(db.String())
    bop_warrant = db.Column(db.String())
    bop_court = db.Column(db.String())


class MF(db.Model):
    __tablename__ = 'miranda form'
    constituent_id = db.Column(db.Integer, ForeignKey('constituents.uuid'), primary_key = True)
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_date = db.Column(db.String(),ForeignKey('forms.form_upload_date'))
    
    booking_name = db.Column(db.String())
    first = db.Column(db.String())
    middle = db.Column(db.String())
    suffix = db.Column(db.String())
    home_address = db.Column(db.String())
    report_date = db.Column(db.String())
    booking_status = db.Column(db.String())
    printed_by = db.Column(db.String())
    sex = db.Column(db.String())
    race = db.Column(db.String())
    date_of_birth = db.Column(db.String())
    district = db.Column(db.String())
    booking_num = db.Column(db.String())
    arrest_date = db.Column(db.String())
    incident_num = db.Column(db.String())
    booking_date = db.Column(db.String())
    charges = db.Column(db.String())
    telephone_used = db.Column(db.String())
    breathalyzer_used = db.Column(db.String())
    examined_at_hospital = db.Column(db.String())
    examined_by_ems = db.Column(db.String())
    visibile_injuries = db.Column(db.String())
    money = db.Column(db.String())
    property_storage_num = db.Column(db.String())
    property = db.Column(db.String())

class PR(db.Model):
    __tablename__ = 'probation record'
    constituent_id = db.Column(db.Integer, ForeignKey('constituents.uuid'), primary_key = True)
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_date = db.Column(db.String(),ForeignKey('forms.form_upload_date'))
    
    pcf = db.Column(db.String())
    date_of_birth = db.Column(db.String())
    age = db.Column(db.String())
    birthplace = db.Column(db.String())
    mother = db.Column(db.String())
    father = db.Column(db.String())
    height = db.Column(db.String())
    weight = db.Column(db.String())
    hair = db.Column(db.String())
    eyes = db.Column(db.String())
    gender = db.Column(db.String())
    race = db.Column(db.String())
    ethnicity = db.Column(db.String())
    driver_license_num = db.Column(db.String())
    cari = db.Column(db.String())
    records_include = db.Column(db.String())
    
"""
if __name__ == "__main__":

    app.url_map.strict_slashes = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.init_app(app)    # this is important!
        db.create_all()
    print('\n\nHello!\n\n')
  
    engine = create_engine("sqlite:///test.db")
    Session = sessionmaker(bind=engine)
    session = Session()


    curtis_form = Forms("curtis-form-07-02-1999", '07-02-1999', "Curtis Mason")
    curtis_form2 = Forms("curtis-form-07-02-2000", '07-02-2000', "Curtis Mason")

    session.add(curtis_form)
    session.add(curtis_form2)
    person = Constituents("Curtis Mason")

    session.add(person)
    session.commit()

    me = session.query(Constituents).get('Curtis Mason')
    print(me.name)

    myforms = session.query(Forms).filter_by(constituent_name=me.name).all())
    print(myforms)
    print(myforms[0].date)


"""
