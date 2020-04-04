import os
import functools
from flask import Blueprint, render_template, request, Flask, session, abort, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from hmrm.models import db, Users, Hospital

# app = Blueprint("hmrm", __name__, static_folder="static/")

app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)

bcrypt = Bcrypt(app)

current_user = {
    "dashboards": [
        {
            "id" : 0,
            "name" : "Hogwarts City",
            "type" : "administration"
        },
        {
            "id" : 1,
            "name" : "Hogwarts Hospital",
            "type" : "institution"
        },
        {
            "id" : 2,
            "name" : "Hogwarts COVID Camp",
            "type" : "institution"
        }
    ]
}

current_entity = {
    "name" : "Hogwarts",
    "id" : 0,
    "shortname" : "Hogwarts",
    "type" : "admnistration",
    "cases" : {
        "suspected" : 64,
        "suspected_increment" : 12,
        "active" : 1432,
        "active_increment" : 1432 - 1244,
        "recovered" : 74,
        "recovered_increment" : 4,
        "fatal" : 16,
        "fatal_increment" : 2
    },

    "history": {
        "active": [62, 109, 450, 683, 892, 1043, 1244, 1432],
        "recovered": [4, 8, 12, 24, 44, 67, 70, 74],
        "fatal": [0, 0, 0, 1, 6, 12, 14, 16],
    }
}

current_entity2 = {
    "name" : "Hogwarts Hospital",
    "id" : 1,
    "shortname" : "HogwartsHsp",
    "type" : "institution",
    "capacity" : 1000,
    "cases" : {
        "suspected" : 64,
        "suspected_increment" : 12,
        "active" : 1432,
        "active_increment" : 1432 - 1244,
        "recovered" : 74,
        "recovered_increment" : 4,
        "fatal" : 16,
        "fatal_increment" : 2
    },

    "history" : {
        "active" : [62, 109, 450, 683, 892, 1043, 1244, 1432],
        "recovered" : [4, 8, 12, 24, 44, 67, 70, 74],
        "fatal" : [0, 0, 0, 1, 6, 12, 14, 16],
    }
}

current_entity3 = {
    "name" : "Hogwarts COVID Camp",
    "id" : 2,
    "shortname" : "HogwartsCOVID",
    "type" : "institution",
    "capacity" : 1000,
    "cases" : {
        "suspected" : 64,
        "suspected_increment" : 12,
        "active" : 56,
        "active_increment" : 4,
        "recovered" : 4,
        "recovered_increment" : 2,
        "fatal" : 1,
        "fatal_increment" : 1
    },

    "history" : {
        "active" : [62, 109, 450, 683, 892, 1043, 1244, 1432],
        "recovered" : [4, 8, 12, 24, 44, 67, 70, 74],
        "fatal" : [0, 0, 0, 1, 6, 12, 14, 16],
    }
}

current_entity4 = {
    "name" : "Hogwarts Clinic",
    "id" : 3,
    "shortname" : "Hogwarts Clinic",
    "type" : "institution",
    "capacity" : 100,
    "cases" : {
        "suspected" : 64,
        "suspected_increment" : 12,
        "active" : 82,
        "active_increment" : 4,
        "recovered" : 14,
        "recovered_increment" : 2,
        "fatal" : 7,
        "fatal_increment" : 1
    },

    "history" : {
        "active" : [62, 109, 450, 683, 892, 1043, 1244, 1432],
        "recovered" : [4, 8, 12, 24, 44, 67, 70, 74],
        "fatal" : [0, 0, 0, 1, 6, 12, 14, 16],
    }
}

current_objects = [current_entity2, current_entity3, current_entity4]
current_admin = {
    "name" : "Hogwarts City",
    "shortname" : "HogwartsCity",
    "type" : "admnistration",
    "cases" : {
        "suspected" : 64,
        "suspected_increment" : 12,
        "active" : 1432,
        "active_increment" : 1432 - 1244,
        "recovered" : 74,
        "recovered_increment" : 4,
        "fatal" : 16,
        "fatal_increment" : 2
    },

    "history" : {
        "active" : [62, 109, 450, 683, 892, 1043, 1244, 1432],
        "recovered" : [4, 8, 12, 24, 44, 67, 70, 74],
        "fatal" : [0, 0, 0, 1, 6, 12, 14, 16],
    },
}

