from flask import jsonify
from sqlalchemy.orm import aliased
from datetime import date

from app import db
from api import api_blueprint
from models import *
from utils import generate_table


@api_blueprint.route("/current-season", methods=["GET"])
def index():
    season = Season.query.first().season
    standings_dict = get_matches_by_season(season)
    return jsonify(standings_dict)


@api_blueprint.route("/seasons/<season>", methods=["GET"])
def seasons(season):
    season = season.replace("-", "/")
    standings_dict = get_matches_by_season(season)
    return jsonify(standings_dict)


@api_blueprint.route("/stints/<int:stint_id>", methods=["GET"])
def stints(stint_id):
    manager_stint = ManagerStint.query.filter_by(id=stint_id).first()
    date_start = manager_stint.date_start
    if manager_stint.current:
        date_end = date.today()
    if not manager_stint.current:
        date_end = manager_stint.date_end

    standings_dict = get_matches_by_day(date_start, date_end)
    return jsonify(standings_dict)


@api_blueprint.route("/managers/<int:stint_id>", methods=["GET"])
def managers(stint_id):
    ManagerTable = aliased(Manager, name="manager_table")
    NationTable = aliased(Nation, name="nation_table")
    TeamTable = aliased(Team, name="team_table")

    manager_query = (
        ManagerStint.query.filter_by(id=stint_id)
        .join(ManagerTable, ManagerTable.id == ManagerStint.manager_id)
        .join(NationTable, NationTable.id == ManagerTable.nation_id)
        .join(TeamTable, TeamTable.id == ManagerStint.team_id)
        .add_columns(
            ManagerStint.date_start,
            ManagerStint.date_end,
            ManagerTable.name.label("manager_name"),
            ManagerTable.face_url.label("manager_face_url"),
            NationTable.name.label("nation_name"),
            NationTable.flag_url.label("nation_flag_url"),
            TeamTable.name.label("team_name"),
            TeamTable.crest_url.label("team_crest_url"),
        )
        .first()
    )

    manager_info = {
        "name": manager_query.manager_name,
        "face_url": manager_query.manager_face_url,
        "date_start": manager_query.date_start.strftime("%Y-%m-%d"),
        "date_end": (
            None
            if not manager_query.date_end
            else manager_query.date_end.strftime("%Y-%m-%d")
        ),
        "team_name": manager_query.team_name,
        "team_crest_url": manager_query.team_crest_url,
        "nation_name": manager_query.nation_name,
        "nation_flag_url": manager_query.nation_flag_url,
    }

    return jsonify(manager_info)


@api_blueprint.route("/dates/<date_start>/<date_end>", methods=["GET"])
def dates(date_start, date_end):
    standings_dict = get_matches_by_day(date_start, date_end)
    return jsonify(standings_dict)


@api_blueprint.route("/years/<int:year>", methods=["GET"])
def calendar_year(year):
    date_start = date(year, 1, 1)
    date_end = date(year, 12, 31)
    standings_dict = get_matches_by_day(date_start, date_end)
    return jsonify(standings_dict)


@api_blueprint.route("/deductions/<season>", methods=["GET"])
def point_deductions(season):
    if season == "current":
        season = Season.query.first().season

    season = season.replace("-", "/")
    TeamTable = aliased(Team, name="team_table")
    points_deductions = (
        PointDeduction.query.filter_by(season=season)
        .join(TeamTable, TeamTable.id == PointDeduction.team_id)
        .add_columns(
            PointDeduction.id,
            PointDeduction.points_deducted,
            PointDeduction.reason,
            PointDeduction.season,
            TeamTable.name.label("team_name"),
        )
        .all()
    )

    if len(points_deductions) == 0:
        return jsonify({})

    deductions_dict = {}
    for deduction in points_deductions:
        deductions_dict[deduction.id] = {
            "team_name": deduction.team_name,
            "reason": deduction.reason,
            "points_deducted": deduction.points_deducted,
        }
    return jsonify(deductions_dict)


def get_matches_by_season(season):
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

    return standings_dict


def get_matches_by_day(date_start, date_end):
    HomeTeam = aliased(Team, name="home_team")
    AwayTeam = aliased(Team, name="away_team")

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

    return standings_dict
