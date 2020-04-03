from flask import Flask
from .hmrm import app

def create_app():
    application = Flask(__name__)
    application.register_blueprint(app, url_prefix="/")
    return application
