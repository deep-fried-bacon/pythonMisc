#
# save dir of single spreadsheet excel workbooks as csv files
#

import os

import xlrd


def xlsdir2csvdir(path) :
    l = os.listdir(path)
    for f in l :
        with xlrd.open_workbook (path + f) as wb :
            sheet = wb.sheets()[0]
            
        break
    
    
    #print(l)



xlspath = "D:/People Files/Lab/Data/Dane 2D/xls/"
csvpath = "D:/People Files/Lab/Data/Dane 2D/csv/"

if not os.path.exists(csvpath):
    os.makedirs(csvpath)

xlsdir2csvdir(xlspath)


