import os
from flask import Blueprint, render_template, request, Flask
from flask_sqlalchemy import SQLAlchemy


# app = Blueprint("hmrm", __name__, static_folder="static/")
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)


current_user = {
    "is_authenticated": True,
    "name": "Yashas Samaga",
    "first_name": "Yashas",
    "last_name": "Samaga",
    "email": "trump2020@losers.com",

    "dashboards": [
        {
            "name": "Manguluru City",
            "type": "administration"
        },
        {
            "name": "Aarogya Hospital",
            "type": "institution"
        },
        {
            "name": "Hyderabad COVID Camp",
            "type": "institution"
        }
    ]
}

current_entity = {
    "name": "Mangaluru City",
    "shortname": "MangaluruCity",
    "type": "admnistration",
    "cases": {
        "active": 1432,
        "active_increment": 1432 - 1244,
        "recovered": 74,
        "recovered_increment": 4,
        "deaths": 16,
        "deaths_increment": 2
    },

    "history": {
        "active": [62, 109, 450, 683, 892, 1043, 1244, 1432],
        "recovered": [4, 8, 12, 24, 44, 67, 70, 74],
        "deaths": [0, 0, 0, 1, 6, 12, 14, 16],
    }
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
        pass

    elif request.method == 'POST':
        try:
            # print(request.form['username'])
            # print(request.form['password'])

            # Do stuff
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
            # TODO Verify whether the email is valid.

            # Add user.

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


@app.route("/administration/view")
def administration_view():
    return render_template("administration/view.html", current_user=current_user, current_entity=current_entity)
