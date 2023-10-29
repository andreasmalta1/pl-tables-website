import pandas as pd
import json


def get_current_season_results():
    with open("last_result.json", "r") as json_file:
        data = json.load(json_file)
        last_row = data["last_row"]

    url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
    html = pd.read_html(url, header=0)
    df = (
        html[0][["Date", "Home", "Score", "Away"]]
        .dropna()
        .reset_index()
        .iloc[last_row + 1 :, :]
    )
    print(df)


get_current_season_results()
