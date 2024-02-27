import time
import os
import requests

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup


def ncaaScraper(urlEndpoint, colHeads, fileName):
    baseUrl = f"https://www.ncaa.com/stats/basketball-men/d1/current/team/{urlEndpoint}"

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
    df.to_csv(f"../data/raw/CurrYearData/NCAA/{fileName}.csv", index=False)


def teamRankingsScraper(urlEndpoint, queryDate, statName, category):
    baseUrl = "https://www.teamrankings.com/ncaa-basketball/stat"
    
    options = Options()
    options.add_argument("--headless")
    
    driver = webdriver.Edge(options=options)

    for date in queryDate:
        if date == "current":
            url = f"{baseUrl}/{urlEndpoint}"
            fileName = f"CURRENT_{urlEndpoint}"
            directoryPath = f"../data/raw/CurrYearData/TeamRankings/{category}"
        else:
            url = f"{baseUrl}/{urlEndpoint}?date={date}"
            fileName = f"{str(int(date[:4]) - 1)}-{date[2:4]}_{urlEndpoint}"
            directoryPath = f"../data/raw/HistoricData/TeamRankings/{category}"

        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", {"id": "DataTables_Table_0"})
        rows = table.find_all("tr")[1:] if table else []

        teamData = []
        for row in rows:
            teamData.append(
                {
                    "team": row.find_all("td")[1].text.strip(),
                    f"{statName}": row.find_all("td")[2].text.strip(),
                    f"{statName}_last3": row.find_all("td")[3].text.strip(),
                    f"{statName}_last1": row.find_all("td")[4].text.strip(),
                    f"{statName}_home": row.find_all("td")[5].text.strip(),
                    f"{statName}_away": row.find_all("td")[6].text.strip(),
                    f"{statName}_prevYr": row.find_all("td")[7].text.strip(),
                }
            )

        df = pd.DataFrame(teamData)

        if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)

        filePath = os.path.join(directoryPath, f"{fileName}.csv")
        df.to_csv(filePath, index=False)

    driver.quit()
