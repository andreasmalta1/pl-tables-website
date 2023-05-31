import requests


# Function to generate the table of Premier League results
def generate_results_table(start_date, end_date):
    api_key = "ba45b870269c4028994f6cbd4f516b3f"  # Replace with your own API key
    api_url = f"https://api.football-data.org/v2/competitions/PL/matches?dateFrom={start_date}&dateTo={end_date}"

    headers = {"X-Auth-Token": api_key}

    try:
        response = requests.get(api_url, headers=headers)
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
            score = f"{match['score']['fullTime']['homeTeam']} - {match['score']['fullTime']['awayTeam']}"
            table.append([home_team, away_team, score])

        return table

    except requests.exceptions.RequestException as e:
        print("An error occurred:", str(e))
        return None
