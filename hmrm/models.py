from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy
from datetime import date as DATE


db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    fname = db.Column(db.String())
    lname = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, fname, lname, email, password):
        self.email = email
        self.lname = lname
        self.fname = fname
        self.password = password

    def __repr__(self):
        # return '<id {}>'.format(self.user_id)
        return self

    def serialize(self):
        return {
            'user_id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'password': self.password,
            'email': self.email,
        }


class Hospital(db.Model):
    __tablename__ = 'hospitals'

    hospital_id = db.Column(db.Integer, primary_key=True,autoincrement=True )
    name = db.Column(db.String(80) , nullable = False)
    sname = db.Column(db.String(80), nullable = False)
    address = db.Column(db.String(200))
    email_admin = db.Column(db.String(330))
    email_lab= db.Column(db.String(330))
    phone_lab= db.Column(db.String(30), nullable = False)
    phone_admin= db.Column(db.String(30), nullable = False)
    patient_capacity = db.Column(db.Integer)
    testing_capacity = db.Column(db.Integer)
    admin = db.Column(db.String(330), db.ForeignKey(
        Users.email, ondelete="CASCADE"), nullable=False)

    
    def __init__(self, name, sname, email_admin, phone_admin,
            phone_lab, email_lab, patient_capacity, testing_capacity, address, admin): 
        #, district, state):
        self.name = name
        self.sname = sname
        self.patient_capacity = patient_capacity
        self.testing_capacity = testing_capacity
        self.address = address
        self.email_admin = email_admin
        self.email_lab = email_lab
        self.phone_lab = phone_lab
        self.phone_admin = phone_admin
        self.admin = admin
        # self.admin = 
        # self.district = district
        # self.state = state
    # def __repr__(self):
    #     return self

class Patient(db.Model):
    __tablename__ = 'patients'

    patient_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(80))
    sex = db.Column(db.String(10))
    hospital_id = db.Column(db.Integer, db.ForeignKey(
        Hospital.hospital_id, ondelete="CASCADE"), nullable=False)
    hospital_ref = db.Column(db.String(100))

    condition = db.Column(db.String(32))
    age = db.Column(db.Integer)
    history = db.Column(db.String(1024))

    def __init__(self, name, sex, hospital_id, ref_str, state, history):
        self.name = name
        self.sex = sex
        self.hospital_id = hospital_id
        self.hospital_ref = ref_str

        if state == "suspected":
            self.condition = "SUSPECTED"
        if state == "dead":
            self.condition = "DEAD"
        if state == "recovered":
            self.condition = "RECOVERED"
        if state == "negative":
            self.condition = "NEGATIVE"
        if state == "active":
            self.condition = "ACTIVE"

        self.history = history

class History_patient(db.Model):
    __tablename__ = 'history_patient'
    patient_id_rec = db.Column(db.Integer, primary_key = True,
                 nullable = False, autoincrement=True)
    # patient_id = db.Column(db.Integer, nullable = False)
    date = db.Column(db.DateTime)
    condition = db.Column(db.String(32))
    patient_id = db.Column(db.Integer, db.ForeignKey(
        Patient.patient_id, ondelete="CASCADE"), nullable = False)

    def __init__(self, patient_id, state):
        self.date = DATE.today()
        self.patient_id = patient_id

        if state == "suspected":
            self.condition = "SUSPECTED"
        if state == "dead":
            self.condition = "DEAD"
        if state == "recovered":
            self.condition = "RECOVERED"
        if state == "negative":
            self.condition = "NEGATIVE"
        if state == "active":
            self.condition = "ACTIVE"

class Administration(db.Model):
    doff_id = db.Column(db.Integer, primary_key = True, nullable = False, 
            autoincrement = True)
    name = db.Column(db.String(100))
    sname = db.Column(db.String(30))
    region = db.Column(db.String(50))
    admin = db.Column(db.String(330), db.ForeignKey(
        Users.email, ondelete="CASCADE"), nullable=False)

    def __init__(self, name, sname, admin, region):
        self.name = name
        self.sname = sname
        self.region = region
        self.admin = admin

class Member(db.Model):
    __tablename__ = 'member'

    memberid = db.Column(db.Integer, primary_key = True, nullable = False, 
            autoincrement = True)
    userid = db.Column(db.String(330), db.ForeignKey(
        Users.email, ondelete="CASCADE"), nullable=False)
    type = db.Column(db.String(30))
    dashboard_id = db.Column(db.Integer)

    def __init__(self, userid, type, dashboard_id):
        self.userid = userid
        self.type = type
        self.dashboard_id = dashboard_id

class Invitation(db.Model):
    __tablename__ = 'invitation'
    inviteid = db.Column(db.Integer, primary_key = True, nullable = False, 
            autoincrement = True)
    to_user = db.Column(db.String(330), db.ForeignKey(
        Users.email, ondelete="CASCADE"), nullable=False)
    from_user = db.Column(db.String(330), db.ForeignKey(
        Users.email, ondelete="CASCADE"), nullable=False)
    invited_date = db.Column(db.DateTime)
    type = db.Column(db.String(30))
    dashboard_id = db.Column(db.Integer)

    def __init__(self, to_user, from_user, type, dashboard_id):
        self.to_user = to_user
        self.from_user = from_user
        self.invited_date = DATE.today()
        self.type = type
        self.dashboard_id = dashboard_id       
