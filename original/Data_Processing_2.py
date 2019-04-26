import pandas as pd
import calendar
import numpy as np
file = r'C:\Users\YU-TING\Desktop\Project\雨量(日)_北區(_2016.12)(已標記)(已加空時間).xlsx'

df = pd.read_excel(file)


def findYearIndex(dataframe, length=25, repeat=3):
    for j in range(repeat):
        a = dataframe.iloc[j*3, 0:25].values
        for i in range(length - 1):
            try:
                if 1850 < a[i] < 2050 and 0 < a[i+1] < 13:
                    return i
            except:
                continue
    return 0


def pdToExcel(dataframe, filename):
    pds = pdSeparation(dataframe)
    with pd.ExcelWriter(filename) as writer:
        for i, p in enumerate(pds):
            p.to_excel(writer, sheet_name="Sheet" + str(i + 1), index=False)


def pdSeparation(dataframe, unit_sheet=1000000):
    rows, _ = dataframe.shape
    a = []
    for i in range(rows // unit_sheet + 1):
        a.append(dataframe.iloc[i*unit_sheet:(i + 1)*unit_sheet, :])
    return a


def monthDays():
    cache = {}
    for i in range(28, 32):
        data = np.array([np.arange(1, i + 1)]).T
        cache[i] = pd.DataFrame(data, columns=['Day'])
    return cache


yearIndex = findYearIndex(df)
monthIndex = yearIndex + 1

row, columns = df.shape
df_empty = pd.DataFrame()
cache = monthDays()

for i in range(60):
    days = calendar.monthrange(df.iloc[i, yearIndex], df.iloc[i, monthIndex])[1]
    content = df.iloc[i, :monthIndex + 1]
    copy = pd.concat([content] * days, axis=1, ignore_index=True).T
    a = pd.concat([copy, cache[days]], axis=1)
    df_empty = pd.concat([df_empty, a], ignore_index=True)

pdToExcel(df_empty, r"C:\Users\YU-TING\Desktop\ChatbotMidori2\hello.xlsx")