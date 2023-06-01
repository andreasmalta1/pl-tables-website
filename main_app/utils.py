from requests import get, exceptions
from os import getenv
from collections import defaultdict


# Function to generate the table of Premier League results
def generate_results_table(start_date, end_date):
    API_KEY = getenv("API_KEY")
    API_URL = getenv("API_URL")

    API_URL = f"{API_URL}?dateFrom={start_date}&dateTo={end_date}"
    headers = {"X-Auth-Token": API_KEY}

    try:
        response = get(API_URL, headers=headers)
        response.raise_for_status()

        data = response.json()
        matches = data["matches"]

        if len(matches) == 0:
            return None

        table = []
        headers = ["Home Team", "Away Team", "Score"]

        # https://www.football-data.org/documentation/quickstart
        # Check v2 vs v4

        # Create table rows with match details
        for match in matches:
            home_team = match["homeTeam"]["name"]
            away_team = match["awayTeam"]["name"]
            home_score = match["score"]["fullTime"]["homeTeam"]
            away_score = match["score"]["fullTime"]["awayTeam"]
            table.append([home_team, away_team, home_score, away_score])

        return table

    except exceptions.RequestException as e:
        print("An error occurred:", str(e))
        return None


def generate_standings_table(results_table):
    standing = defaultdict(lambda: {"played": 0, "points": 0, "goal_diff": 0})

    for row in results_table:
        home_team = row[0]
        away_team = row[1]
        home_score = int(row[2])
        away_score = int(row[3])

        # Update played matches count
        standing[home_team]["played"] += 1
        standing[away_team]["played"] += 1

        # Update points and goal differences based on the result
        if home_score > away_score:
            standing[home_team]["points"] += 3
            standing[home_team]["goal_diff"] += home_score - away_score
            standing[away_team]["goal_diff"] += away_score - home_score
        elif home_score < away_score:
            standing[away_team]["points"] += 3
            standing[home_team]["goal_diff"] += home_score - away_score
            standing[away_team]["goal_diff"] += away_score - home_score
        else:
            standing[home_team]["points"] += 1
            standing[away_team]["points"] += 1

    # Sort teams by points and goal differences
    standing_table = sorted(
        standing.items(),
        key=lambda x: (x[1]["points"], x[1]["goal_diff"]),
        reverse=True,
    )

    return standing_table
