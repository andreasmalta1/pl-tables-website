from flask import render_template, request

from custom_date import custom_date_blueprint
from models import Match, Season
from utils import update_visits


@custom_date_blueprint.route("/", methods=["GET"])
def custom_date():
    # Add page visit to db
    update_visits(request.remote_addr, "seasons")

    return render_template("custom_date/custom_dates.html")
