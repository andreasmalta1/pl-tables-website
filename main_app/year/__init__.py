from flask import Blueprint

year_blueprint = Blueprint("year", __name__)


from year import routes
