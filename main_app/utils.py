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

        # Create table rows with match details
        for match in matches:
            home_team = match["homeTeam"]["name"]
            home_team_id = match["homeTeam"]["id"]
            home_score = match["score"]["fullTime"]["home"]
            away_team = match["awayTeam"]["name"]
            away_team_id = match["awayTeam"]["id"]
            away_score = match["score"]["fullTime"]["away"]
            table.append(
                [
                    home_team,
                    away_team,
                    home_score,
                    away_score,
                    home_team_id,
                    away_team_id,
                ]
            )

            team_id = match["homeTeam"]["id"]
            url = f"http://api.football-data.org/v4/teams/{team_id}"
            headers = {"X-Auth-Token": API_KEY}
            response = get(url, headers=headers)
            response.raise_for_status()

            data = response.json()

            print(data["crest"])
            return table

        return table

    except exceptions.RequestException as e:
        print("An error occurred:", str(e))
        return None


def generate_standings_table(results_table):
    standing = defaultdict(
        lambda: {
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

    for row in results_table:
        home_team = row[0]
        away_team = row[1]
        home_score = int(row[2])
        away_score = int(row[3])

        # Update played matches count
        standing[home_team]["played"] += 1
        standing[away_team]["played"] += 1

        standing[home_team]["goals_for"] += home_score
        standing[away_team]["goals_for"] += away_score

        standing[home_team]["goals_against"] += away_score
        standing[away_team]["goals_against"] += home_score

        standing[home_team]["gd"] += home_score - away_score
        standing[away_team]["gd"] += away_score - home_score

        # Update points and goal differences based on the result
        if home_score > away_score:
            standing[home_team]["win"] += 1
            standing[away_team]["loss"] += 1
            standing[home_team]["points"] += 3
        elif home_score < away_score:
            standing[home_team]["loss"] += 1
            standing[away_team]["win"] += 1
            standing[away_team]["points"] += 3
        else:
            standing[home_team]["draw"] += 1
            standing[away_team]["draw"] += 1
            standing[home_team]["points"] += 1
            standing[away_team]["points"] += 1

    # Sort teams by points and goal differences
    standing_table = sorted(
        standing.items(),
        key=lambda x: (x[1]["points"], x[1]["gd"]),
        reverse=True,
    )

    return standing_table
