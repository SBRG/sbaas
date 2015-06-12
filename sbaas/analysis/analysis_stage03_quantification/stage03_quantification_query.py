from analysis.analysis_base import *
import re
from math import copysign

class stage03_quantification_query(base_analysis):
    # Query data from data_stage01_quantification_averagesMIgeo:
    def get_rows_experimentID_dataStage01AveragesMIgeo(self, experiment_id_I):
        """get data from experiment ID"""
        try:
            data = self.session.query(data_stage01_quantification_averagesMIgeo).filter(
                    data_stage01_quantification_averagesMIgeo.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_averagesMIgeo.used_.is_(True)).all();
            data_O = [];
            for d in data: 
                data_O.append({"experiment_id":d.experiment_id,
                    "sample_name_abbreviation":d.sample_name_abbreviation,
                    "time_point":d.time_point,
                    "component_group_name":d.component_group_name,
                    "component_name":d.component_name,
                    "n_replicates":d.n_replicates,
                    "calculated_concentration_average":d.calculated_concentration_average,
                    "calculated_concentration_var":d.calculated_concentration_var,
                    "calculated_concentration_lb":d.calculated_concentration_lb,
                    "calculated_concentration_ub":d.calculated_concentration_ub,
                    "calculated_concentration_units":d.calculated_concentration_units,
                    "used_":d.used_})
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage03_quantification_simulation
    # query sample_name_abbreviations from data_stage03_quantification_simulation
    def get_sampleNameAbbreviations_experimentID_dataStage03QuantificationSimulation(self,experiment_id_I):
        '''Querry sample_name_abbreviations that are used from the experiment'''
        try:
            data = self.session.query(data_stage03_quantification_simulation.sample_name_abbreviation).filter(
                    data_stage03_quantification_simulation.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_simulation.used_.is_(True)).group_by(
                    data_stage03_quantification_simulation.sample_name_abbreviation).order_by(
                    data_stage03_quantification_simulation.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            if data: 
                for d in data:
                    sample_name_abbreviations_O.append(d.sample_name_abbreviation);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndModelID_dataStage03QuantificationSimulation(self,experiment_id_I,model_id_I):
        '''Querry sample_name_abbreviations that are used from the experiment'''
        try:
            data = self.session.query(data_stage03_quantification_simulation.sample_name_abbreviation).filter(
                    data_stage03_quantification_simulation.model_id.like(model_id_I),
                    data_stage03_quantification_simulation.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_simulation.used_.is_(True)).group_by(
                    data_stage03_quantification_simulation.sample_name_abbreviation).order_by(
                    data_stage03_quantification_simulation.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            if data: 
                for d in data:
                    sample_name_abbreviations_O.append(d.sample_name_abbreviation);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndModelIDAndTimePoint_dataStage03QuantificationSimulation(self,experiment_id_I,model_id_I,time_point_I):
        '''Querry sample_name_abbreviations that are used from the experiment'''
        try:
            data = self.session.query(data_stage03_quantification_simulation.sample_name_abbreviation).filter(
                    data_stage03_quantification_simulation.model_id.like(model_id_I),
                    data_stage03_quantification_simulation.time_point.like(time_point_I),
                    data_stage03_quantification_simulation.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_simulation.used_.is_(True)).group_by(
                    data_stage03_quantification_simulation.sample_name_abbreviation).order_by(
                    data_stage03_quantification_simulation.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            if data: 
                for d in data:
                    sample_name_abbreviations_O.append(d.sample_name_abbreviation);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    # query time_points from data_stage03_quantification_simulation
    def get_timePoints_experimentIDAndModelID_dataStage03QuantificationSimulation(self,experiment_id_I,model_id_I):
        '''Querry time-points that are used from the experiment'''
        try:
            data = self.session.query(data_stage03_quantification_simulation.time_point).filter(
                    data_stage03_quantification_simulation.model_id.like(model_id_I),
                    data_stage03_quantification_simulation.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_simulation.used_.is_(True)).group_by(
                    data_stage03_quantification_simulation.time_point).order_by(
                    data_stage03_quantification_simulation.time_point.asc()).all();
            time_points_O = [];
            if data: 
                for d in data:
                    time_points_O.append(d.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # query model_ids from data_stage03_quantification_simulation
    def get_modelID_experimentID_dataStage03QuantificationSimulation(self,experiment_id_I):
        '''Querry model_ids that are used from the experiment'''
        try:
            data = self.session.query(data_stage03_quantification_simulation.model_id).filter(
                    data_stage03_quantification_simulation.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_simulation.used_.is_(True)).group_by(
                    data_stage03_quantification_simulation.model_id).order_by(
                    data_stage03_quantification_simulation.model_id.asc()).all();
            model_ids_O = [];
            if data: 
                for d in data:
                    model_ids_O.append(d.model_id);
            return model_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_modelID_experimentIDAndSampleNameAbbreviations_dataStage03QuantificationSimulation(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry model_ids for the sample_name_abbreviation that are used from the experiment'''
        try:
            data = self.session.query(data_stage03_quantification_simulation.model_id).filter(
                    data_stage03_quantification_simulation.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_simulation.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_simulation.used_.is_(True)).group_by(
                    data_stage03_quantification_simulation.model_id).order_by(
                    data_stage03_quantification_simulation.model_id.asc()).all();
            model_ids_O = [];
            if data: 
                for d in data:
                    model_ids_O.append(d.model_id);
            return model_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # query rows from data_stage03_quantification_simulation
    def get_rows_simulationID_dataStage03QuantificationSimulation(self,simulation_id_I):
        '''Querry rows that are used from the simulation'''
        try:
            data = self.session.query(data_stage03_quantification_simulation).filter(
                    data_stage03_quantification_simulation.simulation_id.like(simulation_id_I),
                    data_stage03_quantification_simulation.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append({
                            'simulation_id':d.simulation_id,
                            'experiment_id':d.experiment_id,
                            'model_id':d.model_id,
                            'sample_name_abbreviation':d.sample_name_abbreviation,
                            'time_point':d.time_point,
                            'simulation_type':d.simulation_type,
                            'used_':d.used_,
                            'comment_':d.comment_});
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
            
    ## Query from data_stage03_quantification_models
    # query row from data_stage03_quantification_models
    def get_row_modelID_dataStage03QuantificationModels(self,model_id_I):
        '''Querry rows by model_id that are used'''
        try:
            data = self.session.query(data_stage03_quantification_models).filter(
                    data_stage03_quantification_models.model_id.like(model_id_I)).order_by(
                    data_stage03_quantification_models.model_id.asc()).all();
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

    ##  Query from data_stage03_quantification_simulationParameters
    # query rows from data_stage03_quantification_simulation
    def get_rows_simulationID_dataStage03QuantificationSimulationParameters(self,simulation_id_I):
        '''Querry rows that are used from the simulationParameters'''
        try:
            data = self.session.query(data_stage03_quantification_simulationParameters).filter(
                    data_stage03_quantification_simulationParameters.simulation_id.like(simulation_id_I),
                    data_stage03_quantification_simulationParameters.used_.is_(True)).all();
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

    ## Query from data_stage03_quantification_otherData
    # query rows from data data_stage03_quantification_otherData
    def get_rows_experimentIDAndTimePointAndSampleNameAbbreviation_dataStage03QuantificationOtherData(self,experiment_id_I,time_point_I,sample_name_abbreviation_I):
        '''Querry rows by model_id that are used'''
        try:
            data = self.session.query(data_stage03_quantification_otherData).filter(
                    data_stage03_quantification_otherData.time_point.like(time_point_I),
                    data_stage03_quantification_otherData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_otherData.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_otherData.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {'experiment_id':d.experiment_id,
                            'sample_name_abbreviation':d.sample_name_abbreviation,
                            'time_point':d.time_point,
                            'compartment_id':d.compartment_id,
                            'pH':d.pH,
                            'temperature':d.temperature,
                            'temperature_units':d.temperature_units,
                            'ionic_strength':d.ionic_strength,
                            'ionic_strength_units':d.ionic_strength_units,
                            'used_':d.used_,
                            'comment_':d.comment_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsFormatted_experimentIDAndTimePointAndSampleNameAbbreviation_dataStage03QuantificationOtherData(self,experiment_id_I,time_point_I,sample_name_abbreviation_I):
        '''Querry rows by model_id that are used'''
        try:
            data = self.session.query(data_stage03_quantification_otherData).filter(
                    data_stage03_quantification_otherData.time_point.like(time_point_I),
                    data_stage03_quantification_otherData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_otherData.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_otherData.used_.is_(True)).all();
            pH_O = {};
            temperature_O = {};
            ionic_strength_O = {};
            if data: 
                for d in data:
                    pH_O[d.compartment_id]={'pH':d.pH};
                    temperature_O[d.compartment_id]={'temperature':d.temperature,
                            'temperature_units':d.temperature_units};
                    ionic_strength_O[d.compartment_id]={'ionic_strength':d.ionic_strength,
                            'ionic_strength_units':d.ionic_strength_units};
            return pH_O,temperature_O,ionic_strength_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage03_quantification_metid2keggid
    # query rows from data data_stage03_quantification_metid2keggid
    def get_rows_dataStage03QuantificationMetid2keggid(self):
        '''Querry rows that are used'''
        try:
            data = self.session.query(data_stage03_quantification_metid2keggid).filter(
                    data_stage03_quantification_metid2keggid.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {
                            'met_id':d.met_id,
                            'KEGG_ID':d.KEGG_id,
                            'used_':d.used_,
                            'comments_':d.comments_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsDict_dataStage03QuantificationMetid2keggid(self):
        '''Querry rows that are used'''
        try:
            data = self.session.query(data_stage03_quantification_metid2keggid).filter(
                    data_stage03_quantification_metid2keggid.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    row_tmp = {};
                    row_tmp[d.met_id] = d.KEGG_id;
                    rows_O.update(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
            
    ## Query from data_stage03_quantification_dG0_f
    # query rows from data data_stage03_quantification_dG0_f
    def get_rows_dataStage03QuantificationDG0f(self):
        '''Querry rows that are used'''
        try:
            data = self.session.query(data_stage03_quantification_dG0_f).filter(
                    data_stage03_quantification_dG0_f.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    row_tmp = {
                            'reference_id':d.reference_id,
                            'met_name':d.met_name,
                            'met_id':d.met_id,
                            'KEGG_ID':d.KEGG_id,
                            'priority':d.priority,
                            'dG0_f':d.dG0_f,
                            'dG0_f_var':d.dG0_f_var,
                            'dG0_f_units':d.dG0_f_units,
                            'temperature':d.temperature,
                            'temperature_units':d.temperature_units,
                            'ionic_strength':d.ionic_strength,
                            'ionic_strength_units':d.ionic_strength_units,
                            'pH':d.pH,
                            'pH_units':d.pH_units,
                            'used_':d.used_,
                            'comments_':d.comments_};
                    rows_O.append(row_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsDict_dataStage03QuantificationDG0f(self):
        '''Querry rows that are used'''
        try:
            data = self.session.query(data_stage03_quantification_dG0_f).filter(
                    data_stage03_quantification_dG0_f.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if d.KEGG_id in rows_O:
                        rows_O[d.KEGG_id].append({
                            'reference_id':d.reference_id,
                            'priority':d.priority,
                            'dG0_f':d.dG0_f,
                            'dG0_f_var':d.dG0_f_var,
                            'dG0_f_units':d.dG0_f_units});
                    else:
                        rows_O[d.KEGG_id] = [];
                        rows_O[d.KEGG_id].append({
                            'reference_id':d.reference_id,
                            'priority':d.priority,
                            'dG0_f':d.dG0_f,
                            'dG0_f_var':d.dG0_f_var,
                            'dG0_f_units':d.dG0_f_units});
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage03_quantification_simulatedData
    # query rows from data_stage03_quantification_simulatedData    
    def get_rows_experimentIDAndModelID_dataStage03QuantificationSimulatedData(self,experiment_id_I,model_id_I):
        '''Query rows that are used'''
        try:
            data = self.session.query(data_stage03_quantification_simulatedData).filter(
                    data_stage03_quantification_simulatedData.model_id.like(model_id_I),
                    data_stage03_quantification_simulatedData.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_simulatedData.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    data_tmp = {'experiment_id':d.experiment_id,
                        'model_id':d.model_id,
                        'rxn_id':d.rxn_id,
                        'fba_flux':d.fba_flux,
                        'fva_minimum':d.fva_minimum,
                        'fva_maximum':d.fva_maximum,
                        'flux_units':d.flux_units,
                        'sra_gr':d.sra_gr,
                        'sra_gr_ratio':d.sra_gr_ratio,
                        'used_':d.used_,
                        'comment_':d.comment_};
                    rows_O.append(data_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);   
    def get_rowsDict_experimentIDAndModelID_dataStage03QuantificationSimulatedData(self,experiment_id_I,model_id_I):
        '''Query rows that are used from the metabolomicsData'''
        try:
            data = self.session.query(data_stage03_quantification_simulatedData).filter(
                    data_stage03_quantification_simulatedData.model_id.like(model_id_I),
                    data_stage03_quantification_simulatedData.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_simulatedData.used_.is_(True)).all();
            fva_data_O = {};
            sra_data_O = {};
            if data: 
                for d in data:
                    if d.rxn_id in fva_data_O:
                        print('duplicate rxn_id found!');
                    else:
                        fva_data_O[d.rxn_id]={
                            'minimum':d.fva_minimum,
                            'maximum':d.fva_maximum};
                        sra_data_O[d.rxn_id]={'gr':d.sra_gr,
                            'gr_ratio':d.sra_gr_ratio};
            return fva_data_O,sra_data_O;
        except SQLAlchemyError as e:
            print(e);
    # update rows of data_stage03_quantification_simulatedData    
    def update_dataStage03SimulatedData(self,data_I):
        '''update rows of data_stage03_quantification_simulatedData'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_simulatedData).filter(
                            data_stage03_quantification_simulatedData.experiment_id.like(d['experiment_id']),
                            data_stage03_quantification_simulatedData.model_id.like(d['model_id']),
                            data_stage03_quantification_simulatedData.rxn_id.like(d['rxn_id'])).update(
                            {
                            'fba_flux':d['fba_flux'],
                            'fva_minimum':d['fva_minimum'],
                            'fva_maximum':d['fva_maximum'],
                            'flux_units':d['flux_units'],
                            'sra_gr':d['sra_gr'],
                            'sra_gr_ratio':d['sra_gr_ratio'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
        
    ## Query from data_stage03_quantification_metabolomicsData
    # query rows from data_stage03_quantification_metabolomicsData    
    def get_rows_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationMetabolomicsData(self,experiment_id_I,time_point_I,sample_name_abbreviation_I):
        '''Query rows that are used from the metabolomicsData'''
        try:
            data = self.session.query(data_stage03_quantification_metabolomicsData).filter(
                    data_stage03_quantification_metabolomicsData.time_point.like(time_point_I),
                    data_stage03_quantification_metabolomicsData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_metabolomicsData.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_metabolomicsData.measured.is_(True),
                    data_stage03_quantification_metabolomicsData.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    data_tmp = {'experiment_id':d.experiment_id,
                        'sample_name_abbreviation':d.sample_name_abbreviation,
                        'time_point':d.time_point,
                        'met_id':d.met_id,
                        'concentration':d.concentration,
                        'concentration_var':d.concentration_var,
                        'concentration_units':d.concentration_units,
                        'concentration_lb':d.concentration_lb,
                        'concentration_ub':d.concentration_ub,
                        'measured':d.measured,
                        'used_':d.used_,
                        'comment_':d.comment_};
                    rows_O.append(data_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);   
    def get_rowsDict_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationMetabolomicsData(self,experiment_id_I,time_point_I,sample_name_abbreviation_I):
        '''Query rows that are used from the metabolomicsData'''
        try:
            data = self.session.query(data_stage03_quantification_metabolomicsData).filter(
                    data_stage03_quantification_metabolomicsData.time_point.like(time_point_I),
                    data_stage03_quantification_metabolomicsData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_metabolomicsData.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_metabolomicsData.measured.is_(True),
                    data_stage03_quantification_metabolomicsData.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if d.met_id in rows_O:
                        print('duplicate met_ids found!');
                    else:
                        rows_O[d.met_id]={'concentration':d.concentration,
                            'concentration_var':d.concentration_var,
                            'concentration_units':d.concentration_units,
                            'concentration_lb':d.concentration_lb,
                            'concentration_ub':d.concentration_ub};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscherLbUb_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationMetabolomicsData(self,experiment_id_I,time_point_I,sample_name_abbreviation_I):
        '''Query rows that are used from the metabolomicsData'''
        try:
            data = self.session.query(data_stage03_quantification_metabolomicsData).filter(
                    data_stage03_quantification_metabolomicsData.time_point.like(time_point_I),
                    data_stage03_quantification_metabolomicsData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_metabolomicsData.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_metabolomicsData.measured.is_(True),
                    data_stage03_quantification_metabolomicsData.used_.is_(True)).all();
            rows_O = [None,None];
            rows_O[0] = {};
            rows_O[1] = {}
            if data: 
                for d in data:
                    rows_O[0][self.convert_metid2escherid(d.met_id)]=d.concentration_lb;
                    rows_O[1][self.convert_metid2escherid(d.met_id)]=d.concentration_ub;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscher_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationMetabolomicsData(self,experiment_id_I,time_point_I,sample_name_abbreviation_I):
        '''Query rows that are used from the metabolomicsData'''
        try:
            data = self.session.query(data_stage03_quantification_metabolomicsData).filter(
                    data_stage03_quantification_metabolomicsData.time_point.like(time_point_I),
                    data_stage03_quantification_metabolomicsData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_metabolomicsData.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_metabolomicsData.measured.is_(True),
                    data_stage03_quantification_metabolomicsData.used_.is_(True)).all();
            rows_O = {}
            if data: 
                for d in data:
                    rows_O[self.convert_metid2escherid(d.met_id)]=d.concentration;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
        
    ## Query from data_stage03_quantification_dG_f
    # query rows from data_stage03_quantification_dG_f    
    def get_rows_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDGf(self,experiment_id_I,model_id_I,time_point_I,sample_name_abbreviation_I):
        '''Query rows that are used'''
        try:
            data = self.session.query(data_stage03_quantification_dG_f).filter(
                    data_stage03_quantification_dG_f.model_id.like(model_id_I),
                    data_stage03_quantification_dG_f.time_point.like(time_point_I),
                    data_stage03_quantification_dG_f.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_dG_f.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_dG_f.measured.is_(True),
                    data_stage03_quantification_dG_f.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    data_tmp = {'experiment_id':d.experiment_id,
                    'model_id':d.model_id,
                    'sample_name_abbreviation':d.sample_name_abbreviation,
                    'time_point':d.time_point,
                    'met_name':d.met_name,
                    'met_id':d.met_id,
                    'dG_f':d.dG_f,
                    'dG_f_var':d.dG_f_var,
                    'dG_f_units':d.dG_f_units,
                    'dG_f_lb':d.dG_f_lb,
                    'dG_f_ub':d.dG_f_ub,
                    'temperature':d.temperature,
                    'temperature_units':d.temperature_units,
                    'ionic_strength':d.ionic_strength,
                    'ionic_strength_units':d.ionic_strength_units,
                    'pH':d.pH,
                    'pH_units':d.pH_units,
                    'measured':d.measured,
                    'used_':d.used_,
                    'comment_':d.comment_};
                    rows_O.append(data_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);   
    def get_rowsDict_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDGf(self,experiment_id_I,model_id_I,time_point_I,sample_name_abbreviation_I):
        '''Query rows that are used from the metabolomicsData'''
        try:
            data = self.session.query(data_stage03_quantification_dG_f).filter(
                    data_stage03_quantification_dG_f.model_id.like(model_id_I),
                    data_stage03_quantification_dG_f.time_point.like(time_point_I),
                    data_stage03_quantification_dG_f.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_dG_f.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_dG_f.measured.is_(True),
                    data_stage03_quantification_dG_f.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if d.met_id in rows_O:
                        print('duplicate met_ids found!');
                    else:
                        rows_O[d.met_id]={'dG_f':d.dG_f,
                            'dG_f_var':d.dG_f_var,
                            'dG_f_units':d.dG_f_units,
                            'dG_f_lb':d.dG_f_lb,
                            'dG_f_ub':d.dG_f_ub};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
            
    ## Query from data_stage03_quantification_dG0_r
    # query rows from data_stage03_quantificaton_dG0_r
    def get_rowsDict_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDG0r(self,experiment_id_I,
                                                                                                           model_id_I,
                                                                                                           time_point_I,
                                                                                                           sample_name_abbreviation_I,
                                                                                                 measured_dG_f_coverage_criteria_I=0.0):
        '''Query rows that are used from the dG_r'''
        try:
            data = self.session.query(data_stage03_quantification_dG0_r).filter(
                    data_stage03_quantification_dG0_r.model_id.like(model_id_I),
                    data_stage03_quantification_dG0_r.time_point.like(time_point_I),
                    data_stage03_quantification_dG0_r.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_dG0_r.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_dG0_r.model_id.like(data_stage03_quantification_tcc.model_id),
                    data_stage03_quantification_dG0_r.time_point.like(data_stage03_quantification_tcc.time_point),
                    data_stage03_quantification_dG0_r.sample_name_abbreviation.like(data_stage03_quantification_tcc.sample_name_abbreviation),
                    data_stage03_quantification_dG0_r.experiment_id.like(data_stage03_quantification_tcc.experiment_id),
                    data_stage03_quantification_dG0_r.rxn_id.like(data_stage03_quantification_tcc.rxn_id),
                    data_stage03_quantification_tcc.measured_dG_f_coverage>measured_dG_f_coverage_criteria_I,
                    data_stage03_quantification_dG0_r.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if d.rxn_id in rows_O:
                        print('duplicate rxn_id found!');
                    else:
                        rows_O[d.rxn_id]={
                        'Keq_lb':d.Keq_lb,
                        'Keq_ub':d.Keq_ub,
                        'dG_r':d.dG0_r,
                        'dG_r_var':d.dG0_r_var,
                        'dG_r_units':d.dG0_r_units,
                        'dG_r_lb':d.dG0_r_lb,
                        'dG_r_ub':d.dG0_r_ub};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    # update rows of data_stage03_quantification_dG0_r     
    def update_dataStage03DG0r(self,data_I):
        '''update rows of data_stage03_quantification_dG0_r'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_dG0_r).filter(
                            data_stage03_quantification_dG0_r.experiment_id.like(d['experiment_id']),
                            data_stage03_quantification_dG0_r.model_id.like(d['model_id']),
                            data_stage03_quantification_dG0_r.rxn_id.like(d['rxn_id']),
                            data_stage03_quantification_dG_r.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                            data_stage03_quantification_dG_r.time_point.like(d['time_point'])).update(
                            {
                            'Keq_lb':d['Keq_lb'],
                            'Keq_ub':d['Keq_ub'],
                            'dG0_r':d['dG0_r'],
                            'dG0_r_var':d['dG0_r_var'],
                            'dG0_r_units':d['dG0_r_units'],
                            'dG0_r_lb':d['dG0_r_lb'],
                            'dG0_r_ub':d['dG0_r_ub'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    ## Query from data_stage03_quantification_dG_r
    # query rows from data_stage03_quantification_dG_r   
    def get_rows_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDGr(self,experiment_id_I,
                                                                                                           model_id_I,
                                                                                                           time_point_I,
                                                                                                           sample_name_abbreviation_I,
                                                                                                 measured_concentration_coverage_criteria_I=0.5,
                                                                                                 measured_dG_f_coverage_criteria_I=0.99):
        '''Query rows that are used from the dG_r'''
        try:
            data = self.session.query(data_stage03_quantification_dG_r).filter(
                    data_stage03_quantification_dG_r.model_id.like(model_id_I),
                    data_stage03_quantification_dG_r.time_point.like(time_point_I),
                    data_stage03_quantification_dG_r.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_dG_r.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_dG_r.model_id.like(data_stage03_quantification_tcc.model_id),
                    data_stage03_quantification_dG_r.time_point.like(data_stage03_quantification_tcc.time_point),
                    data_stage03_quantification_dG_r.sample_name_abbreviation.like(data_stage03_quantification_tcc.sample_name_abbreviation),
                    data_stage03_quantification_dG_r.experiment_id.like(data_stage03_quantification_tcc.experiment_id),
                    data_stage03_quantification_dG_r.rxn_id.like(data_stage03_quantification_tcc.rxn_id),
                    data_stage03_quantification_tcc.measured_concentration_coverage>measured_concentration_coverage_criteria_I,
                    data_stage03_quantification_tcc.measured_dG_f_coverage>measured_dG_f_coverage_criteria_I,
                    data_stage03_quantification_tcc.used_.is_(True),
                    data_stage03_quantification_dG_r.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    data_tmp = {'experiment_id':d.experiment_id,
                        'model_id':d.model_id,
                        'sample_name_abbreviation':d.sample_name_abbreviation,
                        'time_point':d.time_point,
                        'rxn_id':d.rxn_id,
                        'Keq_lb':d.Keq_lb,
                        'Keq_ub':d.Keq_ub,
                        'dG_r':d.dG_r,
                        'dG_r_var':d.dG_r_var,
                        'dG_r_units':d.dG_r_units,
                        'dG_r_lb':d.dG_r_lb,
                        'dG_r_ub':d.dG_r_ub,
                        'displacement_lb':d.displacement_lb,
                        'displacement_ub':d.displacement_ub,
                        'Q_lb':d.Q_lb,
                        'Q_ub':d.Q_ub,
                        'used_':d.used_,
                        'comment_':d.comment_};
                    rows_O.append(data_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);   
    def get_rowsDict_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDGr(self,experiment_id_I,
                                                                                                           model_id_I,
                                                                                                           time_point_I,
                                                                                                           sample_name_abbreviation_I,
                                                                                                 measured_concentration_coverage_criteria_I=0.0,
                                                                                                 measured_dG_f_coverage_criteria_I=0.0):
        '''Query rows that are used from the dG_r'''
        try:
            data = self.session.query(data_stage03_quantification_dG_r).filter(
                    data_stage03_quantification_dG_r.model_id.like(model_id_I),
                    data_stage03_quantification_dG_r.time_point.like(time_point_I),
                    data_stage03_quantification_dG_r.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_dG_r.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_dG_r.model_id.like(data_stage03_quantification_tcc.model_id),
                    data_stage03_quantification_dG_r.time_point.like(data_stage03_quantification_tcc.time_point),
                    data_stage03_quantification_dG_r.sample_name_abbreviation.like(data_stage03_quantification_tcc.sample_name_abbreviation),
                    data_stage03_quantification_dG_r.experiment_id.like(data_stage03_quantification_tcc.experiment_id),
                    data_stage03_quantification_dG_r.rxn_id.like(data_stage03_quantification_tcc.rxn_id),
                    data_stage03_quantification_tcc.measured_concentration_coverage>measured_concentration_coverage_criteria_I,
                    data_stage03_quantification_tcc.measured_dG_f_coverage>measured_dG_f_coverage_criteria_I,
                    data_stage03_quantification_dG_r.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if d.rxn_id in rows_O:
                        print('duplicate rxn_id found!');
                    else:
                        rows_O[d.rxn_id]={
                        'Keq_lb':d.Keq_lb,
                        'Keq_ub':d.Keq_ub,
                        'dG_r':d.dG_r,
                        'dG_r_var':d.dG_r_var,
                        'dG_r_units':d.dG_r_units,
                        'dG_r_lb':d.dG_r_lb,
                        'dG_r_ub':d.dG_r_ub};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscherDGrLbUb_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDGr(self,experiment_id_I,
                                                                                                           model_id_I,
                                                                                                           time_point_I,
                                                                                                           sample_name_abbreviation_I,
                                                                                                 measured_concentration_coverage_criteria_I=0.5,
                                                                                                 measured_dG_f_coverage_criteria_I=0.99):
        '''Query rows that are used from the dG_r'''
        try:
            data = self.session.query(data_stage03_quantification_dG_r).filter(
                    data_stage03_quantification_dG_r.model_id.like(model_id_I),
                    data_stage03_quantification_dG_r.time_point.like(time_point_I),
                    data_stage03_quantification_dG_r.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_dG_r.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_dG_r.model_id.like(data_stage03_quantification_tcc.model_id),
                    data_stage03_quantification_dG_r.time_point.like(data_stage03_quantification_tcc.time_point),
                    data_stage03_quantification_dG_r.sample_name_abbreviation.like(data_stage03_quantification_tcc.sample_name_abbreviation),
                    data_stage03_quantification_dG_r.experiment_id.like(data_stage03_quantification_tcc.experiment_id),
                    data_stage03_quantification_dG_r.rxn_id.like(data_stage03_quantification_tcc.rxn_id),
                    data_stage03_quantification_tcc.measured_concentration_coverage>measured_concentration_coverage_criteria_I,
                    data_stage03_quantification_tcc.measured_dG_f_coverage>measured_dG_f_coverage_criteria_I,
                    data_stage03_quantification_tcc.used_.is_(True),
                    data_stage03_quantification_dG_r.used_.is_(True)).all();
            rows_O = [None,None];
            rows_O[0] = {};
            rows_O[1] = {}
            if data: 
                for d in data:
                    rows_O[0][d.rxn_id]=d.dG_r_lb;
                    rows_O[1][d.rxn_id]=d.dG_r_ub;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsEscherDGr_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDGr(self,experiment_id_I,
                                                                                                           model_id_I,
                                                                                                           time_point_I,
                                                                                                           sample_name_abbreviation_I,
                                                                                                 measured_concentration_coverage_criteria_I=0.5,
                                                                                                 measured_dG_f_coverage_criteria_I=0.99):
        '''Query rows that are used from the dG_r'''
        try:
            data = self.session.query(data_stage03_quantification_dG_r).filter(
                    data_stage03_quantification_dG_r.model_id.like(model_id_I),
                    data_stage03_quantification_dG_r.time_point.like(time_point_I),
                    data_stage03_quantification_dG_r.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_dG_r.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_dG_r.model_id.like(data_stage03_quantification_tcc.model_id),
                    data_stage03_quantification_dG_r.time_point.like(data_stage03_quantification_tcc.time_point),
                    data_stage03_quantification_dG_r.sample_name_abbreviation.like(data_stage03_quantification_tcc.sample_name_abbreviation),
                    data_stage03_quantification_dG_r.experiment_id.like(data_stage03_quantification_tcc.experiment_id),
                    data_stage03_quantification_dG_r.rxn_id.like(data_stage03_quantification_tcc.rxn_id),
                    data_stage03_quantification_tcc.measured_concentration_coverage>measured_concentration_coverage_criteria_I,
                    data_stage03_quantification_tcc.measured_dG_f_coverage>measured_dG_f_coverage_criteria_I,
                    data_stage03_quantification_tcc.used_.is_(True),
                    data_stage03_quantification_dG_r.used_.is_(True)).all();
            rows_O = {}
            if data: 
                for d in data:
                    rows_O[d.rxn_id]=(d.dG_r_lb+d.dG_r_ub)/2;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    # update rows of data_stage03_quantification_dG_r    
    def update_dataStage03DGr(self,data_I):
        '''update rows of data_stage03_quantification_dG_r'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_dG_r).filter(
                            data_stage03_quantification_dG_r.experiment_id.like(d['experiment_id']),
                            data_stage03_quantification_dG_r.model_id.like(d['model_id']),
                            data_stage03_quantification_dG_r.rxn_id.like(d['rxn_id']),
                            data_stage03_quantification_dG_r.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                            data_stage03_quantification_dG_r.time_point.like(d['time_point'])).update(
                            {
                            'Keq_lb':d['Keq_lb'],
                            'Keq_ub':d['Keq_ub'],
                            'dG_r':d['dG_r'],
                            'dG_r_var':d['dG_r_var'],
                            'dG_r_units':d['dG_r_units'],
                            'dG_r_lb':d['dG_r_lb'],
                            'dG_r_ub':d['dG_r_ub'],
                            'displacement_lb':d['displacement_lb'],
                            'displacement_ub':d['displacement_ub'],
                            'Q_lb':d['Q_lb'],
                            'Q_ub':d['Q_ub'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    ## Query from data_stage03_quantification_tcc
    # query rows from data_stage03_quantification_tcc   
    def get_rows_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationTCC(self,experiment_id_I,
                                                                                                           model_id_I,
                                                                                                           time_point_I,
                                                                                                           sample_name_abbreviation_I,
                                                                                                 measured_concentration_coverage_criteria_I=0.5,
                                                                                                 measured_dG_f_coverage_criteria_I=0.99):
        '''Query rows that are used from the dG_r'''
        try:
            data = self.session.query(data_stage03_quantification_dG_r,
                    data_stage03_quantification_tcc.measured_concentration_coverage,
                    data_stage03_quantification_tcc.measured_dG_f_coverage,
                    data_stage03_quantification_tcc.feasible).filter(
                    data_stage03_quantification_dG_r.model_id.like(model_id_I),
                    data_stage03_quantification_dG_r.time_point.like(time_point_I),
                    data_stage03_quantification_dG_r.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_dG_r.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_dG_r.model_id.like(data_stage03_quantification_tcc.model_id),
                    data_stage03_quantification_dG_r.time_point.like(data_stage03_quantification_tcc.time_point),
                    data_stage03_quantification_dG_r.sample_name_abbreviation.like(data_stage03_quantification_tcc.sample_name_abbreviation),
                    data_stage03_quantification_dG_r.experiment_id.like(data_stage03_quantification_tcc.experiment_id),
                    data_stage03_quantification_dG_r.rxn_id.like(data_stage03_quantification_tcc.rxn_id),
                    data_stage03_quantification_tcc.measured_concentration_coverage>measured_concentration_coverage_criteria_I,
                    data_stage03_quantification_tcc.measured_dG_f_coverage>measured_dG_f_coverage_criteria_I,
                    data_stage03_quantification_tcc.used_.is_(True),
                    data_stage03_quantification_dG_r.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    data_tmp = {'experiment_id':d.data_stage03_quantification_dG_r.experiment_id,
                        'model_id':d.data_stage03_quantification_dG_r.model_id,
                        'sample_name_abbreviation':d.data_stage03_quantification_dG_r.sample_name_abbreviation,
                        'time_point':d.data_stage03_quantification_dG_r.time_point,
                        'rxn_id':d.data_stage03_quantification_dG_r.rxn_id,
                        'dG_r_units':d.data_stage03_quantification_dG_r.dG_r_units,
                        'dG_r_lb':d.data_stage03_quantification_dG_r.dG_r_lb,
                        'dG_r_ub':d.data_stage03_quantification_dG_r.dG_r_ub,
                        'displacement_lb':d.data_stage03_quantification_dG_r.displacement_lb,
                        'displacement_ub':d.data_stage03_quantification_dG_r.displacement_ub,
                        'feasible':d.feasible,
                        'used_':d.data_stage03_quantification_dG_r.used_,
                        'comment_':d.data_stage03_quantification_dG_r.comment_};
                    rows_O.append(data_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);  
    def get_row_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationTCC(self,experiment_id_I,
                                                                                                           model_id_I,
                                                                                                           time_point_I,
                                                                                                           sample_name_abbreviation_I,
                                                                                                           rxn_id_I,
                                                                                                           dG_r_lb_I,
                                                                                                           dG_r_ub_I,
                                                                                                 measured_concentration_coverage_criteria_I=0.5,
                                                                                                 measured_dG_f_coverage_criteria_I=0.99):
        '''Query rows that are used from the dG_r
        Assumption: dG_r_lb < dG_r_ub'''
        try:
            data = self.session.query(data_stage03_quantification_dG_r,
                    data_stage03_quantification_tcc.measured_concentration_coverage,
                    data_stage03_quantification_tcc.measured_dG_f_coverage,
                    data_stage03_quantification_tcc.feasible).filter(
                    data_stage03_quantification_dG_r.rxn_id.like(rxn_id_I),
                    data_stage03_quantification_dG_r.model_id.like(model_id_I),
                    data_stage03_quantification_dG_r.time_point.like(time_point_I),
                    data_stage03_quantification_dG_r.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_dG_r.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_dG_r.model_id.like(data_stage03_quantification_tcc.model_id),
                    data_stage03_quantification_dG_r.time_point.like(data_stage03_quantification_tcc.time_point),
                    data_stage03_quantification_dG_r.sample_name_abbreviation.like(data_stage03_quantification_tcc.sample_name_abbreviation),
                    data_stage03_quantification_dG_r.experiment_id.like(data_stage03_quantification_tcc.experiment_id),
                    data_stage03_quantification_dG_r.rxn_id.like(data_stage03_quantification_tcc.rxn_id),
                    data_stage03_quantification_dG_r.used_.is_(True),
                    # constraint for statistical significance
                    or_(data_stage03_quantification_dG_r.dG_r_ub < dG_r_lb_I,
                        data_stage03_quantification_dG_r.dG_r_lb > dG_r_ub_I),
                    # constraint for biological significance
                    or_(copysign(1,data_stage03_quantification_dG_r.dG_r_lb) != copysign(1,dG_r_lb_I),
                        copysign(1,data_stage03_quantification_dG_r.dG_r_ub) != copysign(1,dG_r_ub_I)),
                    data_stage03_quantification_tcc.measured_concentration_coverage>measured_concentration_coverage_criteria_I,
                    data_stage03_quantification_tcc.measured_dG_f_coverage>measured_dG_f_coverage_criteria_I,
                    data_stage03_quantification_tcc.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    data_tmp = {'experiment_id':d.data_stage03_quantification_dG_r.experiment_id,
                        'model_id':d.data_stage03_quantification_dG_r.model_id,
                        'sample_name_abbreviation':d.data_stage03_quantification_dG_r.sample_name_abbreviation,
                        'time_point':d.data_stage03_quantification_dG_r.time_point,
                        'rxn_id':d.data_stage03_quantification_dG_r.rxn_id,
                        'dG_r_units':d.data_stage03_quantification_dG_r.dG_r_units,
                        'dG_r_lb':d.data_stage03_quantification_dG_r.dG_r_lb,
                        'dG_r_ub':d.data_stage03_quantification_dG_r.dG_r_ub,
                        'displacement_lb':d.data_stage03_quantification_dG_r.displacement_lb,
                        'displacement_ub':d.data_stage03_quantification_dG_r.displacement_ub,
                        'feasible':d.feasible,
                        'used_':d.data_stage03_quantification_dG_r.used_,
                        'comment_':d.data_stage03_quantification_dG_r.comment_};
                    rows_O.update(data_tmp);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);  
    def get_rowsDict_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationTCC(self,experiment_id_I,
                                                                                                           model_id_I,
                                                                                                           time_point_I,
                                                                                                           sample_name_abbreviation_I,
                                                                                                 measured_concentration_coverage_criteria_I=0.5,
                                                                                                 measured_dG_f_coverage_criteria_I=0.99):
        '''Query rows that are used from the tcc'''
        try:
            data = self.session.query(data_stage03_quantification_tcc.rxn_id,
                    data_stage03_quantification_tcc.measured_concentration_coverage,
                    data_stage03_quantification_tcc.measured_dG_f_coverage,
                    data_stage03_quantification_tcc.feasible).filter(
                    data_stage03_quantification_tcc.model_id.like(model_id_I),
                    data_stage03_quantification_tcc.time_point.like(time_point_I),
                    data_stage03_quantification_tcc.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_tcc.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_tcc.measured_concentration_coverage>measured_concentration_coverage_criteria_I,
                    data_stage03_quantification_tcc.measured_dG_f_coverage>measured_dG_f_coverage_criteria_I,
                    data_stage03_quantification_tcc.used_.is_(True)).all();
            measured_concentration_coverage_O = {};
            measured_dG_f_coverage_O = {};
            feasible_O = {};
            if data: 
                for d in data:
                    if d.rxn_id in measured_concentration_coverage_O:
                        print('duplicate rxn_id found!');
                    else:
                        measured_concentration_coverage_O[d.rxn_id]={
                        'measured_concentration_coverage':d.measured_concentration_coverage
                        };
                        measured_dG_f_coverage_O[d.rxn_id]={
                        'measured_dG_f_coverage':d.measured_dG_f_coverage
                        };
                        feasible_O[d.rxn_id]={
                        'feasible':d.feasible
                        };
            return measured_concentration_coverage_O,measured_dG_f_coverage_O,feasible_O;
        except SQLAlchemyError as e:
            print(e);    
    # update rows of data_stage03_quantification_tcc  
    def update_dataStage03Tcc(self,data_I):
        '''update rows of data_stage03_quantification_tcc'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_tcc).filter(
                            data_stage03_quantification_tcc.experiment_id.like(d['experiment_id']),
                            data_stage03_quantification_tcc.model_id.like(d['model_id']),
                            data_stage03_quantification_tcc.rxn_id.like(d['rxn_id']),
                            data_stage03_quantification_dG_r.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                            data_stage03_quantification_dG_r.time_point.like(d['time_point'])).update(
                            {
                            'feasible':d['feasible'],
                            'measured_concentration_coverage_criteria':d['measured_concentration_coverage_criteria'],
                            'measured_dG_f_coverage_criteria':d['measured_dG_f_coverage_criteria'],
                            'measured_concentration_coverage':d['measured_concentration_coverage'],
                            'measured_dG_f_coverage':d['measured_dG_f_coverage'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    ## Query data from data_stage03_quantification_modelPathways
    # query rows from data_stage03_quantification_modelPathways
    def get_rowsDict_modelID_dataStage03QuantificationModelPathways(self,model_id_I):
        '''Query rows that are used from model pathways'''
        try:
            data = self.session.query(data_stage03_quantification_modelPathways).filter(
                    data_stage03_quantification_modelPathways.model_id.like(model_id_I),
                    data_stage03_quantification_modelPathways.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if d.pathway_id in rows_O:
                        print('duplicate pathway_ids found!');
                    else:
                        rows_O[d.pathway_id]={'reactions':d.reactions,
                            'stoichiometry':d.stoichiometry};
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    #internal functions
    def convert_metid2escherid(self,met_id_I):
        met_formatted = met_id_I;
        met_formatted = re.sub('_DASH_','__',met_formatted)
        met_formatted = re.sub('_LPARANTHES_','__',met_formatted)
        met_formatted = re.sub('_RPARANTHES_','__',met_formatted)
        return met_formatted;

    #TODO:
            
    ## Query from data_stage03_quantification_measuredFluxes
    # query rows from data_stage03_quantification_measuredFluxes
    def get_rows_experimentIDAndSampleNameAbbreviation_dataStage03QuantificationMeasuredFluxes(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry rows by model_id that are used'''
        try:
            data = self.session.query(data_stage03_quantification_measuredFluxes).filter(
                    data_stage03_quantification_measuredFluxes.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_measuredFluxes.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_measuredFluxes.used_.is_(True)).order_by(
                    data_stage03_quantification_measuredFluxes.model_id.asc(),
                    data_stage03_quantification_measuredFluxes.rxn_id.asc()).all();
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
    def get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage03QuantificationMeasuredFluxes(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Querry rows by model_id that are used'''
        try:
            data = self.session.query(data_stage03_quantification_measuredFluxes).filter(
                    data_stage03_quantification_measuredFluxes.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_measuredFluxes.model_id.like(model_id_I),
                    data_stage03_quantification_measuredFluxes.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_measuredFluxes.used_.is_(True)).order_by(
                    data_stage03_quantification_measuredFluxes.model_id.asc(),
                    data_stage03_quantification_measuredFluxes.rxn_id.asc()).all();
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

    ## Query from data_stage03_quantification_sampledData
    # query rows from data_stage03_quantification_sampledData    
    def get_rows_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage03QuantificationSampledData(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage03_quantification_sampledData).filter(
                    data_stage03_quantification_sampledData.model_id.like(model_id_I),
                    data_stage03_quantification_sampledData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_sampledData.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_sampledData.used_.is_(True)).all();
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
    def get_rowsDict_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage03QuantificationSampledData(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage03_quantification_sampledData).filter(
                    data_stage03_quantification_sampledData.model_id.like(model_id_I),
                    data_stage03_quantification_sampledData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_sampledData.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_sampledData.used_.is_(True)).all();
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
    def get_rowsEscherLbUb_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage03QuantificationSampledData(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage03_quantification_sampledData).filter(
                    data_stage03_quantification_sampledData.model_id.like(model_id_I),
                    data_stage03_quantification_sampledData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_sampledData.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_sampledData.used_.is_(True)).all();
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
    def get_rowsEscher_experimentIDAndModelIDAndSampleNameAbbreviations_dataStage03QuantificationSampledData(self,experiment_id_I,model_id_I,sample_name_abbreviation_I):
        '''Query rows that are used from the sampledData'''
        try:
            data = self.session.query(data_stage03_quantification_sampledData).filter(
                    data_stage03_quantification_sampledData.model_id.like(model_id_I),
                    data_stage03_quantification_sampledData.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage03_quantification_sampledData.experiment_id.like(experiment_id_I),
                    data_stage03_quantification_sampledData.used_.is_(True)).all();
            rows_O = {}
            if data: 
                for d in data:
                    rows_O[d.rxn_id]=d.sampling_ave;
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    ##  Query from data_stage03_quantification_sampledPoints
    # query rows from data_stage03_quantification_sampledPoints
    def get_rows_simulationID_dataStage03QuantificationSampledPoints(self,simulation_id_I):
        '''Querry rows that are used from sampledPoints'''
        try:
            data = self.session.query(data_stage03_quantification_sampledPoints).filter(
                    data_stage03_quantification_sampledPoints.simulation_id.like(simulation_id_I),
                    data_stage03_quantification_sampledPoints.used_.is_(True)).all();
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