from flask import Flask, render_template, request
from tabulate import tabulate

from utils import generate_results_table

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        results_table = generate_results_table(start_date, end_date)

        return render_template("index.html", table=results_table)

    return render_template("index.html")


# TODO
# Git
# .env
# CSS
# Create PL table not results
# Add buttons -> since guardiola manager etc
# Add tables by season
