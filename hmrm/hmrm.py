from flask import Blueprint
app = Blueprint("hmrm", __name__, static_folder="static/")

@app.route("/")
def index():
    return "Hello"
