from flask import Blueprint

manager_blueprint = Blueprint("manager", __name__)


from manager import routes
