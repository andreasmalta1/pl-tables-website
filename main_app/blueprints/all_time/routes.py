from flask import Blueprint, render_template

all_time_blueprint = Blueprint("all_time", __name__)


@all_time_blueprint.route("/", methods=["GET"])
def index():
    return render_template("blueprints/all_time.html")
