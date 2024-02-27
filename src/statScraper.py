import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrapeStats(urlId, colHeads, outputFileName):
    baseUrl = f"https://www.ncaa.com/stats/basketball-men/d1/current/team/{urlId}"

    teamData = []
    pageNum = 1

    while True:
        url = baseUrl if pageNum == 1 else f"{baseUrl}/p{pageNum}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "block-stats__stats-table"})

        if not table:
            break

        for row in table.find_all("tr")[1:]:
            rowData = {}
            for colName, colIndex in colHeads.items():
                rowData[colName] = row.find_all("td")[colIndex].text

            teamData.append(rowData)

        pageNum += 1

    df = pd.DataFrame(teamData)
    df.to_csv(f"../data/raw/CurrYearData/{outputFileName}.csv", index=False)
