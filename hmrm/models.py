from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy


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
    max_bed = db.Column(db.Integer)
    current_bed = db.Column(db.Integer)
    state = db.Column(db.String(80))
    district = db.Column(db.String(80))
    ventilator = db.Column(db.Integer)
    mask_needed = db.Column(db.Integer)
    # testing_kits = db.Column(db.Integer)
    # testing_capacity = db.Column(db.Integer)
    capability_day =db.Column(db.Integer)
    # admin = db.relationship(db.String(330), db.ForeignKey('users.email'))
    # admin = db.relationship("Users", ba
    admin = db.Column(db.String(330), db.ForeignKey(
        Users.email, ondelete="CASCADE"), nullable=False)

    
    def __init__(self, name, sname, email_admin, phone_admin,
            phone_lab, email_lab, max_bed, testing_capacity, address, admin): 
        #, district, state):
        self.name = name
        self.sname = sname
        self.max_bed = max_bed
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    sex = db.Column(db.String(1))
    hospital_id = db.Column(db.Integer, db.ForeignKey(
        Hospital.hospital_id, ondelete="CASCADE"), nullable=False)
    hospital_ref = db.relationship(
        "Hospital", backref=db.backref("Hospital", cascade="all"))

    condition = db.Column(db.String(80))
    age = db.Column(db.Integer)
    disease = db.Column(db.String(512))
    history = db.Column(db.String(1024))
