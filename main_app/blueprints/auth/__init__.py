from flask import Blueprint

auth_blueprint = Blueprint("auth", __name__)


from blueprints.auth import routes
