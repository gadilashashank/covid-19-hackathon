from flask import Blueprint, session, render_template, request
app = Blueprint("hmrm", __name__, static_folder="static/")

current_user = {
    "is_authenticated" : True,
    "name" : "Harry Potter",
    "first_name" : "Harry",
    "last_name" : "Potter",
    "email" : "trump2020never@losers.com",

    "dashboards" : [
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

    "history" : {
        "active" : [62, 109, 450, 683, 892, 1043, 1244, 1432],
        "recovered" : [4, 8, 12, 24, 44, 67, 70, 74],
        "deaths" : [0, 0, 0, 1, 6, 12, 14, 16],
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
    return render_template("index.html", current_user = current_user)

@app.route("/user/login")
def user_login():
    return render_template("user/login.html", current_user = current_user)

@app.route("/user/register")
def user_register():
    return render_template("user/register.html", current_user = current_user)

@app.route("/user/logout")
def user_logout():
    current_user["is_authenticated"] = False
    return index()

@app.route("/user/dashboards")
def user_dashboards():
    return render_template("user/dashboards.html", current_user = current_user)

@app.route("/institution/create")
def institution_create():
    return render_template("institution/create.html", current_user = current_user)

@app.route("/administration/create")
def administration_create():
    return render_template("administration/create.html", current_user = current_user)

@app.route("/administration/overview/<int:id>")
def administration_overview(id):
    return render_template("administration/overview.html", overview_id = int(id), current_user = current_user, current_admin = current_admin)

@app.route("/administration/view/<int:id>")
def administration_view(id):
    if id < len(current_objects):
        return render_template("administration/view.html", view_id = int(id), current_user = current_user, current_entity = current_objects[id])
    return user_dashboards()
