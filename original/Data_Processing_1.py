import sys
sys.path.append(r"C:\Users\YU-TING\Documents\GitHub\py-data-project")
import datawtf
import pandas as pd
import numpy as np
import os
import time
os.chdir(r"C:\Users\YU-TING\Desktop\New folder (2)")
filename = r"C:\Users\YU-TING\Desktop\New folder (2)\河川流量(日)_南區(_2016.12)(已標記).xlsx"
df = datawtf.loadFile(filename)




def howManyLack(lastDate, thisDate):
    lastYear, lastMonth = lastDate
    thisYear, thisMonth = thisDate
    lack = thisMonth + 12 * (thisYear - lastYear) - lastMonth - 1
    if lack >= 0:
        return lack
    else:
        return 0
        #raise Exception("The difference in years must be positive {0} {1}".format(lastDate, thisDate))

def fillInformation(extension, stack, fromDate,year_index):
    fromYear, fromMonth = fromDate
    lackNumber = extension.shape[0]
    for i in range(lackNumber):
        if fromMonth == 12:
            extension.iloc[i, year_index] = fromYear = fromYear + 1
            extension.iloc[i, year_index + 1] = fromMonth = 1
        else:
            extension.iloc[i, year_index] = fromYear
            extension.iloc[i, year_index + 1] = fromMonth = fromMonth + 1
    return pd.concat([stack, extension])


def makeUpLacks(df, stack):
    rows, _ = df.shape
    year_index = datawtf.findYearIndex(df)
    month_index = year_index + 1
    index = df.columns[month_index +1 :]
    lack = pd.DataFrame(np.array([-999998] * len(index)), index = index)
    last_st = 0
    for i in range(0, rows):
        if last_st != df.iloc[i,:][year_index-1].rstrip():
            last_st = df.iloc[i, :][year_index-1].rstrip()
            year = df.iloc[i,:][year_index]
            month = df.iloc[i,:][month_index]
            lackNumber = howManyLack((year-1,12),(year, month))
            if lackNumber:
                lacks = pd.concat((df.iloc[i,:month_index + 1], lack))
                extension = datawtf.rowExtension(lacks, lackNumber)
                stack = fillInformation(extension, stack, (year-1, 12), year_index)
        else:
            lastDate = (df.iloc[i-1,year_index], df.iloc[i-1, month_index])
            thisDate = (df.iloc[i, year_index], df.iloc[i, month_index])
            lackNumber = howManyLack(lastDate, thisDate)
            if lackNumber:
                lacks = pd.concat((df.iloc[i,:month_index + 1], lack))
                extension = datawtf.rowExtension(lacks, lackNumber)
                stack = fillInformation(extension, stack, lastDate, year_index)
    return stack
a = time.time()
stack = datawtf.emptyDF()
stack = makeUpLacks(df, stack)
newDF = pd.concat([df, stack])
newDF = newDF.sort_values(['st_no','YY','MM'], ascending=[True,True,True])
datawtf.pdToExcel(newDF, "Try.xlsx")
print("It takes {0} seconds ".format(time.time() - a))


