from flask import render_template

from home import home_blueprint


@home_blueprint.route("/", methods=["GET"])
def index():
    return render_template("main/index.html")
