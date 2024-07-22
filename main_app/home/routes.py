from flask import render_template

from home import home_blueprint


@home_blueprint.route("/", methods=["GET"])
def index():
    return render_template("home/index.html")


@home_blueprint.route("/about", methods=["GET"])
def about():
    return render_template("home/about.html")
