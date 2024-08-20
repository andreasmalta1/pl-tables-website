from flask import jsonify
import os
from datetime import date
import csv
from werkzeug.security import generate_password_hash

from .models import *

BUCKET_URL = os.getenv("S3_BUCKET_URL")


def add_teams():
    team_check = Team.query.first()
    if team_check:
        print("Teams already exist. Skipping")
        return

    csv_file_path = os.path.join("csvs", "teams.csv")
    with open(csv_file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            crest_image_filename = row["name"].lower().replace(" ", "-")
            new_team = Team(
                name=row["name"],
                shortcode=row["shortcode"],
                crest_url=f"{BUCKET_URL}/team/{crest_image_filename}.png",
                current=True if row["current"] == "True" else False,
            )

            db.session.add(new_team)

        # Save data to db
        db.session.commit()
        return jsonify({"msg": "Teams added successfully"})


def add_nations():
    nations_check = Nation.query.first()
    if nations_check:
        print("Nations already exist. Skipping")
        return

    csv_file_path = os.path.join("csvs", "nations.csv")
    with open(csv_file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            flag_image_filename = row["name"].lower().replace(" ", "-")
            new_nation = Nation(
                name=row["name"],
                shortcode=row["shortcode"],
                flag_url=f"{BUCKET_URL}/nation/{flag_image_filename}.png",
            )

            db.session.add(new_nation)

        # Save data to db
        db.session.commit()
        return jsonify({"msg": "Nations added successfully"})


def add_managers():
    managers_check = Manager.query.first()
    if managers_check:
        print("Managers already exist. Skipping")
        return

    nations = Nation.query.all()
    nations_dict = {nation.name: nation.id for nation in nations}
    csv_file_path = os.path.join("csvs", "managers.csv")
    with open(csv_file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row.get("face_image") == "True":
                manager_face_image_filename = row["name"].lower().replace(" ", "-")
                face_url = (f"{BUCKET_URL}/manager/{manager_face_image_filename}.png",)

            if row.get("face_image") == "False":
                face_url = (f"{BUCKET_URL}/manager/no-face.png",)

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
    stints_check = ManagerStint.query.first()
    if stints_check:
        print("Managerial stints already exist. Skipping")
        return

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
    matches_check = Match.query.first()
    if matches_check:
        print("Matches already exist. Skipping")
        return

    teams = Team.query.all()
    teams_dict = {team.name: team.id for team in teams}

    csv_file_path = os.path.join("csvs", "pl_results.csv")
    with open(csv_file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
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


def add_point_deductions():
    deductions_check = PointDeduction.query.first()
    if deductions_check:
        print("Point Deductions already exist. Skipping")
        return

    teams = Team.query.all()
    teams_dict = {team.name: team.id for team in teams}

    csv_file_path = os.path.join("csvs", "point_deductions.csv")
    with open(csv_file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:

            home_team_id = teams_dict.get(row["team_name"])

            new_deduction = PointDeduction(
                team_id=home_team_id,
                points_deducted=row["points_deducted"],
                reason=row["reason"],
                season=row["season"],
            )

            db.session.add(new_deduction)

        # Save data to db
        db.session.commit()
        return jsonify({"msg": "Point Deductions added successfully"})


def add_user():
    user = User.query.first()
    if user:
        print("User already exists. Skipping")
        return

    new_user = User(
        email=os.getenv("ADMIN_EMAIL"),
        first_name=os.getenv("ADMIN_FIRST_NAME"),
        last_name=os.getenv("ADMIN_LAST_NAME"),
        password=generate_password_hash(os.getenv("ADMIN_PASSWORD"), method="sha256"),
    )

    db.session.add(new_user)

    # Save data to db
    db.session.commit()
    return jsonify({"msg": "User added successfully"})


def add_last_row():
    last_row = LastRow.query.first()
    if last_row:
        print("Last Row already exists. Skipping")
        return

    last_row = LastRow(last_row=-1)

    db.session.add(last_row)

    # Save data to db
    db.session.commit()
    return jsonify({"msg": "Last Row added successfully"})
