from flask import jsonify
from sqlalchemy.orm import aliased

from api import api_blueprint
from models import Team, Match, Season
from utils import generate_table


@api_blueprint.route("/seasons/<season>", methods=["GET"])
def seasons(season):
    season = season.replace("-", "/")
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
    standings_dict = {}
    for team in standings:
        standings_dict[team[0]] = team[1]
    return jsonify(standings_dict)
