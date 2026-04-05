from flask import Blueprint, render_template, request, jsonify
from sqlalchemy.orm import aliased
from datetime import datetime

from ...models import *
from ..auth.utils import login_required

admin_blueprint = Blueprint("admin", __name__)


@admin_blueprint.route("/new-team", methods=["POST"])
@login_required
def new_team():
    if request.method == "POST":
        team_name = request.json.get("teamName")
        shortcode = request.json.get("shortcode")
        crest_url = request.json.get("crestUrl")

        if not team_name or not shortcode or not crest_url:
            return jsonify({"msg": "Missing data"}), 409

        shortcode = shortcode.upper().strip()

        team_check = Team.query.filter_by(shortcode=shortcode).first()
        if team_check:
            return jsonify({"msg": "Shortcode already exists"}), 409

        new_team = Team(
            name=team_name.strip(),
            shortcode=shortcode,
            crest_url=crest_url.strip(),
            current=False,
        )

        db.session.add(new_team)
        db.session.commit()

        return jsonify({"status": "success"}), 201


@admin_blueprint.route("/new-nation", methods=["POST"])
@login_required
def new_nation():
    if request.method == "POST":
        nation_name = request.json.get("nationName")
        shortcode = request.json.get("shortcode")
        flag_url = request.json.get("flagUrl")

        if not nation_name or not shortcode or not flag_url:
            return jsonify({"msg": "Missing data"}), 409

        shortcode = shortcode.upper().strip()

        nation_check = Nation.query.filter_by(shortcode=shortcode).first()
        if nation_check:
            return jsonify({"msg": "Shortcode already exists"}), 409

        new_nation = Nation(
            name=nation_name.strip(),
            shortcode=shortcode,
            flag_url=flag_url.strip(),
        )

        db.session.add(new_nation)
        db.session.commit()

        return jsonify({"status": "success"}), 201


@admin_blueprint.route("/new-manager", methods=["POST"])
@login_required
def new_manager():
    if request.method == "POST":
        manager_name = request.json.get("managerName")
        face_url = request.json.get("faceUrl")
        nation_id = request.json.get("nationId")

        if not manager_name or not face_url or not nation_id:
            return jsonify({"msg": "Missing data"}), 409

        nation_id = nation_id.strip()

        nation_check = Nation.query.filter_by(id=nation_id).first()
        if not nation_check:
            return jsonify({"msg": "Nation does not exist"}), 409

        new_manager = Manager(
            name=manager_name.strip(),
            face_url=face_url.strip(),
            nation_id=nation_id,
        )

        db.session.add(new_manager)
        db.session.commit()

        return jsonify({"status": "success"}), 201


@admin_blueprint.route("/new-stint", methods=["POST"])
@login_required
def new_stint():
    if request.method == "POST":
        manager_id = request.json.get("managerId")
        team_id = request.json.get("teamId")
        date_start = request.json.get("dateStart")

        if not manager_id or not team_id or not date_start:
            return jsonify({"msg": "Missing data"}), 409

        team_id = team_id.strip()
        manager_id = manager_id.strip()

        team_check = Team.query.filter_by(id=team_id).first()
        manager_check = Manager.query.filter_by(id=manager_id).first()

        if not team_check:
            return jsonify({"msg": "Chosen team does not exist"}), 409

        if not manager_check:
            return jsonify({"msg": "Chosen manager does not exist"}), 409

        new_stint = ManagerStint(
            manager_id=manager_id,
            team_id=team_id,
            date_start=date_start,
            date_end=None,
            current=True,
        )

        db.session.add(new_stint)
        db.session.commit()

        return jsonify({"status": "success"}), 201


@admin_blueprint.route("/end-stint", methods=["POST"])
@login_required
def end_stint():
    if request.method == "POST":
        stint_id = request.json.get("stintId")
        date_end = request.json.get("dateEnd")

        if not stint_id or not date_end:
            return jsonify({"msg": "Missing data"}), 409

        ended_stint = ManagerStint.query.filter_by(id=stint_id).first()
        if not ended_stint:
            return jsonify({"msg": "Chosen stint does not exist"}), 409

        if datetime.strptime(date_end, "%Y-%m-%d").date() < ended_stint.date_start:
            return jsonify({"msg": "End date must be after start date"}), 409

        ended_stint.date_end = date_end
        ended_stint.current = False

        db.session.commit()

        return jsonify({"status": "success"}), 201


@admin_blueprint.route("/new-point-deduction", methods=["POST"])
@login_required
def new_point_deduction():
    if request.method == "POST":
        team_id = request.json.get("teamId")
        points_deducted = request.json.get("pointsDeducted")
        reason = request.json.get("reason")
        season = request.json.get("season")

        if not team_id or not points_deducted or not reason or not season:
            return jsonify({"msg": "Missing data"}), 409

        seasons_query = Match.query.with_entities(Match.season).distinct().all()
        seasons = [season.season for season in seasons_query]

        team_id = team_id.strip()
        season = season.strip()

        team_check = Team.query.filter_by(id=team_id).first()
        season_check = True if season in seasons else False

        if not team_check:
            return jsonify({"msg": "Chosen team does not exist"}), 409

        if not season_check:
            return jsonify({"msg": "Chosen season does not exist"}), 409

        new_deduction = PointDeduction(
            team_id=team_id,
            points_deducted=points_deducted,
            reason=reason,
            season=season,
        )

        db.session.add(new_deduction)
        db.session.commit()

        return jsonify({"status": "success"}), 201


@admin_blueprint.route("/new-season", methods=["GET", "POST"])
@login_required
def new_season():
    if request.method == "POST":
        data = request.json
        Team.query.filter(Team.id.in_(data["relegate"])).update(
            {"current": False}, synchronize_session=False
        )
        Team.query.filter(Team.id.in_(data["promote"])).update(
            {"current": True}, synchronize_session=False
        )
        current_season = Season.query.order_by(Season.id.desc()).first()
        year_start, year_end = map(int, current_season.season.split("/"))
        new_season_str = f"{year_start + 1}/{year_end + 1}"
        current_season.season = new_season_str

        db.session.commit()
        return (
            jsonify({"msg": f"Success! Welcome to the {new_season_str} Season."}),
            201,
        )


@admin_blueprint.route("/new-match", methods=["GET", "POST"])
@login_required
def new_match():
    if request.method == "POST":
        home_team_id = request.json.get("homeTeamId")
        away_team_id = request.json.get("awayTeamId")
        home_score = request.json.get("homeScore")
        away_score = request.json.get("awayScore")
        match_date = request.json.get("date")

        current_season = Season.query.first().season

        if (
            not home_team_id
            or not away_team_id
            or not home_score
            or not away_score
            or not match_date
        ):
            return jsonify({"msg": "Missing data"}), 409

        home_team_check = Team.query.filter_by(id=int(home_team_id)).first()
        if not home_team_check:
            return jsonify({"msg": "Home team does not exist"}), 409

        away_team_check = Team.query.filter_by(id=int(away_team_id)).first()
        if not away_team_check:
            return jsonify({"msg": "Away team does not exist"}), 409

        new_match = Match(
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            home_score=home_score,
            away_score=away_score,
            season=current_season,
            date=match_date,
        )

        db.session.add(new_match)
        db.session.commit()

        return jsonify({"status": "success"}), 201
