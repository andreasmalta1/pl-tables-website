from flask import Blueprint

home_blueprint = Blueprint("main", __name__)


from main import routes
