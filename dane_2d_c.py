#
# save dir of single spreadsheet excel workbooks as csv files
#

import os

import xlrd
import pyexcelerate as xlerate

from plate_well_cell import plate
from amelia_utils import xlrd_utils
import amelia_utils as autils


# [1,1],[10,50]
def num2xi(num) :
    xi = autils.num2alpha(num[0])
    xi += str(num[1])
    
def nums2xlsIndices(nums) :
    """ 1 based """
    startstr = autils.num2alpha(nums[0][1])
    startstr += str(nums[0][0])

    endstr = autils.num2alpha(nums[1][1])
    endstr += str(nums[1][0])
    
    return [startstr,endstr]

    
def set_xls_range(sheet, rows, nums) :
    xi = nums2xlsIndices(nums)
    sheet.range(xi[0],xi[1]).value = rows
    
def set_xls_range2(sheet, rows, start) :
    rows = autils.make_rec(rows)
    
    c_end = start[0] + len(rows[0])
    r_end = start[1] + len(rows)
    
    xi = nums2xlsIndices([start,[c_end,r_end]])
    sheet.range(xi[0],xi[1]).value = rows

# wrong --> [[c,r][c+width,r+height]]

def set_xls_range3(sheet, rows, empty_row) :
    rows = autils.make_rec(rows)
    
    width = len(rows[0])
    height = len(rows)
    
    c_start = 1
    r_start = empty_row[0] 
    
    empty_row[0] += height

    c_end = c_start + width - 1
    r_end = r_start + height - 1
    
    xi = nums2xlsIndices([[r_start,c_start],[r_end,c_end]])
    sheet.range(xi[0],xi[1]).value = rows


path = "D:/People Files/Lab/Data/dane-2d/"

myplate = plate(path)

xlspath = path+"xls2/"
dirlist = os.listdir(xlspath)
    
well2file_dict = {}
for file_name in dirlist :
    temp = file_name.split('-')[-1]
    well = temp.split('_')[0][:3]
    #print(well)
    #well2file_dict[well] = file_name
    #condit = myplate.condit_dict[well]
    mycondit = None
    for condit, wells in myplate.condit_dict.items() :
        if well in wells :
            mycondit = condit
    if not mycondit == None :
        os.rename(xlspath + file_name, xlspath + mycondit + "_" + well + ".xlsx")
    
    
heading = ['Area','Eccentricity','MajorAxisLength','MinorAxisLength','NumNuc','NucArea','MaxNuc']

if False :
    wb = xlerate.Workbook()
    ws = wb.new_sheet("avgs")
    empty_row = [1]

    headings2 = ['condition'] + heading
    set_xls_range3(ws, [headings2], empty_row)

    for condit in condit_xls :
        rows = xlrd_utils.xls2mat(outpath+condit)
        del rows[0]
        cols = autils.rotate(rows)
        
        avgs = [condit]
        for col in cols :
            #colf = [float(item) for item in col]
            colf = []
            for item in col :
                if not item == "" :
                    colf.append(float(item))
            if len(colf) > 0 :
                avgs.append(autils.calc_avg(colf))
        set_xls_range3(ws,[avgs],empty_row)
        
    wb.save(path + 'butts.xlsx')
            

     
    
