# Add managers
# Add stints
# Add deductions
from flask import jsonify
import os
from datetime import date
import csv

from models import *
from app import db


def add_teams():
    csv_file_path = os.path.join("csvs", "teams.csv")
    with open(csv_file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_team = Team(
                name=row["name"],
                shortcode=row["shortcode"],
                crest_url=f"https://images.fotmob.com/image_resources/logo/teamlogo/{row['logo_id']}.png",
                current=True if row["current"] == "True" else False,
            )

            db.session.add(new_team)

        # Save data to db
        db.session.commit()
        return jsonify({"msg": "Teams added successfully"})


def add_nations():
    csv_file_path = os.path.join("csvs", "nations.csv")
    with open(csv_file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_nation = Nation(
                name=row["name"],
                shortcode=row["shortcode"],
                flag_url=f"https://images.fotmob.com/image_resources/logo/teamlogo/{row['logo_id']}.png",
            )

            db.session.add(new_nation)

        # Save data to db
        db.session.commit()
        return jsonify({"msg": "Nations added successfully"})


def add_managers():
    nations = Nation.query.all()
    nations_dict = {nation.name: nation.id for nation in nations}
    csv_file_path = os.path.join("csvs", "managers.csv")
    with open(csv_file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            face_url = None
            if row.get("face_id"):
                face_url = "https://images.fotmob.com/image_resources/playerimages/{}.png".format(
                    row.get("face_id")
                )

            nation_id = nations_dict.get(row["nationality"])

            new_manager = Manager(
                name=row["name"],
                face_url=face_url,
                nation_id=nation_id,
            )

            db.session.add(new_manager)

        # Save data to db
        db.session.commit()
        return jsonify({"msg": "Managers added successfully"})


def add_managerial_stints():
    teams = Team.query.all()
    teams_dict = {team.name: team.id for team in teams}

    managers = Manager.query.all()
    managers_dict = {manager.name: manager.id for manager in managers}

    csv_file_path = os.path.join("csvs", "managerial_stints.csv")
    with open(csv_file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            current = None

            if row.get("current") == "False":
                current = False
                date_end = row.get("date_end").split("-")
                date_end = date(int(date_end[0]), int(date_end[1]), int(date_end[2]))

            if row.get("current") == "True":
                current = True
                date_end = None

            date_start = row.get("date_start").split("-")
            date_start = date(
                int(date_start[0]), int(date_start[1]), int(date_start[2])
            )

            manager_id = managers_dict.get(row["manager"])
            team_id = teams_dict.get(row["team"])

            new_stint = ManagerStint(
                manager_id=manager_id,
                team_id=team_id,
                date_start=date_start,
                date_end=date_end,
                current=current,
            )

            db.session.add(new_stint)

        # Save data to db
        db.session.commit()
        return jsonify({"msg": "Stints added successfully"})


def add_matches():
    teams = Team.query.all()
    teams_dict = {team.name: team.id for team in teams}

    csv_file_path = os.path.join("csvs", "pl_results.csv")
    with open(csv_file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            current = None

            home_team_id = teams_dict.get(row["home_team_name"])
            away_team_id = teams_dict.get(row["away_team_name"])

            match_date = row.get("date").split("/")
            match_date = date(
                int(match_date[2]), int(match_date[1]), int(match_date[0])
            )

            new_match = Match(
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                home_score=row["home_score"],
                away_score=row["away_score"],
                date=match_date,
                season=row["season"],
            )

            db.session.add(new_match)

        # Save data to db
        db.session.commit()
        return jsonify({"msg": "Matches added successfully"})
