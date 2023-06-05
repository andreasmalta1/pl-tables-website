import requests
from bs4 import BeautifulSoup
import pandas as pd

data = {
    "match_no": [],
    "season": [],
    "home_team": [],
    "away_team": [],
    "home_score": [],
    "away_score": [],
    "date": [],
}

match_no = 0
num_rounds = 42
start_year = 1992
for year in range(start_year, 2023):
    print(year)
    if year > 1994:
        num_rounds = 38
    for round in range(1, num_rounds + 1):
        print(round)
        link = f"https://www.worldfootball.net/schedule/eng-premier-league-{year}-{year+1}-spieltag/{round}/"
        source = requests.get(link).text
        page = BeautifulSoup(source, "lxml")
        table = page.find("table", class_="standard_tabelle")
        rows = table.find_all("tr")

        date = None

        for row in rows:
            cells = row.find_all("td")
            if cells[0].get_text():
                date = cells[0].get_text()

            score = cells[-2].get_text().strip().split()[0].split(":")

            data["match_no"].append(match_no)
            data["season"].append(f"{year}/{year+1}")
            data["home_team"].append(cells[2].get_text().strip())
            data["away_team"].append(cells[4].get_text().strip())
            data["home_score"].append(score[0])
            data["away_score"].append(score[1])
            data["date"].append(date)

            match_no += 1


df = pd.DataFrame(data=data)
df.to_csv("pl_results.csv")
