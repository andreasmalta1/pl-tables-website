from flask import Blueprint

admin_blueprint = Blueprint("admin", __name__)


from blueprints.admin import routes
