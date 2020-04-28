import sys
sys.path.append('/Users/eloisanitorreda/suffolk-county-DA/Flask/')
from SCDA import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, ForeignKey, MetaData, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#app = Flask(__name__) 
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@localhost/constituents"

#db = SQLAlchemy(app)
#database_name = 'constituents'
Base = declarative_base()
#migrate = Migrate(app,db)


class constituents(db.Model):
    __tablename__ = 'constituents'

    id = db.Column(db.Integer, Sequence('id',start=1,increment=1), unique = True, nullable = False) #Autoincrement, map to people's names, could have lookup table
    name = db.Column(db.String(), primary_key = True, nullable = False)
    SSN = db.Column(db.String(), primary_key = True, nullable = False) #only display last 4
    DOB = db.Column(db.String(), primary_key = True, nullable = False)
    #allForms = db.relationship("forms", back_populates="form_upload_date")


    def __init__(self, name, SSN, DOB):
        self.name = name
        self.SSN = SSN
        self.DOB = DOB

    def __repr__(self):
        return f"<Constituent {self.name}>"


class forms(db.Model):
    __tablename__ = 'forms'

    constituent_id = db.Column(db.Integer, ForeignKey('constituents.id'))
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_upload_date = db.Column(db.DateTime(), primary_key= True, nullable=False)
    #The information that should be added here is the date they uploaded, the forms could be null except for the mandatory

    #Mandatory
    IR = db.Column(db.String(), nullable = False)
    ACC = db.Column(db.String(), nullable = False)
    CC = db.Column(db.String(), nullable = False)
    #Optional
    ABF = db.Column(db.String())
    MF = db.Column(db.String())
    PR = db.Column(db.String())

    def __init__(self, constituent_id, form_upload_date, IR, ACC, CC, ABF='', MF='', PR=''):
        self.constituent_id = constituent_id
        self.form_upload_date = form_upload_date
        self.IR = IR
        self.ACC = ACC
        self.CC = CC
        self.ABF = ABF
        self.MF = MF
        self.PR = PR

    

class IR(db.Model):
    __tablename__ = 'incident_report'
    constituent_id = db.Column(db.Integer, ForeignKey('constituents.id'), primary_key=True)
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_upload_date = db.Column(db.DateTime(), ForeignKey('forms.form_upload_date'), primary_key=True)

    case_number = db.Column(db.String())
    CAD_incident_num = db.Column(db.String())
    report_type = db.Column(db.String())
    date_time_occured = db.Column(db.String())
    date_time_reported = db.Column(db.String())
    public_narrative = db.Column(db.String())
    image = db.Column(db.String())

    def __init__(self, constituent_id, form_upload_date, image, case_number='', CAD_incident_num='', report_type='', date_time_occured='', date_time_reported='', public_narrative=''):
        self.constituent_id = constituent_id
        self.form_upload_date = form_upload_date
        self.case_number = case_number
        self.CAD_incident_num = CAD_incident_num
        self.report_type = report_type
        self.date_time_occured = date_time_occured
        self.date_time_reported = date_time_reported
        self.public_narrative = public_narrative
        self.image = image



class ACC(db.Model):
    __tablename__ = 'application_for_criminal_complaint'
    constituent_id = db.Column(db.Integer, ForeignKey('constituents.id'), primary_key=True)
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_upload_date = db.Column(db.DateTime(),ForeignKey('forms.form_upload_date'), primary_key=True)

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
    image = db.Column(db.String())

    def __init__(self,constituent_id,form_upload_date, image, summons='',hearing_requested='',court='',arrest_status_of_accused='',arrest_date='',in_custody='',officer_id_num='',agency='',type='',name='',birth_surname='',address='',date_of_birth='', place_of_birth='',ssn='',pcs_num='',sid='',marital_status='',driver_license_num='',driver_license_exp='',gender='',race='',height='',weight='',eyes='',hair='',ethnicity='',primary_language='',complexion='',scars_marks_tattoos='', employer_name='',school_name='',day_phone='',mother_name='',mother_maiden_name='',father_name='',complainant_type='',police_department=''):
        self.form_upload_date = form_upload_date
        self.hearing_requested = hearing_requested
        self.court = court
        self.arrest_status_of_accused = arrest_status_of_accused
        self.arrest_date = arrest_date
        self.in_custody = in_custody
        self.officer_id_num = officer_id_num
        self.agency = agency
        self.type = type
        self.name = name
        self.birth_surname = birth_surname
        self.address = address
        self.date_of_birth = date_of_birth
        self.place_of_birth = place_of_birth
        self.ssn = ssn
        self.pcs_num = pcs_num
        self.sid = sid
        self.marital_status = marital_status
        self.driver_license_num = driver_license_num
        self.driver_license_state = driver_license_state
        self.driver_license_exp = driver_license_exp
        self.gender = gender
        self.race = race
        self.height = height
        self.weight = weight
        self.eyes = eyes
        self.hair = hair
        self.ethnicity = ethnicity
        self.primary_language = primary_language
        self.complexion = complexion
        self.scars_marks_tattoos = scars_marks_tattoos
        self.employer_name = employer_name
        self.school_name = school_name
        self.day_phone
        self.mother_name = mother_name
        self.mother_maiden_name = mother
        self.father_name = father_name
        self.complainant_type = complainant_type
        self.police_department = police_department
        self.image = image
        
        
     
    


