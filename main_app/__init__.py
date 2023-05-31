from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

from main_app import routes
