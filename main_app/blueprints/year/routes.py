from flask import Blueprint, render_template, request
from datetime import datetime

year_blueprint = Blueprint("year", __name__)


@year_blueprint.route("/", methods=["GET"])
def yearly():
    if request.method == "GET":
        current_year = datetime.now().year

        years = [year for year in range(current_year, 1991, -1)]

        return render_template(
            "blueprints/yearly.html",
            years=years,
        )
