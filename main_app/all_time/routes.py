from flask import render_template, request
from sqlalchemy.orm import aliased

from all_time import all_time_blueprint
from models import Team, Match, Season
from utils import generate_table, update_visits


@all_time_blueprint.route("/", methods=["GET"])
def index():
    update_visits(request.remote_addr, "home")

    return render_template("all_time/all_time.html")
