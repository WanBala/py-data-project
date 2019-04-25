from openpyxl import load_workbook
from openpyxl import Workbook


def loadExcel(file, **kwargs):
    return load_workbook(file, **kwargs)


def createExcel(**kwargs):
    return Workbook(**kwargs)


def getShape(workbook, **kwargs):
    return (workbook.max_row, workbook.max_column)


def indexToAlpha(numbers):
    if 0 < numbers < 27:
        return chr(numbers + 64)
    else:
        raise ValueError("Argument here must from 65 to 91")


def index(number):
    a = ''
    mod = number
    while(1):
        if(0 < mod < 27):
            return a + indexToAlpha(mod)
        
        else:
            number, mod = divmod(mod, 27)
            a = a + indexToAlpha(number)
            

