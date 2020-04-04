import os
from flask import Blueprint, render_template, request, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from hmrm.models import db, Users

# app = Blueprint("hmrm", __name__, static_folder="static/")
app = Flask(__name__)

db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')


bcrypt = Bcrypt(app)

current_user = {
    "is_authenticated": True,
    "name": "Yashas Samaga",
    "first_name": "Yashas",
    "last_name": "Samaga",
    "email": "trump2020@losers.com",

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
        "active" : 1432,
        "active_increment" : 1432 - 1244,
        "recovered" : 74,
        "recovered_increment" : 4,
        "deaths" : 16,
        "deaths_increment" : 2 
    },

    "history": {
        "active": [62, 109, 450, 683, 892, 1043, 1244, 1432],
        "recovered": [4, 8, 12, 24, 44, 67, 70, 74],
        "deaths": [0, 0, 0, 1, 6, 12, 14, 16],
    }
}

current_entity2 = {
    "name" : "Hogwarts Hospital",
    "id" : 1,
    "shortname" : "HogwartsHsp",
    "type" : "institution",
    "capacity" : 1000,
    "cases" : {
        "active" : 1432,
        "active_increment" : 1432 - 1244,
        "recovered" : 74,
        "recovered_increment" : 4,
        "deaths" : 16,
        "deaths_increment" : 2 
    },

    "history" : {
        "active" : [62, 109, 450, 683, 892, 1043, 1244, 1432],
        "recovered" : [4, 8, 12, 24, 44, 67, 70, 74],
        "deaths" : [0, 0, 0, 1, 6, 12, 14, 16],
    }
}

current_entity3 = {
    "name" : "Hogwarts COVID Camp",
    "id" : 2,
    "shortname" : "HogwartsCOVID",
    "type" : "institution",
    "capacity" : 1000,
    "cases" : {
        "active" : 56,
        "active_increment" : 4,
        "recovered" : 4,
        "recovered_increment" : 2,
        "deaths" : 1,
        "deaths_increment" : 1 
    },

    "history" : {
        "active" : [62, 109, 450, 683, 892, 1043, 1244, 1432],
        "recovered" : [4, 8, 12, 24, 44, 67, 70, 74],
        "deaths" : [0, 0, 0, 1, 6, 12, 14, 16],
    }
}

current_entity4 = {
    "name" : "Hogwarts Clinic",
    "id" : 3,
    "shortname" : "Hogwarts Clinic",
    "type" : "institution",
    "capacity" : 100,
    "cases" : {
        "active" : 82,
        "active_increment" : 4,
        "recovered" : 14,
        "recovered_increment" : 2,
        "deaths" : 7,
        "deaths_increment" : 1 
    },

    "history" : {
        "active" : [62, 109, 450, 683, 892, 1043, 1244, 1432],
        "recovered" : [4, 8, 12, 24, 44, 67, 70, 74],
        "deaths" : [0, 0, 0, 1, 6, 12, 14, 16],
    }
}

current_objects = [current_entity2, current_entity3, current_entity4]
current_admin = {
    "name" : "Hogwarts City",
    "shortname" : "HogwartsCity",
    "type" : "admnistration",
    "cases" : {
        "active" : 1432,
        "active_increment" : 1432 - 1244,
        "recovered" : 74,
        "recovered_increment" : 4,
        "deaths" : 16,
        "deaths_increment" : 2 
    },

    "history" : {
        "active" : [62, 109, 450, 683, 892, 1043, 1244, 1432],
        "recovered" : [4, 8, 12, 24, 44, 67, 70, 74],
        "deaths" : [0, 0, 0, 1, 6, 12, 14, 16],
    },

    "objects" : current_objects
}

@app.route("/")
def index():
    return render_template("index.html", current_user=current_user)


@app.route("/user/login", methods=['GET', 'POST'])
def user_login():
    """
    Login API

    Methods = POST, GET


        POST
            Fields:
                username - Username in the form of email for now.
                password

    """

    # Currently, this API is coupled with the rendering part.

    print(request.method)

    if request.method == 'GET':
        if current_user['is_authenticated']:
            print("User already logged in")
            # return a view for already logged in

    elif request.method == 'POST':
        try:

            if current_user['is_authenticated']:
                print("User already logged in")
                # return a view for already logged in

            print(request.form.keys)
            password = request.form['password']
            user_check = Users(email=request.form['username'], password=None,
                               fname=None, lname=None)
            stored = db.session.query(Users.password).filter_by(
                email=request.form['username']).scalar()

            if bcrypt.check_password_hash(stored, password):
                print("User authenticated")
                user_check = db.session.query(Users).filter_by(
                    email=request.form['username']).scalar()
                print(user_check.fname + " has logged in.")
                current_user['name'] = user_check.fname + \
                    " " + user_check.lname
                current_user['first_name'] = user_check.fname
                current_user['last_name'] = user_check.lname
                current_user['email'] = user_check.email
                current_user['is_authenticated'] = True


            else:
                # Wrong password UI
                print("Wrong login credentials")

            pass

        except KeyError as e:
            print(e)
            print("Keyerror")
            # TODO Return an error instead.

    # TODO Use Oauth token based login instead of rendering later.
    return render_template("user/login.html", current_user=current_user)


@app.route("/user/register", methods=['GET', 'POST'])
def user_register():

    print(request.method)
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        try:
            print(request.form.keys)

            if request.form['password'] != request.form['password']:
                print("Passwords do not match")
                # TODO Return an error to the view or API error.
                return render_template("user/register.html",
                                       current_user=current_user)

            password = request.form['password']
            print(password)
            hashed = bcrypt.generate_password_hash(password).decode('utf-8')
            print(hashed)

            # TODO Verify whether the email is valid.

            # Add user.
            user_add = Users(
                request.form['fname'], request.form['lname'],
                request.form['username'], hashed)

            db.session.add(user_add)
            db.session.commit()

            # Do stuff

        except KeyError as e:
            print(e)
            print("Keyerror")

    return render_template("user/register.html", current_user=current_user)


@app.route("/user/logout")
def user_logout():
    current_user["is_authenticated"] = False
    return index()


@app.route("/user/dashboards")
def user_dashboards():
    return render_template("user/dashboards.html", current_user=current_user)


@app.route("/institution/create")
def institution_create():
    return render_template("institution/create.html", current_user=current_user)


@app.route("/administration/create")
def administration_create():
    return render_template("administration/create.html", current_user=current_user)

@app.route("/administration/overview/<int:id>")
def administration_overview(id):
    return render_template("administration/overview.html", overview_id = int(id), current_user = current_user, current_admin = current_admin)

@app.route("/administration/view/<int:id>")
def administration_view(id):
    if id < len(current_objects):
        return render_template("administration/view.html", view_id = int(id), current_user = current_user, current_entity = current_objects[id])
    return user_dashboards()
