from sbaas.analysis.analysis_base import *
from .stage02_physiology_query import *
from .stage02_physiology_io import *
import datetime
from sbaas.resources.sampling import cobra_sampling,cobra_sampling_n
# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file, write_cobra_model_to_sbml_file
from cobra.flux_analysis.variability import flux_variability_analysis
from cobra.flux_analysis.parsimonious import optimize_minimal_flux
from cobra.flux_analysis import flux_variability_analysis
from cobra.manipulation.modify import convert_to_irreversible

class stage02_physiology_execute():
    '''class for physiological analysis analysis'''
    def __init__(self,session_I=None,data_dir_I=None):
        if session_I: self.session = session_I;
        else: self.session = Session();
        self.stage02_physiology_query = stage02_physiology_query(self.session);
        self.calculate = base_calculate();
        self.models = {};
        if data_dir_I: self.data_dir = data_dir_I;
        else: self.data_dir = 'C:/Users/dmccloskey-sbrg/Documents/MATLAB/sampling_physiology'

    #analyses:
    def execute_makeModel(self,experiment_id_I,model_id_I=None,model_id_O=None,date_I=None,model_file_name_I=None,ko_list=[],flux_dict={},description=None,convert2irreversible_I=False):
        '''make the model'''

        qio02 = stage02_physiology_io();

        if model_id_I and model_id_O: #modify an existing model in the database
            cobra_model_sbml = None;
            cobra_model_sbml = self.stage02_physiology_query.get_row_modelID_dataStage02PhysiologyModels(model_id_I);
            # write the model to a temporary file
            if cobra_model_sbml['file_type'] == 'sbml':
                with open(settings.workspace_data + '/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                cobra_model = None;
                cobra_model = create_cobra_model_from_sbml_file(settings.workspace_data + '/cobra_model_tmp.xml', print_time=True);
            elif cobra_model_sbml['file_type'] == 'json':
                with open(settings.workspace_data + '/cobra_model_tmp.json','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                cobra_model = None;
                cobra_model = load_json_model(settings.workspace_data + '/cobra_model_tmp.json');
            else:
                print('file_type not supported')
            if convert2irreversible_I: convert_to_irreversible(cobra_model);
            # Apply KOs, if any:
            for ko in ko_list:
                cobra_model.reactions.get_by_id(ko).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(ko).upper_bound = 0.0;
            # Apply flux constraints, if any:
            for rxn,flux in flux_dict.items():
                cobra_model.reactions.get_by_id(rxn).lower_bound = flux['lb'];
                cobra_model.reactions.get_by_id(rxn).upper_bound = flux['ub'];
            # Change description, if any:
            if description:
                cobra_model.description = description;
            # test the model
            if self.test_model(cobra_model):
                # write the model to a temporary file
                with open(settings.workspace_data + '/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model);
                # upload the model to the database
                qio02.import_dataStage02PhysiologyModel_sbml(model_id_I, date_I, settings.workspace_data + '/cobra_model_tmp.xml');
        elif model_file_name_I and model_id_O: #modify an existing model not in the database
            # Read in the sbml file and define the model conditions
            cobra_model = create_cobra_model_from_sbml_file(model_file_name_I, print_time=True);
            if convert2irreversible_I: convert_to_irreversible(cobra_model);
            # Apply KOs, if any:
            for ko in ko_list:
                cobra_model.reactions.get_by_id(ko).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(ko).upper_bound = 0.0;
            # Apply flux constraints, if any:
            for rxn,flux in flux_dict.items():
                cobra_model.reactions.get_by_id(rxn).lower_bound = flux['lb'];
                cobra_model.reactions.get_by_id(rxn).upper_bound = flux['ub'];
            # Change description, if any:
            if description:
                cobra_model.description = description;
            # test the model
            if self.test_model(cobra_model):
                # write the model to a temporary file
                with open(settings.workspace_data + '/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model);
                # upload the model to the database
                qio02.import_dataStage02PhysiologyModel_sbml(model_id_I, date_I, settings.workspace_data + '/cobra_model_tmp.xml');
        else:
            print('need to specify either an existing model_id or model_file_name!')
        return
    def execute_addMeasuredFluxes(self,experiment_id_I, ko_list={}, flux_dict={}, model_ids_I=[], sample_name_abbreviations_I=[]):
        '''Add flux data for physiological simulation'''
        #Input:
            #flux_dict = {};
            #flux_dict['iJO1366'] = {};
            #flux_dict['iJO1366'] = {};
            #flux_dict['iJO1366']['sna'] = {};
            #flux_dict['iJO1366']['sna']['Ec_biomass_iJO1366_WT_53p95M'] = {'ave':None,'stdev':None,'units':'mmol*gDCW-1*hr-1','lb':0.704*0.9,'ub':0.704*1.1};
            #flux_dict['iJO1366']['sna']['EX_ac_LPAREN_e_RPAREN_'] = {'ave':None,'stdev':None,'units':'mmol*gDCW-1*hr-1','lb':2.13*0.9,'ub':2.13*1.1};
            #flux_dict['iJO1366']['sna']['EX_o2_LPAREN_e_RPAREN__reverse'] = {'ave':None,'units':'mmol*gDCW-1*hr-1','stdev':None,'lb':0,'ub':16};
            #flux_dict['iJO1366']['sna']['EX_glc_LPAREN_e_RPAREN_'] = {'ave':None,'stdev':None,'units':'mmol*gDCW-1*hr-1','lb':-7.4*1.1,'ub':-7.4*0.9};

        data_O = [];
        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage02_physiology_query.get_modelID_experimentID_dataStage02PhysiologySimulation(experiment_id_I);
        for model_id in model_ids:
            # get sample names and sample name abbreviations
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.stage02_physiology_query.get_sampleNameAbbreviations_experimentIDAndModelID_dataStage02PhysiologySimulation(experiment_id_I,model_id);
            for sna_cnt,sna in enumerate(sample_name_abbreviations):
                print('Adding experimental fluxes for sample name abbreviation ' + sna);
                if flux_dict:
                    for k,v in flux_dict[model_id][sna].items():
                        # record the data
                        data_tmp = {'experiment_id':experiment_id_I,
                                'model_id':model_id,
                                'sample_name_abbreviation':sna,
                                'rxn_id':k,
                                'flux_average':v['ave'],
                                'flux_stdev':v['stdev'],
                                'flux_lb':v['lb'], 
                                'flux_ub':v['ub'],
                                'flux_units':v['units'],
                                'used_':True,
                                'comment_':None}
                        data_O.append(data_tmp);
                        #add data to the database
                        row = [];
                        row = data_stage02_physiology_measuredFluxes(
                            experiment_id_I,
                            model_id,
                            sna,
                            k,
                            v['ave'],
                            v['stdev'],
                            v['lb'], 
                            v['ub'],
                            v['units'],
                            True,
                            None);
                        self.session.add(row);
                if ko_list:
                    for k in ko_list[model_id][sna]:
                        # record the data
                        data_tmp = {'experiment_id':experiment_id_I,
                                'model_id':model_id,
                                'sample_name_abbreviation':sna,
                                'rxn_id':k,
                                'flux_average':0.0,
                                'flux_stdev':0.0,
                                'flux_lb':0.0, 
                                'flux_ub':0.0,
                                'flux_units':'mmol*gDCW-1*hr-1',
                                'used_':True,
                                'comment_':None}
                        data_O.append(data_tmp);
                        #add data to the database
                        row = [];
                        row = data_stage02_physiology_measuredFluxes(
                            experiment_id_I,
                            model_id,
                            sna,
                            k,
                            0.0,
                            0.0,
                            0.0, 
                            0.0,
                            'mmol*gDCW-1*hr-1',
                            True,
                            None);
                        self.session.add(row);
        self.session.commit();
    def execute_makeMeasuredFluxes(self,experiment_id_I, metID2RxnID_I = {}, sample_name_abbreviations_I = [], met_ids_I = []):
        '''Collect and flux data from data_stage01_physiology_ratesAverages for physiological simulation'''
        #Input:
        #   metID2RxnID_I = e.g. {'glc-D':{'model_id':'140407_iDM2014','rxn_id':'EX_glc_LPAREN_e_RPAREN_'},
        #                        {'ac':{'model_id':'140407_iDM2014','rxn_id':'EX_ac_LPAREN_e_RPAREN_'},
        #                        {'succ':{'model_id':'140407_iDM2014','rxn_id':'EX_succ_LPAREN_e_RPAREN_'},
        #                        {'lac-L':{'model_id':'140407_iDM2014','rxn_id':'EX_lac_DASH_L_LPAREN_e_RPAREN_'},
        #                        {'biomass':{'model_id':'140407_iDM2014','rxn_id':'Ec_biomass_iJO1366_WT_53p95M'}};

        data_O = [];
        # get sample names and sample name abbreviations
        if sample_name_abbreviations_I:
            sample_name_abbreviations = sample_name_abbreviations_I;
        else:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.stage02_physiology_query.get_sampleNameAbbreviations_experimentID_dataStage02PhysiologySimulation(experiment_id_I);
        for sna in sample_name_abbreviations:
            print('Collecting experimental fluxes for sample name abbreviation ' + sna);
            # get met_ids
            if not met_ids_I:
                met_ids = [];
                met_ids = self.stage02_physiology_query.get_metID_experimentIDAndSampleNameAbbreviation_dataStage01PhysiologyRatesAverages(experiment_id_I,sna);
            else:
                met_ids = met_ids_I;
            if not(met_ids): continue #no component information was found
            for met in met_ids:
                print('Collecting experimental fluxes for metabolite ' + met);
                # get rateData
                slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var = None,None,None,None,None,None,None;
                slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var = self.stage02_physiology_query.get_rateData_experimentIDAndSampleNameAbbreviationAndMetID_dataStage01PhysiologyRatesAverages(experiment_id_I,sna,met);
                rate_stdev = sqrt(rate_var);
                model_id = metID2RxnID_I[met]['model_id'];
                rxn_id = metID2RxnID_I[met]['rxn_id'];
                # record the data
                data_tmp = {'experiment_id':experiment_id_I,
                        'model_id':model_id,
                        'sample_name_abbreviation':sna,
                        'rxn_id':rxn_id,
                        'flux_average':rate_average,
                        'flux_stdev':rate_stdev,
                        'flux_lb':rate_lb, 
                        'flux_ub':rate_ub,
                        'flux_units':rate_units,
                        'used_':True,
                        'comment_':None}
                data_O.append(data_tmp);
                #add data to the database
                row = [];
                row = data_stage02_physiology_measuredFluxes(
                    experiment_id_I,
                    model_id,
                    sna,
                    rxn_id,
                    rate_average,
                    rate_stdev,
                    rate_lb, 
                    rate_ub,
                    rate_units,
                    True,
                    None);
                self.session.add(row);
        self.session.commit();
    def execute_sampling_v1(self,experiment_id_I, model_ids_I = [],
                               sample_name_abbreviations_I=[],
                               rxn_ids_I=[]):
        '''Sample a specified model that is constrained to measured physiological data'''
        
        print('executing sampling...');# get simulation information
        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage02_physiology_query.get_modelID_experimentID_dataStage02PhysiologySimulation(experiment_id_I);
        for model_id in model_ids:
            print('executing sampling for model_id ' + model_id);
            # get the cobra model
            cobra_model = self.models[model_id];
            ## get the time-points
            #if time_points_I:
            #    time_points = time_points_I;
            #else:
            #    time_points = [];
            #    time_points = self.stage02_physiology_query.get_timePoints_experimentIDAndModelID_dataStage02PhysiologySimulation(experiment_id_I,model_id);
            #for tp in time_points:
            # get sample_name_abbreviations
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.stage02_physiology_query.get_sampleNameAbbreviations_experimentIDAndModelID_dataStage02PhysiologySimulation(experiment_id_I,model_id);
            for sna in sample_name_abbreviations:
                print('executing sampling for sample_name_abbreviation ' + sna);
                # copy the model
                cobra_model_copy = cobra_model.copy();
                # get rxn_ids
                if rxn_ids_I:
                    rxn_ids = rxn_ids_I;
                else:
                    rxn_ids = [];
                    rxn_ids = self.stage02_physiology_query.get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02PhysiologyMeasuredFluxes(experiment_id_I,model_id,sna);
                for rxn in rxn_ids:
                    # constrain the model
                    cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).lower_bound = rxn['flux_lb'];
                    cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).upper_bound = rxn['flux_ub'];
                # Test each model
                if self.test_model(cobra_model_I=cobra_model_copy):
                    filename_model = experiment_id_I + '_' + model_id + '_' + sna + '.mat';
                    filename_script = experiment_id_I + '_' + model_id + '_' + sna + '.m';
                    filename_points = experiment_id_I + '_' + model_id + '_' + sna + '_points' + '.mat';
                    self.sampling.export_sampling_matlab(cobra_model=cobra_model_copy,filename_model=filename_model,filename_script=filename_script,filename_points=filename_points);
                else:
                    print('no solution found!');  
    def execute_analyzeSamplingPoints_v1(self,experiment_id_I, model_ids_I = [],
                               sample_name_abbreviations_I=[],
                               rxn_ids_I=[]):
        '''Load and analyze sampling points'''

        print('analyzing sampling points');
        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage02_physiology_query.get_modelID_experimentID_dataStage02PhysiologySimulation(experiment_id_I);
        for model_id in model_ids:
            print('analyzing sampling points model_id ' + model_id);
            # get the cobra model
            cobra_model = self.models[model_id];
            ## get the time-points
            #if time_points_I:
            #    time_points = time_points_I;
            #else:
            #    time_points = [];
            #    time_points = self.stage02_physiology_query.get_timePoints_experimentIDAndModelID_dataStage02PhysiologySimulation(experiment_id_I,model_id);
            #for tp in time_points:
            # get sample_name_abbreviations
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.stage02_physiology_query.get_sampleNameAbbreviations_experimentIDAndModelID_dataStage02PhysiologySimulation(experiment_id_I,model_id);
            for sna in sample_name_abbreviations:
                print('analyzing sampling points for sample_name_abbreviation ' + sna);
                # copy the model
                cobra_model_copy = cobra_model.copy();
                # get rxn_ids
                if rxn_ids_I:
                    rxn_ids = rxn_ids_I;
                else:
                    rxn_ids = [];
                    rxn_ids = self.stage02_physiology_query.get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02PhysiologyMeasuredFluxes(experiment_id_I,model_id,sna);
                for rxn in rxn_ids:
                    # constrain the model
                    cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).lower_bound = rxn['flux_lb'];
                    cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).upper_bound = rxn['flux_ub'];
                # Test each model
                if self.test_model(cobra_model_I=cobra_model_copy):
                    # load the results of sampling
                    filename_points = experiment_id_I + '_' + model_id + '_' + sna + '_points' + '.mat';
                    self.sampling.get_points_matlab(filename_points,'sampler_out');
                    # check if the model contains loops
                    #loops_bool = self.sampling.check_loops();
                    self.sampling.simulate_loops(data_fva='data/loops_fva_tmp.json');
                    self.sampling.find_loops(data_fva='data/loops_fva_tmp.json');
                    self.sampling.remove_loopsFromPoints();
                    # add data to the database
                    for k,v in self.sampling.points.items():
                        data_tmp = {'experiment_id':experiment_id_I,
                            'model_id':model_id,
                            'sample_name_abbreviation':sna,
                            'rxn_id':k,
                            'flux_units':'mmol*gDW-1*hr-1',
                            'sampling_ave':v['ave'],
                            'sampling_var':v['var'],
                            'sampling_lb':v['lb'],
                            'sampling_ub':v['ub'],
                            'mixed_fraction':self.sampling.mixed_fraction,
                            'sampling_points':v['points'],
                            'data_dir':self.sampling.matlab_path+'/'+filename_points,
                            'used_':True,
                            'comment_':None};
                        row = None;
                        row = data_stage02_physiology_sampledPoints(experiment_id_I,
                            model_id,
                            sna,
                            k,
                            'mmol*gDW-1*hr-1',
                            self.sampling.mixed_fraction,
                            #v['points'],
                            None,
                            self.sampling.matlab_path+'/'+filename_points,
                            True,
                            None);
                        self.session.add(row);
                        row = None;
                        row = data_stage02_physiology_sampledData(experiment_id_I,
                            model_id,
                            sna,
                            k,
                            'mmol*gDW-1*hr-1',
                            v['ave'],
                            v['var'],
                            v['lb'],
                            v['ub'],
                            True,
                            None);
                        self.session.add(row);
                else:
                    print('no solution found!');
        self.session.commit()  
    def execute_sampling(self,simulation_id_I,
                               rxn_ids_I=[]):
        '''Sample a specified model that is constrained to measured physiological data'''
        
        print('executing sampling...');
        # get simulation information
        simulation_info_all = [];
        simulation_info_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySimulation(simulation_id_I);
        if not simulation_info_all:
            print('simulation not found!')
            return;
        simulation_info = simulation_info_all[0]; # unique constraint guarantees only 1 row will be returned
        # get simulation parameters
        simulation_parameters_all = [];
        simulation_parameters_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySimulationParameters(simulation_id_I);
        if not simulation_parameters_all:
            print('simulation not found!')
            return;
        simulation_parameters = simulation_parameters_all[0]; # unique constraint guarantees only 1 row will be returned
        # get the cobra model
        cobra_model = self.models[simulation_info['model_id']];
        # copy the model
        cobra_model_copy = cobra_model.copy();
        # get rxn_ids
        if rxn_ids_I:
            rxn_ids = rxn_ids_I;
        else:
            rxn_ids = [];
            rxn_ids = self.stage02_physiology_query.get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02PhysiologyMeasuredFluxes(simulation_info['experiment_id'],simulation_info['model_id'],simulation_info['sample_name_abbreviation']);
        for rxn in rxn_ids:
            # constrain the model
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).lower_bound = rxn['flux_lb'];
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).upper_bound = rxn['flux_ub'];
        # Test model
        if self.test_model(cobra_model_I=cobra_model_copy):
            sampling = cobra_sampling(data_dir_I = self.data_dir);
            if simulation_parameters['sampler_id']=='gpSampler':
                filename_model = simulation_id_I + '.mat';
                filename_script = simulation_id_I + '.m';
                filename_points = simulation_id_I + '_points' + '.mat';
                sampling.export_sampling_matlab(cobra_model=cobra_model_copy,filename_model=filename_model,filename_script=filename_script,filename_points=filename_points,\
                    solver_id_I = simulation_parameters['solver_id'],\
                    n_points_I = simulation_parameters['n_points'],\
                    n_steps_I = simulation_parameters['n_steps'],\
                    max_time_I = simulation_parameters['max_time']);
            elif simulation_parameters['sampler_id']=='optGpSampler':
                return;
            else:
                print('sampler_id not recognized');
        else:
            print('no solution found!');  
    def execute_analyzeSamplingPoints(self,simulation_id_I,
                               rxn_ids_I=[]):
        '''Load and analyze sampling points'''

        print('analyzing sampling points');
        
        # get simulation information
        simulation_info_all = [];
        simulation_info_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySimulation(simulation_id_I);
        if not simulation_info_all:
            print('simulation not found!')
            return;
        simulation_info = simulation_info_all[0]; # unique constraint guarantees only 1 row will be returned
        # get simulation parameters
        simulation_parameters_all = [];
        simulation_parameters_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySimulationParameters(simulation_id_I);
        if not simulation_parameters_all:
            print('simulation not found!')
            return;
        simulation_parameters = simulation_parameters_all[0]; # unique constraint guarantees only 1 row will be returned
        # get the cobra model
        cobra_model = self.models[simulation_info['model_id']];
        # copy the model
        cobra_model_copy = cobra_model.copy();
        # get rxn_ids
        if rxn_ids_I:
            rxn_ids = rxn_ids_I;
        else:
            rxn_ids = [];
            rxn_ids = self.stage02_physiology_query.get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02PhysiologyMeasuredFluxes(simulation_info['experiment_id'],simulation_info['model_id'],simulation_info['sample_name_abbreviation']);
        for rxn in rxn_ids:
            # constrain the model
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).lower_bound = rxn['flux_lb'];
            cobra_model_copy.reactions.get_by_id(rxn['rxn_id']).upper_bound = rxn['flux_ub'];
        # Test each model
        if self.test_model(cobra_model_I=cobra_model_copy):
            sampling = cobra_sampling(data_dir_I = self.data_dir);
            if simulation_parameters['sampler_id']=='gpSampler':
                # load the results of sampling
                filename_points = simulation_id_I + '_points' + '.mat';
                sampling.get_points_matlab(filename_points,'sampler_out');
                # check if the model contains loops
                #loops_bool = self.sampling.check_loops();
                sampling.simulate_loops(data_fva=settings.workspace_data + '/loops_fva_tmp.json');
                sampling.find_loops(data_fva=settings.workspace_data + '/loops_fva_tmp.json');
                sampling.remove_loopsFromPoints();
                sampling.descriptive_statistics();
            elif simulation_parameters['sampler_id']=='optGpSampler':
                return;
            else:
                print('sampler_id not recognized');
            # add data to the database
            row = None;
            row = data_stage02_physiology_sampledPoints(
                simulation_id_I,
                sampling.simulation_dateAndTime,
                sampling.mixed_fraction,
                sampling.matlab_path+'/'+filename_points,
                sampling.loops,
                True,
                None);
            self.session.add(row);
            for k,v in self.sampling.points_statistics.items():
                row = None;
                row = data_stage02_physiology_sampledData(
                    simulation_id_I,
                    sampling.simulation_dateAndTime,
                    k,
                    'mmol*gDW-1*hr-1',
                    None, #v['points'],
                    v['ave'],
                    v['var'],
                    v['lb'],
                    v['ub'],
                    v['min'],
                    v['max'],
                    v['median'],
                    v['iq_1'],
                    v['iq_3'],
                    True,
                    None);
                self.session.add(row);
        else:
            print('no solution found!');
        self.session.commit()  
    #internal functions:
    def format_metid(self,met_id_I,compartment_id_I):
        met_formatted = met_id_I
        met_formatted = re.sub('-','_DASH_',met_formatted)
        met_formatted = re.sub('[(]','_LPARANTHES_',met_formatted)
        met_formatted = re.sub('[)]','_RPARANTHES_',met_formatted)
        met_formatted +='_' + compartment_id_I;
        return met_formatted;
    def test_model(self,cobra_model_I=None,model_id_I=None,ko_list=[],flux_dict={},description=None):
        '''simulate a cobra model'''

        if model_id_I:
            # get the xml model
            cobra_model_sbml = ''
            cobra_model_sbml = self.stage02_physiology_query.get_row_modelID_dataStage02PhysiologyModels(model_id_I);
            # load the model
            if cobra_model_sbml['file_type'] == 'sbml':
                with open(settings.workspace_data + '/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = create_cobra_model_from_sbml_file(settings.workspace_data + '/cobra_model_tmp.xml', print_time=True);
            elif cobra_model_sbml['file_type'] == 'json':
                with open(settings.workspace_data + '/cobra_model_tmp.json','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = load_json_model(settings.workspace_data + '/cobra_model_tmp.json');
            else:
                print('file_type not supported')
        elif cobra_model_I:
            cobra_model = cobra_model_I;
        # implement optimal KOs and flux constraints:
        for ko in ko_list:
            cobra_model.reactions.get_by_id(ko).lower_bound = 0.0;
            cobra_model.reactions.get_by_id(ko).upper_bound = 0.0;
        for rxn,flux in flux_dict.items():
            cobra_model.reactions.get_by_id(rxn).lower_bound = flux['lb'];
            cobra_model.reactions.get_by_id(rxn).upper_bound = flux['ub'];
        # change description, if any:
        if description:
            cobra_model.description = description;
        # test for a solution:
        cobra_model.optimize(solver='gurobi');
        if not cobra_model.solution.f:
            return False;
        else:
            print(cobra_model.solution.f);
            return True;
    def load_models(self,experiment_id_I,model_ids_I=[]):
        '''pre-load all models for the experiment_id'''
        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage02_physiology_query.get_modelID_experimentID_dataStage02PhysiologySimulation(experiment_id_I);
        for model_id in model_ids:
            # get the cobra model
            cobra_model_sbml = None;
            cobra_model_sbml = self.stage02_physiology_query.get_row_modelID_dataStage02PhysiologyModels(model_id);
            # write the model to a temporary file
            if cobra_model_sbml['file_type'] == 'sbml':
                with open(settings.workspace_data + '/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                cobra_model = None;
                cobra_model = create_cobra_model_from_sbml_file(settings.workspace_data + '/cobra_model_tmp.xml', print_time=True);
            elif cobra_model_sbml['file_type'] == 'json':
                with open(settings.workspace_data + '/cobra_model_tmp.json','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                cobra_model = None;
                cobra_model = load_json_model(settings.workspace_data + '/cobra_model_tmp.json');
            else:
                print('file_type not supported')
            self.models[model_id]=cobra_model;
    #table initializations:
    def drop_dataStage02(self):
        try:
            data_stage02_physiology_simulation.__table__.drop(engine,True);
            data_stage02_physiology_modelReactions.__table__.drop(engine,True);
            data_stage02_physiology_modelMetabolites.__table__.drop(engine,True);
            data_stage02_physiology_models.__table__.drop(engine,True);
            data_stage02_physiology_measuredFluxes.__table__.drop(engine,True);
            data_stage02_physiology_simulatedData.__table__.drop(engine,True);
            data_stage02_physiology_sampledPoints.__table__.drop(engine,True);
            data_stage02_physiology_sampledData.__table__.drop(engine,True);
            data_stage02_physiology_simulationParameters.__table__.drop(engine,True);
            data_stage02_physiology_pairWiseTest.__table__.drop(engine,True);
            data_stage02_physiology_pairWiseTestMetabolites.__table__.drop(engine,True);
            data_stage02_physiology_pairWiseTestSubsystems.__table__.drop(engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02(self,experiment_id_I = None,simulation_id_I=None):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage02_physiology_simulation).filter(data_stage02_physiology_simulation.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_models).filter(data_stage02_physiology_models.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_measuredFluxes).filter(data_stage02_physiology_measuredFluxes.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_simulatedData).filter(data_stage02_physiology_simulatedData.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_sampledPoints).filter(data_stage02_physiology_sampledPoints.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_sampledData).filter(data_stage02_physiology_sampledData.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_modelReactions).filter(data_stage02_physiology_modelReactions.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_modelMetabolites).filter(data_stage02_physiology_modelMetabolites.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_simulationParameters).filter(data_stage02_physiology_simulationParameters.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
            elif simulation_id_I:
                reset = self.session.query(data_stage02_physiology_simulation).filter(data_stage02_physiology_simulation.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_simulatedData).filter(data_stage02_physiology_simulatedData.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_sampledPoints).filter(data_stage02_physiology_sampledPoints.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_sampledData).filter(data_stage02_physiology_sampledData.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_simulationParameters).filter(data_stage02_physiology_simulationParameters.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_physiology_simulation).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_models).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_measuredFluxes).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_simulatedData).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_sampledPoints).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_sampledData).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_modelReactions).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_modelMetabolites).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_simulationParameters).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_sampledData_pairWiseTest).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_sampledData_pairWiseTestMetabolites).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_sampledData_pairWiseTestSubsystems).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_dataStage02(self):
        try:
            data_stage02_physiology_simulation.__table__.create(engine,True);
            data_stage02_physiology_models.__table__.create(engine,True);
            data_stage02_physiology_measuredFluxes.__table__.create(engine,True);
            data_stage02_physiology_simulatedData.__table__.create(engine,True);
            data_stage02_physiology_sampledPoints.__table__.create(engine,True);
            data_stage02_physiology_sampledData.__table__.create(engine,True);
            data_stage02_physiology_modelReactions.__table__.create(engine,True);
            data_stage02_physiology_modelMetabolites.__table__.create(engine,True);
            data_stage02_physiology_simulationParameters.__table__.create(engine,True);
            data_stage02_physiology_pairWiseTest.__table__.create(engine,True);
            data_stage02_physiology_pairWiseTestMetabolites.__table__.create(engine,True);
            data_stage02_physiology_pairWiseTestSubsystems.__table__.create(engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_pairWiseTests(self,simulation_id_I=None):   
        try:         
            if simulation_group_id_I:
                reset = self.session.query(data_stage02_physiology_sampledData_pairWiseTest).filter(data_stage02_physiology_sampledData_pairWiseTest.simulation_id_1.like(simulation_id_1_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_sampledData_pairWiseTestMetabolites).filter(data_stage02_physiology_sampledData_pairWiseTestMetabolites.simulation_id_1.like(simulation_id_1_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_sampledData_pairWiseTestSubsystems).filter(data_stage02_physiology_sampledData_pairWiseTestSubsystems.simulation_id_1.like(simulation_id_1_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_physiology_sampledData_pairWiseTest).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_sampledData_pairWiseTestMetabolites).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_physiology_sampledData_pairWiseTestSubsystems).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    #def reset_dataStage02_nTests(self,simulation_group_id_I=None):   
    #    try:         
    #        if simulation_group_id_I:
    #            reset = self.session.query(data_stage02_physiology_pca_scores).filter(data_stage02_physiology_pca_scores.simulation_group_id.like(simulation_group_id_I)).delete(synchronize_session=False);
    #            reset = self.session.query(data_stage02_physiology_pca_loadings).filter(data_stage02_physiology_pca_loadings.simulation_group_id.like(simulation_group_id_I)).delete(synchronize_session=False);
    #        else:
    #            reset = self.session.query(data_stage02_physiology_sampledData_pca_scores).delete(synchronize_session=False);
    #            reset = self.session.query(data_stage02_physiology_sampledData_pca_loadings).delete(synchronize_session=False);
    #        self.session.commit();
    #    except SQLAlchemyError as e:
    #        print(e);
    #TODO:
    def execute_samplingPairWiseTests(self,simulation_ids_I=[],control_I=False):
        '''calculate the p-value and mean difference between sampling distributions
        '''
        #Input:
        #   simulation_ids_I = list of simulation ids
        #   control_I = True: simulation_ids_I[0]=control,simulation_ids_I[1:]=perturbation
        #               False: pairwise test is performed on all

        # get simulation information
        simulation_info_all = [];
        for simulation_id in simulation_ids_I:
            simulation_info_1_all = [];
            simulation_info_1_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySimulation(simulation_id);
            if not simulation_info_1_all:
                print('simulation not found!')
                return;
            simulation_1_info = simulation_info_1_all[0]; # unique constraint guarantees only 1 row will be returned
            simulation_info_all.append(simulation_1_info);
        # get sampled_data
        sampledPoints_all = [];
        for simulation_id in simulation_ids_I:
            sampledPoints_1_all = [];
            sampledPoints_1_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySampledPoints(simulation_id);
            if not sampledPoints_1_all:
                print('simulation not found!')
                return;
            sampledPoints_1_info = sampledPoints_1_all[0]; # unique constraint guarantees only 1 row will be returned
            sampledPoints_all.append(sampledPoints_1_info);
        # get simulation parameters
        simulation_parameters_all = [];
        for simulation_id in simulation_ids_I:
            simulation_parameters_1_all = [];
            simulation_parameters_1_all = self.stage02_physiology_query.get_rows_simulationID_dataStage02PhysiologySimulationParameters(simulation_id);
            if not simulation_parameters_1_all:
                print('simulation not found!')
                return;
            simulation_1_parameters = simulation_parameters_1_all[0]; # unique constraint guarantees only 1 row will be returned
            simulation_parameters_all.append(simulation_1_parameters);
        # check that all models are the same
        model_ids_all = [x['model_id'] for x in simulation_info_all]
        model_ids_unique = list(set(model_ids_all));
        if len(model_ids_unique) != 1:
            print('more than 1 model_id found')
            return
        else:
            model_id = model_ids_unique[0];
        # get the base cobra model
        cobra_model = self.models[model_id];
        # extract out the data directories and simulation_ids
        data_dirs = [x['data_dir'] for x in sampledPoints_all]
        simulation_ids = [x['simulation_id'] for x in sampledPoints_all]
        infeasible_loops = [x['infeasible_loops'] for x in sampledPoints_all]
        # extract out sampling parameters
        sampler_ids = [x['sampler_id'] for x in simulation_parameters_all]
        # make filename points
        filename_points = [s + '_points' + '.mat' for s in simulation_ids_I];
        # perform the analysis
        sampling_n = cobra_sampling_n(data_dir_I=self.data_dir,
                                      model_I = cobra_model,
                                      loops_I = infeasible_loops,
                                      sample_ids_I = simulation_ids,
                                      samplers_I = sampler_ids,
                                      control_I = control_I);
        sampling_n.get_points(filename_points);
        #pairwisetest
        sampling_n.calculate_pairWiseTest();
        # load data into the database
        for d in sampling_n.data:
            row = None;
            row = data_stage02_physiology_pairWiseTest(
                d['sample_id_1'],
                d['sample_id_2'],
                d['rxn_id'],
                'mmol*gDW-1*hr-1',
                d['mean_difference'],
                d['test_stat'],
                d['test_description'],
                d['pvalue'],
                None,None,None,None,None,
                d['fold_change'],
                True,None
                )
            self.session.add(row);
        self.session.commit();
        ##pairwisetest_metabolites
        #sampling_n.calculate_pairWiseTest_metabolites();
        ## load data into the database
        #for d in sampling_n.data:
        #    row = None;
        #    row = data_stage02_physiology_pairWiseTestMetabolites(
        #        d['sample_id_1'],
        #        d['sample_id_2'],
        #        d['met_id'],
        #        'mmol*gDW-1*hr-1',
        #        d['mean_difference'],
        #        d['test_stat'],
        #        d['test_description'],
        #        d['pvalue'],
        #        None,None,None,None,None,
        #        d['fold_change'],
        #        True,None
        #        )
        #    self.session.add(row);
        #self.session.commit();
        ##pairwisetest_subsystems
        #sampling_n.calculate_pairWiseTest_subsystems();
        ## load data into the database
        #for d in sampling_n.data:
        #    row = None;
        #    row = data_stage02_physiology_pairWiseTestSubsystems(
        #        d['sample_id_1'],
        #        d['sample_id_2'],
        #        d['subsystem_id'],
        #        'mmol*gDW-1*hr-1',
        #        d['mean_difference'],
        #        d['test_stat'],
        #        d['test_description'],
        #        d['pvalue'],
        #        None,None,None,None,None,
        #        d['fold_change'],
        #        True,None
        #        )
        #    self.session.add(row);
        #self.session.commit();