current_institution = {
    "name" : "Hogwarts Central Hospital",
    "id" : 1,
    "shortname" : "HogwartsCentral",
    "type" : "institution",
    "cases" : {
        "suspected" : 64,
        "suspected_increment" : 12,
        "active" : 1432,
        "active_increment" : 1432 - 1244,
        "recovered" : 74,
        "recovered_increment" : 4,
        "fatal" : 16,
        "fatal_increment" : 2
    },

    "history" : {
        "active" : [62, 109, 450, 683, 892, 1043, 1244, 1432],
        "recovered" : [4, 8, 12, 24, 44, 67, 70, 74],
        "fatal" : [0, 0, 0, 1, 6, 12, 14, 16],
    },
}


# decorator for requiring login to access a page
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kws):
        if session.get('is_authenticated') is not True:
            return redirect(url_for('user_login') + '?source_url=' + request.path)
        return f(*args, **kws)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html", current_user=current_user)

@app.route("/user/login", methods=['GET', 'POST'])
def user_login():
    success_url = request.args.get('source_url', url_for('user_dashboards'))

    if request.method == 'GET':
        if session.get('is_authenticated') is True:
            return redirect(success_url)

    if request.method == 'POST':
        try:
            if session.get('is_authenticated') is True:
                return redirect(success_url)

            password = request.form['password']
            user_check = Users(email=request.form['email'], password=None, fname=None, lname=None)
            stored = db.session.query(Users.password).filter_by(email=request.form['email']).scalar()

            if stored is not None and bcrypt.check_password_hash(stored, password):
                user_check = db.session.query(Users).filter_by(email=request.form['email']).scalar()
                session['name'] = user_check.fname + ' ' + user_check.lname
                session['first_name'] = user_check.fname
                session['last_name'] = user_check.lname
                session['email'] = user_check.email
                session['is_authenticated'] = True
                return redirect(success_url)
            else:
                return render_template("user/login.html", notification="Invalid login credentials.", current_user=current_user)

        except KeyError as e:
            print("KeyError: ", e)
            return render_template("user/login.html", notification="Oops! Something went wrong.", current_user=current_user)

    # TODO Use Oauth token based login instead of rendering later.
    return render_template("user/login.html", current_user=current_user)

@app.route("/user/register", methods=['GET', 'POST'])
def user_register():
    session.clear()
    if request.method == 'POST':
        try:
            if request.form['password'] != request.form['confirm_password']:
                return render_template("user/register.html", notification="password mismatch", current_user=current_user)

            password = request.form['password']
            hashed = bcrypt.generate_password_hash(password).decode('utf-8')

            user_add = Users(
                request.form['fname'], request.form['lname'],
                request.form['email'], hashed)

            db.session.add(user_add)
            db.session.commit()

            session['name'] = user_add.fname + ' ' + user_add.lname
            session['first_name'] = user_add.fname
            session['last_name'] = user_add.lname
            session['email'] = user_add.email
            session['is_authenticated'] = True
            return index()

        except KeyError as e:
            print("Keyerror: ", e)
            return render_template("user/register.html", notification="Something went wrong! Sorry", current_user=current_user)

    return render_template("user/register.html", current_user=current_user)

@app.route("/user/notifications")
@login_required
def user_notifications():
    invitations = [{
        "dashboard_name" : "Hogwarts City",
        "type" : "administration",
        "invited_date" : "04 April 2020 17:24 IST",
    },
    {
        "dashboard_name" : "Hogwarts Central Hospital",
        "type" : "institution",
        "invited_date" : "04 April 2020 17:37 IST",
    }]
    return render_template("user/notifications.html", current_user = current_user, invitations = invitations)

@app.route("/user/logout")
def user_logout():
    session.clear()
    return index()

