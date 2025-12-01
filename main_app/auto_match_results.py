#!/usr/bin/python

import os
import psycopg2
import pandas as pd
import soccerdata as sd
from dotenv import load_dotenv

load_dotenv()


def connect_to_db():
    connection = psycopg2.connect(os.getenv("SQLALCHEMY_DATABASE_URI"))
    cursor = connection.cursor()
    return connection, cursor


def disconnect_from_db(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


def post_results(results, conn, cur):
    try:
        for result in results:
            result = tuple(result)
            insert_query = """INSERT INTO matches (home_team_id, home_score, away_team_id, away_score, season, date) VALUES (%s,%s,%s,%s,%s,%s)"""
            cur.execute(insert_query, result)
            conn.commit()
            print("Record inserted successfully into match table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)


def update_row(last_row, conn, cur):
    try:
        update_query = """UPDATE lastrow SET last_row = %s"""
        cur.execute(update_query, [last_row])
        conn.commit()
        print("Last row updated successfully")

    except (Exception, psycopg2.Error) as error:
        print(error)


def main():
    conn, cur = connect_to_db()

    get_current_season = """SELECT season FROM season LIMIT 1"""
    cur.execute(get_current_season)
    season = cur.fetchall()[0][0]

    get_last_row = """SELECT last_row FROM lastrow LIMIT 1"""
    cur.execute(get_last_row)
    last_row = cur.fetchall()[0][0]

    get_teams = """SELECT id, name FROM teams"""
    cur.execute(get_teams)
    teams = dict(cur.fetchall())

    for team_id, team_value in teams.items():
        if team_value == "Nottingham Forest":
            teams[team_id] = "Nott'ham Forest"

        if team_value == "Brighton & Hove Albion":
            teams[team_id] = "Brighton"

        if team_value == "West Ham United":
            teams[team_id] = "West Ham"

        if team_value == "Tottenham Hotspur":
            teams[team_id] = "Tottenham"

        if team_value == "Wolverhampton Wanderers":
            teams[team_id] = "Wolves"

        if "AFC" in team_value:
            teams[team_id] = teams[team_id].replace("AFC ", "").replace(" AFC", "")

        if "FC" in team_value:
            teams[team_id] = teams[team_id].replace(" FC", "")

        if "United" in team_value and "Leeds" not in team_value:
            teams[team_id] = teams[team_id].replace("United", "Utd")

    teams_dict = {value: key for key, value in teams.items()}

    fbref = sd.FBref(leagues="ENG-Premier League", seasons=season.split("/")[0])
    schedule = fbref.read_schedule()
    df = (
        schedule[["date", "home_team", "score", "away_team"]]
        .dropna()
        .reset_index()
        .iloc[last_row + 1 :, :]
    )

    results_to_post = []

    for index, row in df.iterrows():
        last_row += 1
        score = row["score"].split("–")
        home_score = int(score[0])
        away_score = int(score[1])
        home_team_id = teams_dict[row["home_team"]]
        away_team_id = teams_dict[row["away_team"]]

        results_to_post.append(
            [
                home_team_id,
                home_score,
                away_team_id,
                away_score,
                season,
                row["date"],
            ]
        )

    if results_to_post:
        post_results(results_to_post, conn, cur)

    update_row(last_row, conn, cur)

    disconnect_from_db(conn, cur)


if __name__ == "__main__":
    main()
