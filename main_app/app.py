import sys
from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
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


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    mail.init_app(app)

    db.init_app(app)

    from .models import User
    from . import init_db

    from .blueprints.api.routes import api_blueprint as api
    from .blueprints.home.routes import home_blueprint as home
    from .blueprints.all_time.routes import all_time_blueprint as all_time
    from .blueprints.manager.routes import manager_blueprint as manager
    from .blueprints.season.routes import season_blueprint as season
    from .blueprints.year.routes import year_blueprint as year
    from .blueprints.custom_date.routes import custom_date_blueprint as custom_date
    from .blueprints.auth.routes import auth_blueprint as auth_blueprint
    from .blueprints.admin.routes import admin_blueprint as admin
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

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error_handling/404.html"), 404

    # Register blueprints
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(home)
    app.register_blueprint(all_time, url_prefix="/league")
    app.register_blueprint(manager, url_prefix="/managers")
    app.register_blueprint(season, url_prefix="/seasons")
    app.register_blueprint(year, url_prefix="/year")
    app.register_blueprint(custom_date, url_prefix="/custom-date")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(contact_page, url_prefix="/contact")
    app.register_error_handler(404, page_not_found)

    return app
