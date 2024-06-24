from flask import render_template, request
from sqlalchemy.orm import aliased

from all_time import all_time_blueprint
from models import Team, Match, Season
from utils import generate_table, update_visits


@all_time_blueprint.route("/", methods=["GET"])
def index():
    update_visits(request.remote_addr, "home")

    HomeTeam = aliased(Team, name="home_team")
    AwayTeam = aliased(Team, name="away_team")

    matches = (
        Match.query.join(HomeTeam, HomeTeam.id == Match.home_team_id)
        .join(AwayTeam, AwayTeam.id == Match.away_team_id)
        .add_columns(
            HomeTeam.name.label("home_team_name"),
            Match.home_score,
            AwayTeam.name.label("away_team_name"),
            Match.away_score,
        )
        .all()
    )

    standings = generate_table(matches, None)

    return render_template("main/index.html", standings=standings)
