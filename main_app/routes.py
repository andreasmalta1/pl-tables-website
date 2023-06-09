from flask import render_template, request, flash, url_for, jsonify
from flask_mail import Mail, Message
from os import getenv
from datetime import date, datetime
import requests
import csv

from main_app import app, db
from main_app.models import Match
from main_app.forms import ContactForm
from main_app.utils import generate_table, get_pl_matches, get_teams_info
from main_app.managers import managers_dict
from main_app.teams import NATIONS

CREST_URL = getenv("CREST_URL")
MANAGER_FACE_URL = getenv("MANAGER_FACE_URL")
EMPTY_FACE_URL = getenv("EMPTY_FACE_URL")
POST_KEY = getenv("POST_KEY")

TEAMS = get_teams_info()


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
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


@app.route("/custom", methods=["GET", "POST"])
def custom_dates():
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


@app.route("/managers", methods=["GET", "POST"])
def managers():
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

        response = requests.post(url_for("custom_dates", _external=True), data=data)
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


@app.route("/seasons", methods=["GET", "POST"])
def seasons():
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


@app.route(f"/matches", methods=["GET", "POST"])
def matches():
    authorization_key = request.headers.get("authorization-key")
    if authorization_key != getenv("POST_KEY"):
        return jsonify({"msg": "No authorization key found"})

    if request.method == "POST":
        get_pl_matches()

        with open("csvs/pl_results.csv", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # Convert each row into a dictionary and add it to data
            for row in csv_reader:
                match_date = row["date"].split("/")
                match_date = date(
                    int(match_date[2]), int(match_date[1]), int(match_date[0])
                )
                new_match = Match(
                    season=row["season"],
                    home_team_id=row["home_team_id"],
                    home_team_name=row["home_team_name"],
                    away_team_id=row["away_team_id"],
                    away_team_name=row["away_team_name"],
                    home_score=row["home_score"],
                    away_score=row["away_score"],
                    date=match_date,
                )
                db.session.add(new_match)

        db.session.commit()
        return jsonify({"msg": "Matches added successfully"})

    if request.method == "GET":
        data = {}

        date_from = request.args.get("dateFrom")
        date_to = request.args.get("dateTo")
        season = request.args.get("season")

        if date_from and date_to:
            date_from = date_from.split("-")
            date_to = date_to.split("-")

            matches = Match.query.filter(
                db.and_(
                    Match.date
                    >= date(
                        year=int(date_from[0]),
                        month=int(date_from[1]),
                        day=int(date_from[2]),
                    ),
                    Match.date
                    <= date(
                        year=int(date_to[0]), month=int(date_to[1]), day=int(date_to[2])
                    ),
                )
            ).all()

        if season:
            matches = Match.query.filter_by(season=season).all()

        if not date_from and not date_to and not season:
            matches = Match.query.all()

        if not matches:
            return jsonify({"msg": "No Matches Found"})

        for match in matches:
            data[match.id] = {
                "season": match.season,
                "home_team": {
                    "team_id": match.home_team_id,
                    "team_name": match.home_team_name,
                    "score": match.home_score,
                },
                "away_team": {
                    "team_id": match.away_team_id,
                    "team_name": match.away_team_name,
                    "score": match.away_score,
                },
                "date": match.date,
            }

        return jsonify(data)


@app.route("/contact", methods=["GET", "POST"])
def contact_us():
    form = ContactForm()
    if request.method == "POST":
        if form.validate() == False:
            flash("Enter a valid email address", category="error")
            return render_template("contact.html", form=form)

        mail = Mail()
        mail.init_app(app)
        msg = Message(
            form.subject.data,
            sender=form.email.data,
            recipients=[getenv("MAIL_USERNAME")],
        )
        msg.body = "From: %s <%s> \n%s" % (
            form.name.data,
            form.email.data,
            form.message.data,
        )
        mail.send(msg)
        return render_template("contact.html")

    if request.method == "GET":
        return render_template("contact.html", form=form)


# TODO
# Errors css & closing button (different for custom and email)
# In downloaded images add credits and site url
# Views blueprints
# Serialiser (see image)

# Add check to never add already posted matches and never double scrape data (Better to test during the season)
# Use postgres database instead of sqlite
# How many page viewers
# Check about post key viewable in network

# Create readme
# Document code

# Deploy
