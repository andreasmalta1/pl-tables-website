from flask import render_template, request, flash
from os import getenv
from datetime import date

from main_app import app
from main_app.utils import generate_table
from main_app.managers import current_managers
from main_app.teams import TEAMS, NATIONS


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        if end_date < start_date:
            flash("End date must be after start date", category="error")
            return render_template("index.html")

        standings_table = generate_table(start_date, end_date)

        return render_template(
            "index.html",
            standings_table=standings_table,
            start_date=start_date,
            end_date=end_date,
        )

    return render_template("index.html")


@app.route("/mangers", methods=["GET", "POST"])
def managers():
    if request.method == "POST":
        manager = request.form.get("manager")

    for manager in current_managers:
        date_start = current_managers[manager]["date_start"].split("-")
        date_today = date.today()
        d0 = date(int(date_start[2]), int(date_start[1]), int(date_start[0]))
        delta = date_today - d0

        current_managers[manager]["days_in_charge"] = delta.days
        current_managers[manager][
            "nationality_url"
        ] = f"{getenv('API_CREST_URL')}{NATIONS.get(current_managers[manager]['nationality'])}.png"
        current_managers[manager][
            "club_url"
        ] = f"{getenv('API_CREST_URL')}{TEAMS.get(current_managers[manager]['club'])}.png"

    return render_template("managers.html", current_managers=current_managers)


# TODO
# How many page viewers
# CSS
# Add buttons -> since guardiola manager etc, Fergie's time in charge ...
# Add tables by season
# Footer -> Add send email and SupportMe
# Landing page

# Add managers face
