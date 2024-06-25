from flask import jsonify
from sqlalchemy.orm import aliased
from datetime import date

from app import db
from api import api_blueprint
from models import Team, Match, ManagerStint
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


@api_blueprint.route("/managers/<int:stint_id>", methods=["GET"])
def managers(stint_id):
    manager_stint = ManagerStint.query.filter_by(id=stint_id).first()
    date_start = manager_stint.date_start
    if manager_stint.current:
        date_end = date.today()
    if not manager_stint.current:
        date_end = manager_stint.date_end

    # date_start = date_start.split("-")
    # date_end = date_end.split("-")

    HomeTeam = aliased(Team, name="home_team")
    AwayTeam = aliased(Team, name="away_team")

    # matches = (
    #     Match.query.filter(
    #         db.and_(
    #             Match.date
    #             >= date(
    #                 year=int(date_start[0]),
    #                 month=int(date_start[1]),
    #                 day=int(date_start[2]),
    #             ),
    #             Match.date
    #             <= date(
    #                 year=int(date_end[0]), month=int(date_end[1]), day=int(date_end[2])
    #             ),
    #         )
    #     )
    #     .join(HomeTeam, HomeTeam.id == Match.home_team_id)
    #     .join(AwayTeam, AwayTeam.id == Match.away_team_id)
    #     .add_columns(
    #         HomeTeam.name.label("home_team_name"),
    #         Match.home_score,
    #         AwayTeam.name.label("away_team_name"),
    #         Match.away_score,
    #     )
    #     .all()
    matches = (
        Match.query.filter(db.and_(Match.date >= date_start, Match.date <= date_end))
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

    standings = generate_table(matches, None)
    standings_dict = {}
    for team in standings:
        standings_dict[team[0]] = team[1]
    return jsonify(standings_dict)
