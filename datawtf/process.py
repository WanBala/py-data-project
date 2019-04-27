import basics
import calendar
import pandas as pd
import numpy as np


def tranStraight(filename):
    """This function is customized
    """
    df = basics.loadFile(filename)
    yearIndex = basics.findYearIndex(df)
    monthIndex = yearIndex + 1

    rows, _ = df.shape
    df_empty = basics.emptyDF()
    cache = basics.monthDays()

    for i in range(rows):
        days = calendar.monthrange(df.iloc[i, yearIndex],
                                   df.iloc[i, monthIndex])[1]
        content = df.iloc[i, :monthIndex + 1]
        copy = basics.rowExtension(content, days)
        a = pd.concat([copy, cache[days]], axis=1)
        df_empty = pd.concat([df_empty, a], ignore_index=True)

    basics.pdToExcel(df_empty, filename)
