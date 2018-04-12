import os
import mia
import sys
import copy

class plate :
    """ plate """
    def __init__(self, path, pmap_name=None) :
        """ plate constructor """
        self.except_count = 0
        
        self.path = path
        self.name = os.path.basename(self.path[:-1])
        #self.out_path = self.make_out_path()

                
        # pmap --> plate map
        self.pmap_path = self.get_pmap_path(pmap_name) 
        
        # condit_dict --> condition dictionary
        # condit_dict--> keys = condits : values = well_names
        self.condit_dict = self.create_condit_dict()
        #self.conditions = self.create_conditions()
        
        #self.all_condit_cols = self.get_all_condit_cols()
        #self.print_to_csv()
        
        
    def make_out_path(self) :
        out_path = self.path + self.name + "_conditions.csv"
        return out_path
        
    def print_to_csv(self) :
        rows = mia.rotate(self.all_condit_cols)
        mia.arr_to_csv(rows,self.out_path,mode="w")
        
    def get_all_condit_cols(self) :
        all_condit_cols = []
        for condit in self.conditions :
            temp = [condit.name]
            temp.extend(condit.avg_col)
            all_condit_cols.append(temp)
        return all_condit_cols
            

        
    def get_pmap_path(self, pmap_name) :
        """ takes name of plate_map and makes full length path """
        if pmap_name == None :
            return self.path + self.name + "_plate-map.csv"
        else : return self.path + pmap_name
    
    # requires self.pmap_path to already be instantiated
    # takes pmap_path, opens it and turns it into condit_dict
    def create_condit_dict(self) :
        """takes pmap_path, opens it and turns it into condit_dict (conditions dict)"""
            # open plate map and get headings
        pmap_rows = mia.csv_to_arr(self.pmap_path)
        col_headings = pmap_rows[0][1:]
        del pmap_rows[0]
        pmap_cols = mia.rotate(pmap_rows)
        row_headings = pmap_cols[0]
        
        del pmap_cols[0]
        pmap_cols = delete_empty_arrs(pmap_cols, col_headings, blank='')
        pmap_rows = mia.rotate(pmap_cols)
        pmap_rows = delete_empty_arrs(pmap_rows, row_headings, blank='')
        pmap_cols = mia.rotate(pmap_rows)
        
            # make dict keys
        condit_dict = {}
        for row in pmap_rows :
            for item in row :
                condit_dict[item] = []
               
        
            # put in values
        for r in range(len(pmap_rows)) :
            for c in range(len(pmap_rows[r])) :
                well_name = (row_headings[r] 
                                + double_digits(col_headings[c]))
                condit_dict[pmap_rows[r][c]].append(well_name)
        
        self.pmap_rows = pmap_rows
        self.condit_index = sorted(condit_dict.keys())
     
        
        return condit_dict

    
    def create_conditions(self) :
        """ 
            takes each condition from the 
            condit_index (from condit_dict.keys())
            and makes a new condition instance with list of
            well_names from condit_dict.vallues()
        """
        conditions = []
        for condit in self.condit_index :
            if condit != '' :
                conditions.append(condition(condit, self,
                                    self.condit_dict[condit]))
                
            
            
        return conditions
    
    
        
class condition :
    """ condition """
    def __init__(self, name, plate, well_names) : 
        """ condition constructor """
        self.name = name
        self.plate = plate
        self.well_names = well_names
        self.wells = self.create_wells()
        
        self.all_dist_cols = self.get_all_dist_cols()
        self.avg_col = self.make_avg_col()
        if "IKK + Idel" in self.name :
            self.print_to_csv()

    
    def get_all_dist_cols(self) :
        
        #all_dist_cols = {}
        #for well in wells :
            #for cell in well.cells :
                #all_dist_cols[
                
                
        all_dist_cols = []
        for well in self.wells :
            for cell in well.cells :
                all_dist_cols.append(cell.dist_col)
        
        return all_dist_cols
        
    
    def make_avg_col(self) :
        #mia.print_types(self.all_dist_cols)
        dist_rows = mia.rotate(self.all_dist_cols) 
        
        avg_col = []
        for row in dist_rows :
            #try :
            avg_col.append(mia.calc_avg(row))
            #except TypeError :
                #print("condition = {0}, row = {1}".format(self.name,row))
                #if self.plate.except_count == 0 : 
                    #print(self.name)
                    #mia.print_arr(dist_rows)
                    #self.plate.except_count+=1
        
        return avg_col
        
    def create_wells(self) :
        wells = []
        for well_name in self.well_names :
            wells.append(well(self,well_name))
            
            
        return wells
        
        
    def make_out_path(self) :
        #temp = self.name.replace(".","-")
        #temp2 = 
        out_path = self.plate.path + self.plate.name + "_" + self.name + ".csv"
        #print(out_path)
        return out_path
        
    def print_to_csv(self) :
        self.out_path = self.make_out_path()
        rows = mia.rotate(self.all_dist_cols)
        mia.arr_to_csv(rows,self.out_path,mode="w")


