from flask import render_template, request
from flask_login import current_user

from blueprints.custom_date import custom_date_blueprint
from utils import update_visits


@custom_date_blueprint.route("/", methods=["GET"])
def custom_date():
    admin = False
    if current_user.is_authenticated:
        admin = True

    update_visits(request.remote_addr, "custom_dates", admin)

    return render_template("custom_date/custom_dates.html")
