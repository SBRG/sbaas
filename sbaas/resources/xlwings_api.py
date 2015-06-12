from xlwings import Workbook, Sheet, Range, Chart, ChartType

class xlwings_workbook():
    def __init__(self):
        self.wb = self.new_workbook();

    def new_workbook(self):
        '''create a workbook object'''
        wb = Workbook();
        return wb;

    def add_data2sheet(self,sheet_I='Sheet1',cell_I='A1',data_I=[]):
        '''add data to exel workbook sheet
        INPUT:
            sheet_I: name of sheet
            cell_I: range or starting cell range
            data_I: list of lists where data_I[0]=header and data_I[1:]=data'''
        # output the data to Excel
        Range(sheet_I,cell_I).value = data_I

    def convert_ORMClass2ExcelList(self,ormclass_I):
        '''convert sqlalchemy orm class to excel list'''
        # reformat the data into a list of lists
        excelList = [];
        for i,d in enumerate(ormclass_I):
            if i==0:
                excelList.append(list(d.__repr__dict__().keys()))
            excelList.append(list(d.__repr__dict__().values()))
        return excelList;

    def convert_tableDictList2ExcelList(self,tableDictList_I):
        '''convert database table list of dictionaries (i.e., rows of a database) to excel list'''
        # reformat the data into a list of lists
        excelList = [];
        for i,d in enumerate(tableDictList_I):
            if i==0:
                excelList.append(list(d.keys()))
            excelList.append(list(d.values()))
        return excelList;

    def read_workbook(self,sheet_I='Sheet1',cell_I='A1'):
        '''read data from exel workbook sheet
        INPUT:
            sheet_I: name of sheet
            cell_I: range or starting cell range
        OUTPUT:
            tableDictList_O: a list of dictionaries (i.e., a database table row
                              where keys represent table columns)'''
        # read back in the table after making changes
        header = Range(sheet_I,cell_I).table.value[0]
        table = Range(sheet_I,cell_I).table.value[1:]
        # reformat the data into a list of dictionaries
        tableDictList_O = []
        for row in table:
            row_dict = dict(list(zip(header,row)))
            tableDictList_O.append(row_dict)
        return tableDictList_O;

    def delete_workbook(self):
        '''delete the workbook object'''
        self.wb = None;