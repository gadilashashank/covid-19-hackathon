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
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'user_id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'password': self.password,
            'email': self.email,
        }
