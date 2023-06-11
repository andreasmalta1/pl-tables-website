from flask import Blueprint, request, jsonify
from os import getenv
from datetime import date
import csv

from main_app import db
from main_app.models import Match
from main_app.utils import get_pl_matches


api = Blueprint("api", __name__)


@api.route(f"/matches", methods=["GET", "POST"])
def matches():
    """
    Matches API
    The POST method, reads the csv containing csv info and saves to the database
    The GET method retrieves match info and is queryable by dates and seasons.
    """
    # Confirm that key authorisation key has been passed and mathces
    authorization_key = request.headers.get("authorization-key")
    if authorization_key != getenv("POST_KEY"):
        return jsonify({"msg": "No authorization key found"})

    if request.method == "POST":
        # Retrieve matches info
        get_pl_matches()

        with open("csvs/pl_results.csv", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # Convert each row into a dictionary and add it to data
            for row in csv_reader:
                match_date = row["date"].split("/")
                match_date = date(
                    int(match_date[2]), int(match_date[1]), int(match_date[0])
                )
                new_match = Match(
                    season=row["season"],
                    home_team_id=row["home_team_id"],
                    home_team_name=row["home_team_name"],
                    away_team_id=row["away_team_id"],
                    away_team_name=row["away_team_name"],
                    home_score=row["home_score"],
                    away_score=row["away_score"],
                    date=match_date,
                )
                db.session.add(new_match)

        # Save data to db
        db.session.commit()
        return jsonify({"msg": "Matches added successfully"})

    if request.method == "GET":
        data = {}

        # Get headers from GET request
        date_from = request.args.get("dateFrom")
        date_to = request.args.get("dateTo")
        season = request.args.get("season")

        # Query matches with given dates
        if date_from and date_to:
            date_from = date_from.split("-")
            date_to = date_to.split("-")

            matches = Match.query.filter(
                db.and_(
                    Match.date
                    >= date(
                        year=int(date_from[0]),
                        month=int(date_from[1]),
                        day=int(date_from[2]),
                    ),
                    Match.date
                    <= date(
                        year=int(date_to[0]), month=int(date_to[1]), day=int(date_to[2])
                    ),
                )
            ).all()

        # Query match with given season
        if season:
            matches = Match.query.filter_by(season=season).all()

        # Retrieve all matches
        if not date_from and not date_to and not season:
            matches = Match.query.all()

        if not matches:
            return jsonify({"msg": "No Matches Found"})

        # Return matches in json format
        for match in matches:
            data[match.id] = {
                "season": match.season,
                "home_team": {
                    "team_id": match.home_team_id,
                    "team_name": match.home_team_name,
                    "score": match.home_score,
                },
                "away_team": {
                    "team_id": match.away_team_id,
                    "team_name": match.away_team_name,
                    "score": match.away_score,
                },
                "date": match.date,
            }

        return jsonify(data)
