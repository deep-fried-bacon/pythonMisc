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

# def nums2xlsIndices(start,end) :
    # """ 1 based """
    # startstr = autils.num2alpha(start[0])
    # startstr += str(start[1])

    # endstr = autils.num2alpha(end[0])
    # endstr += str(end[1])
    
    #return [startsr,endstr]
    
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
    
    #print(width)
    #print(length)
    
    c_start = 1
    r_start = empty_row[0] 
    
    empty_row[0] += height

    c_end = c_start + width - 1
    r_end = r_start + height - 1
    
    xi = nums2xlsIndices([[r_start,c_start],[r_end,c_end]])
    sheet.range(xi[0],xi[1]).value = rows
    
    
    
# def nums2xlsIndices2(start,end=None,rows=None,) :
# def n2xi (start,end)
# def n2xi (start,rec size)
# def n2xi (start,rows)
# def n2xi (start,cols)



path = "D:/People Files/Lab/Data/dane-2d/"

myplate = plate(path)
#myplate.condit_dict)
print(myplate.condit_dict)

# if not os.path.exists(path+"csv/"):
    # os.makedirs(path+"csv/")


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



#outpath = path + 'output_xls/'


#condit_xls = os.listdir(outpath)


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
            #print(colf)
            if len(colf) > 0 :
                avgs.append(autils.calc_avg(colf))
        set_xls_range3(ws,[avgs],empty_row)
        
    wb.save(path + 'butts.xlsx')
            


# if not os.path.exists(outpath) :
    # os.makedirs(outpath)
    
# for condit, wells in myplate.condit_dict.items() :
    # wb = xlerate.Workbook()
    # all_sheet = wb.new_sheet("All " + condit)
    # allsheet_emptyrow = [1];
    
    # width = len(heading)
    ##[[c,r][c+width,r+height]]
    # set_xls_range(all_sheet, [heading], [[1,1],[1,width]])
    
    # allsheet_emptyrow[0]+=1
    
    # for well in wells :
        # if well in well2file_dict :
            ##well_sheet = wb.new_sheet(well)
            # rows = xlrd_utils.xls2mat(xlspath + well2file_dict[well])
            # del rows[0]
            ##set_xls_range3(well_sheet,rows,[1])
            # well_sheet = wb.new_sheet(well, rows)
            # set_xls_range3(all_sheet,rows, allsheet_emptyrow)
        # else :
            # print('warning: no xls sheet found for well ' + well)
    
    # wb.save(outpath + condit + '.xlsx')
    
     
    
