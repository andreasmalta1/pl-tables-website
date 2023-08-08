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

matches = Blueprint("matches", __name__)


@matches.route(f"/matches/{POST_KEY}", methods=["GET", "POST"])
def new_match_results():
    # Create a view, accessible only using the auth key
    # Select date, team, team score (home and away) - get season and teams from current teams model
    # Ablilty to post match score or enter a new match
    # First make sure functionality to get post one match is done.
    # Then work to enter multiple matches at once
    # Then CSS

    if request.method == "GET":
        current_teams = CurrentTeams.query.all()
        return render_template("post_match_results.html", current_teams=current_teams)

    if request.method == "GET":
        # Get data from form
        # Get season as already done
        # Post to DB
        current_teams = CurrentTeams.query.all()
        return render_template("post_match_results.html", current_teams=current_teams)

    # # Get all unique seasons present in db
    # season = CurrentTeams.query.first().season

    # current_table = generate_table(None, None, season)
    # all_time_table = generate_table(None, None, None)

    # return render_template(
    #     "index.html", current_table=current_table, all_time_table=all_time_table
    # )
