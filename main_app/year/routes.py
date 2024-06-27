from flask import render_template, request
from datetime import datetime

from year import year_blueprint
from utils import update_visits


@year_blueprint.route("/", methods=["GET"])
def yearly():
    # Add page visit to db
    update_visits(request.remote_addr, "seasons")

    if request.method == "GET":
        current_year = datetime.now().year

        years = [year for year in range(current_year, 1991, -1)]

        return render_template(
            "year/yearly.html",
            years=years,
        )
