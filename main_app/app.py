import sys
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_session import Session
from dotenv import load_dotenv

from .models import db

if sys.version_info >= (3, 12):
    from .config import Config
elif sys.version_info >= (3, 10):
    from main_app.config import Config
else:
    raise RuntimeError("Unsupported Python version. Please use Python 3.10 or later.")

load_dotenv()

mail = Mail()
s = Session()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    mail.init_app(app)
    s.init_app(app)

    CORS(app, supports_credentials=True)

    db.init_app(app)

    from . import init_db
    from .blueprints.api.routes import api_blueprint as api
    from .blueprints.admin.routes import admin_blueprint as admin
    from .blueprints.auth.routes import auth_blueprint as auth
    from .blueprints.contact_page.routes import contact_page_blueprint as contact_page

    with app.app_context():
        db.create_all()
        init_db.add_teams()
        init_db.add_nations()
        init_db.add_managers()
        init_db.add_managerial_stints()
        init_db.add_matches()
        init_db.add_point_deductions()
        init_db.add_user()
        init_db.add_last_row()

    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return render_template("error_handling/404.html"), 404

    # Register blueprints
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(admin, url_prefix="/api/admin")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(contact_page, url_prefix="/contact")
    # app.register_error_handler(404, page_not_found)

    return app
