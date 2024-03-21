import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrapeData(statYear, statDay, statName, statAbbrev):
    url = f"https://www.teamrankings.com/ncaa-basketball/stat/{statName}?date={statYear}-{statDay}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    data = []
    columns = ["team", "year", statAbbrev]

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        rowData = {
            "team": cells[1].text.strip(),
            "year": int(statYear),
            statAbbrev: cells[2].text.strip(),
        }
        data.append(rowData)

    return pd.DataFrame(data, columns=columns)


def compileData(statYear, statDay, stats):
    dfs = []
    for stat in stats:
        statName = stat["name"]
        statAbbrev = stat["abbrev"]
        df = scrapeData(statYear, statDay, statName, statAbbrev)
        df.sort_values(by="team", inplace=True)
        if dfs:
            df = df.drop(columns=["year"])
        dfs.append(df)

    combinedDf = dfs[0]
    for df in dfs[1:]:
        combinedDf = combinedDf.merge(df, on="team")

    return combinedDf
