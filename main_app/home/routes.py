from flask import render_template, request

from home import home_blueprint
from models import Season
from utils import generate_table, update_visits


@home_blueprint.route("/", methods=["GET"])
def index():
    update_visits(request.remote_addr, "home")
    season = Season.query.first().season

    standings = generate_table(None, None, season)

    return render_template("main/index.html", standings=standings)
