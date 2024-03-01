import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrapeTable(statYear, statName, statAbbrev):
    url = f"https://www.teamrankings.com/ncaa-basketball/stat/{statName}?date={statYear}-05-01"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    data = []
    if statYear == "2024":
        columns = [
            "team",
            "year",
            statAbbrev,
            f"{statAbbrev}_last3",
            f"{statAbbrev}_Home",
            f"{statAbbrev}_Away",
        ]
    else:
        columns = ["team", "year", statAbbrev]

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if statYear == "2024":
            rowData = {
                "team": cells[1].text.strip(),
                "year": 2024,
                statAbbrev: cells[2].text.strip(),
                f"{statAbbrev}_last3": cells[3].text.strip(),
                f"{statAbbrev}_Home": cells[5].text.strip(),
                f"{statAbbrev}_Away": cells[6].text.strip(),
            }
        else:
            rowData = {
                "team": cells[1].text.strip(),
                "year": int(statYear),
                statAbbrev: cells[2].text.strip(),
            }
        data.append(rowData)

    return pd.DataFrame(data, columns=columns)


def compileTables(statYear, statNames, statAbbrevs):
    dfs = []
    for name, abbrev in zip(statNames, statAbbrevs):
        df = scrapeTable(statYear, name, abbrev)
        df.sort_values(by="team", inplace=True)
        if dfs:
            df = df.drop(columns=["year"])
        dfs.append(df)

    combinedDf = dfs[0]
    for df in dfs[1:]:
        combinedDf = combinedDf.merge(df, on="team")

    return combinedDf
