import numpy as np
import pandas as pd
            

def findYearIndex(dataframe, length=25, repeat=3):
    '''
        Find which cell includes year
    '''
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
    '''
        Writing Datatframe to a Excel file
    '''
    pds = pdSeparation(dataframe)
    with pd.ExcelWriter(filename) as writer:
        for i, p in enumerate(pds):
            p.to_excel(writer, sheet_name="Sheet" + str(i + 1), index=False)


def pdSeparation(dataframe, unit_sheet=1000000):
    '''
        Because an Excel Sheet can only have 1048576 rows, 
        we seperate a dataframe to many pieces
    '''
    rows, _ = dataframe.shape
    a = []
    for i in range(rows // unit_sheet + 1):
        a.append(dataframe.iloc[i*unit_sheet:(i + 1)*unit_sheet, :])
    return a


def pdArange(from_index, to_index, name, straight=0):
    '''
        Create an arange DataFrame
        ex:
            pdArange(1, 10, 'Day', straight=1)
                Day
            0     1
            1     2
            2     3
            3     4
            4     5
            5     6
            6     7
            7     8
            8     9
            9    10
    '''
    if straight == 1:
        data = np.array([np.arange(from_index, to_index)]).T
        return pd.DataFrame(data, columns=[name])
    elif straight == 0:
        data = np.array([np.arange(from_index, to_index)])
        return pd.DataFrame(data, index=[name])


def monthDays():
    '''
        create a dict that includes dataframe 
        including value from 1 to monthdays
    '''
    cache = {}
    for i in range(28, 32):
        cache[i] = pdArange(1, i+1, 'Day', straight=1)
    return cache


def emptyDF(**args):
    '''
        This function is used to create a empty DataFrame.
        Easily to use for concat or stack operation in loops
    '''
    return pd.DataFrame(**args)