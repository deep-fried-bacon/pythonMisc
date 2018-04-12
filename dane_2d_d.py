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
    well = temp.split('_')[0]
    well2file_dict[well] = file_name
    
msr_types = ['Area','Eccentricity','MajorAxisLength','MinorAxisLength','NumNuc','NucArea','MaxNuc']

outpath = path + 'output_xls/'

condit_xls = os.listdir(outpath)


if True :
    wb = xlerate.Workbook()
    
    i = 0
    m_cols_dict = {}
    for msr_type in msr_types :
        m_cols_dict[msr_type] = []
    
    headings = []
    for condit in condit_xls :
        headings.append(condit[:-5])
       
        rows = xlrd_utils.xls2mat(outpath+condit)
        del rows[0]
        cols = autils.rotate(rows)
        
        for i in range(0,len(msr_types)) :
        
            temp = [item for item in reversed(sorted(cols[i]))]
            m_cols_dict[msr_types[i]].append(temp)            
    
    for msr_type, cols in m_cols_dict.items() :
        rows = [headings] + autils.rotate(cols)
        ws = wb.new_sheet(msr_type,rows)
        
    wb.save(path + 'butts3.xlsx')
            

    
