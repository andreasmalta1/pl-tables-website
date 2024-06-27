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
from home import home_blueprint as home
from all_time import all_time_blueprint as all_time
from manager import manager_blueprint as manager
from season import season_blueprint as season
from custom_date import custom_date_blueprint as custom_date
from contact_page import contact_page_blueprint as contact_page

with app.app_context():
    db.create_all()
    init_db.add_teams()
    init_db.add_nations()
    init_db.add_managers()
    init_db.add_managerial_stints()
    init_db.add_matches()


# Register blueprints
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(home)
app.register_blueprint(all_time, url_prefix="/league")
app.register_blueprint(manager, url_prefix="/managers")
app.register_blueprint(season, url_prefix="/seasons")
app.register_blueprint(custom_date, url_prefix="/custom-date")
app.register_blueprint(contact_page, url_prefix="/contact")
