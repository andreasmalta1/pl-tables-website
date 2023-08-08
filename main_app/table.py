from flask import Blueprint, render_template, request, flash, url_for
from os import getenv
from datetime import date, datetime
import requests

from main_app.models import Match, CurrentTeams
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
    """
    Home Route
    The GET method retrieves and displays the current season's table and the all time PL table.
    """

    # Add page visit to db
    update_visits(request.remote_addr, "home")

    # Get all unique seasons present in db
    season = CurrentTeams.query.first().season

    current_table = generate_table(None, None, season)
    all_time_table = generate_table(None, None, None)

    return render_template(
        "index.html", current_table=current_table, all_time_table=all_time_table
    )


@table.route("/custom", methods=["GET", "POST"])
def custom_dates():
    """
    Custom dates route.
    The POST method gets two dates and displays the PL table in between those dates
    """

    # Add page visit to db
    update_visits(request.remote_addr, "custom")

    if request.method == "POST":
        # Get the dates from the request
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        # Format dates to match db entries
        start_date_check = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_check = datetime.strptime(end_date, "%Y-%m-%d")

        # Ensure end date is after start date
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
    """
    Managers route
    The GET method displays are hardcoded list of mangers and ther times in charge
    The POST method reroutes to the custom page and shows the table for the time in charge for the chosen manager
    """

    # Add page visit to db
    update_visits(request.remote_addr, "managers")

    if request.method == "POST":
        # Get the chosen manager from the mangers dict
        manager_ids = len(managers_dict)
        for manager_id in range(1, manager_ids + 1):
            manager = request.form.get(str(manager_id))
            if manager:
                break

        # Get the managers dates in charge
        if managers_dict[manager_id]["status"] == "current":
            manager_start = managers_dict[manager_id]["date_start"]
            manager_end = datetime.strftime(date.today(), "%Y-%m-%d")

        if managers_dict[manager_id]["status"] == "memorable":
            manager_start = managers_dict[manager_id]["date_start"]
            manager_end = managers_dict[manager_id]["date_end"]
            if manager_end == "today":
                manager_end = datetime.strftime(date.today(), "%Y-%m-%d")

        standings_table = generate_table(manager_start, manager_end, None)

        return render_template(
            "custom_dates.html",
            standings_table=standings_table,
            start_date=manager_start,
            end_date=manager_end,
        )

    if request.method == "GET":
        # Split the mangagers dict in 2 dictionaries
        current_managers, memorable_managers = {}, {}

        # Get today's date
        date_today = date.today()

        for manager_id in managers_dict:
            if managers_dict[manager_id]["status"] == "current":
                current_managers[manager_id] = managers_dict[manager_id]
                # Get the managers start date and calculate number of day's in charge
                date_start = current_managers[manager_id]["date_start"].split("-")
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
                # Get manager's start date
                date_start = memorable_managers[manager_id]["date_start"].split("-")
                date_end = memorable_managers[manager_id]["date_end"]
                # Get managers end day even if manager is still active
                if date_end == "today":
                    date_end = date_today
                    memorable_managers[manager_id]["date_end"] = datetime.strftime(
                        date_today, "%Y-%m-%d"
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

        # Sort managers by days in charge
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
    """
    Seasons route
    The GET method displays all the seasons from 1992.
    THE POST method shows the table for the chosen seasons
    """

    # Add page visit to db
    update_visits(request.remote_addr, "seasons")

    # Get all unique seasons present in db
    seasons = []
    years = Match.query.with_entities(Match.season).distinct().all()
    for year in years:
        seasons.append(year.season)

    # Sort them from most recent down
    seasons.sort(reverse=True)

    if request.method == "POST":
        season = request.form.get("season")
        standings_table = generate_table(None, None, season)

        return render_template(
            "seasons.html", seasons=seasons, standings_table=standings_table
        )

    if request.method == "GET":
        return render_template("seasons.html", seasons=seasons)
