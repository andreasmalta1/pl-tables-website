from flask import Blueprint

custom_date_blueprint = Blueprint("custom_date", __name__)


from blueprints.custom_date import routes
