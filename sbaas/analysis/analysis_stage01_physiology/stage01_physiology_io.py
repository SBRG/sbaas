from analysis.analysis_base import *
from stage01_physiology_query import stage01_physiology_query

class stage01_physiology_io(base_analysis):

    def __init__(self):
        self.session = Session();
        self.stage01_physiology_query = stage01_physiology_query();
        self.calculate = base_calculate();

    def import_dataStage01PhysiologyData_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage01PhysiologyData(data.data);
        data.clear_data();

    def add_dataStage01PhysiologyData(self, data_I):
        '''add rows of data_stage01_physiology_data'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage01_physiology_data(d['experiment_id'],
                                            d['sample_id'],
                                            #d['sample_name_short'],
                                            #d['time_point'],
                                            #d['sample_date'],
                                            d['met_id'],
                                            d['data_raw'],
                                            d['data_corrected'],
                                            d['data_units'],
                                            d['data_reference'],
                                            d['used_'],
                                            d['notes']); #d['comment_']
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage01PhysiologyData_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01PhysiologyData(data.data);
        data.clear_data();

    def update_dataStage01PhysiologyData(self,data_I):
        '''update rows of data_stage01_physiology_data'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage01_physiology_data).filter(
                            data_stage01_physiology_data.id == d['id']).update(
                            {'experiment_id':d['experiment_id'],
                            'sample_id':d['sample_id'],
                            #'sample_name_short':d['sample_name_short'],
                            #'time_point':d['time_point'],
                            #'sample_date':d['sample_date'],
                            'met_id':d['met_id'],
                            'data_raw':d['data_raw'],
                            'data_corrected':d['data_corrected'],
                            'data_units':d['data_units'],
                            'data_reference':d['data_reference'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def export_dataStage01PhysiologyRatesAverages_d3(self, experiment_id,
                                                 sample_name_abbreviations_I=[],
                                                 met_ids_include_I=[],
                                                 met_ids_exclude_I=[],
                                                 json_var_name='data',
                                                 filename=[settings.visualization_data,'/physiology/barchart/data.js']):
        '''Export data for viewing using d3'''

        #Input:
        #   experiment_id
        #Output:
        #   
        data_O = [];
        # query sample_names
        if sample_name_abbreviations_I:
            sample_name_abbreviations = sample_name_abbreviations_I;
        else:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.stage01_physiology_query.get_sampleNameAbbreviations_experimentID_dataStage01PhysiologyRatesAverages(experiment_id);
        for sna in sample_name_abbreviations:
            # query met_ids
            if met_ids_include_I:
                met_ids = met_ids_include_I;
            else:
                met_ids = [];
                met_ids = self.stage01_physiology_query.get_metIDs_experimentID_dataStage01PhysiologyRatesAverages(experiment_id,sna);
            for met in met_ids:
                # query rate data
                slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var = None,None,None,None,None,None,None;
                slope_average, intercept_average, \
                    rate_average, rate_lb, rate_ub, \
                    rate_units, rate_var = self.stage01_physiology_query.get_rateData_experimentIDAndSampleNameAbbreviationAndMetID_dataStage01PhysiologyRatesAverages(experiment_id,sna,met);
                data_O.append({'sample_name_abbreviation':sna,
                            'met_id':met,'rate_average':rate_average,
                            'rate_lb':rate_lb,
                            'rate_ub':rate_ub,
                            'rate_units':rate_units,
                            'rate_var':rate_var});
        # restructure into input for d3
        if met_ids_include_I:
            met_ids_unique = met_ids_include_I;
        else:
            met_ids = [x['met_id'] for x in data_O]
            met_ids_unique = list(set(met_ids));
        met_ids_unique = [x for x in met_ids_unique if not x in met_ids_exclude_I];
        if sample_name_abbreviations_I:
            sample_name_abbreviations_unique = sample_name_abbreviations_I;
        else:
            sample_name_abbreviations = [x['sample_name_abbreviation'] for x in data_O]
            sample_name_abbreviations_unique = list(set(sample_name_abbreviations));
        ##Original .csv implementation:
        #json_O = [];
        #for met_id in met_ids_unique:
        #    row = {};
        #    for sna in sample_name_abbreviations_unique:
        #        row[sna] = 0.0;
        #        for d in data_O:
        #            if d['met_id'] == met_id and d['sample_name_abbreviation'] == sna:
        #                row[sna] = d['rate_average'];
        #    row['label']=met_id;
        #    json_O.append(row);
        ## dump the data to a json file
        #be = base_exportData(json_O);
        #headers = ['label']+sample_name_abbreviations;
        #be.write_dict2csv(filename,headers);
        #Updated js variable implementation:
        json_O = {};
        d3data_O = [];
        for met_id in met_ids_unique:
            data_tmp = {};
            data_tmp['samples']=[];
            data_tmp['label']=met_id;
            for sna in sample_name_abbreviations_unique:
                row = {};
                row['name'] = sna;
                row['value'] = 0.0;
                row['value_lb'] = 0.0;
                row['value_ub'] = 0.0;
                row['value_var'] = 0.0;
                for d in data_O:
                    if d['met_id'] == met_id and d['sample_name_abbreviation'] == sna:
                        row['value'] = d['rate_average'];
                        row['value_lb'] = d['rate_lb'];
                        row['value_ub'] = d['rate_ub'];
                        row['value_var'] = d['rate_var'];
                data_tmp['samples'].append(row);
            d3data_O.append(data_tmp);
        json_O['samplenames'] = sample_name_abbreviations_unique;
        json_O['data'] = d3data_O;
        # dump the data to a json file
        json_str = 'var ' + json_var_name + ' = ' + json.dumps(json_O);
        filename_O = filename[0] + '/' + experiment_id + filename[1];
        with open(filename_O,'w') as file:
            file.write(json_str);
    