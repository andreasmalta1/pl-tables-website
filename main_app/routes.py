from flask import render_template, request, flash

from main_app import app
from main_app.utils import generate_table


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        if end_date < start_date:
            flash("End date must be after start date", category="error")
            return render_template("index.html")

        standings_table = generate_table(start_date, end_date)

        return render_template(
            "index.html",
            standings_table=standings_table,
            start_date=start_date,
            end_date=end_date,
        )

    return render_template("index.html")


# TODO
# How many page viewers
# CSS
# Add buttons -> since guardiola manager etc, Fergie's time in charge ...
# Add tables by season
# Footer -> Add send email and SupportMe
# Landing page

# https://stackoverflow.com/questions/37259740/passing-variables-from-flask-to-javascript
