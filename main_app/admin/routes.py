from flask import render_template, request
from flask_login import login_required
from sqlalchemy.orm import aliased
from datetime import datetime

from app import db
from admin import admin_blueprint
from models import *


@admin_blueprint.route("/", methods=["GET"])
@login_required
def index():
    if request.method == "GET":
        return render_template("admin/index.html")


@admin_blueprint.route("/new-team", methods=["GET", "POST"])
@login_required
def new_team():
    if request.method == "GET":
        return render_template("admin/new_team.html")

    if request.method == "POST":
        team_name = request.form.get("team_name")
        shortcode = request.form.get("shortcode")
        crest_url = request.form.get("crest_url")

        if not team_name or not shortcode or not crest_url:
            error_message = "Invalid Inputs"
            return render_template("admin/new_team.html", message=error_message)

        shortcode = shortcode.upper().strip()

        team_check = Team.query.filter_by(shortcode=shortcode).first()
        if team_check:
            error_message = "Shortcode already exists"
            return render_template("admin/new_team.html", message=error_message)

        new_team = Team(
            name=team_name.strip(),
            shortcode=shortcode,
            crest_url=crest_url.strip(),
            current=False,
        )

        db.session.add(new_team)
        db.session.commit()

        return render_template("admin/new_team.html", team=new_team)


@admin_blueprint.route("/new-nation", methods=["GET", "POST"])
@login_required
def new_nation():
    if request.method == "GET":
        return render_template("admin/new_nation.html")

    if request.method == "POST":
        nation_name = request.form.get("nation_name")
        shortcode = request.form.get("shortcode")
        flag_url = request.form.get("flag_url")

        if not nation_name or not shortcode or not flag_url:
            error_message = "Invalid Inputs"
            return render_template("admin/new_nation.html", message=error_message)

        shortcode = shortcode.upper().strip()

        nation_check = Nation.query.filter_by(shortcode=shortcode).first()
        if nation_check:
            error_message = "Shortcode already exists"
            return render_template("admin/new_nation.html", message=error_message)

        new_nation = Nation(
            name=nation_name.strip(),
            shortcode=shortcode,
            flag_url=flag_url.strip(),
        )

        db.session.add(new_nation)
        db.session.commit()

        return render_template("admin/new_nation.html", nation=new_nation)


@admin_blueprint.route("/new-manager", methods=["GET", "POST"])
@login_required
def new_manager():
    nations = Nation.query.order_by(Nation.name).all()

    if request.method == "GET":
        return render_template("admin/new_manager.html", nations=nations)

    if request.method == "POST":
        manager_name = request.form.get("manager_name")
        face_url = request.form.get("face_url")
        nation_id = request.form.get("nation")

        if not manager_name or not face_url or not nation_id:
            error_message = "Invalid Inputs"
            return render_template(
                "admin/new_manager.html", nations=nations, message=error_message
            )

        nation_id = nation_id.strip()

        nation_check = Nation.query.filter_by(id=nation_id).first()
        if not nation_check:
            error_message = "Chosen nation does not exist"
            return render_template(
                "admin/new_manager.html", nations=nations, message=error_message
            )

        new_manager = Manager(
            name=manager_name.strip(),
            face_url=face_url.strip(),
            nation_id=nation_id,
        )

        db.session.add(new_manager)
        db.session.commit()

        NationTable = aliased(Nation, name="nation_table")

        manager = (
            Manager.query.filter_by(id=new_manager.id)
            .join(NationTable, NationTable.id == Manager.nation_id)
            .add_columns(
                Manager.name,
                Manager.face_url,
                NationTable.name.label("nation_name"),
                NationTable.flag_url.label("flag_url"),
            )
            .first()
        )

        return render_template("admin/new_manager.html", manager=manager)


@admin_blueprint.route("/new-stint", methods=["GET", "POST"])
@login_required
def new_stint():
    managers = Manager.query.order_by(Manager.name).all()
    teams = Team.query.order_by(Team.name).all()

    if request.method == "GET":
        return render_template("admin/new_stint.html", managers=managers, teams=teams)

    if request.method == "POST":
        manager_id = request.form.get("manager")
        team_id = request.form.get("team")
        current = request.form.get("current")
        date_start = request.form.get("start-date")

        if not manager_id or not team_id or not date_start:
            error_message = "Invalid Inputs"
            return render_template(
                "admin/new_stint.html",
                managers=managers,
                teams=teams,
                message=error_message,
            )

        team_id = team_id.strip()
        manager_id = manager_id.strip()

        team_check = Team.query.filter_by(id=team_id).first()
        manager_check = Manager.query.filter_by(id=manager_id).first()

        if not team_check:
            error_message = "Chosen team does not exist"
            return render_template(
                "admin/new_stint.html",
                managers=managers,
                teams=teams,
                message=error_message,
            )

        if not manager_check:
            error_message = "Chosen manager does not exist"
            return render_template(
                "admin/new_stint.html",
                managers=managers,
                teams=teams,
                message=error_message,
            )

        if not current:
            current = False
            date_end = request.form.get("end-date")

        if current:
            current = True
            date_end = None

        new_stint = ManagerStint(
            manager_id=manager_id,
            team_id=team_id,
            date_start=date_start,
            date_end=date_end,
            current=current,
        )

        db.session.add(new_stint)
        db.session.commit()

        ManagerTable = aliased(Manager, name="manager_table")
        TeamTable = aliased(Team, name="team_table")

        stint = (
            ManagerStint.query.filter_by(id=new_stint.id)
            .join(ManagerTable, ManagerTable.id == ManagerStint.manager_id)
            .join(TeamTable, TeamTable.id == ManagerStint.team_id)
            .add_columns(
                ManagerStint.date_start,
                ManagerStint.date_end,
                ManagerStint.current,
                ManagerTable.name.label("manager_name"),
                ManagerTable.face_url.label("face_url"),
                TeamTable.name.label("team_name"),
                TeamTable.crest_url.label("crest_url"),
            )
            .first()
        )

        return render_template("admin/new_stint.html", stint=stint)


