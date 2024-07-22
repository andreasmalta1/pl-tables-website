from flask import render_template, request

from all_time import all_time_blueprint
from utils import update_visits


@all_time_blueprint.route("/", methods=["GET"])
def index():
    update_visits(request.remote_addr, "home")

    return render_template("all_time/all_time.html")