class CC(db.Model):
    __tablename__ = 'criminal_complaint'
    constituent_id = db.Column(db.Integer, ForeignKey('constituents.id'), primary_key=True)
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_upload_date = db.Column(db.DateTime(),ForeignKey('forms.form_upload_date'))

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
    image = db.Column(db.String())
    
    def __init__(self,constituent_id,form_upload_date, image, docket_number='', full_name='', date_of_birth='', date_of_issued_complaint='', date_of_offense='',date_of_arrest='',next_event_date='',obtn_num='',incident_report_num='',court_address='',defendant_address='',offense_code=''):
        self.constituent_id = constituent_id
        self.form_upload_date = form_upload_date
        self.docket_number = docket_number
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.date_of_issued_complaint = date_of_issued_complaint
        self.date_of_offense = date_of_offense
        self.date_of_arrest = date_of_arrest
        self.next_event_date = next_event_date
        self.obtn_num = obtn_num
        self.incident_report_num = incident_report_num
        self.court_address = constituents
        self.defendant_address = defendant_address
        self.offense_code = offense_code
        self.image = image


class ABF(db.Model):
    __tablename__ = 'arrest_booking_form'
    constituent_id = db.Column(db.Integer, ForeignKey('constituents.id'), primary_key=True)
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_upload_date = db.Column(db.DateTime(),ForeignKey('forms.form_upload_date'))

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
    mother_name = db.Column(db.String())
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
    i_selected_the_bail_comm = db.Column(db.String())
    bailed_by = db.Column(db.String())
    amount = db.Column(db.String())
    bop_check = db.Column(db.String())
    suicide_check = db.Column(db.String())
    bop_warrant = db.Column(db.String())
    bop_court = db.Column(db.String())
    image = db.Column(db.String())

    def __init__(self,constituent_id,form_upload_date, image,report_date='',booking_status='',printed_by='',district='',ucr_code='',obtn='',court_of_appearance='',master_name='',age='',location_of_arrest='',booking_name='',alias='',pad='',charges='',booking_num='',incident_report_num='',cr_num='',booking_date='',arrest_date='',ra_num='',sex='',height='',occupation='',race='',weight='', employer_school='', date_of_birth='',build='',employer_school_address='',place_of_birth='',eye_color='',ssn='',marital_status='',hair_color='',operators_license='',mother_name='',complexion='',state='',fathers_name='',phone_used='',scars_marks_tattoos='',examined_at_hospital='',clothing_description='',breathalyzer_used='',examined_by_ems='',arresting_officer='',cell_number='',booking_officer='',partners_number='',informed_of_rights='',unit_number='',placed_in_cell_by='',trans_unit_num='',searched_by='',cautions='',booking_comments='',visibile_injuries='',person_notified='',relationship='',phone='',address='',juv_prob_officer='',notified_by='',notified_date_time='',bail_set_by='',i_selected_the_bail_comm='',bailed_by='',amount='',bop_check='',suicide_check='',bop_warrant='',bop_court=''):
        self.report_date = report_date
        self.booking_status = booking_status
        self.printed_by = printed_by
        self.district = district
        self.ucr_code = ucr_code
        self.obtn = obtn
        self.court_of_appearance = court_of_appearance
        self.master_name = master_name
        self.age = age
        self.location_of_arrest = location_of_arrest
        self.booking_name = booking_name
        self.alias = alias
        self.pad = pad
        self.charges = charges
        self.booking_num = booking_num
        self.incident_report_num = incident_report_num
        self.cr_num = cr_num
        self.booking_date = booking_date
        self.arrest_date = arrest_date
        self.ra_num = ra_num
        self.sex = sex
        self.height = height
        self.occupation = occupation
        self.race = race
        self.weight = weight
        self.employer_school = employer_school
        self.date_of_birth = date_of_birth
        self.build = build
        self.employer_school_address = employer_school_address
        self.place_of_birth = place_of_birth
        self.eye_color = eye_color
        self.ssn = ssn
        self.marital_status = marital_status
        self.hair_color = hair_color
        self.operators_license = operators_license
        self.mother_name = mother_name
        self.complexion = complexion
        self.state = state
        self.fathers_name = fathers_name
        self.phone_used = phone_used
        self.scars_marks_tattoos = scars_marks_tattoos
        self.examined_at_hospital = examined_at_hospital
        self.clothing_description = clothing_description
        self.breathalyzer_used = breathalyzer_used
        self.examined_by_ems = examined_by_ems
        self.arresting_officer = arresting_officer
        self.cell_number = cell_number
        self.booking_officer = booking_officer
        self.partners_number = partners_number
        self.informed_of_rights = informed_of_rights
        self.unit_number = unit_number
        self.placed_in_cell_by = placed_in_cell_by
        self.trans_unit_num = trans_uni
        self.searched_by = searched_by
        self.cautions = cautions
        self.booking_comments = booking_comments
        self.visibile_injuries = visibile_injuries
        self.person_notified = person_notified
        self.relationship = relationship
        self.phone = phone
        self.address = address
        self.juv_prob_officer = juv_prob_officer
        self.notified_by = notified_by
        self.notified_date_time = notified_date_time
        self.bail_set_by = bail_set_by
        self.i_selected_the_bail_comm = i_selected_the_bail_comm
        self.bailed_by = bailed_by
        self.amount = amount
        self.bop_check = bop_check
        self.suicide_check = suicide_check
        self.bop_warrant = bop_warrant
        self.bop_court = bop_court
        self.image = image

