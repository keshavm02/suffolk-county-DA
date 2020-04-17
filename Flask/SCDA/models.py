from SCDA import db
from sqlalchemy.orm import relationship


class constituents(db.Model):
    __tablename__ = 'constituents'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    SSN = db.Column(db.String()) #we should hash, or only display last 4
    DOB = db.Column(db.String())
    forms = db.Column(db.) 
    

    def __init__(self, name, SSN, DOB):
        self.name = name
        self.SSN = SSN
        self.DOB = DOB

    def __repr__(self):
        return f"<Constituent {self.name}>"


class forms(db.Model):
    __tablename__ = 'forms'

    #Mandatory
    IR = db.Column()
    ACC = db.Column()
    CC = db.Column()
    #Optional
    ABF = db.Column()
    MF = db.Column()
    PR = db.Column()

    Customer.invoices = relationship("Invoice", order_by = Invoice.id, back_populates = "customer")
    
class IR(db.Model):
    __tablename__ = 'incident report'

class ACC(db.Model):
    __tablename__ = 'application for criminal complaint'

class CC(db.Model):
    __tablename__ = 'criminal complaint'

class ABF(db.Model):
    __tablename__ = 'arrest booking form'

class MF(db.Model):
    __tablename__ = 'miranda form'

class PR(db.Model):
    __tablename__ = 'probation record'

    pr_date = #this represent the date that the probation record was made
     #this date will lead a table that has all the information about this specific form on this specific date
    
class pr_date(Model.PR):
    #learn how to make a template model for each form
    #how much space would this take 




