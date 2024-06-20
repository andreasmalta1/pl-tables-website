# Add managers
# Add stints
# Add deductions
from flask import jsonify
import os
import csv

from models import *
from app import db


def add_teams():
    csv_file_path = os.path.join("csvs", "teams.csv")
    with open(csv_file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_team = Team(
                name=row["team_name"],
                shortcode=row["team_code"],
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
        return jsonify({"msg": "Nations added successfully"})