class MF(db.Model):
    __tablename__ = 'miranda_form'
    constituent_id = db.Column(db.Integer, ForeignKey('constituents.id'), primary_key=True)
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_upload_date = db.Column(db.DateTime(),ForeignKey('forms.form_upload_date'))
    
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
    image = db.Column(db.String())
    
    def __init__(self,constituent_id,form_upload_date, image, booking_name="",first="",middle="",suffix="",home_address="",report_date="",booking_status="",printed_by="",sex="",race="",date_of_birth="",district="",booking_num="",charges="",telephone_used="",breathalyzer_used="", examined_at_hospital="",examined_by_ems="",visibile_injuries="",money="",property_storage_num="",property=""):    
         self.booking_name =  booking_name
         self.first = first
         self.middle=middle
         self.suffix=suffix
         self.home_address=home_address
         self.report_date=report_date
         self.booking_status=booking_status
         self.printed_by=printed_by
         self.sex =sex 
         self.race=race
         self.date_of_birth=date_of_birth
         self.district=district
         self.booking_num=booking_num
         self.charges=charges
         self.telephone_used=telephone_used
         self.breathalyzer_used=breathalyzer_used
         self.examined_at_hospital=examined_at_hospital
         self.examined_by_ems=examined_by_ems
         self.visibile_injuries=  isibile_injuries
         self.money=money
         self.property_storage_num=property_storage_num
         self.property=property
         self.image = image
         

class PR(db.Model):
    __tablename__ = 'probation_record'
    constituent_id = db.Column(db.Integer, ForeignKey('constituents.id'), primary_key=True)
    #constituent_name = db.Column(db.String(), ForeignKey('constituents.name'))
    form_upload_date = db.Column(db.DateTime(),ForeignKey('forms.form_upload_date'))
    image = db.Column(db.String())
    
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
    image = db.Column(db.String())

    def __init__(self,constituent_id,form_upload_date, image,pcf="",date_of_birth="",age="", birthplace="",mother="",father="",height="", weight="", hair="", eyes="", gender="", race="", ethnicity="", driver_license_num="", cari="",records_include=""):
        self.pcf=pcf
        self.date_of_birth=date_of_birth
        self.age=age
        self.birthplace =  birthplace
        self.mother=mother
        self.father =father 
        self.height=height
        self.weight=weight
        self.hair=hair
        self.eyes=eyes
        self.gender=gender
        self.race=race
        self.ethnicity =ethnicity 
        self.driver_license_num=driver_license_num
        self.cari=cari
        self.records_include=records_include
        self.image = image
        
        
        
        
        
        
        
        

        
        
        
        


if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)    # this is important!
        db.create_all()
    engine = create_engine("postgresql://postgres@localhost/constituents")
    Session = sessionmaker(bind=engine)
    session = Session()

    test_constituent = constituents("Test", '1234', "01/01/2020")
    session.add(test_constituent)
    test_constituent_2 = constituents("Test2", '5678', "01/01/2019")
    session.add(test_constituent_2)
    session.commit()

    test_id = test_constituent.id

    test_form = forms(test_id, '04/24/2020', '04/24/2020', '04/24/2020', '04/24/2020')
    test_form_2 = forms(test_constituent_2.id, '04/25/2020', '04/25/2020', '04/25/2020', '04/25/2020')
    test_form_3 = forms(test_constituent_2.id, '04/26/2020', '04/26/2020', '04/26/2020', '04/26/2020')
    session.add(test_form)
    session.add(test_form_2)
    session.add(test_form_3)
    session.commit()

    me = session.query(constituents).get(('Test', '1234', '01/01/2020'))
    you = session.query(constituents).get(('Test2', '5678', '01/01/2019'))
    #print(test_id)
    print(me.id)
    print(you.id)
    myforms = session.query(forms).filter_by(constituent_id=me.id).all()
    yourforms = session.query(forms).filter_by(constituent_id=you.id).all()
    print(myforms)
    print(yourforms)

    test_ir = IR(me.id, myforms[0].IR, 'A', 'A', 'A', 'A', 'A', 'A')
    session.add(test_ir)
    session.commit()
    myir = session.query(IR).filter_by(constituent_id=me.id).all()
    print(myir)

    
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