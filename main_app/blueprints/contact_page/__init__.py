from flask import Blueprint

contact_page_blueprint = Blueprint("contact_page", __name__)


from blueprints.contact_page import routes
