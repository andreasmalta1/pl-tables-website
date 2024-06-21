import pandas as pd
import os
from requests import get
from os import getenv
from collections import defaultdict
from bs4 import BeautifulSoup
from datetime import date
from dotenv import load_dotenv

load_dotenv()

from models import Visit


def generate_table(start_date, end_date, season):
    """
    Returns the table for the chose start and end dates.

        Parameters:
            start_date (str): A date in string format
            end_date (str): Another date in string format

        Returns:
            standings_table (dict): A dictionary of teams and their league info
    """

    # Get teams data including id and logo id
    team_data = get_teams_info()

    if start_date and end_date:
        date_from = start_date.split("-")
        date_to = end_date.split("-")
        matches = Match.query.filter(
            db.and_(
                Match.date
                >= date(
                    year=int(date_from[0]),
                    month=int(date_from[1]),
                    day=int(date_from[2]),
                ),
                Match.date
                <= date(
                    year=int(date_to[0]), month=int(date_to[1]), day=int(date_to[2])
                ),
            )
        ).all()

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

    if season:
        matches = Match.query.filter_by(season=season).all()
        if not matches:
            teams = CurrentTeams.query.order_by(CurrentTeams.team_name).all()
            for team in teams:
                standings[team.team_name]["played"] = 0

            # Update data with team id and logo
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

            # Add ranking
            rank = 1
            for team in standings_table:
                team[1]["rk"] = rank
                rank += 1

            return standings_table

    if not start_date and not end_date and not season:
        matches = Match.query.all()

    # Go though matches and save data
    for match in matches:
        home_team = match.home_team_name
        home_score = match.home_score
        away_team = match.away_team_name
        away_score = match.away_score

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

    if len(standings) < 20 and season:
        teams = CurrentTeams.query.order_by(CurrentTeams.team_name).all()
        for team in teams:
            if not standings.get(team.team_name):
                standings[team.team_name]["team_id"]: None
                standings[team.team_name]["url"] = None
                standings[team.team_name]["played"] = 0
                standings[team.team_name]["win"] = 0
                standings[team.team_name]["draw"] = 0
                standings[team.team_name]["loss"] = 0
                standings[team.team_name]["goals_for"] = 0
                standings[team.team_name]["goals_against"] = 0
                standings[team.team_name]["gd"] = 0
                standings[team.team_name]["points"] = 0

    # Update data with team id and logo
    for team in standings:
        if not standings[team]["url"]:
            team_id = team_data.get(team)["logo_id"]
            if team:
                standings[team]["url"] = f"{getenv('CREST_URL')}{team_id}.png"

    # Sort teams by points and goal differences
    standings_table = sorted(
        standings.items(),
        key=lambda x: (x[1]["points"], x[1]["gd"], x[1]["goals_for"]),
        reverse=True,
    )

    # Add ranking
    rank = 1
    for team in standings_table:
        team[1]["rk"] = rank
        rank += 1

    return standings_table


def get_pl_matches():
    """
    A utility to scrape PL matches information
    """
    data = {
        "match_no": [],
        "season": [],
        "home_team_name": [],
        "away_team_name": [],
        "home_score": [],
        "away_score": [],
        "date": [],
    }

    match_no = 1
    num_rounds = 42
    for year in range(1992, 2024):
        print(year)
        if year > 1994:
            num_rounds = 38
        for round in range(1, num_rounds + 1):
            link = f"{getenv('PL_MATCHES_URL')}{year}-{year+1}-spieltag/{round}"
            source = get(link).text
            page = BeautifulSoup(source, "lxml")
            table = page.find("table", class_="standard_tabelle")
            rows = table.find_all("tr")

            date = None

            for row in rows:
                cells = row.find_all("td")
                if cells[0].get_text():
                    date = cells[0].get_text()

                home_team_name = cells[2].get_text().strip()
                away_team_name = cells[4].get_text().strip()
                score = cells[-2].get_text().strip().split()[0].split(":")

                data["match_no"].append(match_no)
                data["season"].append(f"{year}/{year+1}")
                data["home_team_name"].append(home_team_name)
                data["away_team_name"].append(away_team_name)
                data["home_score"].append(score[0])
                data["away_score"].append(score[1])
                data["date"].append(date)

                match_no += 1

    df = pd.DataFrame(data=data)
    csv_file_path = os.path.join("..", "csvs", "pl_results.csv")
    df.to_csv(csv_file_path)


def update_visits(ip_address, page_name):
    """Add a user's visit to the Visit model"""
    visit = Visit()
    visit.update_visits(user_ip=ip_address, pagename=page_name)
