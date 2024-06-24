from flask import Blueprint

all_time_blueprint = Blueprint("all_time", __name__)


from all_time import routes
