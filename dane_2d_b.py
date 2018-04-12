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


if not os.path.exists(path+"csv/"):
    os.makedirs(path+"csv/")


xlspath = path+"xls/"
dirlist = os.listdir(xlspath)
    
well2file_dict = {}
for file_name in dirlist :
    temp = file_name.split('-')[-1]
    well = temp.split('_')[0]
    well2file_dict[well] = file_name
    
heading = ['Area','Eccentricity','MajorAxisLength','MinorAxisLength','NumNuc','NucArea','MaxNuc']



outpath = path + 'output_xls/'
if not os.path.exists(outpath) :
    os.makedirs(outpath)
    
for condit, wells in myplate.condit_dict.items() :
    wb = xlerate.Workbook()
    all_sheet = wb.new_sheet("All " + condit)
    allsheet_emptyrow = [1];
    
    width = len(heading)
    set_xls_range(all_sheet, [heading], [[1,1],[1,width]])
    
    allsheet_emptyrow[0]+=1
    
    for well in wells :
        if well in well2file_dict :
            rows = xlrd_utils.xls2mat(xlspath + well2file_dict[well])
            well_sheet = wb.new_sheet(well, rows)
            
            del rows[0]
            set_xls_range3(all_sheet,rows, allsheet_emptyrow)
            
        else :
            print('warning: no xls sheet found for well ' + well)
    
    wb.save(outpath + condit + '.xlsx')
    
     
    
