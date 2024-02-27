# import requests
# from bs4 import BeautifulSoup
# import pandas as pd


# def scrapeStats(urlId, columnHeaders, outputFileName):
#     baseUrl = f"https://www.ncaa.com/stats/basketball-men/d1/current/team/{urlId}"

#     teamData = []
#     pageNum = 1

#     while True:
#         url = baseUrl if pageNum == 1 else f"{baseUrl}/p{pageNum}"
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, "html.parser")
#         table = soup.find("table", {"class": "block-stats__stats-table"})

#         if not table:
#             break

#         for row in table.find_all("tr")[1:]:
#             rowData = {}
#             for colName, colIndex in columnHeaders.items():
#                 rowData[colName] = row.find_all("td")[colIndex].text

#             teamData.append(rowData)

#         pageNum += 1

#     df = pd.DataFrame(teamData)
#     df.to_csv(outputFileName, index=False)


# import requests
# from bs4 import BeautifulSoup
# import pandas as pd


# def scrapeStats(urlEndpoint, queryDate, columnHeaders, fileName):
#     baseUrl = "https://www.teamrankings.com/ncaa-basketball/stat"

#     # url = baseUrl if queryDate = "" else f"{baseUrl}/{urlEndpoint}?date={queryDate}"
#     if queryDate != "current":
#         url = f"{baseUrl}/{urlEndpoint}?date={queryDate}"
#     else:
#         url = baseUrl

#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     # table = soup.find("table", {"class": "tr-table datatable scrollable"})
#     table = soup.find("table", {"class": "tr-table"})
#     # table = soup.find("table", {"id": "DataTables_Table_0"})

#     data = []

#     for row in table.find_all("tr")[1:]:
#         rowData = {}
#         for colName, colIndex in columnHeaders.items():
#             rowData[colName] = row.find_all("td")[colIndex].text

#         data.append(rowData)

#     df = pd.DataFrame(data).to_csv(fileName, index=False)
#     # df.to_csv(fileName, index=False)


# urlEndpoint = "games-played"
# queryDate = "current"
# columnHeaders = {"Team": 1, "Games": 2, "Last3": 3, "Last1": 4, "Home": 5, "Away": 6}
# fileName = "testScrape_2023_games_played.csv"

# scrapeStats(urlEndpoint, queryDate, columnHeaders, fileName)

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time


def statScraper(urlEndpoint, queryDate, statCat):
    baseUrl = "https://www.teamrankings.com/ncaa-basketball/stat"
    service = Service(executable_path="msedgedriver.exe")
    driver = webdriver.Edge(service=service)

    for date in queryDate:
        if date != "current":
            url = f"{baseUrl}/{urlEndpoint}?date={date}"
            fileName = f"{str(int(date[:4]) - 1)}-{date[2:4]}_{urlEndpoint}.csv"
        else:
            url = f"{baseUrl}/{urlEndpoint}"
            fileName = f"CURRENT_{urlEndpoint}.csv"

        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", {"id": "DataTables_Table_0"})
        rows = table.find_all("tr")[1:] if table else []

        data = []
        for row in rows:
            data.append(
                {
                    "team": row.find_all("td")[1].text.strip(),
                    f"{statCat}_season": row.find_all("td")[2].text.strip(),
                    f"{statCat}_last3": row.find_all("td")[3].text.strip(),
                    f"{statCat}_last1": row.find_all("td")[4].text.strip(),
                    f"{statCat}_home": row.find_all("td")[5].text.strip(),
                    f"{statCat}_away": row.find_all("td")[6].text.strip(),
                    f"{statCat}_lastYr": row.find_all("td")[7].text.strip(),
                }
            )

        df = pd.DataFrame(data)

        if date != "current":
            df.to_csv(f"./data/raw/HistoricData/{fileName}", index=False)
        else:
            df.to_csv(f"./data/raw/CurrYearData/{fileName}", index=False)

    driver.quit()


statScraper(
    urlEndpoint="steals-perpossession",
    queryDate=["2020-03-12", "2021-04-06", "2022-04-05", "2023-04-04", "current"],
    statCat="stlsPerPoss",
)
