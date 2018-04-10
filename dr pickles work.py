"""
dr pickles 
and dir pickles gui work
nov 12th
"""
#import xlrd
import os
import csv
import time
import math
import easygui
import pyexcelerate as xlerate



	# make sures that arr2d is a rectangel or makes it one
def csv_to_arr(path) :
    arr2d = []
    with open(path, "r") as csvfile :
        my_reader = csv.reader(csvfile)
        for row in my_reader :
            arr2d.append(row)
    return arr2d

def arr_to_csv_asrows(arr2d,path,mode="a") :
    with open(path, mode) as csvfile :
        my_writer = csv.writer(csvfile)
        [my_writer.writerow(arr) for arr in arr2d]
    return

	# requires a rectangle
def arr_to_csv_ascols(arr2d,path,mode="a") :
    arr2d = make_rec(arr2d)
    with open(path, mode) as csvfile :
        my_writer = csv.writer(csvfile)
        [my_writer.writerow([arr[i] for arr in arr2d]) for i in range(0,len(arr2d[0]))]
    return

def make_rec(arr) :
    longest = len(arr[0])
    gotta_change = False
    for i in range(0,len(arr)) :
        if len(arr[i]) > longest :
            gotta_change = True
            longest = len(arr[i])
    if gotta_change :
        for i, item in enumerate(arr) :
            while(len(item)<longest) :
                item.append("")
    return arr

def rotate(arr1) :
    #arr1 = make_rec(arr1)
    arr2 = []
    for i in range(0,len(arr1[0])) :
        arr2.append([arr[i] for arr  in arr1])
    return arr2

def make_csv_files(file_path, csv_dir) :  
    with xlrd.open_workbook(file_path) as wb:
        for sheet in wb.sheets() :
            with open(csv_dir + sheet.name + ".csv", 'w', newline="") as f:
                print(sheet.name)
                c = csv.writer(f)
                for r in range(sheet.nrows):
                    #print (sheet.row_values(r))
                    c.writerow(sheet.row_values(r))
                    
                    
                    



testing = True


if testing :
    file_path="C:/Users/localuser/Desktop/Code Laboratory/Spanky (Nov)/secondrun8celllines_Raw.xlsx"
else :
    cwd = os.getcwd()
    file_path = easygui.fileopenbox(default=(cwd + "/*.xlsx"))


head_dir = os.path.split(file_path)[0] + "/"
file = os.path.split(file_path)[1]

file_name = file.split(".")[0]

csv_dir = head_dir + file_name + "_csv/"

if not os.path.exists(csv_dir) :
    os.makedirs(csv_dir)
    import xlrd
    make_csv_files(file_path, csv_dir)
 
$start = time.perf_counter()


csv_files = os.listdir(csv_dir)

if csv_files[-1] == "Sheet1.csv" :
    del csv_files[-1]

for i, f in enumerate(csv_files) :
    if not f.endswith(".csv") :
        del csv_files[i]
        i-=1

print_count = 0
print_count2 = 0
all_avg_dists = []
inter_col2 = ["", "cell count", ""]
for i in range(0,107) :
    inter_col2.append(str((i+1)*10) + " - " + str((i+2)*10))
all_avg_dists.append(inter_col2)

inter_col = inter_col2.copy()
del inter_col[0:3]


wb = xlerate.Workbook()

for csv_sheet in csv_files :
    sheet_name = csv_sheet.split(".")[0]
    #print(sheet_name)
    
    rows = csv_to_arr(csv_dir + csv_sheet)
    if len(rows) > 0 :

        cols = rotate(rows)

        headings2 = rows[3]
        all_dists = []

        for i in range(0,len(headings2)) :
            if headings2[i] == 'x(Pixel Position)' and headings2[i+1] == 'y(Pixel Position)':
                cell_id = cols[i][0]
                x_col = i
                y_col = i+1
                x_range = cols[x_col][4:]
                y_range = cols[y_col][4:]

                if len(x_range) == 0 :
                    print(sheet_name + " no x_range")
                    break;

                dists = []
                row_counter = 0
                for j in range(1, len(x_range)) :
                    if not (x_range[j] == "" or x_range[j-1] == "") :
                        row_counter+=1
                        x_dif = float(x_range[j-1]) - float(x_range[j])
                        y_dif = float(y_range[j-1]) - float(y_range[j])
                        dists.append(math.sqrt((x_dif*x_dif)+(y_dif*y_dif)))
                    else : dists.append("")
                if not len(dists) == 112 :
                    print(sheet_name + " len(dists) = " + str(len(dists)))
                    while not len(dists) == 112 :
                        dists.append("")
                all_dists.append(dists)
        
        if len(all_dists) > 0 :
            avg_dists = [sheet_name, len(all_dists), ""]
            for t in range(0, len(all_dists[0])) :
                sum = 0
                count = 0
                for cell in all_dists :
                    if not cell[t] == "": 
                        count+=1
                        sum+=cell[t]
                if not count == 0 :
                    avg_dists.append(sum/count)
                else : avg_dists.append("")

            all_avg_dists.append(avg_dists)
            all_dists.insert(0,inter_col)
            
            data = rotate(all_dists)
            data.insert(0,[sheet_name])
            wb.new_sheet(sheet_name, data=data)




data = rotate(all_avg_dists)
wb.new_sheet("Summary", data=data)
wb.save(file_name + "_cell-velocities.xlsx")


#end = time.perf_counter()
#temp2 = (end-start)/60
#print("time = " + str(end-start) + " sec = " + str(temp2) + " min")







    
