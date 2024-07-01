from flask import Blueprint

updates_blueprint = Blueprint("updates", __name__)


from updates import routes
