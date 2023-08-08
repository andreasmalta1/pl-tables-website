from flask import Blueprint, render_template, request, flash
from os import getenv

from main_app import db
from main_app.models import Match, CurrentTeams
from main_app.utils import get_teams_info

CREST_URL = getenv("CREST_URL")
MANAGER_FACE_URL = getenv("MANAGER_FACE_URL")
EMPTY_FACE_URL = getenv("EMPTY_FACE_URL")
POST_KEY = getenv("POST_KEY")

TEAMS = get_teams_info()

matches = Blueprint("matches", __name__)


@matches.route(f"/matches/{POST_KEY}", methods=["GET", "POST"])
def new_match_results():
    # Enter multiple matches at once
    # Check that date exists and team ids is not the same
    # CSS

    current_teams = CurrentTeams.query.all()

    if request.method == "GET":
        return render_template("post_match_results.html", current_teams=current_teams)

    if request.method == "POST":
        match_date = request.form["match-day"]
        home_team_id = request.form["home-team"]
        home_team_name = (
            CurrentTeams.query.filter_by(team_id=home_team_id).first().team_name
        )
        home_score = request.form["home-team-score"]

        away_team_id = request.form["away-team"]
        away_team_name = (
            CurrentTeams.query.filter_by(team_id=away_team_id).first().team_name
        )
        away_score = request.form["away-team-score"]

        if home_team_id == away_team_id:
            flash("Teams cannot be the same", category="error")
            return render_template(
                "post_match_results.html", current_teams=current_teams
            )

        season = CurrentTeams.query.first().season
        new_match = Match(
            season=season,
            home_team_id=home_team_id,
            home_team_name=home_team_name,
            away_team_id=away_team_id,
            away_team_name=away_team_name,
            home_score=home_score,
            away_score=away_score,
            date=match_date,
        )
        db.session.add(new_match)
        db.session.commit()
        return render_template("post_match_results.html", current_teams=current_teams)
