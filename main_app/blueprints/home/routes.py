from flask import Blueprint, render_template

home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/", methods=["GET"])
def index():
    return render_template("home/index.html")


@home_blueprint.route("/about", methods=["GET"])
def about():
    return render_template("home/about.html")


@home_blueprint.route("/generate", methods=["GET"])
def generate():
    return render_template("home/generate.html")
