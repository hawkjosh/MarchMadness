import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def createDfsDict(dirPath, years, prefix):
    trny = {}
    for year in years:
        filepath = f"{dirPath}/{prefix}{year}.csv"
        trny[year] = pd.read_csv(filepath)

    return trny


def calcStats(df):
    defAvg = np.mean(df["ADE"])
    defStd = np.std(df["ADE"])
    offAvg = np.mean(df["AOE"])
    offStd = np.std(df["AOE"])

    return defAvg, defStd, offAvg, offStd


def calcBounds(df, rnd=None):
    dAvg, dStd, oAvg, oStd = calcStats(df)
    if rnd is not None:
        if rnd == 1:
            xMin = dAvg - (1.75 * dStd)
            xMax = dAvg + (0.5 * dStd)
            yMin = oAvg - (0.75 * oStd)
            yMax = oAvg + (2 * oStd)
        if rnd == 2 or rnd == 3:
            xMin = dAvg - (1.5 * dStd)
            xMax = dAvg + (0.75 * dStd)
            yMin = oAvg - (0.75 * oStd)
            yMax = oAvg + (2 * oStd)
        if rnd == 4:
            xMin = dAvg - dStd
            xMax = dAvg + (0.75 * dStd)
            yMin = oAvg - oStd
            yMax = oAvg + (2 * oStd)
        if rnd == 5:
            xMin = dAvg - dStd
            xMax = dAvg + (0.5 * dStd)
            yMin = oAvg - oStd
            yMax = oAvg + (2 * oStd)
        if rnd == 6:
            xMin = dAvg - dStd
            xMax = dAvg + (0.5 * dStd)
            yMin = oAvg - (0.5 * oStd)
            yMax = oAvg + oStd
    else:
        xMin = dAvg - dStd
        xMax = dAvg + dStd
        yMin = oAvg - oStd
        yMax = oAvg + oStd

    return xMin, xMax, yMin, yMax


def setColorProp(df, rnd):
    if df["finish"].isna().all() or len(df) == 0:
        colors = ["yellow"]
    else:
        colors = ["lime" if x < (8 - rnd) else "tomato" for x in df["finish"]]

    return colors


def renderPlot(df, rnd, rndTitle, ptLabels=False):
    dAvg, _, oAvg, _ = calcStats(df)
    xMinB, xMaxB, yMinB, yMaxB = calcBounds(df)
    xMinSc, xMaxSc, yMinSc, yMaxSc = calcBounds(df, rnd=rnd)

    _, ax = plt.subplots()

    ax.set_facecolor("slategray")
    ax.set_title(f"2014-2023 Offense/Defense Efficiencies ({rndTitle})")
    ax.set_xlabel("Adjusted Defensive Efficiency")
    ax.set_ylabel("Adjusted Offensive Efficiency")

    ax.axvline(x=(xMinSc), color="orangered", linestyle="-.", linewidth=0.625)
    ax.axvline(x=(xMaxSc), color="orangered", linestyle="-.", linewidth=0.625)
    ax.axhline(y=(yMinSc), color="orangered", linestyle="-.", linewidth=0.625)
    ax.axhline(y=(yMaxSc), color="orangered", linestyle="-.", linewidth=0.625)
    ax.fill_between(
        x=[xMinSc, xMaxSc],
        y1=yMinSc,
        y2=yMaxSc,
        color="orangered",
        alpha=0.25,
    )

    ax.axvline(x=dAvg, color="white", linestyle="-", linewidth=0.5)
    ax.axhline(y=oAvg, color="white", linestyle="-", linewidth=0.5)
    ax.fill_between(
        x=[xMinB, xMaxB],
        y1=yMinB,
        y2=yMaxB,
        color="white",
        alpha=0.25,
        linewidth=0,
    )

    ax.scatter(
        df["ADE"],
        df["AOE"],
        c=setColorProp(df, rnd),
        s=20,
    )

    if ptLabels:
        for _, pt in df.iterrows():
            ax.text(
                pt["ADE"] - 0.125,
                pt["AOE"] + 0.25,
                pt["seed"],
                fontsize=8,
                ha="right",
                va="bottom",
                c="white",
            )

        for _, pt in df.iterrows():
            ax.text(
                pt["ADE"] + 0.125,
                pt["AOE"] + 0.25,
                pt["team"],
                fontsize=8,
                ha="left",
                va="bottom",
                c="white",
            )

    return plt.show()
