import pandas as pd
import requests
from bs4 import BeautifulSoup


def endRegSeasonScrape(statName, statAbbrev):
    url = (
        f"https://www.teamrankings.com/ncaa-basketball/stat/{statName}?date=2024-03-11"
    )
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    data = []

    columns = ["team", "year", statAbbrev]

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        rowData = {
            "team": cells[1].text.strip(),
            "year": 2024,
            statAbbrev: cells[2].text.strip(),
        }
        data.append(rowData)

    return pd.DataFrame(data, columns=columns)


def endRegSeasonUpdate(stats):
    dfs = []
    for stat in stats:
        name = stat["name"]
        abbrev = stat["abbrev"]
        df = endRegSeasonScrape(name, abbrev)
        df.sort_values(by="team", inplace=True)
        if dfs:
            df = df.drop(columns=["year"])
        dfs.append(df)

    combinedDf = dfs[0]
    for df in dfs[1:]:
        combinedDf = combinedDf.merge(df, on="team")

    return combinedDf
