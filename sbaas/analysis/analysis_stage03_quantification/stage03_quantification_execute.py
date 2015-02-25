'''quantitative metabolomics analysis class'''
# Dependencies
from analysis.analysis_base import *
from stage03_quantification_query import *
from stage03_quantification_io import *
from math import pow
import re
import copy
# Dependencies from thermodynamics
from thermodynamics.thermodynamics_dG_f_data import thermodynamics_dG_f_data
from thermodynamics.thermodynamics_dG_p_data import thermodynamics_dG_p_data
from thermodynamics.thermodynamics_dG_r_data import thermodynamics_dG_r_data
from thermodynamics.thermodynamics_metabolomicsData import thermodynamics_metabolomicsData
from thermodynamics.thermodynamics_otherData import thermodynamics_otherData
from thermodynamics.thermodynamics_simulatedData import thermodynamics_simulatedData
from thermodynamics.thermodynamics_tfba import thermodynamics_tfba
# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file, write_cobra_model_to_sbml_file
from cobra.flux_analysis.variability import flux_variability_analysis
from cobra.flux_analysis.parsimonious import optimize_minimal_flux
from cobra.flux_analysis import flux_variability_analysis

class stage03_quantification_execute():
    '''class for quantitative metabolomics analysis'''
    def __init__(self):
        self.session = Session();
        self.stage03_quantification_query = stage03_quantification_query();
        self.calculate = base_calculate();
        self.models = {};
    # analyses:
    def execute_makeMetabolomicsData_intracellular(self,experiment_id_I,data_I=[],compartment_id_I='c'):
        '''Get the currated metabolomics data from data_stage01_quantification_averagesMIGeo'''
        # get rows:
        
        met_id_conv_dict = {'Hexose_Pool_fru_glc-D':['glc-D','fru-D'],
                            'Pool_2pg_3pg':['2pg','3pg'],
                            '23dpg':['13dpg']};
        data_O = [];
        if data_I:
            data = data_I;
        else:
            data = [];
            data = self.stage03_quantification_query.get_rows_experimentID_dataStage01AveragesMIgeo(experiment_id_I);
        for d in data:
            if d['component_group_name'] in met_id_conv_dict.keys():
                met2conv = d['component_group_name'];
                for met_conv in met_id_conv_dict[met2conv]:
                    row_tmp = copy.copy(d)
                    row_tmp['component_group_name'] = met_conv;
                    data_O.append(row_tmp);
            else:
                data_O.append(d);
        for d in data_O:
            row = None;
            row = data_stage03_quantification_metabolomicsData(d['experiment_id'],
                    d['sample_name_abbreviation'],
                    d['time_point'],
                    self.format_metid(d['component_group_name'],compartment_id_I),
                    d['calculated_concentration_average'],
                    d['calculated_concentration_var'],
                    d['calculated_concentration_units'],
                    d['calculated_concentration_lb'],
                    d['calculated_concentration_ub'],
                    True,
                    d['used_'],
                    None);
            self.session.add(row);
        self.session.commit();
    def execute_makeModel(self,experiment_id_I,model_id_I=None,model_id_O=None,date_I=None,model_file_name_I=None,ko_list=[],flux_dict={},description=None):
        '''make the thermodynamic model'''

        qio03 = stage03_quantification_io();

        if model_id_I and model_id_O: #modify an existing model in the database
            cobra_model_sbml = None;
            cobra_model_sbml = self.stage03_quantification_query.get_row_modelID_dataStage03QuantificationModels(model_id_I);
            # write the model to a temporary file
            with open('data/cobra_model_tmp.xml','wb') as file:
                file.write(cobra_model_sbml['sbml_file']);
            # Read in the sbml file and define the model conditions
            cobra_model = create_cobra_model_from_sbml_file('data/cobra_model_tmp.xml', print_time=True);
            # Apply KOs, if any:
            for ko in ko_list:
                cobra_model.reactions.get_by_id(ko).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(ko).upper_bound = 0.0;
            # Apply flux constraints, if any:
            for rxn,flux in flux_dict.iteritems():
                cobra_model.reactions.get_by_id(rxn).lower_bound = flux['lb'];
                cobra_model.reactions.get_by_id(rxn).upper_bound = flux['ub'];
            # Change description, if any:
            if description:
                cobra_model.description = description;
            # test the model
            if self.test_model(cobra_model):
                # write the model to a temporary file
                with open('data/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model);
                # upload the model to the database
                qio03.import_dataStage03QuantificationModel_sbml(model_id_I, date_I, 'data/cobra_model_tmp.xml');
        elif model_file_name_I and model_id_O: #modify an existing model in not in the database
            # Read in the sbml file and define the model conditions
            cobra_model = create_cobra_model_from_sbml_file(model_file_name_I, print_time=True);
            # Apply KOs, if any:
            for ko in ko_list:
                cobra_model.reactions.get_by_id(ko).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(ko).upper_bound = 0.0;
            # Apply flux constraints, if any:
            for rxn,flux in flux_dict.iteritems():
                cobra_model.reactions.get_by_id(rxn).lower_bound = flux['lb'];
                cobra_model.reactions.get_by_id(rxn).upper_bound = flux['ub'];
            # Change description, if any:
            if description:
                cobra_model.description = description;
            # test the model
            if self.test_model(cobra_model):
                # write the model to a temporary file
                with open('data/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model);
                # upload the model to the database
                qio03.import_dataStage03QuantificationModel_sbml(model_id_I, date_I, 'data/cobra_model_tmp.xml');
        else:
            print 'need to specify either an existing model_id or model_file_name!'
        return
    def execute_makeSimulatedData(self,experiment_id_I,model_ids_I = []):
        '''make simulated data'''

        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage03_quantification_query.get_modelID_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
        for model_id in model_ids:
            # get the cobra model
            cobra_model = self.models[model_id];
            # make simulated data
            simulated_data = thermodynamics_simulatedData();
            simulated_data.generate_sra_data(cobra_model); # perform single reaction deletion analysis
            simulated_data.generate_fva_data(cobra_model); # perform flux variability analysis
            # upload the results to the database
            data_O = [];
            for k,v in simulated_data.fva_data.iteritems():
                data_tmp = {'experiment_id':experiment_id_I,
                'model_id':model_id,
                'rxn_id':k,
                'fba_flux':None, #reserved for parsimonious fba
                'fva_minimum':simulated_data.fva_data[k]['minimum'],
                'fva_maximum':simulated_data.fva_data[k]['maximum'],
                'flux_units':'mmol*gDCW-1*hr-1',
                'sra_gr':simulated_data.sra_data[k]['gr'],
                'sra_gr_ratio':simulated_data.sra_data[k]['gr_ratio'],
                'used_':True,
                'comment_':None};
                data_O.append(data_tmp);
                try:
                    row = None;
                    row = data_stage03_quantification_simulatedData(experiment_id_I,
                            model_id,
                            k,
                            None, #reserved for parsimonious fba
                            simulated_data.fva_data[k]['minimum'],
                            simulated_data.fva_data[k]['maximum'],
                            'mmol*gDCW-1*hr-1',
                            simulated_data.sra_data[k]['gr'],
                            simulated_data.sra_data[k]['gr_ratio'],
                            True,
                            None);
                    self.session.add(row);
                    self.session.commit();
                except sqlalchemy.exc.IntegrityError as e:
                    print e;
                    print "Press any key to continue"
                    a=raw_input();
                    self.stage03_quantification_query.update_dataStage03SimulatedData([tmp]);
    def execute_adjust_dG_f(self,experiment_id_I,model_ids_I = [],time_points_I=[],sample_name_abbreviations_I=[]):
        '''adjust dG0_f to specified temperature, pH, and ionic strength'''
        
        # query dG0f data
        id2kegg = {};
        id2kegg = self.stage03_quantification_query.get_rowsDict_dataStage03QuantificationMetid2keggid();
        dG0_f = {};
        dG0_f = self.stage03_quantification_query.get_rowsDict_dataStage03QuantificationDG0f();
        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage03_quantification_query.get_modelID_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
        for model_id in model_ids:
            # get the cobra model
            cobra_model = self.models[model_id];
            # get the time-points
            if time_points_I:
                time_points = time_points_I;
            else:
                time_points = [];
                time_points = self.stage03_quantification_query.get_timePoints_experimentIDAndModelID_dataStage03QuantificationSimulation(experiment_id_I,model_id);
            for tp in time_points:
                # get sample_name_abbreviations
                if sample_name_abbreviations_I:
                    sample_name_abbreviations = sample_name_abbreviations_I;
                else:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.stage03_quantification_query.get_sampleNameAbbreviations_experimentIDAndModelIDAndTimePoint_dataStage03QuantificationSimulation(experiment_id_I,model_id,tp);
                for sna in sample_name_abbreviations:
                    # get otherData
                    pH,temperature,ionic_strength = {},{},{}
                    pH,temperature,ionic_strength = self.stage03_quantification_query.get_rowsFormatted_experimentIDAndTimePointAndSampleNameAbbreviation_dataStage03QuantificationOtherData(experiment_id_I,tp,sna);
                    # load pH, ionic_strength, and temperature parameters
                    other_data = thermodynamics_otherData(pH_I=pH,temperature_I=temperature,ionic_strength_I=ionic_strength);
                    #other_data.load_defaultData();
                    other_data.check_data();
                    # adjust dG0f to environmental conditions
                    dG_f_data = thermodynamics_dG_f_data(id2KEGGID_I=id2kegg);
                    dG_f_data.get_transformed_dG_f(dG0_f,cobra_model,other_data.pH,other_data.temperature,other_data.ionic_strength); # adjust the non-transformed dG0_f data to physiological pH, temperature, and ionic strength (this step has already been completed)
                    # upload to database for later use
                    for k,v in dG_f_data.dG_f.iteritems():
                        compartment = k.split('_')[-1]; #compartment id is appended to the met_id
                        data_tmp={'experiment_id':experiment_id_I,
                            'model_id':model_id,
                            'sample_name_abbreviation':sna,
                            'time_point':tp,
                            'met_name':None,
                            'met_id':k,
                            'dG_f':v['dG_f'],
                            'dG_f_var':v['dG_f_var'],
                            'dG_f_units':v['dG_f_units'],
                            'dG_f_lb':None,
                            'dG_f_ub':None,
                            'temperature':temperature[compartment]['temperature'],
                            'temperature_units':temperature[compartment]['temperature_units'],
                            'ionic_strength':ionic_strength[compartment]['ionic_strength'],
                            'ionic_strength_units':ionic_strength[compartment]['ionic_strength_units'],
                            'pH':pH[compartment]['pH'],
                            'pH_units':None,
                            'measured':True,
                            'used_':True,
                            'comment_':None};
                        row = None;
                        row = data_stage03_quantification_dG_f(experiment_id_I,
                            model_id,
                            sna,
                            tp,
                            None,
                            k,
                            v['dG_f'],
                            v['dG_f_var'],
                            v['dG_f_units'],
                            None,
                            None,
                            temperature[compartment]['temperature'],
                            temperature[compartment]['temperature_units'],
                            ionic_strength[compartment]['ionic_strength'],
                            ionic_strength[compartment]['ionic_strength_units'],
                            pH[compartment]['pH'],
                            None,
                            True,
                            True,
                            None);
                        self.session.add(row);
        self.session.commit();
    def execute_calculate_dG_r(self,experiment_id_I,model_ids_I = [],
                               time_points_I=[],sample_name_abbreviations_I=[],
                               inconsistent_dG_f_I=[],inconsistent_concentrations_I=[],
                               measured_concentration_coverage_criteria_I=0.5,
                               measured_dG_f_coverage_criteria_I=0.99):
        '''calculate dG0_r, dG_r, displacements, and perform a thermodynamic consistency check'''
        
        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage03_quantification_query.get_modelID_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
        for model_id in model_ids:
            # get the cobra model
            cobra_model = self.models[model_id];
            # get simulated data
            fva_data,sra_data = {},{};
            fva_data,sra_data = self.stage03_quantification_query.get_rowsDict_experimentIDAndModelID_dataStage03QuantificationSimulatedData(experiment_id_I,model_id);
            # load simulated data
            simulated_data = thermodynamics_simulatedData(fva_data_I=fva_data,sra_data_I=sra_data);
            simulated_data.check_data();
            # get the time-points
            if time_points_I:
                time_points = time_points_I;
            else:
                time_points = [];
                time_points = self.stage03_quantification_query.get_timePoints_experimentIDAndModelID_dataStage03QuantificationSimulation(experiment_id_I,model_id);
            for tp in time_points:
                # get sample_name_abbreviations
                if sample_name_abbreviations_I:
                    sample_name_abbreviations = sample_name_abbreviations_I;
                else:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.stage03_quantification_query.get_sampleNameAbbreviations_experimentIDAndModelIDAndTimePoint_dataStage03QuantificationSimulation(experiment_id_I,model_id,tp);
                for sna in sample_name_abbreviations:
                    # get otherData
                    pH,temperature,ionic_strength = {},{},{}
                    pH,temperature,ionic_strength = self.stage03_quantification_query.get_rowsFormatted_experimentIDAndTimePointAndSampleNameAbbreviation_dataStage03QuantificationOtherData(experiment_id_I,tp,sna);
                    # load pH, ionic_strength, and temperature parameters
                    other_data = thermodynamics_otherData(pH_I=pH,temperature_I=temperature,ionic_strength_I=ionic_strength);
                    other_data.check_data();
                    # get dG_f data:
                    dG_f = {};
                    dG_f = self.stage03_quantification_query.get_rowsDict_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDGf(experiment_id_I,model_id,tp,sna);
                    dG_f_data = thermodynamics_dG_f_data(dG_f_I=dG_f);
                    dG_f_data.format_dG_f();
                    dG_f_data.generate_estimated_dG_f(cobra_model)
                    dG_f_data.check_data(); 
                    # remove an inconsistent dGf values
                    if inconsistent_dG_f_I: dG_f_data.remove_measured_dG_f(inconsistent_dG_f_I)
                    # query metabolomicsData
                    concentrations = [];
                    concentrations = self.stage03_quantification_query.get_rowsDict_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationMetabolomicsData(experiment_id_I,tp,sna);
                    # load metabolomicsData
                    metabolomics_data = thermodynamics_metabolomicsData(measured_concentrations_I=concentrations);
                    metabolomics_data.generate_estimated_metabolomics_data(cobra_model);
                    # remove an inconsistent concentration values
                    if inconsistent_concentrations_I: metabolomics_data.remove_measured_concentrations(inconsistent_concentrations_I);
                    # calculate dG0r, dGr, displacements, and perform a thermodynamic consistency check based on model simulations
                    tcc = thermodynamics_dG_r_data();
                    tcc.calculate_dG0_r_v3(cobra_model, dG_f_data.measured_dG_f, dG_f_data.estimated_dG_f, other_data.temperature); # calculate the change in free energy of reaction without accounting for metabolite concentrations
                    tcc.calculate_dG_r_v3(cobra_model,metabolomics_data.measured_concentrations, metabolomics_data.estimated_concentrations,
                                       other_data.pH, other_data.ionic_strength, other_data.temperature); # adjust the change in free energy of reaction for intracellular metabolite concentrations
                    tcc.check_thermodynamicConsistency(cobra_model,simulated_data.fva_data,
                                       metabolomics_data.measured_concentrations,
                                       metabolomics_data.estimated_concentrations,
                                       other_data.pH,other_data.ionic_strength,other_data.temperature,
                                       measured_concentration_coverage_criteria_I,
                                       measured_dG_f_coverage_criteria_I); # check the thermodynamic consistency of the data
                    tcc.calculate_displacement_v3(cobra_model,metabolomics_data.measured_concentrations, metabolomics_data.estimated_concentrations); # calculate the displacements from equillibrium
                    tcc.simulate_infeasibleReactions(cobra_model); # simulate thermodynamically inconsistent data
                    tcc.constrain_infeasibleReactions(cobra_model); # remove thermodynamically inconsistent reactions from the model
                    # upload dG0r, dGr, displacements, and results of tcc
                    for k,v in tcc.dG_r.iteritems():
                        dG0_r_tmp = {'experiment_id':experiment_id_I,
                                'model_id':model_id,
                                'sample_name_abbreviation':sna,
                                'time_point':tp,
                                'rxn_id':k,
                                'Keq_lb':tcc.dG0_r[k]['Keq_lb'],
                                'Keq_ub':tcc.dG0_r[k]['Keq_ub'],
                                'dG0_r':tcc.dG0_r[k]['dG_r'],
                                'dG0_r_var':tcc.dG0_r[k]['dG_r_var'],
                                'dG0_r_units':tcc.dG0_r[k]['dG_r_units'],
                                'dG0_r_lb':tcc.dG0_r[k]['dG_r_lb'],
                                'dG0_r_ub':tcc.dG0_r[k]['dG_r_ub'],
                                'used_':True,
                                'comment_':None};
                        dG_r_tmp = {'experiment_id':experiment_id_I,
                                'model_id':model_id,
                                'sample_name_abbreviation':sna,
                                'time_point':tp,
                                'rxn_id':k,
                                'Keq_lb':tcc.dG_r[k]['Keq_lb'],
                                'Keq_ub':tcc.dG_r[k]['Keq_ub'],
                                'dG_r':tcc.dG_r[k]['dG_r'],
                                'dG_r_var':tcc.dG_r[k]['dG_r_var'],
                                'dG_r_units':tcc.dG_r[k]['dG_r_units'],
                                'dG_r_lb':tcc.dG_r[k]['dG_r_lb'],
                                'dG_r_ub':tcc.dG_r[k]['dG_r_ub'],
                                'displacement_lb':tcc.displacement[k]['displacement_lb'],
                                'displacement_ub':tcc.displacement[k]['displacement_ub'],
                                'Q_lb':tcc.displacement[k]['Q_lb'],
                                'Q_ub':tcc.displacement[k]['Q_ub'],
                                'used_':True,
                                'comment_':None};
                        tcc_tmp = {'experiment_id':experiment_id_I,
                                'model_id':model_id,
                                'sample_name_abbreviation':sna,
                                'time_point':tp,
                                'rxn_id':k,
                                'feasible':tcc.thermodynamic_consistency_check[k],
                                'measured_concentration_coverage_criteria':measured_concentration_coverage_criteria_I,
                                'measured_dG_f_coverage_criteria':measured_dG_f_coverage_criteria_I,
                                'measured_concentration_coverage':tcc.metabolomics_coverage[k],
                                'measured_dG_f_coverage':tcc.dG_r_coverage[k],
                                'used_':True,
                                'comment_':None};
                        try:
                            row = None;
                            row = data_stage03_quantification_dG0_r(experiment_id_I,
                                    model_id,
                                    sna,
                                    tp,
                                    k,
                                    tcc.dG0_r[k]['Keq_lb'],
                                    tcc.dG0_r[k]['Keq_ub'],
                                    tcc.dG0_r[k]['dG_r'],
                                    tcc.dG0_r[k]['dG_r_var'],
                                    tcc.dG0_r[k]['dG_r_units'],
                                    tcc.dG0_r[k]['dG_r_lb'],
                                    tcc.dG0_r[k]['dG_r_ub'],
                                    True,
                                    None);
                            self.session.add(row);
                            row = None;
                            row = data_stage03_quantification_dG_r(experiment_id_I,
                                    model_id,
                                    sna,
                                    tp,
                                    k,
                                    tcc.dG_r[k]['Keq_lb'],
                                    tcc.dG_r[k]['Keq_ub'],
                                    tcc.dG_r[k]['dG_r'],
                                    tcc.dG_r[k]['dG_r_var'],
                                    tcc.dG_r[k]['dG_r_units'],
                                    tcc.dG_r[k]['dG_r_lb'],
                                    tcc.dG_r[k]['dG_r_ub'],
                                    tcc.displacement[k]['displacement_lb'],
                                    tcc.displacement[k]['displacement_ub'],
                                    tcc.displacement[k]['Q_lb'],
                                    tcc.displacement[k]['Q_ub'],
                                    True,
                                    None);
                            self.session.add(row);
                            row = None;
                            row = data_stage03_quantification_tcc(experiment_id_I,
                                    model_id,
                                    sna,
                                    tp,
                                    k,
                                    tcc.thermodynamic_consistency_check[k],
                                    measured_concentration_coverage_criteria_I,
                                    measured_dG_f_coverage_criteria_I,
                                    tcc.metabolomics_coverage[k],
                                    tcc.dG_r_coverage[k],
                                    True,
                                    None);
                            self.session.add(row);
                        except sqlalchemy.exc.IntegrityError as e:
                            print e;
                            print "Press any key to continue"
                            a=raw_input();
                    self.session.commit();    
    #TODO                
    def execute_calculate_dG_p(self,experiment_id_I,model_ids_I = [],
                               time_points_I=[],sample_name_abbreviations_I=[]):
        '''calculate dG0_r, dG_r, displacements, and perform a thermodynamic consistency check'''
        
        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage03_quantification_query.get_modelID_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
        for model_id in model_ids:
            # get the cobra model
            cobra_model = self.models[model_id];
            # get pathway data
            pathways = {};
            pathways = self.stage03_quantification_query.get_rowsDict_modelID_dataStage03QuantificationModelPathways(model_id);
            # get the time-points
            if time_points_I:
                time_points = time_points_I;
            else:
                time_points = [];
                time_points = self.stage03_quantification_query.get_timePoints_experimentIDAndModelID_dataStage03QuantificationSimulation(experiment_id_I,model_id);
            for tp in time_points:
                # get sample_name_abbreviations
                if sample_name_abbreviations_I:
                    sample_name_abbreviations = sample_name_abbreviations_I;
                else:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.stage03_quantification_query.get_sampleNameAbbreviations_experimentIDAndModelIDAndTimePoint_dataStage03QuantificationSimulation(experiment_id_I,model_id,tp);
                for sna in sample_name_abbreviations:
                    # get dG0_r and dG_r data
                    dG0_r={};
                    dG0_r=self.stage03_quantification_query.get_rowsDict_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDG0r(experiment_id_I,model_id,tp,sna);
                    dG_r={};
                    dG_r=self.stage03_quantification_query.get_rowsDict_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDGr(experiment_id_I,model_id,tp,sna);
                    # load dG0r and dGr
                    tcc = thermodynamics_dG_r_data(dG0_r_I=dG0_r,dG_r_I=dG_r);
                    # calculate dG_p for biosynthetic pathways
                    tccp = thermodynamics_dG_p_data(pathways_I=pathways);
                    tccp.calculate_dG_p(cobra_model,tcc.dG0_r,tcc.dG_r);
                    # upload dG_p
                    for k,v in tccp.dG_p.iteritems():
                        dG0_p_tmp = {'experiment_id':experiment_id_I,
                                'model_id':model_id,
                                'sample_name_abbreviation':sna,
                                'time_point':tp,
                                'pathway_id':k,
                                'dG0_p':tccp.dG0_p[k]['dG0_p'],
                                'dG0_p_var':tccp.dG0_p[k]['dG0_p_var'],
                                'dG0_p_units':tccp.dG0_p[k]['dG0_p_units'],
                                'dG0_p_lb':tccp.dG0_p[k]['dG0_p_lb'],
                                'dG0_p_ub':tccp.dG0_p[k]['dG0_p_ub'],
                                'used_':True,
                                'comment_':None};
                        dG_p_tmp = {'experiment_id':experiment_id_I,
                                'model_id':model_id,
                                'sample_name_abbreviation':sna,
                                'time_point':tp,
                                'pathway_id':k,
                                'dG_p':tccp.dG_p[k]['dG_p'],
                                'dG_p_var':tccp.dG_p[k]['dG_p_var'],
                                'dG_p_units':tccp.dG_p[k]['dG_p_units'],
                                'dG_p_lb':tccp.dG_p[k]['dG_p_lb'],
                                'dG_p_ub':tccp.dG_p[k]['dG_p_ub'],
                                'used_':True,
                                'comment_':None};
                        try:
                            row = None;
                            row = data_stage03_quantification_dG0_p(experiment_id_I,
                                    model_id,
                                    sna,
                                    tp,
                                    k,
                                    tccp.dG0_p[k]['dG0_p'],
                                    tccp.dG0_p[k]['dG0_p_var'],
                                    tccp.dG0_p[k]['dG0_p_units'],
                                    tccp.dG0_p[k]['dG0_p_lb'],
                                    tccp.dG0_p[k]['dG0_p_ub'],
                                    True,
                                    None);
                            self.session.add(row);
                            row = None;
                            row = data_stage03_quantification_dG_p(experiment_id_I,
                                    model_id,
                                    sna,
                                    tp,
                                    k,
                                    tccp.dG_p[k]['dG_p'],
                                    tccp.dG_p[k]['dG_p_var'],
                                    tccp.dG_p[k]['dG_p_units'],
                                    tccp.dG_p[k]['dG_p_lb'],
                                    tccp.dG_p[k]['dG_p_ub'],
                                    True,
                                    None);
                            self.session.add(row);
                        except sqlalchemy.exc.IntegrityError as e:
                            print e;
                            print "Press any key to continue"
                            a=raw_input();
                    self.session.commit();                 
    # data_stage01_quantification initializations
    def drop_dataStage03_quantification(self):
        try:
            data_stage03_quantification_simulatedData.__table__.drop(engine,True);
            data_stage03_quantification_otherData.__table__.drop(engine,True);
            data_stage03_quantification_dG0_r.__table__.drop(engine,True);
            data_stage03_quantification_dG_r.__table__.drop(engine,True);
            data_stage03_quantification_dG0_f.__table__.drop(engine,True);
            data_stage03_quantification_dG_f.__table__.drop(engine,True);
            data_stage03_quantification_metabolomicsData.__table__.drop(engine,True);
            data_stage03_quantification_tcc.__table__.drop(engine,True);
            data_stage03_quantification_dG0_p.__table__.drop(engine,True);
            data_stage03_quantification_modelPathways.__table__.drop(engine,True);
            data_stage03_quantification_dG_p.__table__.drop(engine,True);
            data_stage03_quantification_metid2keggid.__table__.drop(engine,True);
            data_stage03_quantification_models.__table__.drop(engine,True);
            data_stage03_quantification_modelReactions.__table__.drop(engine,True);
            data_stage03_quantification_modelMetabolites.__table__.drop(engine,True);
            data_stage03_quantification_simulation.__table__.drop(engine,True);
            data_stage03_quantification_measuredFluxes.__table__.drop(engine,True);
            data_stage03_quantification_sampledPoints.__table__.drop(engine,True);
            data_stage03_quantification_sampledData.__table__.drop(engine,True);
            data_stage03_quantification_simulationParameters.__table__.drop(engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage03_quantification(self,experiment_id_I = None,simulation_id_I=None):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage03_quantification_simulatedData).filter(data_stage03_quantification_simulatedData.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_otherData).filter(data_stage03_quantification_otherData.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG0_r).filter(data_stage03_quantification_dG0_r.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG0_f).filter(data_stage03_quantification_dG0_f.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_f).filter(data_stage03_quantification_dG_f.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_metabolomicsData).filter(data_stage03_quantification_metabolomicsData.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_r).filter(data_stage03_quantification_dG_r.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_tcc).filter(data_stage03_quantification_tcc.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG0_p).filter(data_stage03_quantification_dG0_p.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_modelPathways).filter(data_stage03_quantification_modelPathways.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_p).filter(data_stage03_quantification_dG_p.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_metid2keggid).filter(data_stage03_quantification_metid2keggid.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_models).filter(data_stage03_quantification_models.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_modelReactions).filter(data_stage03_quantification_modelReactions.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_modelMetabolites).filter(data_stage03_quantification_modelMetabolites.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_simulation).filter(data_stage03_quantification_simulation.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_simulationParameters).filter(data_stage03_quantification_simulationParameters.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_measuredFluxes).delete(synchronize_session=False);
            elif simulation_id_I:
                reset = self.session.query(data_stage03_quantification_simulation).filter(data_stage03_quantification_simulation.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_sampledPoints).filter(data_stage03_quantification_sampledPoints.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_sampledData).filter(data_stage03_quantification_sampledData.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_simulationParameters).filter(data_stage03_quantification_simulationParameters.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage03_quantification_simulatedData).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_otherData).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG0_r).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG0_f).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_metabolomicsData).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_f).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_r).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_p).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_metid2keggid).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_models).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_modelReactions).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_modelMetabolites).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_simulation).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_tcc).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG0_p).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_modelPathways).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_measuredFluxes).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_sampledPoints).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_sampledData).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_simulationParameters).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_dataStage03_quantification(self):
        try:
            data_stage03_quantification_simulatedData.__table__.create(engine,True);
            data_stage03_quantification_otherData.__table__.create(engine,True);
            data_stage03_quantification_dG0_r.__table__.create(engine,True);
            data_stage03_quantification_dG_r.__table__.create(engine,True);
            data_stage03_quantification_dG0_f.__table__.create(engine,True);
            data_stage03_quantification_dG_f.__table__.create(engine,True);
            data_stage03_quantification_metabolomicsData.__table__.create(engine,True);
            data_stage03_quantification_tcc.__table__.create(engine,True);
            data_stage03_quantification_dG0_p.__table__.create(engine,True);
            data_stage03_quantification_modelPathways.__table__.create(engine,True);
            data_stage03_quantification_dG_p.__table__.create(engine,True);
            data_stage03_quantification_metid2keggid.__table__.create(engine,True);
            data_stage03_quantification_models.__table__.create(engine,True);
            data_stage03_quantification_modelReactions.__table__.create(engine,True);
            data_stage03_quantification_modelMetabolites.__table__.create(engine,True);
            data_stage03_quantification_simulation.__table__.create(engine,True);
            data_stage03_quantification_simulation.__table__.drop(engine,True);
            data_stage03_quantification_measuredFluxes.__table__.drop(engine,True);
            data_stage03_quantification_sampledPoints.__table__.drop(engine,True);
            data_stage03_quantification_sampledData.__table__.drop(engine,True);
            data_stage03_quantification_simulationParameters.__table__.drop(engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage03_quantification_dG_r(self,experiment_id_I = None):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage03_quantification_dG0_r).filter(data_stage03_quantification_dG0_r.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_r).filter(data_stage03_quantification_dG_r.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_tcc).filter(data_stage03_quantification_tcc.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG0_p).filter(data_stage03_quantification_dG0_p.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_p).filter(data_stage03_quantification_dG_p.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                
            else:
                reset = self.session.query(data_stage03_quantification_dG0_r).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_r).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_tcc).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG0_p).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_p).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage03_quantification_thermodynamicAnalysis(self,experiment_id_I = None):
        try:
            if experiment_id_I:
                #reset = self.session.query(data_stage03_quantification_simulatedData).filter(data_stage03_quantification_simulatedData.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_otherData).filter(data_stage03_quantification_otherData.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG0_r).filter(data_stage03_quantification_dG0_r.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_dG0_f).filter(data_stage03_quantification_dG0_f.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_f).filter(data_stage03_quantification_dG_f.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_metabolomicsData).filter(data_stage03_quantification_metabolomicsData.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_r).filter(data_stage03_quantification_dG_r.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_tcc).filter(data_stage03_quantification_tcc.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG0_p).filter(data_stage03_quantification_dG0_p.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_modelPathways).filter(data_stage03_quantification_modelPathways.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_p).filter(data_stage03_quantification_dG_p.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_metid2keggid).filter(data_stage03_quantification_metid2keggid.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_models).filter(data_stage03_quantification_models.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_modelReactions).filter(data_stage03_quantification_modelReactions.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_modelMetabolites).filter(data_stage03_quantification_modelMetabolites.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_simulation).filter(data_stage03_quantification_simulation.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
            else:
                #reset = self.session.query(data_stage03_quantification_simulatedData).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_otherData).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG0_r).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_dG0_f).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_metabolomicsData).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_f).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_r).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG_p).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_metid2keggid).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_models).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_modelReactions).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_modelMetabolites).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_simulation).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_tcc).delete(synchronize_session=False);
                reset = self.session.query(data_stage03_quantification_dG0_p).delete(synchronize_session=False);
                #reset = self.session.query(data_stage03_quantification_modelPathways).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
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
            model_xml = ''
            model_xml = self.stage03_quantification_query.get_row_modelID_dataStage03QuantificationModels(model_id_I);
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
                print 'file_type not supported'
        elif cobra_model_I:
            cobra_model = cobra_model_I;
        # implement optimal KOs and flux constraints:
        for ko in ko_list:
            cobra_model.reactions.get_by_id(ko).lower_bound = 0.0;
            cobra_model.reactions.get_by_id(ko).upper_bound = 0.0;
        for rxn,flux in flux_dict.iteritems():
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
            print cobra_model.solution.f;
            return True;
    def load_models(self,experiment_id_I,model_ids_I=[]):
        '''pre-load all models for the experiment_id'''
        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage03_quantification_query.get_modelID_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
        for model_id in model_ids:
            # get the cobra model
            cobra_model_sbml = None;
            cobra_model_sbml = self.stage03_quantification_query.get_row_modelID_dataStage03QuantificationModels(model_id);
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
                print 'file_type not supported'
            self.models[model_id]=cobra_model;
    def execute_thermodynamicSampling(self,simulation_ids_I=[]):
        '''execute a thermodynamic analysis using the thermodynamic
        module for cobrapy'''

        print 'execute_thermodynamicSmpling...'

    def execute_compareThermodynamicStates(self,experiment_id_I):
        '''perform a  pairwise comparison of thermodynamic states'''

        print 'execute_compareThermodynamicStates'

    def execute_visualizeThermodynamicStates(self,experiment_id_I):
        '''exports thermodynamic data for visualization using escher'''

        print 'execute_visualizeThermodynamicStates'

    #TODO:
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
            model_ids = self.stage03_quantification_query.get_modelID_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
        for model_id in model_ids:
            # get sample names and sample name abbreviations
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.stage03_quantification_query.get_sampleNameAbbreviations_experimentIDAndModelID_dataStage03QuantificationSimulation(experiment_id_I,model_id);
            for sna_cnt,sna in enumerate(sample_name_abbreviations):
                print 'Adding experimental fluxes for sample name abbreviation ' + sna;
                if flux_dict:
                    for k,v in flux_dict[model_id][sna].iteritems():
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
                        row = data_stage03_quantification_measuredFluxes(
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
                        row = data_stage03_quantification_measuredFluxes(
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
            sample_name_abbreviations = self.stage03_quantification_query.get_sampleNameAbbreviations_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
        for sna in sample_name_abbreviations:
            print 'Collecting experimental fluxes for sample name abbreviation ' + sna;
            # get met_ids
            if not met_ids_I:
                met_ids = [];
                met_ids = self.stage03_quantification_query.get_metID_experimentIDAndSampleNameAbbreviation_dataStage01PhysiologyRatesAverages(experiment_id_I,sna);
            else:
                met_ids = met_ids_I;
            if not(met_ids): continue #no component information was found
            for met in met_ids:
                print 'Collecting experimental fluxes for metabolite ' + met;
                # get rateData
                slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var = None,None,None,None,None,None,None;
                slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var = self.stage03_quantification_query.get_rateData_experimentIDAndSampleNameAbbreviationAndMetID_dataStage01PhysiologyRatesAverages(experiment_id_I,sna,met);
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
                row = data_stage03_quantification_measuredFluxes(
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
    def execute_makeEstimatedFluxes(self,experimentID2IsotopomerSimulationID_I = {},sample_name_abbreviations_I = [],snaIsotopomer2snaPhysiology_I={}):
        '''Collect estimated flux data from data_stage02_istopomer_netFluxes for thermodynamic simulation'''
        return
            