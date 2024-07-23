from flask import render_template, request
from flask_login import current_user

from all_time import all_time_blueprint
from utils import update_visits


@all_time_blueprint.route("/", methods=["GET"])
def index():
    admin = False
    if current_user.is_authenticated:
        admin = True

    update_visits(request.remote_addr, "all_time", admin)

    return render_template("all_time/all_time.html")
