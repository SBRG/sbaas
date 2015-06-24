from sbaas.analysis.analysis_base import *
from sbaas.analysis.analysis_stage01_physiology.stage01_physiology_query import stage01_physiology_query

class stage02_physiology_query(stage01_physiology_query): 
    def __init__(self,session_I=None):
        if session_I: self.session = session_I;
        else: self.session = Session();       
    ## Query from data_stage01_physiology_ratesAverages:
    # query met_ids from data_stage01_physiology_ratesAverages
    def get_metID_experimentIDAndSampleNameAbbreviation_dataStage01PhysiologyRatesAverages(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry rate data by sample id and met id that are used from
        the experiment'''
        try:
            data = self.session.query(data_stage01_physiology_ratesAverages.sample_name_abbreviation,
                    data_stage01_physiology_ratesAverages.met_id).filter(
                    data_stage01_physiology_ratesAverages.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_ratesAverages.used_.is_(True),
                    data_stage01_physiology_ratesAverages.sample_name_abbreviation.like(sample_name_abbreviation_I)).group_by(
                    data_stage01_physiology_ratesAverages.sample_name_abbreviation,
                    data_stage01_physiology_ratesAverages.met_id).order_by(
                    data_stage01_physiology_ratesAverages.met_id.asc()).all();
            met_id_O = [];
            if data: 
                for d in data:
                    met_id_O.append(d.met_id);
            return met_id_O;
        except SQLAlchemyError as e:
            print(e);
    # query rate from data_stage01_physiology_ratesAverages
    def get_rateData_experimentIDAndSampleNameAbbreviationAndMetID_dataStage01PhysiologyRatesAverages(self,experiment_id_I,sample_name_abbreviation_I,met_id_I):
        '''Querry rate data by sample id and met id that are used from
        the experiment'''
        try:
            data = self.session.query(data_stage01_physiology_ratesAverages.slope_average,
                    data_stage01_physiology_ratesAverages.intercept_average,
                    data_stage01_physiology_ratesAverages.rate_average,
                    data_stage01_physiology_ratesAverages.rate_lb,
                    data_stage01_physiology_ratesAverages.rate_ub,
                    data_stage01_physiology_ratesAverages.rate_units,
                    data_stage01_physiology_ratesAverages.rate_var).filter(
                    data_stage01_physiology_ratesAverages.met_id.like(met_id_I),
                    data_stage01_physiology_ratesAverages.experiment_id.like(experiment_id_I),
                    data_stage01_physiology_ratesAverages.used_.is_(True),
                    data_stage01_physiology_ratesAverages.sample_name_abbreviation.like(sample_name_abbreviation_I)).first();
            slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var = None,None,None,None,None,None,None;
            if data: 
                slope_average, intercept_average,\
                    rate_average, rate_lb, rate_ub, rate_units, rate_var = data.slope_average, data.intercept_average,\
                    data.rate_average, data.rate_lb, data.rate_ub, data.rate_units, data.rate_var;
            return slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage02_physiology_simulation
    # query sample_name_abbreviations from data_stage02_physiology_simulation
    def get_sampleNameAbbreviations_experimentID_dataStage02PhysiologySimulation(self,experiment_id_I):
        '''Querry sample_name_abbreviations that are used from the experiment'''
        try:
            data = self.session.query(data_stage02_physiology_simulation.sample_name_abbreviation).filter(
                    data_stage02_physiology_simulation.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_simulation.used_.is_(True)).group_by(
                    data_stage02_physiology_simulation.sample_name_abbreviation).order_by(
                    data_stage02_physiology_simulation.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            if data: 
                for d in data:
                    sample_name_abbreviations_O.append(d.sample_name_abbreviation);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndModelID_dataStage02PhysiologySimulation(self,experiment_id_I,model_id_I):
        '''Querry sample_name_abbreviations that are used from the experiment'''
        try:
            data = self.session.query(data_stage02_physiology_simulation.sample_name_abbreviation).filter(
                    data_stage02_physiology_simulation.model_id.like(model_id_I),
                    data_stage02_physiology_simulation.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_simulation.used_.is_(True)).group_by(
                    data_stage02_physiology_simulation.sample_name_abbreviation).order_by(
                    data_stage02_physiology_simulation.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            if data: 
                for d in data:
                    sample_name_abbreviations_O.append(d.sample_name_abbreviation);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    #def get_sampleNameAbbreviations_experimentIDAndModelIDAndTimePoint_dataStage02PhysiologySimulation(self,experiment_id_I,model_id_I,time_point_I):
    #    '''Querry sample_name_abbreviations that are used from the experiment'''
    #    try:
    #        data = self.session.query(data_stage02_physiology_simulation.sample_name_abbreviation).filter(
    #                data_stage02_physiology_simulation.model_id.like(model_id_I),
    #                data_stage02_physiology_simulation.time_point.like(time_point_I),
    #                data_stage02_physiology_simulation.experiment_id.like(experiment_id_I),
    #                data_stage02_physiology_simulation.used_.is_(True)).group_by(
    #                data_stage02_physiology_simulation.sample_name_abbreviation).order_by(
    #                data_stage02_physiology_simulation.sample_name_abbreviation.asc()).all();
    #        sample_name_abbreviations_O = [];
    #        if data: 
    #            for d in data:
    #                sample_name_abbreviations_O.append(d.sample_name_abbreviation);
    #        return sample_name_abbreviations_O;
    #    except SQLAlchemyError as e:
    #        print(e);
    ## query time_points from data_stage02_physiology_simulation
    #def get_timePoints_experimentIDAndModelID_dataStage02PhysiologySimulation(self,experiment_id_I,model_id_I):
    #    '''Querry time-points that are used from the experiment'''
    #    try:
    #        data = self.session.query(data_stage02_physiology_simulation.time_point).filter(
    #                data_stage02_physiology_simulation.model_id.like(model_id_I),
    #                data_stage02_physiology_simulation.experiment_id.like(experiment_id_I),
    #                data_stage02_physiology_simulation.used_.is_(True)).group_by(
    #                data_stage02_physiology_simulation.time_point).order_by(
    #                data_stage02_physiology_simulation.time_point.asc()).all();
    #        time_points_O = [];
    #        if data: 
    #            for d in data:
    #                time_points_O.append(d.time_point);
    #        return time_points_O;
    #    except SQLAlchemyError as e:
    #        print(e);
    # query model_ids from data_stage02_physiology_simulation
    def get_modelID_experimentID_dataStage02PhysiologySimulation(self,experiment_id_I):
        '''Querry model_ids that are used from the experiment'''
        try:
            data = self.session.query(data_stage02_physiology_simulation.model_id).filter(
                    data_stage02_physiology_simulation.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_simulation.used_.is_(True)).group_by(
                    data_stage02_physiology_simulation.model_id).order_by(
                    data_stage02_physiology_simulation.model_id.asc()).all();
            model_ids_O = [];
            if data: 
                for d in data:
                    model_ids_O.append(d.model_id);
            return model_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_modelID_experimentIDAndSampleNameAbbreviations_dataStage02PhysiologySimulation(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry model_ids for the sample_name_abbreviation that are used from the experiment'''
        try:
            data = self.session.query(data_stage02_physiology_simulation.model_id).filter(
                    data_stage02_physiology_simulation.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_simulation.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_simulation.used_.is_(True)).group_by(
                    data_stage02_physiology_simulation.model_id).order_by(
                    data_stage02_physiology_simulation.model_id.asc()).all();
            model_ids_O = [];
            if data: 
                for d in data:
                    model_ids_O.append(d.model_id);
            return model_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # query simulation_id
    def get_simulationID_experimentIDAndSampleNameAbbreviationsAndModelID_dataStage02PhysiologySimulation(self,experiment_id_I,sample_name_abbreviation_I,model_id_I):
        '''Querry simulation_ids for the sample_name_abbreviation that are used from the experiment'''
        try:
            data = self.session.query(data_stage02_physiology_simulation.simulation_id).filter(
                    data_stage02_physiology_simulation.model_id.like(model_id_I),
                    data_stage02_physiology_simulation.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_simulation.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_simulation.used_.is_(True)).group_by(
                    data_stage02_physiology_simulation.simulation_id).order_by(
                    data_stage02_physiology_simulation.simulation_id.asc()).all();
            simulation_ids_O = [];
            if data: 
                for d in data:
                    simulation_ids_O.append(d.simulation_id);
            return simulation_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_simulationID_experimentID_dataStage02PhysiologySimulation(self,experiment_id_I):
        '''Querry simulation_ids that are used from the experiment'''
        try:
            data = self.session.query(data_stage02_physiology_simulation.simulation_id).filter(
                    data_stage02_physiology_simulation.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_simulation.used_.is_(True)).group_by(
                    data_stage02_physiology_simulation.simulation_id).order_by(
                    data_stage02_physiology_simulation.simulation_id.asc()).all();
            simulation_ids_O = [];
            if data: 
                for d in data:
                    simulation_ids_O.append(d.simulation_id);
            return simulation_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # query rows from data_stage02_physiology_simulation
    def get_rows_simulationID_dataStage02PhysiologySimulation(self,simulation_id_I):
        '''Querry rows that are used from the simulation'''
        try:
            data = self.session.query(data_stage02_physiology_simulation).filter(
                    data_stage02_physiology_simulation.simulation_id.like(simulation_id_I),
                    data_stage02_physiology_simulation.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append({
                            'simulation_id':d.simulation_id,
                            'experiment_id':d.experiment_id,
                            'model_id':d.model_id,
                            'sample_name_abbreviation':d.sample_name_abbreviation,
                            #'time_point':d.time_point,
                            'simulation_type':d.simulation_type,
                            'used_':d.used_,
                            'comment_':d.comment_});
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
            
    ## Query from data_stage02_physiology_models
    # query row from data_stage02_physiology_models
    def get_row_modelID_dataStage02PhysiologyModels(self,model_id_I):
        '''Querry rows by model_id that are used'''
        try:
            data = self.session.query(data_stage02_physiology_models).filter(
                    data_stage02_physiology_models.model_id.like(model_id_I)).order_by(
                    data_stage02_physiology_models.model_id.asc()).all();
            rows_O = {};
            if len(data)>1:
                print('multiple rows retrieved!');
            if data: 
                for d in data:
                    row_tmp = {'model_id':d.model_id,
                                'model_name':d.model_name,
                                'model_description':d.model_description,
                                'model_file':d.model_file,
                                'file_type':d.file_type,
                                'date':d.date};
                    rows_O.update(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
            
    ## Query from data_stage02_physiology_measuredFluxes
    # query rows from data_stage02_physiology_measuredFluxes
    def get_rows_experimentIDAndSampleNameAbbreviation_dataStage02PhysiologyMeasuredFluxes(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry rows by model_id that are used'''
        try:
            data = self.session.query(data_stage02_physiology_measuredFluxes).filter(
                    data_stage02_physiology_measuredFluxes.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_measuredFluxes.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_measuredFluxes.used_.is_(True)).order_by(
                    data_stage02_physiology_measuredFluxes.model_id.asc(),
                    data_stage02_physiology_measuredFluxes.rxn_id.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'experiment_id':d.experiment_id,
                    'model_id':d.model_id,
                    'sample_name_abbreviation':d.sample_name_abbreviation,
                    #'time_point':d.time_point,
                    'rxn_id':d.rxn_id,
                    'flux_average':d.flux_average,
                    'flux_stdev':d.flux_stdev,
                    'flux_lb':d.flux_lb,
                    'flux_ub':d.flux_ub,
                    'flux_units':d.flux_units,
                    'used_':d.used_,
                    'comment_':d.comment_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02PhysiologyMeasuredFluxes(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Querry rows by model_id that are used'''
        try:
            data = self.session.query(data_stage02_physiology_measuredFluxes).filter(
                    data_stage02_physiology_measuredFluxes.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_measuredFluxes.model_id.like(model_id_I),
                    data_stage02_physiology_measuredFluxes.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_measuredFluxes.used_.is_(True)).order_by(
                    data_stage02_physiology_measuredFluxes.model_id.asc(),
                    data_stage02_physiology_measuredFluxes.rxn_id.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'experiment_id':d.experiment_id,
                    'model_id':d.model_id,
                    'sample_name_abbreviation':d.sample_name_abbreviation,
                    #'time_point':d.time_point,
                    'rxn_id':d.rxn_id,
                    'flux_average':d.flux_average,
                    'flux_stdev':d.flux_stdev,
                    'flux_lb':d.flux_lb,
                    'flux_ub':d.flux_ub,
                    'flux_units':d.flux_units,
                    'used_':d.used_,
                    'comment_':d.comment_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage02_physiology_sampledData
    # query rows from data_stage02_physiology_sampledData    
    def get_rows_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage02PhysiologySampledData(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage02_physiology_sampledData).filter(
                    data_stage02_physiology_sampledData.model_id.like(model_id_I),
                    data_stage02_physiology_sampledData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_sampledData.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_sampledData.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    data_tmp = {'experiment_id':d.experiment_id,
                'model_id':d.model_id,
                'sample_name_abbreviation':d.sample_name_abbreviation,
                'rxn_id':d.rxn_id,
                'flux_units':d.flux_units,
                'sampling_ave':d.sampling_ave,
                'sampling_var':d.sampling_var,
                'sampling_lb':d.sampling_lb,
                'sampling_ub':d.sampling_ub,
                'used_':d.used_,
                'comment_':d.comment_};
                    rows_O.append(data_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);   
    def get_rowsDict_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage02PhysiologySampledData(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage02_physiology_sampledData).filter(
                    data_stage02_physiology_sampledData.model_id.like(model_id_I),
                    data_stage02_physiology_sampledData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_sampledData.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_sampledData.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if d.rxn_id in rows_O:
                        print('duplicate rxn_ids found!');
                    else:
                        rows_O[d.rxn_id]={'sampling_ave':d.sampling_ave,
                'sampling_var':d.sampling_var,
                'sampling_lb':d.sampling_lb,
                'sampling_ub':d.sampling_ub};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscherLbUb_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage02PhysiologySampledData(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage02_physiology_sampledData).filter(
                    data_stage02_physiology_sampledData.model_id.like(model_id_I),
                    data_stage02_physiology_sampledData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_sampledData.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_sampledData.used_.is_(True)).all();
            rows_O = [None,None];
            rows_O[0] = {};
            rows_O[1] = {}
            if data: 
                for d in data:
                    rows_O[0][d.rxn_id]=d.sampling_lb;
                    rows_O[1][d.rxn_id]=d.sampling_ub;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscher_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage02PhysiologySampledData(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage02_physiology_sampledData).filter(
                    data_stage02_physiology_sampledData.model_id.like(model_id_I),
                    data_stage02_physiology_sampledData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_physiology_sampledData.experiment_id.like(experiment_id_I),
                    data_stage02_physiology_sampledData.used_.is_(True)).all();
            rows_O = {}
            if data: 
                for d in data:
                    rows_O[d.rxn_id]=d.sampling_ave;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    ##  Query from data_stage02_physiology_simulationParameters
    # query rows from data_stage02_physiology_simulation
    def get_rows_simulationID_dataStage02PhysiologySimulationParameters(self,simulation_id_I):
        '''Querry rows that are used from the simulationParameters'''
        try:
            data = self.session.query(data_stage02_physiology_simulationParameters).filter(
                    data_stage02_physiology_simulationParameters.simulation_id.like(simulation_id_I),
                    data_stage02_physiology_simulationParameters.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append({
                            'simulation_id':d.simulation_id,
                            #'simulation_dateAndTime':d.simulation_dateAndTime,
                            'solver_id':d.solver_id,
                            'n_points':d.n_points,
                            'n_steps':d.n_steps,
                            'max_time':d.max_time,
                            'sampler_id':d.sampler_id,
                            #'solve_time':d.solve_time,
                            #'solve_time_units':d.solve_time_units,
                            'used_':d.used_,
                            'comment_':d.comment_});
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    ##  Query from data_stage02_physiology_sampledPoints
    # query rows from data_stage02_physiology_sampledPoints
    def get_rows_simulationID_dataStage02PhysiologySampledPoints(self,simulation_id_I):
        '''Querry rows that are used from sampledPoints'''
        try:
            data = self.session.query(data_stage02_physiology_sampledPoints).filter(
                    data_stage02_physiology_sampledPoints.simulation_id.like(simulation_id_I),
                    data_stage02_physiology_sampledPoints.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append({
                            'simulation_id':d.simulation_id,
                            'simulation_dateAndTime':d.simulation_dateAndTime,
                            'mixed_fraction':d.mixed_fraction,
                            'data_dir':d.data_dir,
                            'infeasible_loops':d.infeasible_loops,
                            'used_':d.used_,
                            'comment_':d.comment_});
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage02_physiology_pairWiseTest
    
    # Query data from data_stage02_physiology_pairWiseTest
    def get_RDataList_simulationIDs_dataStage02PhysiologyPairWiseTest(self,simulation_id_1_I,simulation_id_2_I):
        """get data from simulation_ids 1 and 2"""
        #Tested
        try:
            data = self.session.query(
                    data_stage02_physiology_pairWiseTest.simulation_id_1,
                    data_stage02_physiology_pairWiseTest.simulation_id_2,
                    data_stage02_physiology_pairWiseTest.rxn_id,
                    data_stage02_physiology_pairWiseTest.test_stat,
                    data_stage02_physiology_pairWiseTest.test_description,
                    data_stage02_physiology_pairWiseTest.pvalue,
                    data_stage02_physiology_pairWiseTest.pvalue_corrected,
                    data_stage02_physiology_pairWiseTest.pvalue_corrected_description,
                    data_stage02_physiology_pairWiseTest.mean,
                    data_stage02_physiology_pairWiseTest.ci_lb,
                    data_stage02_physiology_pairWiseTest.ci_ub,
                    data_stage02_physiology_pairWiseTest.ci_level,
                    data_stage02_physiology_pairWiseTest.fold_change).filter(
                    data_stage02_physiology_pairWiseTest.simulation_id_1.like(simulation_id_1_I),
                    data_stage02_physiology_pairWiseTest.simulation_id_2.like(simulation_id_2_I),
                    data_stage02_physiology_pairWiseTest.used_.is_(True)).group_by(
                    data_stage02_physiology_pairWiseTest.simulation_id_1,
                    data_stage02_physiology_pairWiseTest.simulation_id_2,
                    data_stage02_physiology_pairWiseTest.rxn_id,
                    data_stage02_physiology_pairWiseTest.test_stat,
                    data_stage02_physiology_pairWiseTest.test_description,
                    data_stage02_physiology_pairWiseTest.pvalue,
                    data_stage02_physiology_pairWiseTest.pvalue_corrected,
                    data_stage02_physiology_pairWiseTest.pvalue_corrected_description,
                    data_stage02_physiology_pairWiseTest.mean,
                    data_stage02_physiology_pairWiseTest.ci_lb,
                    data_stage02_physiology_pairWiseTest.ci_ub,
                    data_stage02_physiology_pairWiseTest.ci_level,
                    data_stage02_physiology_pairWiseTest.fold_change).order_by(
                    data_stage02_physiology_pairWiseTest.simulation_id_2.asc(),
                    data_stage02_physiology_pairWiseTest.rxn_id.asc()).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['simulation_id_1'] = d.simulation_id_1;
                data_1['simulation_id_2'] = d.simulation_id_2;
                data_1['rxn_id'] = d.rxn_id;
                data_1['test_stat'] = d.test_stat;
                data_1['test_description'] = d.test_description;
                data_1['pvalue_negLog10'] = None;
                data_1['pvalue_corrected_description'] = None
                if d.pvalue_corrected:
                    data_1['pvalue_corrected_negLog10'] = -log(d.pvalue_corrected,10);
                if d.pvalue:
                    data_1['pvalue_negLog10'] = -log(d.pvalue,10);
                data_1['pvalue_corrected_description'] = d.pvalue_corrected_description;
                data_1['mean'] = d.mean;
                data_1['ci_lb'] = d.ci_lb;
                data_1['ci_ub'] = d.ci_ub;
                data_1['ci_level'] = d.ci_level;
                data_1['fold_change'] = d.fold_change;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);

