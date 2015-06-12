from models import *
from sqlalchemy.exc import SQLAlchemyError
import xl
import numpy

class ORM2Excel():
    """class to view, manipulate and update data from an ORM"""

    xlColumnNames = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                     'AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU',
                     'AV','AW','AX','AY','AZ','BA','BB','BC','BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM','BN','BO','BP',
                     'BQ','BR','BS','BT','BU','BV','BW','BX','BY','BZ','CA','CB','CC','CD','CE','CF','CG','CH','CI','CJ','CK',
                     'CL','CM','CN','CO','CP','CQ','CR','CS','CT','CU','CV','CW','CX','CY','CZ','DA','DB','DC','DD','DE','DF',
                     'DG','DH','DI','DJ','DK','DL','DM','DN','DO','DP','DQ','DR','DS','DT','DU','DV','DW','DX','DY','DZ','EA',
                     'EB','EC','ED','EE','EF','EG','EH','EI','EJ','EK','EL','EM','EN','EO','EP','EQ','ER','ES','ET','EU','EV',
                     'EW','EX','EY','EZ','EA','EB','EC','ED','EE','EF','EG','EH','EI','EJ','EK','EL','EM','EN','EO','EP','EQ',
                     'ER','ES','ET','EU','EV','EW','EX','EY','EZ'];
    def __init__(self):
        self.session = Session();

    def getSelectionExcel(self,workbook_I=None):
        ###TODO
        # read back data from the active selection of excel
        # i.e. a column of data
        if workbook_I:
            #data_stage01_isotopomer_normalized.xlsx
            wb = xl.Workbook(workbook_I).get();
        data_O = [];

        return data_O;

    def calcAveAndCV(self,data_I):
        # calculate the average and CV of a data selection
        ave_O = numpy.mean(numpy.array(data_I));
        var_O = numpy.var(numpy.array(data_I));
        if (ave_O <= 0): cv_O = 0;
        else: cv_O = sqrt(cv_O)/ave_O*100; 
        print('average\tCV')
        print(ave_O,cv_O)
        return ave_O, cv_O;

    def viewQueryExcel(self,dataHeader,dataList):
        # view the data in excel
        wb = xl.Workbook();
        xlColumns = [];
        for j,dh in enumerate(dataHeader):
            dataColumn = [];
            for row in dataList:
                dataColumn.append(row[dh]);
            xlColumns.append(wb.view(dataColumn,dh));
            #xlHeader = xlColumnNames[j] + str(1)+':'+xlColumnNames[j]+str(1);
            #xlRange = xlColumnNames[j]+str(2)+':'+xlColumnNames[j]+str(len(dataList));
            #wb.get(xlHeader).set(dh)
            #wb.get(xlRange).set(dataColumn)
        return xlColumns;

    def getActiveExcel(self,dataHeader,xlColumns):
        # read data back from active view of excel
        dataColumn = [];
        for j,dh in enumerate(dataHeader):
            dataColumn.append(xlColumns[j].get());
        dataListListUpdated = [];
        for i in range(len(dataColumn[0])):
            dataRow = [];
            for j,dc in enumerate(dataColumn):
                dataRow.append(dc[i]);
            dataListListUpdated.append(dataRow);
        dataListUpdated = [];
        for j,dh in enumerate(dataHeader):
            dataListUpdated.append(dict(list(zip(dataHeader, dataListListUpdated[j])))) #dict(zip(keys, values)
        return dataListUpdated;

    def query_table(self,table_I,experiment_id_I=None):
        # query sql table and store the results in a list of dictionaries
        try:
            if experiment_id_I:
                results = self.session.query(table_I).filter(
                        table_I.experiment_id.like(experiment_id_I)).all();
            else:
                results = self.session.query(table_I).all();

        except SQLAlchemyError as e:
            print(e);
        dataHeader = [col for col in list(results[0].__table__.columns.keys())];
        dataList = [];
        for data in results:
            dataList.append(dict((col, getattr(data, col)) for col in list(data.__table__.columns.keys())));
        return dataHeader,dataList;

    def update_data_stage01_isotopomer_normalized(self,dataListUpdated_I):
        # update the data_stage01_isotopomer_normalized
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage01_isotopomer_normalized).filter(
                        data_stage01_isotopomer_normalized.id == d['id']).update(		
                        {'intensity':d['intensity'],
                        'intensity_units':d['intensity_units'],
                        'intensity_corrected':d['intensity_corrected'],
                        'intensity_corrected_units':d['intensity_corrected_units'],
                        'intensity_normalized':d['intensity_normalized'],
                        'intensity_normalized_units':d['intensity_normalized_units'],
                        'used_':d['used_'],
                        'comment_':d['comment_']},
                        synchronize_session=False);
                if data_update == 0:
                    print('row not found.')
                    print(d)
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def update_data_stage01_isotopomer_peakSpectrum(self,dataListUpdated_I):
        # update the data_stage01_isotopomer_peakSpectrum
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage01_isotopomer_peakSpectrum).filter(
                        data_stage01_isotopomer_peakSpectrum.id == d['id']).update(
                        #data_stage01_isotopomer_peakSpectrum.experiment_id.like(d['experiment_id']),
                        #data_stage01_isotopomer_peakSpectrum.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                        #data_stage01_isotopomer_peakSpectrum.time_point.like(d['time_point']),
                        #data_stage01_isotopomer_peakSpectrum.sample_type.like(d['sample_type']),
                        #data_stage01_isotopomer_peakSpectrum.replicate_number == d['replicate_number'],
                        #data_stage01_isotopomer_peakSpectrum.met_id.like(d['met_id']),
                        #data_stage01_isotopomer_peakSpectrum.precursor_formula.like(d['precursor_formula']),
                        #data_stage01_isotopomer_peakSpectrum.precursor_mass == d['precursor_mass'],
                        #data_stage01_isotopomer_peakSpectrum.product_formula.like(d['product_formula']),
                        #data_stage01_isotopomer_peakSpectrum.product_mass == d['product_mass']).update(		
                        {'intensity':d['intensity'],
                        'intensity_units':d['intensity_units'],
                        'intensity_corrected':d['intensity_corrected'],
                        'intensity_corrected_units':d['intensity_corrected_units'],
                        'intensity_normalized':d['intensity_normalized'],
                        'intensity_normalized_units':d['intensity_normalized_units'],
                        'scan_type':d['scan_type'],
                        'used_':d['used_'],
                        'comment_':d['comment_']},
                        synchronize_session=False);
                if data_update == 0:
                    print('row not found.')
                    print(d)
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def execute_ORM2Excel_data_stage01_isotopomer_normalized(self,experiment_id_I):
        # execute Excel session with data_stage01_isotopomer_normalized

        # query the data
        dataHeader,dataList = self.query_table(data_stage01_isotopomer_normalized,experiment_id_I);

        # view the data
        xlColumns = self.viewQueryExcel(dataHeader,dataList)

        # manipulate the data...
        getInput = True;
        while getInput:
            cmd = input('1: end session, do not update\n2: end session, update\n3: continue session, update\nEnter a command: ')
            if cmd == '1':
                getInput = False;
            elif cmd == '2':
                getInput = False;
                # read back the data
                dataListUpdated = self.getActiveExcel(dataHeader,xlColumns);
                # update the database
                self.update_data_stage01_isotopomer_normalized(dataListUpdated)
            elif cmd == '3':
                getInput = True;
                # read back the data
                dataListUpdated = self.getActiveExcel(dataHeader,xlColumns);
                # update the database
                self.update_data_stage01_isotopomer_normalized(dataListUpdated)
            else:
                print(('Error: Command ' + cmd + ' is not recognized'));
                getInput = True;

    def execute_ORM2Excel_data_stage01_isotopomer_peakSpectrum(self,experiment_id_I):
        # execute Excel session with data_stage01_isotopomer_peakSpectrum

        # query the data
        dataHeader,dataList = self.query_table(data_stage01_isotopomer_peakSpectrum,experiment_id_I);

        # view the data
        xlColumns = self.viewQueryExcel(dataHeader,dataList)

        # manipulate the data...
        getInput = True;
        while getInput:
            cmd = input('1: end session, do not update\n2: end session, update\n3: continue session, update\nEnter a command: ')
            if cmd == '1':
                getInput = False;
            elif cmd == '2':
                getInput = False;
                # read back the data
                try:
                    dataListUpdated = self.getActiveExcel(dataHeader,xlColumns);
                except Exception:
                    print(e)
                    print("Changes not saved, retry command");
                    getInput = True;
                    continue;
                # update the database
                self.update_data_stage01_isotopomer_peakSpectrum(dataListUpdated)
            elif cmd == '3':
                getInput = True;
                # read back the data
                try:
                    dataListUpdated = self.getActiveExcel(dataHeader,xlColumns);
                except Exception as e:
                    print(e)
                    print("Changes not saved, retry command");
                    getInput = True;
                    continue;
                # update the database
                self.update_data_stage01_isotopomer_peakSpectrum(dataListUpdated)
            else:
                print(('Error: Command ' + cmd + ' is not recognized'));
                getInput = True;

    def execute_ORM2Excel_ms_components(self):
        ###WARNING: Method is broken
        ###ms_components contains array data types that are not imported correctly by pyvot
        # execute Excel session with ms_components

        # query the data
        dataHeader,dataList = self.query_table(MS_components);

        # view the data
        xlColumns = self.viewQueryExcel(dataHeader,dataList)

        # manipulate the data...
        getInput = True;
        while getInput:
            cmd = input('1: end session, do not update\n2: end session, update\n3: continue session, update\nEnter a command: ')
            if cmd == '1':
                getInput = False;
            #elif cmd == '2':
            #    getInput = False;
            #    # read back the data
            #    try:
            #        dataListUpdated = self.getActiveExcel(dataHeader,xlColumns);
            #    except StandardError:
            #        print e
            #        print "Changes not saved, retry command";
            #        getInput = True;
            #        continue;
            #    # update the database
            #    #self.update_data_stage01_isotopomer_peakSpectrum(dataListUpdated)
            #elif cmd == '3':
            #    getInput = True;
            #    # read back the data
            #    try:
            #        dataListUpdated = self.getActiveExcel(dataHeader,xlColumns);
            #    except StandardError as e:
            #        print e
            #        print "Changes not saved, retry command";
            #        getInput = True;
            #        continue;
            #    # update the database
            #    #self.update_data_stage01_isotopomer_peakSpectrum(dataListUpdated)
            else:
                print(('Error: Command ' + cmd + ' is not recognized'));
                getInput = True;

def __main__():
    from resources.pyvot import ORM2Excel

    com = ORM2Excel();
    com.execute_ORM2Excel_data_stage01_isotopomer_normalized('WTEColi12C01');
    com.execute_ORM2Excel_data_stage01_isotopomer_peakSpectrum('WTEColi12C01');
