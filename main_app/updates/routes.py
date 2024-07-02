from flask import jsonify, render_template, request
from flask_login import login_required

from app import db
from updates import updates_blueprint
from models import *


@updates_blueprint.route("/new-team", methods=["GET", "POST"])
@login_required
def new_team():
    if request.method == "GET":
        return render_template("updates/new_team.html")

    if request.method == "POST":
        team_name = request.form.get("team_name")
        shortcode = request.form.get("shortcode")
        crest_url = request.form.get("crest_url")

        new_team = Team(
            name=team_name,
            shortcode=shortcode,
            crest_url=crest_url,
            current=False,
        )

        db.session.add(new_team)
        db.session.commit()

        return render_template("updates/new_team.html", team=new_team)


@updates_blueprint.route("/new-nation", methods=["GET", "POST"])
@login_required
def new_nation():
    if request.method == "GET":
        return render_template("updates/new_nation.html")

    if request.method == "POST":
        nation_name = request.form.get("nation_name")
        shortcode = request.form.get("shortcode")
        flag_url = request.form.get("flag_url")

        new_nation = Nation(
            name=nation_name,
            shortcode=shortcode,
            flag_url=flag_url,
        )

        db.session.add(new_nation)
        db.session.commit()

        return render_template("updates/new_nation.html", nation=new_nation)


@updates_blueprint.route("/new-manager", methods=["GET", "POST"])
@login_required
def new_manager():
    if request.method == "GET":
        nations = Nation.query.all()
        return render_template("updates/new_manager.html", nations=nations)

    if request.method == "POST":
        manager_name = request.form.get("manager_name")
        face_url = request.form.get("face_url")
        nation_id = request.form.get("nation")

        new_manager = Manager(
            name=manager_name,
            face_url=face_url,
            nation_id=nation_id,
        )

        db.session.add(new_manager)
        db.session.commit()

        return render_template("updates/new_manager.html", manager=new_manager)


@updates_blueprint.route("/new-stint", methods=["GET", "POST"])
@login_required
def new_stint():
    if request.method == "GET":
        managers = Manager.query.all()
        teams = Team.query.all()
        return render_template("updates/new_stint.html", managers=managers, teams=teams)

    if request.method == "POST":
        manager_id = request.form.get("manager")
        team_id = request.form.get("team")
        current = request.form.get("current")
        date_start = request.form.get("start-date")
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

        return render_template("updates/new_stint.html", stint=new_stint)
