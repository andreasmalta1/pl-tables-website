from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from config import Config

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Create db instance
db = SQLAlchemy()
db.init_app(app)

from models import *
import init_db

from api import api_blueprint as api
from manager import manager_blueprint as manager

with app.app_context():
    db.create_all()
    # init_db.add_teams()
    # init_db.add_nations()
    # init_db.add_managers()
    # init_db.add_managerial_stints()


# Register blueprints
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(manager, url_prefix="/managers")
