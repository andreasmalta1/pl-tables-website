from flask import render_template

from main import home_blueprint


@home_blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")
