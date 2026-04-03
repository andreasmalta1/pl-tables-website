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


@admin_blueprint.route("/new-point-deduction", methods=["GET", "POST"])
# @login_required
def new_point_deduction():
    teams = Team.query.order_by(Team.name).all()
    seasons_query = Match.query.with_entities(Match.season).distinct().all()
    seasons = [season.season for season in seasons_query]
    seasons.sort(reverse=True)

    if request.method == "GET":
        return render_template(
            "admin/new_point_deduction.html", teams=teams, seasons=seasons
        )

    if request.method == "POST":
        team_id = request.form.get("team")
        points_deducted = request.form.get("points-deducted")
        reason = request.form.get("reason")
        season = request.form.get("season")

        if not team_id or not points_deducted or not reason or not season:
            error_message = "Invalid Inputs"
            return render_template(
                "admin/new_point_deduction.html",
                teams=teams,
                seasons=seasons,
                message=error_message,
            )

        team_id = team_id.strip()
        season = season.strip()

        team_check = Team.query.filter_by(id=team_id).first()
        season_check = True if season in seasons else False

        if not team_check:
            error_message = "Chosen team does not exist"
            return render_template(
                "admin/new_point_deduction.html",
                teams=teams,
                seasons=seasons,
                message=error_message,
            )

        if not season_check:
            error_message = "Chosen season does not exist"
            return render_template(
                "admin/new_point_deduction.html",
                teams=teams,
                seasons=seasons,
                message=error_message,
            )

        new_deduction = PointDeduction(
            team_id=team_id,
            points_deducted=points_deducted,
            reason=reason,
            season=season,
        )

        db.session.add(new_deduction)
        db.session.commit()

        TeamTable = aliased(Team, name="team_table")

        deduction = (
            PointDeduction.query.filter_by(id=new_deduction.id)
            .join(TeamTable, TeamTable.id == PointDeduction.team_id)
            .add_columns(
                PointDeduction.points_deducted,
                PointDeduction.reason,
                PointDeduction.season,
                TeamTable.name.label("team_name"),
                TeamTable.crest_url.label("crest_url"),
            )
            .first()
        )

        return render_template("admin/new_point_deduction.html", deduction=deduction)


@admin_blueprint.route("/new-season", methods=["GET", "POST"])
# @login_required
def new_season():
    season = Season.query.first().season
    current_teams = Team.query.filter_by(current=True).order_by(Team.name).all()
    non_current_teams = Team.query.filter_by(current=False).order_by(Team.name).all()

    current_year = int(season.split("/")[0])
    new_season = f"{current_year + 1}/{current_year + 2}"

    if request.method == "GET":
        return render_template(
            "admin/new_season.html",
            current_teams=current_teams,
            non_current_teams=non_current_teams,
            season=new_season,
        )

    if request.method == "POST":
        relegated_teams = request.form.getlist("relegated-teams")
        promoted_teams = request.form.getlist("promoted-teams")
        new_season_entry = request.form.get("season")

        if not relegated_teams or not promoted_teams or not new_season_entry:
            error_message = "Invalid Inputs"
            return render_template(
                "admin/new_season.html",
                current_teams=current_teams,
                non_current_teams=non_current_teams,
                season=new_season,
                error_message=error_message,
            )

        relegated_teams_list = []
        for team_id in relegated_teams:
            team = Team.query.filter_by(id=int(team_id)).first()
            error_message = "Team not found"
            if not team:
                return render_template(
                    "admin/new_season.html",
                    current_teams=current_teams,
                    non_current_teams=non_current_teams,
                    season=new_season,
                    error_message=error_message,
                )
            team.current = False
            relegated_teams_list.append(team)

        promoted_teams_list = []
        for team_id in promoted_teams:
            team = Team.query.filter_by(id=int(team_id)).first()
            if not team:
                return render_template(
                    "admin/new_season.html",
                    current_teams=current_teams,
                    non_current_teams=non_current_teams,
                    season=new_season,
                    error_message=error_message,
                )
            team.current = True
            promoted_teams_list.append(team)

        season = Season.query.first()
        season.season = new_season

        last_row = LastRow.query.first()
        last_row.last_row = -1

        db.session.commit()

        return render_template(
            "admin/new_season.html",
            new_season=new_season,
            promoted_teams=promoted_teams_list,
            relegated_teams=relegated_teams_list,
        )


@admin_blueprint.route("/new-match", methods=["GET", "POST"])
# @login_required
def new_match():
    current_season = Season.query.first().season
    current_teams = Team.query.filter_by(current=True).order_by(Team.name).all()

    if request.method == "GET":
        return render_template(
            "admin/new_match.html",
            teams=current_teams,
            season=current_season,
        )

    if request.method == "POST":
        new_matches = []
        HomeTeam = aliased(Team, name="home_team")
        AwayTeam = aliased(Team, name="away_team")

        home_team_ids = request.form.getlist("home-team")
        away_team_ids = request.form.getlist("away-team")
        home_scores = request.form.getlist("home-score")
        away_scores = request.form.getlist("away-score")
        match_dates = request.form.getlist("match-date")

        for home_team_id, away_team_id, home_score, away_score, match_date in zip(
            home_team_ids, away_team_ids, home_scores, away_scores, match_dates
        ):

            if (
                not home_team_id
                or not away_team_id
                or not home_score
                or not away_score
                or not match_date
            ):
                error_message = "Invalid Inputs"
                return render_template(
                    "admin/new_match.html",
                    teams=current_teams,
                    season=current_season,
                    error_message=error_message,
                )

            home_team_check = Team.query.filter_by(id=int(home_team_id)).first()
            if not home_team_check:
                error_message = "Home Team not found"
                return render_template(
                    "admin/new_match.html",
                    teams=current_teams,
                    season=current_season,
                    error_message=error_message,
                )

            away_team_check = Team.query.filter_by(id=int(away_team_id)).first()
            if not away_team_check:
                error_message = "Away Team not found"
                return render_template(
                    "admin/new_match.html",
                    teams=current_teams,
                    season=current_season,
                    error_message=error_message,
                )

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

            match = (
                Match.query.filter_by(id=new_match.id)
                .join(HomeTeam, HomeTeam.id == Match.home_team_id)
                .join(AwayTeam, AwayTeam.id == Match.away_team_id)
                .add_columns(
                    HomeTeam.name.label("home_team_name"),
                    Match.home_score,
                    HomeTeam.crest_url.label("home_crest_url"),
                    AwayTeam.name.label("away_team_name"),
                    Match.away_score,
                    AwayTeam.crest_url.label("away_crest_url"),
                    Match.date,
                    Match.season,
                )
                .first()
            )

            new_matches.append(match)

        return render_template(
            "admin/new_match.html",
            new_matches=new_matches,
        )
