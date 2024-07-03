from flask import Blueprint

admin_blueprint = Blueprint("admin", __name__)


from admin import routes
