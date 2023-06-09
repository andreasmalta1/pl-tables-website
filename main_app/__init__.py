from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["MAIL_SERVER"] = getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(getenv("MAIL_PORT"))
app.config["MAIL_USE_SSL"] = getenv("MAIL_USE_SSL")
app.config["MAIL_USERNAME"] = getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = getenv("MAIL_PASSWORD")

db = SQLAlchemy(app)

from main_app.api import api
from main_app.contact import contact
from main_app.table import table

from main_app import models

app.register_blueprint(api, url_prefix="/")
app.register_blueprint(contact, url_prefix="/")
app.register_blueprint(table, url_prefix="/")


with app.app_context():
    db.create_all()
