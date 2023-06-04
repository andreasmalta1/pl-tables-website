from requests import get, exceptions
from os import getenv
from collections import defaultdict

from main_app.teams import TEAMS


# Function to generate the table of Premier League results
def generate_table(start_date, end_date):
    API_KEY = getenv("API_KEY")
    API_URL = getenv("API_URL")

    API_URL = f"{API_URL}?dateFrom={start_date}&dateTo={end_date}"
    headers = {"X-Auth-Token": API_KEY}

    try:
        response = get(API_URL, headers=headers)
        data = response.json()
        matches = data["matches"]

        if len(matches) == 0:
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

        for match in matches:
            home_team = match["homeTeam"]["name"]
            home_score = match["score"]["fullTime"]["home"]
            away_team = match["awayTeam"]["name"]
            away_score = match["score"]["fullTime"]["away"]

            standings[home_team]["team_id"] = match["homeTeam"]["id"]
            standings[away_team]["team_id"] = match["awayTeam"]["id"]

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
                team_id = TEAMS[team]
                standings[team]["url"] = f"{getenv('API_CREST_URL')}{team_id}.png"

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
