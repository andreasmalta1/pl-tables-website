from flask import Blueprint, render_template, request
from flask_login import current_user

from ...utils import update_visits

all_time_blueprint = Blueprint("all_time", __name__)


@all_time_blueprint.route("/", methods=["GET"])
def index():
    admin = False
    if current_user.is_authenticated:
        admin = True

    update_visits(request.remote_addr, "all_time", admin)

    return render_template("blueprints/all_time.html")
