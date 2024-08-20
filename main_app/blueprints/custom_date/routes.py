from flask import Blueprint, render_template, request
from flask_login import current_user

from ...utils import update_visits

custom_date_blueprint = Blueprint("custom_date", __name__)


@custom_date_blueprint.route("/", methods=["GET"])
def custom_date():
    admin = False
    if current_user.is_authenticated:
        admin = True

    update_visits(request.remote_addr, "custom_dates", admin)

    return render_template("blueprints/custom_dates.html")
