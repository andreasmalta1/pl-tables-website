from flask import Blueprint, render_template, request
from flask_login import current_user

from ...utils import update_visits

home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/", methods=["GET"])
def index():
    admin = False
    if current_user.is_authenticated:
        admin = True

    update_visits(request.remote_addr, "home", admin)
    return render_template("home/index.html")


@home_blueprint.route("/about", methods=["GET"])
def about():
    return render_template("home/about.html")


@home_blueprint.route("/generate", methods=["GET"])
def generate():
    return render_template("home/generate.html")