@app.route("/user/dashboards")
@login_required
def user_dashboards():
    # BACKEND TODO: fetch all dashboards of a user
    # need to make a list like the one below
    # [
    #     {
    #         "id" : 0,
    #         "name" : "Hogwarts City",
    #         "type" : "administration"
    #     },
    #     {
    #         "id" : 1,
    #         "name" : "Hogwarts Hospital",
    #         "type" : "institution"
    #     }
    # ]
    # current_user is the wrong way to do it but use it for now; Yashas will fix thing once the backend can populate info in the current way
    return render_template("user/dashboards.html", current_user=current_user)

@app.route("/institution/create")
@login_required
def institution_create():
    if request.method == "POST":
        data = request.data()
        institution = Hospital(
            name = data['name'],
            max_bed = data['max_bed'],
            current_beds = data['current_bed'],
            state = data['state'],
            district = data['district'],
            num_ventilators = data['num_ventilators'],
            mask_needed = data['num_needed'],
            num_testing_kits = data['num_testing_kits'],
            testing_capacity = data['testing_capacity']
            )
        db.session.add(institution)
        db.commit()
        return jsonify({"status": "success"})
    return render_template("institution/create.html", current_user=current_user)

@app.route("/institution/<int:id>/overview")
# @login_required
def institution_overview(id):
    hospital = db.session.query(Hospital).filter(Hospital.id == id).first()

    dead_patients = db.session.query(Patient).filter(Patient.id == id, Patient.condition == "DEAD").sum()
    suspected_patients = db.session.query(Patient).filter(Patient.id == id, Patient.condition == "SUSPECTED").sum()
    recovered_patients = db.session.query(Patient).filter(Patient.id == id, Patient.condition == "RECOVERED   ").sum()
    active_patients = db.session.query(Patient).filter(Patient.id == id, Patient.condition == "ACTIVE").sum()

    history = db.session.query(History).filter(History.id == id).order_by(date).all()

    active = []
    recovered = []
    fatal = []
    for i in history:
        active.append(i.active)
        recovered.append(i.active)
        fatal.append(i.active)

    entity = {
        "name": hospital.name,
        "id": hospital.id,
        "cases": {
            "active": active,
            "recovered": recovered_patients,
            "fatal": dead_patients,
            "suspected": suspected_patients
        },

        "history": {
            "active": active,
            "recovered": recovered,
            "fatal": fatal
        }
    }
    return render_template("institution/overview.html", current_user = current_user, current_institution = entity)

@app.route("/institution/<int:id>/members")
@login_required
def institution_members(id):
    invitations = [{
      "name" : "Hermi",
      "userid" : 12,
      "created" : "04 April 2020 17:24 IST",
    },
    {
      "name" : "Albus Dumbledore",
      "userid" : 15,
      "created" : "04 April 2020 18:34 IST",
    }]
    return render_template("institution/members.html", current_user = current_user, current_institution = current_institution, invitations = invitations)

@app.route("/institution/<int:id>/information")
@login_required
def institution_information(id):
    contact_info = {
        "phone_admin" : 987654321,
        "phone_lab" :   989762343,
        "email_admin" : "admin@hogwarts.med",
        "email_lab" : "lab@hogwarts.med",
        "address" : "hogwarts"
    }

    capacity_info = {
        "patient_capacity" : 1000,
        "testing_capacity" : 0,
    }

    return render_template("institution/information.html", current_user = current_user, current_institution = current_institution, capacity_info = capacity_info, contact_info = contact_info)

@app.route("/institution/<int:id>/records/patients")
@login_required
def institution_records_patients(id):
    # BACKEND TODO limit to top ten results
    find_results = [
        {
            "recordid" : 1,
            "name" : "Albus Dumbledore",
            "ref" : "HOG#15292883"
        },
        {
            "recordid" : 2,
            "name" : "Albuz Zumbledore",
            "ref" : "HOG#15292884"
        }
    ]
    return render_template("institution/records/patients.html", current_user = current_user, current_institution = current_institution, find_results = find_results)

@app.route("/administration/create")
@login_required
def administration_create():
    return render_template("administration/create.html", current_user=current_user)

@app.route("/administration/<int:id>/overview/")
@login_required
def administration_overview(id):
    return render_template("administration/overview.html", overview_id = int(id), current_user = current_user, current_admin = current_admin)

@app.route("/administration/view/<int:id>")
@login_required
def administration_view(id):
    pass
