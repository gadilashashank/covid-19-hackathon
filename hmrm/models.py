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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    max_bed = db.Column(db.Integer)
    current_beds = db.Column(db.Integer)
    state = db.Column(db.String(80))
    district = db.Column(db.String(80))
    num_ventilators = db.Column(db.Integer)
    mask_needed = db.Column(db.Integer)
    num_testing_kits = db.Column(db.Integer)
    testing_capacity = db.Column(db.Integer)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    sex = db.Column(db.String(1))
    hospital_id = db.Column(db.Integer, db.ForeignKey(
        Hospital.id, ondelete="CASCADE"), nullable=False)
    # hospital_ref = db.relationship("hospital", backref=db.backref("hospital_from_patient", cascade="all"))
    hospital_ref = db.relationship(
        "Hospital", backref=db.backref("Hospital", cascade="all"))

    condition = db.Column(db.String(80))
    age = db.Column(db.Integer)
    disease = db.Column(db.String(512))
    history = db.Column(db.String(1024))
