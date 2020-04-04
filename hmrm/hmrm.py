import os
import functools
from flask import Blueprint, render_template, request, Flask, session, abort, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from hmrm.models import db, Users, Hospital, Patient, History_patient, Administration, Member, Invitation
# from models import db, Users, Hospital

# app = Blueprint("hmrm", __name__, static_folder="static/")

app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)

bcrypt = Bcrypt(app)

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
    return render_template("index.html")

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
                session['userid'] = user_check.user_id
                session['name'] = user_check.fname + ' ' + user_check.lname
                session['first_name'] = user_check.fname
                session['last_name'] = user_check.lname
                session['email'] = user_check.email
                session['is_authenticated'] = True
                return redirect(success_url)
            else:
                return render_template("user/login.html", notification="Invalid login credentials.")

        except KeyError as e:
            print("KeyError: ", e)
            return render_template("user/login.html", notification="Oops! Something went wrong.")

    # TODO Use Oauth token based login instead of rendering later.
    return render_template("user/login.html")

@app.route("/user/register", methods=['GET', 'POST'])
def user_register():
    session.clear()
    if request.method == 'POST':
        try:
            if request.form['password'] != request.form['confirm_password']:
                return render_template("user/register.html", notification="password mismatch")

            password = request.form['password']
            hashed = bcrypt.generate_password_hash(password).decode('utf-8')

            user_add = Users(
                request.form['fname'], request.form['lname'],
                request.form['email'], hashed)

            db.session.add(user_add)
            db.session.commit()

            session['userid'] = user_add.user_id
            session['name'] = user_add.fname + ' ' + user_add.lname
            session['first_name'] = user_add.fname
            session['last_name'] = user_add.lname
            session['email'] = user_add.email
            session['is_authenticated'] = True
            return index()

        except KeyError as e:
            print("Keyerror: ", e)
            return render_template("user/register.html", notification="Something went wrong! Sorry")

    return render_template("user/register.html")

@app.route("/user/notifications", methods=['GET', 'POST'])
@login_required
def user_notifications():
    if request.method == "POST":
        id = request.args["inviteid"]
        Invitation.query.filter_by(inviteid=id).delete()

        type = request.args["type"]
        dbid = request.args["dbid"]
        member_add = Member(session['email'], type, dbid)
        db.session.add(member_add)

        db.session.commit()

    invitations = []

    invs = db.session.query(Invitation).filter(Invitation.to_user == session['email']).all()
    for invitation in invs:
        dashboard_name = ""
        type = invitation.type
        if type == "administration":
            admin = db.session.query(Administration).filter(Administration.doff_id == invitation.dashboard_id).scalar()
            dashboard_name = admin.name
        else:
            hospital = db.session.query(Hospital).filter(Hospital.hospital_id == invitation.dashboard_id).scalar()
            dashboard_name = hospital.name

        invitations.append({
            "inviteid" : invitation.inviteid,
            "dashboard_id" : invitation.dashboard_id,
            "dashboard_name" : dashboard_name,
            "type" : invitation.type,
            "invited_date" : str(invitation.invited_date)
        })

    return render_template("user/notifications.html", invitations = invitations)

@app.route("/user/logout")
def user_logout():
    session.clear()
    return index()

@app.route("/user/dashboards")
@login_required
def user_dashboards():
    # BACKEND TODO: fetch all dashboards of a user
    # need to make a list like the one below
    dashboards = []
    boards = db.session.query(Member).filter(Member.userid == session['email']).all()
    for board in boards:
        dashboard_name = ""
        type = board.type
        if type == "administration":
            admin = db.session.query(Administration).filter(Administration.doff_id == board.dashboard_id).scalar()
            dashboard_name = admin.name
        else:
            hospital = db.session.query(Hospital).filter(Hospital.hospital_id == board.dashboard_id).scalar()
            dashboard_name = hospital.name

        dashboards.append({
            "id" : board.dashboard_id,
            "name" : dashboard_name,
            "type" : board.type
        })

    return render_template("user/dashboards.html", dashboards = dashboards)

@app.route("/institution/create", methods=['GET', 'POST'])
@login_required
def institution_create():
    if request.method == "POST":
        data = request.form
        institution = Hospital(
            name = data['name'],
            sname = data['sname'],
            patient_capacity = data['patient_capacity'],
            testing_capacity = data['testing_capacity'], # Per day capacity
            address = data['address'],
            email_admin = data['email_admin'],
            email_lab = data['email_lab'],
            phone_lab = data['phone_lab'],
            phone_admin = data['phone_admin'],
            admin = session['email']
            )
        db.session.add(institution)
        db.session.flush()

        member_add = Member(session['email'], "institution", institution.hospital_id)
        db.session.add(member_add)

        db.session.commit()
        return redirect(url_for('user_dashboards'))
    return render_template("institution/create.html")

