from flask import Blueprint, render_template, request
from flask_login import current_user
from datetime import datetime

from ...utils import update_visits

year_blueprint = Blueprint("year", __name__)


@year_blueprint.route("/", methods=["GET"])
def yearly():
    admin = False
    if current_user.is_authenticated:
        admin = True

    update_visits(request.remote_addr, "season", admin)

    if request.method == "GET":
        current_year = datetime.now().year

        years = [year for year in range(current_year, 1991, -1)]

        return render_template(
            "blueprints/yearly.html",
            years=years,
        )
