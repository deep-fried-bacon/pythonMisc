import xlrd
import os
import csv
import time

start = time.perf_counter()
path = "C:/Users/localuser/Desktop/Development/Spanky Stuff/"
file_name = "8celllinesfirstrun_Raw-3.xlsx"

temp = file_name.split(".")
csv_dir = path+temp[0] + "_csv/"
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

with xlrd.open_workbook(path+file_name) as wb:
    for sheet in wb.sheets() :
        with open(csv_dir + sheet.name + ".csv", 'w', newline="") as f:
            print(sheet.name)
            c = csv.writer(f)
            for r in range(sheet.nrows):
                #print (sheet.row_values(r))
                c.writerow(sheet.row_values(r))
                
        
    

end = time.perf_counter()
print(end-start)
