import requests
import pandas as pd
import csv
from requests import get, exceptions
from os import getenv
from collections import defaultdict
from bs4 import BeautifulSoup


# Function to generate the table of Premier League results
def generate_table(start_date, end_date, season):
    team_data = get_teams_info()

    if start_date and end_date:
        API_URL = (
            f"{getenv('HOST_NAME')}/matches?dateFrom={start_date}&dateTo={end_date}"
        )

    if season:
        API_URL = f"{getenv('HOST_NAME')}/matches?season={season}"

    headers = {"authorization-key": getenv("POST_KEY")}

    try:
        response = get(API_URL, headers=headers)
        matches = response.json()

        if not matches or len(matches) == 0:
            return None

        standings = defaultdict(
            lambda: {
                "team_id": None,
                "url": None,
                "played": 0,
                "win": 0,
                "draw": 0,
                "loss": 0,
                "goals_for": 0,
                "goals_against": 0,
                "gd": 0,
                "points": 0,
            }
        )

        for match_id in matches:
            home_team = matches[match_id]["home_team"]["team_name"]
            home_score = matches[match_id]["home_team"]["score"]
            away_team = matches[match_id]["away_team"]["team_name"]
            away_score = matches[match_id]["away_team"]["score"]

            standings[home_team]["played"] += 1
            standings[away_team]["played"] += 1

            standings[home_team]["goals_for"] += home_score
            standings[away_team]["goals_for"] += away_score

            standings[home_team]["goals_against"] += away_score
            standings[away_team]["goals_against"] += home_score

            standings[home_team]["gd"] += home_score - away_score
            standings[away_team]["gd"] += away_score - home_score

            # Update points and goal differences based on the result
            if home_score > away_score:
                standings[home_team]["win"] += 1
                standings[away_team]["loss"] += 1
                standings[home_team]["points"] += 3
            elif home_score < away_score:
                standings[home_team]["loss"] += 1
                standings[away_team]["win"] += 1
                standings[away_team]["points"] += 3
            else:
                standings[home_team]["draw"] += 1
                standings[away_team]["draw"] += 1
                standings[home_team]["points"] += 1
                standings[away_team]["points"] += 1

        for team in standings:
            if not standings[team]["url"]:
                team_id = team_data.get(team)["logo_id"]
                if team:
                    standings[team]["url"] = f"{getenv('CREST_URL')}{team_id}.png"

        # Sort teams by points and goal differences
        standings_table = sorted(
            standings.items(),
            key=lambda x: (x[1]["points"], x[1]["gd"]),
            reverse=True,
        )

        return standings_table

    except exceptions.RequestException as e:
        print("An error occurred:", str(e))
        return None


def get_pl_matches():
    data = {
        "match_no": [],
        "season": [],
        "home_team_id": [],
        "home_team_name": [],
        "away_team_id": [],
        "away_team_name": [],
        "home_score": [],
        "away_score": [],
        "date": [],
    }

    team_data = get_teams_info()

    match_no = 0
    num_rounds = 42
    start_year = 1992
    for year in range(start_year, 2023):
        if year > 1994:
            num_rounds = 38
        for round in range(1, num_rounds + 1):
            link = f"{getenv('PL_MATCHES_URL')}{year}-{year+1}-spieltag/{round}"
            source = requests.get(link).text
            page = BeautifulSoup(source, "lxml")
            table = page.find("table", class_="standard_tabelle")
            rows = table.find_all("tr")

            date = None

            for row in rows:
                cells = row.find_all("td")
                if cells[0].get_text():
                    date = cells[0].get_text()

                home_team_name = cells[2].get_text().strip()
                home_team_id = team_data[home_team_name]["team_id"]
                away_team_name = cells[2].get_text().strip()
                away_team_id = team_data[away_team_name]["team_id"]
                score = cells[-2].get_text().strip().split()[0].split(":")

                data["match_no"].append(match_no)
                data["season"].append(f"{year}/{year+1}")
                data["home_team_id"].append(home_team_id)
                data["home_team_name"].append(home_team_name)
                data["away_team_id"].append(away_team_id)
                data["away_team_name"].append(cells[4].get_text().strip())
                data["home_score"].append(score[0])
                data["away_score"].append(score[1])
                data["date"].append(date)

                match_no += 1

    df = pd.DataFrame(data=data)
    df.to_csv("csvs/pl_results.csv")


def get_teams_info():
    team_data = {}

    with open("csvs/team_ids.csv", "r") as file:
        csvreader = csv.reader(file)
        next(csvreader, None)

        for row in csvreader:
            team_data[row[1]] = {"team_id": row[0], "logo_id": row[2]}

    return team_data
