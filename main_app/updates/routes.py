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
