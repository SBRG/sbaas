from analysis.analysis_base import *
from stage01_ale_query import stage01_ale_query
from scipy.io import loadmat

class stage01_ale_io(base_analysis):

    def __init__(self):
        self.session = Session();
        self.stage01_ale_query = stage01_ale_query();
        self.calculate = base_calculate();

    def import_dataStage01AleTrajectories_matlab(self, experiment_id_I, filename_I):
        '''table adds'''
        #data = base_importData();
        #data.read_csv(filename);
        #data.format_data();
        # load matlab data
        ale_ids = loadmat(filename_I)['ALEsKOs']['ale_id'][0];
        time = loadmat(filename_I)['ALEsKOs']['time'][0];
        growth_rate = loadmat(filename_I)['ALEsKOs']['growth_rate'][0];
        # format data
        data = [];
        for i,id in enumerate(ale_ids):
            times = [j for j in time[i][0]];
            rates = [j for j in growth_rate[i][0]];
            for j,t in enumerate(times):
                data.append({'experiment_id':experiment_id_I,
                                            'sample_name_abbreviation':id[0],
                                            'ale_time':t,
                                            'ale_time_units':'days',
                                            'rate':rates[j],
                                            'rate_units':'hr-1',
                                            'used_':True,
                                            'comment_':None})
        # add data to table
        self.add_dataStage01AleTrajectories(data);
        #self.add_dataStage01AleTrajectories(data.data);
        #data.clear_data();

    def add_dataStage01AleTrajectories(self, data_I):
        '''add rows of data_stage01_ale_trajectories'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage01_ale_trajectories(d['experiment_id'],
                                    d['sample_name_abbreviation'],
                                    d['ale_time'],
                                    d['ale_time_units'],
                                    d['rate'],
                                    d['rate_units'],
                                    d['used_'],
                                    d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage01AleTrajectories_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01AleTrajectories(data.data);
        data.clear_data();

    def update_dataStage01AleTrajectories(self,data_I):
        '''update rows of data_stage01_ale_trajectories'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage01_ale_trajectories).filter(
                            data_stage01_ale_trajectories.id == d['id']).update(
                            {
                            'experiment_id':d['experiment_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'ale_time':d['ale_time'],
                            'ale_time_units':d['ale_time_units'],
                            'rate':d['rate'],
                            'rate_units':d['rate_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
            
    def import_dataStage01AleJumps_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage01AleJumps(data.data);
        data.clear_data();

    def add_dataStage01AleJumps(self, data_I):
        '''add rows of data_stage01_ale_jumps'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage01_ale_jumps(d['experiment_id'],
                        d['sample_name_abbreviation'],
                        d['ale_time'],
                        d['ale_time_units'],
                        d['rate_fitted'],
                        d['rate_fitted_units'],
                        d['jump_region'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage01AleJumps_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01AleJumps(data.data);
        data.clear_data();

    def update_dataStage01AleJumps(self,data_I):
        '''update rows of data_stage01_ale_jumps'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage01_ale_jumps).filter(
                            data_stage01_ale_jumps.id == d['id']).update(
                            {'experiment_id':d['experiment_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'ale_time':d['ale_time'],
                            'ale_time_units':d['ale_time_units'],
                            'rate_fitted':d['rate_fitted'],
                            'rate_fitted_units':d['rate_fitted_units'],
                            'jump_region':d['jump_region'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
   
    def export_dataStage01AleTrajectories_d3(self, experiment_id_I,
                                                 sample_name_abbreviations_I=[],
                                                 fit_func_I='lowess',
                                                 x_axis_I=[],
                                                 y_axis_I=[],
                                                 json_var_name='data',
                                                 filename=['visualization/data/ALEsKOs01/','/scatterlineplot/','.js']):
        '''Export data for viewing using d3'''
        
        data_O = [];
        data_fitted_O = [];
        #query sample_name abbreviations
        if sample_name_abbreviations_I:
            sample_name_abbreviations = sample_name_abbreviations_I;
        else:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.stage01_ale_query.get_sampleNameAbbreviations_experimentID_dataStage01AleTrajectories(experiment_id_I);
        for sna in sample_name_abbreviations:
            #query growth rates and times
            growth_rates = [];
            growth_rates = self.stage01_ale_query.get_rows_experimentIDAndSampleNameAbbreviation_dataStage01AleTrajectories(experiment_id_I,sna)
            #smooth growth rates
            x,y=[],[];
            for k in growth_rates:
                x.append(k['ale_time'])
                y.append(k['rate'])
                data_O.append({'samples':sna,
                               'x_data':k['ale_time'],
                               'y_data':k['rate']});
            x_fit,y_fit=[],[];
            x_fit,y_fit=self.calculate.fit_trajectories(x,y,fit_func_I,plot_fit_I=False);
            # restructure into input for d3
            for i,x in enumerate(x_fit):
                data_fitted_O.append({'samples':sna,
                               'x_data_fitted':x_fit[i],
                               'y_data_fitted':y_fit[i]});
        options_O = {};
        options_O['x_axis'] = x_axis_I;
        options_O['y_axis'] = y_axis_I;
        options_O['x_axis_label'] = 'time [days]';
        options_O['y_axis_label'] = 'growth rate [hr-1]';
        options_O['feature_name'] = 'sample';
        options_O['fit_function'] = 'basis';
       
        #Updated js variable implementation:
        json_O = {};
        json_O['data'] = data_O;
        json_O['data_fitted'] = data_fitted_O;
        json_O['options'] = options_O;
        # dump the data to a json file
        json_str = 'var ' + json_var_name + ' = ' + json.dumps(json_O);
        #filename_str = filename[0] + experiment_id + filename[1] + filename[2] + 'filter.js'
        with open(filename,'w') as file:
            file.write(json_str);
    