def get_institution_entity(id):
    hospital = db.session.query(Hospital).filter(Hospital.hospital_id == id).first()

    # dead_patients = db.session.query(Patient).filter(Patient.patient_id == id, Patient.condition == "DEAD").sum()
    # suspected_patients = db.session.query(Patient).filter(Patient.id == id, Patient.condition == "SUSPECTED").sum()
    # recovered_patients = db.session.query(Patient).filter(Patient.id == id, Patient.condition == "RECOVERED").sum()
    # active_patients = db.session.query(Patient).filter(Patient.id == id, Patient.condition == "ACTIVE").sum()

    # history = db.session.query(History).filter(History.id == id).order_by(date).all()

    suspected = []
    active = []
    recovered = []
    fatal = []
    # for i in history:
    #     suspected.append(i.suspected)
    #     active.append(i.active)
    #     recovered.append(i.recovered)
    #     fatal.append(i.fatal)

    suspected_increment = 0
    active_increment = 0
    recovered_increment = 0
    fatal_increment = 0

    if len(suspected) > 1:
        suspected_increment = suspected[-1] - suspected[-2]

    if len(active) > 1:
        active_increment = active[-1] - active[-2]

    if len(recovered) > 1:
        recovered_increment = recovered[-1] - recovered[-2]

    if len(suspected) > 1:
        fatal_increment = fatal[-1] - fatal[-2]
    
    entity = {
        "name": hospital.name,
        "shortname" : hospital.sname,
        "id": id,
        "email_admin" : hospital.email_admin,
        "email_lab" : hospital.email_lab,
        "phone_admin" : hospital.phone_admin,
        "phone_lab" : hospital.phone_lab,
        "address" : hospital.address,
        "type" : "institution",
        "patient_capacity" : hospital.patient_capacity,
        "testing_capacity" : hospital.testing_capacity,
        "cases": {
            "suspected" : 64,
            "suspected_increment" : 12,
            "active" : 1432,
            "active_increment" : 1432 - 1244,
            "recovered" : 74,
            "recovered_increment" : 4,
            "fatal" : 16,
            "fatal_increment" : 2
            # "suspected": suspected_patients,
            # "suspected_increment": suspected_increment,
            # "active": active_patients,
            # "active_increment": active_increment,
            # "recovered": recovered_patients,
            # "recovered_increment": recovered_increment,
            # "fatal": dead_patients,
            # "fatal_increment": fatal_increment            
        },

        "history": {
            "active" : [62, 109, 450, 683, 892, 1043, 1244, 1432],
            "recovered" : [4, 8, 12, 24, 44, 67, 70, 74],
            "fatal" : [0, 0, 0, 1, 6, 12, 14, 16],
            # "active": active,
            # "recovered": recovered,
            # "fatal": fatal
        }
    }

    return entity

@app.route("/institution/<int:id>/overview")
@login_required
def institution_overview(id):
    return render_template("institution/overview.html", current_institution = get_institution_entity(id))

@app.route("/institution/<int:id>/members", methods=["POST", "GET"])
@login_required
def institution_members(id):
    invite_error = None
    if request.method == "POST":
        if "inviteid" in request.args:
            # cancelling an invite
            inviteid = request.args["inviteid"]
            Invitation.query.filter_by(inviteid=inviteid).delete()
            db.session.commit()
            return redirect(url_for('institution_members', id = id))
        elif "sendinvite" in request.args:
            # sending an invite
            user_check = db.session.query(Users).filter(Users.email == request.form["email"]).first()
            if user_check == None:
                invite_error = "user does not exist"
            else:
                invite_add = Invitation(request.form["email"], session["email"], "institution", id)
                db.session.add(invite_add)
                db.session.commit()
                return redirect(url_for('institution_members', id = id))

    invitations = []

    invs = db.session.query(Invitation).filter((Invitation.dashboard_id == id) & (Invitation.type == "institution")).all()
    for invitation in invs:
        target = db.session.query(Users).filter(Users.email == invitation.to_user).first()
        invitations.append({
            "name" : target.fname + ' ' + target.lname,
            "userid" : target.user_id,
            "created" : invitation.invited_date,
            "inviteid" : invitation.inviteid
        })

    return render_template("institution/members.html", current_institution = get_institution_entity(id), invitations = invitations, invite_error = invite_error)

@app.route("/institution/<int:id>/information")
@login_required
def institution_information(id):
    return render_template("institution/information.html", current_institution = get_institution_entity(id))

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
    return render_template("institution/records/patients.html", current_institution = get_institution_entity(id), find_results = find_results)

def get_administration_entity(id):
    administration = db.session.query(Administration).filter(Administration.doff_id == id).first()

    current_objects = []
    institutions = db.session.query(Hospital).all()
    for institution in institutions:
        current_objects.append(get_institution_entity(institution.hospital_id))

    entity = {
        "id" : administration.doff_id,
        "name" : administration.name,
        "shortname" : administration.sname,

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

        "objects" : current_objects
    }

    return entity

@app.route("/administration/create", methods=['GET', 'POST'])
@login_required
def administration_create():
    if request.method == "POST":
        data = request.form
        administration = Administration(
            name = data['name'],
            sname = data['sname'],
            region = data['region'],
            admin = session['email']
        )
        db.session.add(administration)
        db.session.flush()

        member_add = Member(session['email'], "administration", administration.doff_id)
        db.session.add(member_add)
        db.session.commit()
        return redirect(url_for('user_dashboards'))

    return render_template("administration/create.html")

@app.route("/administration/<int:id>/overview/")
@login_required
def administration_overview(id):
    return render_template("administration/overview.html", current_admin = get_administration_entity(id))

@app.route("/administration/<int:id>/members")
@login_required
def administration_members(id):
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
    return render_template("administration/members.html", current_admin =  get_administration_entity(id), invitations = invitations)

@app.route("/administration/<int:admin_id>/view/<int:view_id>")
@login_required
def administration_view(admin_id, view_id):
    return render_template("administration/view.html", current_admin =  get_administration_entity(admin_id), current_entity = get_institution_entity(view_id))

