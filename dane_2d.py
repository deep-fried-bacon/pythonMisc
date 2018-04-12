#
# save dir of single spreadsheet excel workbooks as csv files
#

import os

import xlrd

from plate_well_cell import plate
from amelia_utils import xlrd


def dane_2d(path) :

    l = os.listdir(path)
    for f in l :
        #print(f[-20:])
        
        temp = f.split('-')[-1]
        sheet_name = temp.split('_')[0]
        rows = xlrd.xls2mat(path + f)
        
        
        
        
        #sheet = None
        # with xlrd.open_workbook (path + f) as wb :
            # sheet = wb.sheets()[0]
            # temp = f.split('-')[-1]           
            # sheet_name = temp.split('_')[0]
            # rows = xlrd.xls2mat(
            #print(rows[
            #print(sheet_name)
            # rows = []
            # for i in range(sheet.nrows) :
                # rows.append(sheet.row_values(i))
            #print(rows[1:4])
            #return sheet
        break
    
    
    #print(l)



path = "D:/People Files/Lab/Data/dane-2d/"

myplate = plate(path)
print(myplate.condit_dict)


if not os.path.exists(path+"csv/"):
    os.makedirs(path+"csv/")

sheet = dane_2d(path+"xls/")