class well :
    """ well """

    def __init__(self, condition, name) :
        """ well constructor """
        self.condition = condition
        self.plate = self.condition.plate
        
        self.name = name
        self.path = (self.plate.path + self.plate.name 
                    + "_" + self.name + ".csv")
        self.rows = mia.csv_to_arr(self.path)
        
       
        for i, item in enumerate(self.rows[0]):
            self.rows[0][i] = spec_encode(item)
            
     
        self.col_headings = self.rows[0]
        del self.rows[0]
        self.cols = mia.rotate(self.rows)
        
        
        self.cell_col_h = "Track nÂ°"

        self.cell_col_h = spec_encode(self.cell_col_h)
   
        self.make_cells()
            
        
    def make_cells(self) :
        """ 
            in progress, makes cells 
            need to refactor all of well class
        """
        
        try :
            col_del_num = self.col_headings.index(" ")
        except ValueError :         #use 'in' to do this instead
            col_del_num = -1
        if col_del_num > -1 :
            del self.cols[col_del_num]
            del self.col_headings[col_del_num]
        
        cell_col_num = self.col_headings.index(self.cell_col_h)
        self.row_headings = self.cols[cell_col_num]
        del self.cols[cell_col_num]
        del self.col_headings[cell_col_num]
        
        
        self.rows = mia.rotate(self.cols) 
        cell_ids = sorted(set(self.row_headings))
        
        cell_dict = {}
        for cell_id in cell_ids :
            cell_dict[cell_id] = []
            
        for i, rh in enumerate(self.row_headings) :
            cell_dict[rh].append(self.rows[i])
        
        self.cells=[]
        
        for id_num, rows in cell_dict.items() :
            self.cells.append(cell(id_num, self.condition, self, rows,copy.copy(self.col_headings)))
           

    
class cell :
    """ cell  """
    def __init__(self, id_num, condition,
                    well, rows, col_headings) :
        """ cell constructor """
       
        self.id_num = id_num
        self.condition = condition
        self.well = well

        self.rows = rows
        
        
        self.col_headings = col_headings
        self.cols = mia.rotate(rows)
        
        x_i = self.col_headings.index("X")
        y_i = self.col_headings.index("Y")
        
        self.x_col = self.cols[x_i]
        self.y_col = self.cols[y_i]
        
        self.dist_col = self.make_dist_col()
        

    def make_dist_col(self) :
        if not len(self.x_col) == len(self.y_col) :
            pass
            raise mia.LengthError("Length of x_col = {0} and length of y_col = {1}".format(len(self.x_col,len(self.y_col))))
        dist_col = []
        for i in range(len(self.x_col)-1) : 
        
            #account for possible None values or empty strings!!!
            test = [self.x_col[i],self.x_col[i+1],self.y_col[i],self.y_col[i+1]]
            for item in test :
                if item is None or item == "" or item == " " :
                    print("uh oh")
                    #raise error here
            
            
            x1 = int(self.x_col[i])
            x2 = int(self.x_col[i+1])
            y1 = int(self.y_col[i])
            y2 = int(self.y_col[i+1])
            dist_col.append(mia.calc_dist((x1,y1),(x2,y2)))
        return dist_col
            
    
    
    
    
def delete_empty_arrs(arr2d, headings, blank=None) :
    j = 0
    for i in range(len(arr2d)) :
        delete = True
        #print(str(i-j) + " " +str(len(arr2d)))

        for item in arr2d[i-j] :
            if not item == blank :
                delete = False
                break
        if delete :
            #print("\t" + stri-ji) + " " +str(len(arr2d)))
            del arr2d[i-j]
            del headings[i-j]
            j +=1;
    return arr2d;
    
    
# s assumed to type str representing a whole number 
def double_digits(s) :
    if len(s) == 1 :
        s = "0" + s
    return s

    
def spec_encode(s) :
    for c, char in enumerate(s) :
        try :
           char.encode(sys.stdout.encoding)
        except UnicodeEncodeError :
            temp = (s[0:c] + "*" + s[c+1:])
            s = temp
    return s