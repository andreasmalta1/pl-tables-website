from flask import render_template, request
from sqlalchemy.orm import aliased

from home import home_blueprint
from models import Team, Match, Season
from utils import generate_table, update_visits


@home_blueprint.route("/", methods=["GET"])
def index():
    update_visits(request.remote_addr, "home")
    season = Season.query.first().season

    HomeTeam = aliased(Team, name="home_team")
    AwayTeam = aliased(Team, name="away_team")

    matches = (
        Match.query.filter_by(season=season)
        .join(HomeTeam, HomeTeam.id == Match.home_team_id)
        .join(AwayTeam, AwayTeam.id == Match.away_team_id)
        .add_columns(
            HomeTeam.name.label("home_team_name"),
            Match.home_score,
            AwayTeam.name.label("away_team_name"),
            Match.away_score,
        )
        .all()
    )

    standings = generate_table(matches, season)

    return render_template("main/index.html", standings=standings)
