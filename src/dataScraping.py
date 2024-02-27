import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup


def teamRankingsScraper(endpoint, stat, category):
    baseUrl = "https://www.teamrankings.com/ncaa-basketball/stat"
    dates = [
        "2014-04-07",
        "2015-04-06",
        "2016-04-05",
        "2017-04-04",
        "2018-04-03",
        "2019-04-09",
        "2020-03-12",
        "2021-04-06",
        "2022-04-05",
        "2023-04-04",
        "current",
    ]

    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Edge(options=options)

    for date in dates:
        if date == "current":
            url = f"{baseUrl}/{urlEndpoint}"
            fileName = f"CURRENT_{urlEndpoint}"
            filePath = f"../data/raw/CurrYearData/{category}"
        else:
            url = f"{baseUrl}/{urlEndpoint}?date={date}"
            fileName = f"{str(int(date[:4]) - 1)}-{date[2:4]}_{urlEndpoint}"
            filePath = f"../data/raw/HistoricData/{category}"

        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", {"id": "DataTables_Table_0"})
        rows = table.find_all("tr")[1:] if table else []

        data = []
        for row in rows:
            if date == "current":
                data.append(
                    {
                        "team": row.find_all("td")[1].text.strip(),
                        f"{statName}": row.find_all("td")[2].text.strip(),
                        f"{statName}_home": row.find_all("td")[5].text.strip(),
                        f"{statName}_away": row.find_all("td")[6].text.strip(),
                        f"{statName}_last3": row.find_all("td")[3].text.strip(),
                    }
                )
            else:
                data.append(
                    {
                        "team": row.find_all("td")[1].text.strip(),
                        f"{statName}": row.find_all("td")[2].text.strip(),
                        f"{statName}_home": row.find_all("td")[5].text.strip(),
                        f"{statName}_away": row.find_all("td")[6].text.strip(),
                    }
                )

        df = pd.DataFrame(data)
        df.to_csv(f"{filePath}/{fileName}.csv", index=False)

    driver.quit()
