#!/usr/bin/python

import os
import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
URL = "http://api.football-data.org/v4/competitions/PL/matches"
STATUS = "FINISHED"
LIMIT = 380
HEADERS = {"X-Auth-Token": API_KEY}


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
            insert_query = """INSERT INTO matches (id, home_team_id, home_score, away_team_id, away_score, season, date) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING;"""
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

    get_teams = """SELECT id, name FROM teams"""
    cur.execute(get_teams)
    teams = dict(cur.fetchall())

    teams_dict = {value: key for key, value in teams.items()}

    api_data = requests.get(
        url=f"{URL}?status={STATUS}&limit={LIMIT}",
        headers=HEADERS,
    )

    matches = api_data.json().get("matches")

    results_to_post = []

    for match in matches:
        match_id = match.get("id")
        home_score = match.get("score").get("fullTime").get("home")
        away_score = match.get("score").get("fullTime").get("away")
        home_team_name = match.get("homeTeam").get("name")
        away_team_name = match.get("homeTeam").get("name")
        home_team_id = teams_dict.get(home_team_name) or teams_dict.get(
            home_team_name.replace(" FC", "")
        )
        away_team_id = teams_dict.get(away_team_name) or teams_dict.get(
            away_team_name.replace(" FC", "")
        )
        match_date = match.get("utcDate").split("T")[0]

        results_to_post.append(
            [
                match_id,
                home_team_id,
                home_score,
                away_team_id,
                away_score,
                season,
                match_date,
            ]
        )

    if results_to_post:
        post_results(results_to_post, conn, cur)

    disconnect_from_db(conn, cur)


if __name__ == "__main__":
    main()
