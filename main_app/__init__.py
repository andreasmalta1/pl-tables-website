from flask import Flask
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

from main_app import routes