@admin_blueprint.route("/end-stint", methods=["GET", "POST"])
@login_required
def end_stint():
    TeamTable = aliased(Team, name="team_table")
    ManagerTable = aliased(Manager, name="manager_table")

    stints = (
        ManagerStint.query.filter_by(current=True)
        .join(TeamTable, TeamTable.id == ManagerStint.team_id)
        .join(ManagerTable, ManagerTable.id == ManagerStint.manager_id)
        .order_by(ManagerStint.date_start)
        .add_columns(
            ManagerStint.id,
            TeamTable.name.label("team_name"),
            ManagerTable.name.label("manager_name"),
        )
        .all()
    )

    if request.method == "GET":
        return render_template("admin/end_stint.html", stints=stints)

    if request.method == "POST":
        stint_id = request.form.get("stint")
        date_end = request.form.get("end-date")

        if not stint_id or not date_end:
            error_message = "Invalid Inputs"
            return render_template(
                "admin/end_stint.html",
                stints=stints,
                message=error_message,
            )

        ended_stint = ManagerStint.query.filter_by(id=stint_id).first()
        if not ended_stint:
            error_message = "Chosen stint does not exist"
            return render_template(
                "admin/end_stint.html",
                stints=stints,
                message=error_message,
            )

        if datetime.strptime(date_end, "%Y-%m-%d").date() < ended_stint.date_start:
            error_message = "End date must be after start date"
            return render_template(
                "admin/end_stint.html",
                stints=stints,
                message=error_message,
            )

        ended_stint.date_end = date_end
        ended_stint.current = False

        db.session.commit()

        stint = (
            ManagerStint.query.filter_by(id=ended_stint.id)
            .join(ManagerTable, ManagerTable.id == ManagerStint.manager_id)
            .join(TeamTable, TeamTable.id == ManagerStint.team_id)
            .add_columns(
                ManagerStint.date_start,
                ManagerStint.date_end,
                ManagerTable.name.label("manager_name"),
                ManagerTable.face_url.label("face_url"),
                TeamTable.name.label("team_name"),
                TeamTable.crest_url.label("crest_url"),
            )
            .first()
        )

        return render_template("admin/end_stint.html", ended_stint=stint)


@admin_blueprint.route("/new-point-deduction", methods=["GET", "POST"])
@login_required
def new_point_deduction():
    if request.method == "GET":
        teams = Team.query.order_by(Team.name).all()
        season = Season.query.first().season
        return render_template(
            "admin/new_point_deduction.html", teams=teams, season=season
        )

    if request.method == "POST":
        team_id = request.form.get("team")
        points_deducted = request.form.get("points-deducted")
        reason = request.form.get("reason")
        season = request.form.get("season")

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
@login_required
def new_season():
    if request.method == "GET":
        season = Season.query.first().season
        current_teams = Team.query.filter_by(current=True).order_by(Team.name).all()
        non_current_teams = (
            Team.query.filter_by(current=False).order_by(Team.name).all()
        )

        current_year = int(season.split("/")[0])
        new_season = f"{current_year + 1}/{current_year + 2}"
        return render_template(
            "admin/new_season.html",
            current_teams=current_teams,
            non_current_teams=non_current_teams,
            season=new_season,
        )

    if request.method == "POST":
        relegated_teams = request.form.getlist("relegated-teams")
        promoted_teams = request.form.getlist("promoted-teams")
        new_season = request.form.get("season")

        relegated_teams_list = []
        for team_id in relegated_teams:
            team = Team.query.filter_by(id=int(team_id)).first()
            team.current = False
            relegated_teams_list.append(team)

        promoted_teams_list = []
        for team_id in promoted_teams:
            team = Team.query.filter_by(id=int(team_id)).first()
            team.current = True
            promoted_teams_list.append(team)

        season = Season.query.first()
        season.season = new_season

        db.session.commit()

        return render_template(
            "admin/new_season.html",
            new_season=new_season,
            promoted_teams=promoted_teams_list,
            relegated_teams=relegated_teams_list,
        )
