from flask import render_template, request
from tabulate import tabulate

from main_app import app
from main_app.utils import generate_results_table, generate_standings_table


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        results_table = generate_results_table(start_date, end_date)
        results_table = generate_results_table(start_date, end_date)
        standing_table = generate_standings_table(results_table)

        return render_template(
            "index.html", results_table=results_table, standing_table=standing_table
        )

    return render_template("index.html")


# TODO
# CSS -> + logos maybe
# Create PL table not results
# Add buttons -> since guardiola manager etc
# Add tables by season
# Make sure correct dates
# Date to = current date default

# https://stackoverflow.com/questions/37259740/passing-variables-from-flask-to-javascript
