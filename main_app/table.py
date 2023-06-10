from flask import Blueprint, render_template, request, flash, url_for
from os import getenv
from datetime import date, datetime
import requests

from main_app.models import Match
from main_app.utils import generate_table, get_teams_info, update_visits
from main_app.managers import managers_dict
from main_app.teams import NATIONS

CREST_URL = getenv("CREST_URL")
MANAGER_FACE_URL = getenv("MANAGER_FACE_URL")
EMPTY_FACE_URL = getenv("EMPTY_FACE_URL")
POST_KEY = getenv("POST_KEY")

TEAMS = get_teams_info()

table = Blueprint("table", __name__)


@table.route("/", methods=["GET"])
@table.route("/home", methods=["GET"])
def home():
    update_visits(request.remote_addr, "home")
    seasons = []
    years = Match.query.with_entities(Match.season).distinct().all()
    for year in years:
        seasons.append(year.season)

    seasons.sort(reverse=True)
    season = seasons[0]
    current_table = generate_table(None, None, season)
    all_time_table = generate_table(None, None, None)

    return render_template(
        "index.html", current_table=current_table, all_time_table=all_time_table
    )


@table.route("/custom", methods=["GET", "POST"])
def custom_dates():
    update_visits(request.remote_addr, "custom")
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        start_date_check = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_check = datetime.strptime(end_date, "%Y-%m-%d")

        if end_date_check < start_date_check:
            flash("End date must be after start date", category="error")
            return render_template("custom_dates.html")

        standings_table = generate_table(start_date, end_date, None)

        return render_template(
            "custom_dates.html",
            standings_table=standings_table,
            start_date=start_date,
            end_date=end_date,
        )

    return render_template("custom_dates.html")


@table.route("/managers", methods=["GET", "POST"])
def managers():
    update_visits(request.remote_addr, "managers")
    if request.method == "POST":
        manager_ids = len(managers_dict)
        for manager_id in range(1, manager_ids + 1):
            manager = request.form.get(str(manager_id))
            if manager:
                break

        if managers_dict[manager_id]["status"] == "current":
            manager_start = managers_dict[manager_id]["date_start"]
            data = {
                "start_date": manager_start,
                "end_date": datetime.strftime(date.today(), "%Y-%m-%d"),
            }

        if managers_dict[manager_id]["status"] == "memorable":
            manager_start = managers_dict[manager_id]["date_start"]
            manager_end = managers_dict[manager_id]["date_end"]
            if manager_end == "today":
                manager_end = datetime.strftime(date.today(), "%Y-%m-%d")
            data = {"start_date": manager_start, "end_date": manager_end}

        response = requests.post(
            url_for("table.custom_dates", _external=True), data=data
        )
        return response.content

    if request.method == "GET":
        current_managers, memorable_managers = {}, {}

        for manager_id in managers_dict:
            if managers_dict[manager_id]["status"] == "current":
                current_managers[manager_id] = managers_dict[manager_id]

                date_start = current_managers[manager_id]["date_start"].split("-")
                date_today = date.today()
                d0 = date(int(date_start[0]), int(date_start[1]), int(date_start[2]))
                delta = date_today - d0

                current_managers[manager_id]["days_in_charge"] = delta.days
                current_managers[manager_id][
                    "manager_url"
                ] = f"{MANAGER_FACE_URL}{current_managers[manager_id]['fotmob_id']}.png"
                current_managers[manager_id][
                    "nationality_url"
                ] = f"{CREST_URL}{NATIONS.get(current_managers[manager_id]['nationality'])}.png"
                current_managers[manager_id][
                    "club_url"
                ] = f"{CREST_URL}{TEAMS.get(current_managers[manager_id]['club'])['logo_id']}.png"

            if managers_dict[manager_id]["status"] == "memorable":
                memorable_managers[manager_id] = managers_dict[manager_id]
                date_start = memorable_managers[manager_id]["date_start"].split("-")
                date_end = memorable_managers[manager_id]["date_end"]
                if date_end == "today":
                    date_end = date.today()
                    memorable_managers[manager_id]["date_end"] = datetime.strftime(
                        date.today(), "%Y-%m-%d"
                    )
                else:
                    date_end = date_end.split("-")
                    date_end = date(
                        int(date_end[0]), int(date_end[1]), int(date_end[2])
                    )

                d0 = date(int(date_start[0]), int(date_start[1]), int(date_start[2]))
                delta = date_end - d0

                memorable_managers[manager_id]["days_in_charge"] = delta.days
                if memorable_managers[manager_id]["fotmob_id"]:
                    memorable_managers[manager_id][
                        "manager_url"
                    ] = f"{MANAGER_FACE_URL}{memorable_managers[manager_id]['fotmob_id']}.png"
                else:
                    memorable_managers[manager_id]["manager_url"] = f"{EMPTY_FACE_URL}"

                memorable_managers[manager_id][
                    "nationality_url"
                ] = f"{CREST_URL}{NATIONS.get(memorable_managers[manager_id]['nationality'])}.png"
                memorable_managers[manager_id][
                    "club_url"
                ] = f"{CREST_URL}{TEAMS.get(memorable_managers[manager_id]['club'])['logo_id']}.png"

        sorted_current_managers = sorted(
            current_managers.items(),
            key=lambda x: x[1]["days_in_charge"],
            reverse=True,
        )
        sorted_current_managers = dict(sorted_current_managers)

        sorted_memorable_managers = sorted(
            memorable_managers.items(),
            key=lambda x: x[1]["days_in_charge"],
            reverse=True,
        )
        sorted_memorable_managers = dict(sorted_memorable_managers)

        return render_template(
            "managers.html",
            current_managers=sorted_current_managers,
            memorable_managers=sorted_memorable_managers,
        )


@table.route("/seasons", methods=["GET", "POST"])
def seasons():
    update_visits(request.remote_addr, "seasons")
    seasons = []
    years = Match.query.with_entities(Match.season).distinct().all()
    for year in years:
        seasons.append(year.season)

    seasons.sort(reverse=True)

    if request.method == "POST":
        season = request.form.get("season")
        standings_table = generate_table(None, None, season)

        return render_template(
            "seasons.html", seasons=seasons, standings_table=standings_table
        )

    if request.method == "GET":
        return render_template("seasons.html", seasons=seasons)
