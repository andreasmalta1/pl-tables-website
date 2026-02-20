from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.orm import aliased
from datetime import date
import os
import json
import hashlib

from ...models import *
from ...utils import generate_table

api_blueprint = Blueprint("api", __name__)

STATS_FILE = os.path.join("utils", "pl-yt-stats.json")


@api_blueprint.route("/current-season", methods=["GET"])
def index():
    season = Season.query.first().season
    standings = get_matches_by_season(season)
    return jsonify(standings)


@api_blueprint.route("/all-time", methods=["GET"])
def get_all_time():
    standings = get_matches_by_season(season=None)
    return jsonify(standings)


@api_blueprint.route("/seasons-list", methods=["GET"])
def get_seasons():
    seasons_query = Match.query.with_entities(Match.season).distinct().all()
    seasons = [season.season for season in seasons_query]
    seasons.sort(reverse=True)
    return jsonify(seasons)


@api_blueprint.route("/seasons/<season>", methods=["GET"])
def seasons(season):
    season = season.replace("-", "/")
    standings = get_matches_by_season(season)
    return jsonify(standings)


@api_blueprint.route("/manager-list/<manager_type>", methods=["GET"])
def get_manager_list(manager_type):
    if manager_type == "current":
        managerial_stints = (
            ManagerStint.query.join(Team, ManagerStint.team_id == Team.id)
            .join(Manager, ManagerStint.manager_id == Manager.id)
            .join(Nation, Manager.nation_id == Nation.id)
            .filter(ManagerStint.current == True, Team.current == True)
            .with_entities(
                Team.crest_url.label("crest_url"),
                Manager.name.label("manager_name"),
                Manager.face_url.label("face_url"),
                Nation.flag_url.label("flag_url"),
                ManagerStint.id,
                ManagerStint.date_start,
                ManagerStint.current,
            )
            .all()
        )

    if manager_type == "past":
        managerial_stints = (
            ManagerStint.query.filter_by(current=False)
            .join(Team, ManagerStint.team_id == Team.id)
            .join(Manager, ManagerStint.manager_id == Manager.id)
            .join(Nation, Manager.nation_id == Nation.id)
            .with_entities(
                Team.crest_url.label("crest_url"),
                Manager.name.label("manager_name"),
                Manager.face_url.label("face_url"),
                Nation.flag_url.label("flag_url"),
                ManagerStint.id,
                ManagerStint.date_start,
                ManagerStint.date_end,
                ManagerStint.current,
            )
            .all()
        )

    stints = [row._asdict() for row in managerial_stints]
    return jsonify(stints)


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


@api_blueprint.route("/dates", methods=["GET"])
def dates():
    date_start = request.args.get("start")
    date_end = request.args.get("end")

    standings = get_matches_by_day(date_start, date_end)
    return jsonify(standings)


@api_blueprint.route("/years/<int:year>", methods=["GET"])
def calendar_year(year):
    date_start = date(year, 1, 1)
    date_end = date(year, 12, 31)
    standings = get_matches_by_day(date_start, date_end)
    return jsonify(standings)


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


@api_blueprint.route("/yt-stats", methods=["GET"])
def get_stats():
    with open(STATS_FILE, "r") as f:
        data = json.load(f)

    return jsonify(data)


@api_blueprint.route("/track-visit", methods=["POST"])
def track_visit():
    data = request.json

    # Hash the IP so you aren't storing PII (Personal Identifiable Information)
    ip_addr = request.remote_addr
    ip_hash = hashlib.sha256(ip_addr.encode()).hexdigest()

    new_visit = Visit(ip_hash=ip_hash, page_path=data.get("path"))
    db.session.add(new_visit)
    db.session.commit()
    return jsonify({"status": "success"}), 201


@api_blueprint.route("/visitor-stats", methods=["GET"])
def get_visitor_stats():
    total_views = Visit.query.count()
    unique_visitors = db.session.query(Visit.ip_hash).distinct().count()

    # Get views per day for the last 7 days
    results = (
        db.session.query(
            func.date(Visit.timestamp).label("date"),
            func.count(Visit.id).label("views"),
        )
        .group_by(func.date(Visit.timestamp))
        .order_by(func.date(Visit.timestamp))
        .all()
    )

    time_series = [{"date": str(r.date), "views": r.views} for r in results]

    return jsonify(
        {
            "total_views": total_views,
            "unique_visitors": unique_visitors,
            "time_series": time_series,
        }
    )


def get_matches_by_season(season=None):
    HomeTeam = aliased(Team, name="home_team")
    AwayTeam = aliased(Team, name="away_team")

    if season:
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

    if not season:
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

    standings = generate_table(matches, season)
    standings_list = []
    for name, stats in standings:
        item = {"name": name, **stats}
        standings_list.append(item)

    return standings_list


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
    standings_list = []
    for name, stats in standings:
        item = {"name": name, **stats}
        standings_list.append(item)

    return standings_list
