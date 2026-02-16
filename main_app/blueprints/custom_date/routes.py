from flask import Blueprint, render_template

custom_date_blueprint = Blueprint("custom_date", __name__)


@custom_date_blueprint.route("/", methods=["GET"])
def custom_date():
    return render_template("blueprints/custom_dates.html")
