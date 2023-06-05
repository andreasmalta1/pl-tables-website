from flask import render_template, request, flash, url_for
from os import getenv
from datetime import date, datetime
import requests

from main_app import app
from main_app.utils import generate_table
from main_app.managers import current_managers, memorable_managers
from main_app.teams import TEAMS, NATIONS


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        start_date_check = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_check = datetime.strptime(end_date, "%Y-%m-%d")

        if end_date_check < start_date_check:
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
        current_manager = request.form.get("currentManager")
        if current_manager:
            manager_start = current_managers[current_manager]["date_start"]
            data = {
                "start_date": manager_start,
                "end_date": datetime.strftime(date.today(), "%Y-%m-%d"),
            }

            response = requests.post(url_for("index", _external=True), data=data)
            return response.content

        memorable_manager = request.form.get("memorableManager")
        if memorable_manager:
            manager_start = memorable_managers[memorable_manager]["date_start"]
            manager_end = memorable_managers[memorable_manager]["date_end"]
            if manager_end == "today":
                manager_end = datetime.strftime(date.today(), "%Y-%m-%d")
            data = {"start_date": manager_start, "end_date": manager_end}

            response = requests.post(url_for("index", _external=True), data=data)
            return response.content

    if request.method == "GET":
        for manager in current_managers:
            date_start = current_managers[manager]["date_start"].split("-")
            date_today = date.today()
            d0 = date(int(date_start[0]), int(date_start[1]), int(date_start[2]))
            delta = date_today - d0

            current_managers[manager]["days_in_charge"] = delta.days
            current_managers[manager][
                "manager_url"
            ] = f"{getenv('API_MANAGER_URL')}{current_managers[manager]['fotmob_id']}.png"
            current_managers[manager][
                "nationality_url"
            ] = f"{getenv('API_CREST_URL')}{NATIONS.get(current_managers[manager]['nationality'])}.png"
            current_managers[manager][
                "club_url"
            ] = f"{getenv('API_CREST_URL')}{TEAMS.get(current_managers[manager]['club'])}.png"

        for manager in memorable_managers:
            date_start = memorable_managers[manager]["date_start"].split("-")
            date_end = memorable_managers[manager]["date_end"]
            if date_end == "today":
                date_end = date.today()
                memorable_managers[manager]["date_end"] = datetime.strftime(
                    date.today(), "%Y-%m-%d"
                )
            else:
                date_end = date_end.split("-")
                date_end = date(int(date_end[0]), int(date_end[1]), int(date_end[2]))

            d0 = date(int(date_start[0]), int(date_start[1]), int(date_start[2]))
            delta = date_end - d0

            memorable_managers[manager]["days_in_charge"] = delta.days
            if memorable_managers[manager]["fotmob_id"]:
                memorable_managers[manager][
                    "manager_url"
                ] = f"{getenv('API_MANAGER_URL')}{memorable_managers[manager]['fotmob_id']}.png"
            else:
                memorable_managers[manager][
                    "manager_url"
                ] = f"{getenv('API_EMPTY_URL')}"

            memorable_managers[manager][
                "nationality_url"
            ] = f"{getenv('API_CREST_URL')}{NATIONS.get(memorable_managers[manager]['nationality'])}.png"
            memorable_managers[manager][
                "club_url"
            ] = f"{getenv('API_CREST_URL')}{TEAMS.get(memorable_managers[manager]['club'])}.png"

        return render_template(
            "managers.html",
            current_managers=current_managers,
            memorable_managers=memorable_managers,
        )


# TODO
# Going back multiple seasons is problematic with the API -> Find new API or build own model/API
# Managers with mutiple clubs
# Add ability to save table as image / pdf -> maybe add an embed link
# Add PL logo
# Add tables by season
# CSS
# Landing page -> show current table and all time pl table
# Footer -> Add send email and SupportMe
# How many page viewers
