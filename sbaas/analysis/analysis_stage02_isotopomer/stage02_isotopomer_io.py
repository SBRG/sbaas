# Dependencies
from analysis.analysis_base import *
from stage02_isotopomer_query import stage02_isotopomer_query
from resources.molmass import Formula
from copy import copy
from math import isnan, isinf
import re
# Dependencies from 3rd party
import scipy.io
import numpy
import h5py
# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file, write_cobra_model_to_sbml_file
from cobra.io import load_matlab_model, save_json_model, load_json_model
from cobra.manipulation.modify import convert_to_irreversible, revert_to_reversible
from cobra.core.Reaction import Reaction
from cobra.core.Metabolite import Metabolite
from cobra.core.Model import Model
# Dependencies from escher
from escher import Builder
# Dependencies from models
from analysis.models.models_query import models_query

class stage02_isotopomer_io(base_analysis):
    def __init__(self,session_I=None):
        if session_I: self.session = session_I;
        else: self.session = Session();
        self.stage02_isotopomer_query = stage02_isotopomer_query(self.session);
    
    def import_data_stage02_isotopomer_analysis_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(settings.workspace_data+filename);
        data.format_data();
        self.add_data_stage02_isotopomer_analysis(data.data);
        data.clear_data();
    def add_data_stage02_isotopomer_analysis(self, data_I):
        '''add rows of data_stage02_isotopomer_analysis'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_analysis(
                            d['analysis_id'],d['simulation_id'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def import_data_stage02_isotopomer_simulation_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(settings.workspace_data+filename);
        data.format_data();
        self.add_data_stage02_isotopomer_simulation(data.data);
        data.clear_data();
    def add_data_stage02_isotopomer_simulation(self, data_I):
        '''add rows of data_stage02_isotopomer_simulation'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_simulation(d['simulation_id'],
                            d['experiment_id'],
                            d['model_id'],
                            d['mapping_id'],
                            d['sample_name_abbreviation'],
                            d['time_point'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit()
    def add_data_stage02_isotopomer_calcFragments(self, data_I):
        '''add rows of data_stage02_isotopomer_calcFragments'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_calcFragments(d['experiment_id'],
                            d['model_id'],
                            d['mapping_id'],
                            d['sample_name_abbreviation'],
                            d['time_point'],
                            d['met_id'],
                            d['fragment_name'],
                            d['fragment_formula'],
                            d['fragment_mass'],
                            d['idv_average'],
                            d['idv_stdev'],
                            d['idv_units'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def import_data_stage02_isotopomer_calcFluxes_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(settings.workspace_data+filename);
        data.format_data();
        self.add_data_stage02_isotopomer_calcFluxes(data.data);
        data.clear_data();
    def add_data_stage02_isotopomer_calcFluxes(self, data_I):
        '''add rows of data_stage02_isotopomer_calcFluxes'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_calcFluxes(d['experiment_id'],
                            d['model_id'],
                            d['mapping_id'],
                            d['sample_name_abbreviation'],
                            d['time_point'],
                            d['rxn_id'],
                            d['flux_average'],
                            d['flux_stdev'],
                            d['flux_lb'],
                            d['flux_ub'],
                            d['flux_units'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def import_data_stage02_isotopomer_tracers_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(settings.workspace_data+filename);
        data.format_data();
        self.add_data_stage02_isotopomer_tracers(data.data);
        data.clear_data();
    def add_data_stage02_isotopomer_tracers(self, data_I):
        '''add rows of data_stage02_isotopomer_tracers'''
        if data_I:
            for d in data_I:
                met_elements = None;
                if d['met_elements']:
                    met_elements = d['met_elements']
                    met_elements = met_elements.replace('{','')
                    met_elements = met_elements.replace('}','')
                    met_elements = met_elements.split(',')
                met_atompositions = None;
                if d['met_atompositions']:
                    met_atompositions = d['met_atompositions']
                    met_atompositions = met_atompositions.replace('{','')
                    met_atompositions = met_atompositions.replace('}','')
                    met_atompositions = met_atompositions.split(',')
                    met_atompositions = [int(x) for x in met_atompositions];
                isotopomer_formula = None;
                if d['isotopomer_formula']:
                    isotopomer_formula = d['isotopomer_formula']
                    isotopomer_formula = isotopomer_formula.replace('{','')
                    isotopomer_formula = isotopomer_formula.replace('}','')
                    isotopomer_formula = isotopomer_formula.split(',')
                try:
                    data_add = data_stage02_isotopomer_tracers(d['experiment_id'],
                            d['sample_name_abbreviation'],
                            d['met_id'],
                            d['met_name'],
                            isotopomer_formula,
                            met_elements,
                            met_atompositions,
                            d['ratio'],
                            d['supplier'],
                            d['supplier_reference'],
                            d['purity'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_models(self, data_I):
        '''add rows of data_stage02_isotopomer_models'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_models(d['model_id'],
                            d['model_name'],
                            d['model_description'],
                            d['model_file'],
                            d['file_type'],
                            d['date']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_modelReactions(self, data_I):
        '''add rows of data_stage02_isotopomer_modelReactions'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_modelReactions(d['model_id'],
                                d['rxn_id'],
                                d['equation'],
                                d['subsystem'],
                                d['gpr'],
                                d['genes'],
                                d['reactants_stoichiometry'],
                                d['products_stoichiometry'],
                                d['reactants_ids'],
                                d['products_ids'],
                                d['lower_bound'],
                                d['upper_bound'],
                                d['objective_coefficient'],
                                d['flux_units'],
                                d['fixed'],
                                d['free'],
                                d['reversibility'],
                                d['weight'],
                                d['used_'],
                                d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_modelMetabolites(self, data_I):
        '''add rows of data_stage02_isotopomer_modelMetabolites'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_modelMetabolites(d['model_id'],
                            d['met_name'],
                            d['met_id'],
                            d['formula'],
                            d['charge'],
                            d['compartment'],
                            d['bound'],
                            d['constraint_sense'],
                            d['lower_bound'],
                            d['upper_bound'],
                            d['balanced'],
                            d['fixed'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def import_data_stage02_isotopomer_measuredFluxes_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(settings.workspace_data+filename);
        data.format_data();
        self.add_data_stage02_isotopomer_measuredFluxes(data.data);
        data.clear_data();
    def add_data_stage02_isotopomer_measuredFluxes(self, data_I):
        '''add rows of data_stage02_isotopomer_measuredFluxes'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_measuredFluxes(d['experiment_id'],
                            d['model_id'],
                            d['sample_name_abbreviation'],
                            #d['time_point'],
                            d['rxn_id'],
                            d['flux_average'],
                            d['flux_stdev'],
                            d['flux_lb'],
                            d['flux_ub'],
                            d['flux_units'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_measuredPools(self, data_I):
        '''add rows of data_stage02_isotopomer_measuredPools'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_measuredPools(d['experiment_id'],
                            d['model_id'],
                            d['sample_name_abbreviation'],
                            d['time_point'],
                            d['met_id'],
                            d['pool_size'],
                            d['concentration_average'],
                            d['concentration_var'],
                            d['concentration_lb'],
                            d['concentration_ub'],
                            d['concentration_units'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def import_data_stage02_isotopomer_measuredFragments_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(settings.workspace_data+filename);
        data.format_data();
        self.add_data_stage02_isotopomer_measuredFragments(data.data);
        data.clear_data();
    def add_data_stage02_isotopomer_measuredFragments(self, data_I):
        '''add rows of data_stage02_isotopomer_measuredFragments'''
        if data_I:
            for d in data_I:
                intensity_normalized_average = None;
                if d['intensity_normalized_average']:
                    intensity_normalized_average = d['intensity_normalized_average']
                    intensity_normalized_average = intensity_normalized_average.replace('{','')
                    intensity_normalized_average = intensity_normalized_average.replace('}','')
                    intensity_normalized_average = intensity_normalized_average.split(',')
                intensity_normalized_cv = None;
                if d['intensity_normalized_cv']:
                    intensity_normalized_cv = d['intensity_normalized_cv']
                    intensity_normalized_cv = intensity_normalized_cv.replace('{','')
                    intensity_normalized_cv = intensity_normalized_cv.replace('}','')
                    intensity_normalized_cv = intensity_normalized_cv.split(',')
                intensity_normalized_stdev = None;
                if d['intensity_normalized_stdev']:
                    intensity_normalized_stdev = d['intensity_normalized_stdev']
                    intensity_normalized_stdev = intensity_normalized_stdev.replace('{','')
                    intensity_normalized_stdev = intensity_normalized_stdev.replace('}','')
                    intensity_normalized_stdev = intensity_normalized_stdev.split(',')
                met_elements = None;
                if d['met_elements']:
                    met_elements = d['met_elements']
                    met_elements = met_elements.replace('{','')
                    met_elements = met_elements.replace('}','')
                    met_elements = met_elements.split(',')
                met_atompositions = None;
                if d['met_atompositions']:
                    met_atompositions = d['met_atompositions']
                    met_atompositions = met_atompositions.replace('{','')
                    met_atompositions = met_atompositions.replace('}','')
                    met_atompositions = met_atompositions.split(',')
                    met_atompositions = [int(x) for x in met_atompositions];
                try:
                    data_add = data_stage02_isotopomer_measuredFragments(d['experiment_id'],
                                d['sample_name_abbreviation'],
                                d['time_point'],
                                d['met_id'],
                                d['fragment_id'],
                                d['fragment_formula'],
                                intensity_normalized_average,
                                intensity_normalized_cv,
                                intensity_normalized_stdev,
                                d['intensity_normalized_units'],
                                d['scan_type'],
                                met_elements,
                                met_atompositions,
                                d['used_'],
                                d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_atomMappingReactions(self, data_I):
        '''add rows of data_stage02_isotopomer_atomMappingReactions'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_atomMappingReactions(
                                #d['id'],
                                d['mapping_id'],
                                d['rxn_id'],
                                d['rxn_description'],
                                d['reactants_stoichiometry_tracked'],
                                d['products_stoichiometry_tracked'],
                                d['reactants_ids_tracked'],
                                d['products_ids_tracked'],
                                d['reactants_elements_tracked'],
                                d['products_elements_tracked'],
                                d['reactants_positions_tracked'],
                                d['products_positions_tracked'],
                                d['reactants_mapping'],
                                d['products_mapping'],
                                d['rxn_equation'],
                                d['used_'],
                                d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_atomMappingMetabolites(self, data_I):
        '''add rows of data_stage02_isotopomer_atomMappingMetabolites'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_atomMappingMetabolites(
                                #d['id'],
                                d['mapping_id'],
                                d['met_id'],
                                d['met_elements'],
                                d['met_atompositions'],
                                d['met_symmetry_elements'],
                                d['met_symmetry_atompositions'],
                                d['used_'],
                                d['comment_'],
                                d['met_mapping'],
                                d['base_met_ids'],
                                d['base_met_elements'],
                                d['base_met_atompositions'],
                                d['base_met_symmetry_elements'],
                                d['base_met_symmetry_atompositions'],
                                d['base_met_indices']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_modelReactionsAtomMapping(self, data_I):
        '''add rows of data_stage02_isotopomer_modelReactionsAtomMapping'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_modelReactionsAtomMapping(d['model_id'],
                                d['mapping_id'],
                                d['rxn_id'],
                                d['equation'],
                                d['subsystem'],
                                d['gpr'],
                                d['genes'],
                                d['reactants_stoichiometry'],
                                d['products_stoichiometry'],
                                d['reactants_ids'],
                                d['products_ids'],
                                d['reactants_stoichiometry_tracked'],
                                d['products_stoichiometry_tracked'],
                                d['reactants_ids_tracked'],
                                d['products_ids_tracked'],
                                d['reactants_elements_tracked'],
                                d['products_elements_tracked'],
                                d['reactants_mapping'],
                                d['products_mapping'],
                                d['rxn_equation'],
                                d['lower_bound'],
                                d['upper_bound'],
                                d['objective_coefficient'],
                                d['flux_units'],
                                d['fixed'],
                                d['free'],
                                d['reversibility'],
                                d['weight'],
                                d['used_'],
                                d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_modelMetabolitesAtomMapping(self, data_I):
        '''add rows of data_stage02_isotopomer_modelMetabolitesAtomMapping'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_modelMetabolitesAtomMapping(d['model_id'],
                                d['mapping_id'],
                            d['met_name'],
                            d['met_id'],
                            d['formula'],
                            d['charge'],
                            d['compartment'],
                            d['bound'],
                            d['constraint_sense'],
                            d['met_elements'],
                            d['met_atompositions'],
                            d['balanced'],
                            d['met_symmetry_elements'],
                            d['met_symmetry_atompositions'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_fittedFluxes(self, data_I):
        '''add rows of data_stage02_isotopomer_fittedFluxes'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_fittedFluxes(d['simulation_id'],
                    d['simulation_dateAndTime'],
                    #d['experiment_id'],
                    #d['model_id'],
                    #d['mapping_id'],
                    #d['sample_name_abbreviation'],
                    #d['time_point'],
                    d['rxn_id'],
                    d['flux'],
                    d['flux_stdev'],
                    d['flux_lb'],
                    d['flux_ub'],
                    d['flux_units'],
                    d['fit_alf'],
                    d['fit_chi2s'],
                    d['fit_cor'],
                    d['fit_cov'],
                    d['free'],
                    d['used_'],
                    d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_fittedFragments(self, data_I):
        '''add rows of data_stage02_isotopomer_fittedFragments'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_fittedFragments(d['simulation_id'],
                            d['simulation_dateAndTime'],
                            d['experiment_id'],
                            #d['model_id'],
                            #d['mapping_id'],
                            d['sample_name_abbreviation'],
                            d['time_point'],
                            d['fragment_id'],
                            #d['fragment_formula'],
                            d['fragment_mass'],
                            d['fit_val'],
                            d['fit_stdev'],
                            d['fit_units'],
                            d['fit_alf'],
                            d['fit_cor'],
                            d['fit_cov'],
                            d['free'],
                            d['used_'],
                            d['comment_']
                            );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_fittedData(self, data_I):
        '''add rows of data_stage02_isotopomer_fittedData'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_fittedData(d['simulation_id'],
                    d['simulation_dateAndTime'],
                    #d['experiment_id'],
                    #d['model_id'],
                    #d['mapping_id'],
                    #d['sample_name_abbreviation'],
                    #d['time_point'],
                    d['fitted_echi2'],
                    d['fitted_alf'],
                    d['fitted_chi2'],
                    d['fitted_dof'],
                    d['used_'],
                    d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_fittedMeasuredFluxes(self, data_I):
        '''add rows of data_stage02_isotopomer_fittedMeasuredFluxes'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_fittedMeasuredFluxes(d['simulation_id'],
                    d['simulation_dateAndTime'],
                    d['experiment_id'],
                    #d['model_id'],
                    #d['mapping_id'],
                    d['sample_name_abbreviation'],
                    #d['time_point'],
                    d['rxn_id'],
                    d['fitted_sres'],
                    d['used_'],
                    d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_fittedMeasuredFragments(self, data_I):
        '''add rows of data_stage02_isotopomer_fittedMeasuredFragments'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_fittedMeasuredFragments(d['simulation_id'],
                    d['simulation_dateAndTime'],
                    d['experiment_id'],
                    #d['model_id'],
                    #d['mapping_id'],
                    d['sample_name_abbreviation'],
                    #d['time_point'],
                    #d['met_id'],
                    d['fragment_id'],
                    #d['fragment_formula'],
                    d['fitted_sres'],
                    d['used_'],
                    d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_fittedMeasuredFluxResiduals(self, data_I):
        '''add rows of data_stage02_isotopomer_fittedMeasuredFluxResiduals'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_fittedMeasuredFluxResiduals(d['simulation_id'],
                    d['simulation_dateAndTime'],
                    d['experiment_id'],
                    #d['model_id'],
                    #d['mapping_id'],
                    d['sample_name_abbreviation'],
                    d['time_point'],
                    d['rxn_id'],
                    d['res_data'],
                    d['res_esens'],
                    d['res_fit'],
                    d['res_msens'],
                    d['res_peak'],
                    d['res_stdev'],
                    d['res_val'],
                    d['used_'],
                    d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_fittedMeasuredFragmentResiduals(self, data_I):
        '''add rows of data_stage02_isotopomer_fittedMeasuredFragmentResiduals'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_fittedMeasuredFragmentResiduals(d['simulation_id'],
                    d['simulation_dateAndTime'],
                    d['experiment_id'],
                    #d['model_id'],
                    #d['mapping_id'],
                    d['sample_name_abbreviation'],
                    d['time_point'],
                    d['fragment_id'],
                    #d['fragment_formula'],
                    d['fragment_mass'],
                    d['res_data'],
                    d['res_esens'],
                    d['res_fit'],
                    d['res_msens'],
                    d['res_peak'],
                    d['res_stdev'],
                    d['res_val'],
                    d['used_'],
                    d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_simulationParameters(self, data_I):
        '''add rows of data_stage02_isotopomer_simulationParameters'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_simulationParameters(d['simulation_id'],
                    d['simulation_dateAndTime'],
                    d['cont_alpha'],
                    d['cont_reltol'],
                    d['cont_steps'],
                    d['fit_nudge'],
                    d['fit_reinit'],
                    d['fit_reltol'],
                    d['fit_starts'],
                    d['fit_tau'],
                    d['hpc_mcr'],
                    d['hpc_on'],
                    d['hpc_serve'],
                    d['int_maxstep'],
                    d['int_reltol'],
                    d['int_senstol'],
                    d['int_timeout'],
                    d['int_tspan'],
                    d['ms_correct'],
                    d['oed_crit'],
                    d['oed_reinit'],
                    d['oed_tolf'],
                    d['oed_tolx'],
                    d['sim_more'],
                    d['sim_na'],
                    d['sim_sens'],
                    d['sim_ss'],
                    d['sim_tunit']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_data_stage02_isotopomer_fittedNetFluxes(self, data_I):
        '''add rows of data_stage02_isotopomer_fittedNetFluxes'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_isotopomer_fittedNetFluxes(d['simulation_id'],
                    d['simulation_dateAndTime'],
                    #d['experiment_id'],
                    #d['model_id'],
                    #d['mapping_id'],
                    #d['sample_name_abbreviation'],
                    #d['time_point'],
                    d['rxn_id'],
                    d['flux'],
                    d['flux_stdev'],
                    d['flux_lb'],
                    d['flux_ub'],
                    d['flux_units'],
                    d['used_'],
                    d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    # TODO: add filters for update queries:
    def update_data_stage02_isotopomer_analysis(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_analysis'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_analysis).filter(
                            data_stage02_isotopomer_analysis.id.like(d['id'])
                            ).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'simulation_id':d['simulation_id'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_simulation(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_simulation'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_simulation).filter(
                            data_stage02_isotopomer_simulation.id.like(d['id'])
                            ).update(
                            {
                            'simulation_id':d['simulation_id'],
                            'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'mapping_id':d['mapping_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_calcFragments(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_calcFragments'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_calcFragments).filter(
                            #sample.sample_name.like(d['sample_name'])
                            ).update(
                            {'experiment_id':d['experiment_id'],
                                'model_id':d['model_id'],
                                'mapping_id':d['mapping_id'],
                                'sample_name_abbreviation':d['sample_name_abbreviation'],
                                'time_point':d['time_point'],
                                'met_id':d['met_id'],
                                'fragment_name':d['fragment_name'],
                                'fragment_formula':d['fragment_formula'],
                                'fragment_mass':d['fragment_mass'],
                                'idv_average':d['idv_average'],
                                'idv_stdev':d['idv_stdev'],
                                'idv_units':d['idv_units'],
                                'used_':d['used_'],
                                'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_calcFluxes(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_calcFluxes'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_calcFluxes).filter(
                            #sample.sample_name.like(d['sample_name'])
                            ).update(
                            {'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'mapping_id':d['mapping_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'rxn_id':d['rxn_id'],
                            'flux_average':d['flux_average'],
                            'flux_stdev':d['flux_stdev'],
                            'flux_lb':d['flux_lb'],
                            'flux_ub':d['flux_ub'],
                            'flux_units':d['flux_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_tracers(self,data_I):
        #TODO:
        '''update rows of '''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(sample).filter(
                            #sample.sample_name.like(d['sample_name'])
                            ).update(
                            {'experiment_id':d['experiment_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'model_id':d['model_id'],
                            'met_id':d['met_id'],
                            'met_name':d['met_name'],
                            'isotopomer_formula':d['isotopomer_formula'],
                            'met_elements':d['met_elements'],
                            'met_atompositions':d['met_atompositions'],
                            'ratio':d['ratio'],
                            'supplier':d['supplier'],
                            'supplier_reference':d['supplier_reference'],
                            'purity':d['purity'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_models(self,data_I):
        '''update rows of data_stage02_isotopomer_models'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_models).filter(
                            data_stage02_isotopomer_models.model_id.like(d['model_id'])
                            ).update(
                            {
                                #'model_id':d['model_id'],
                            'model_name':d['model_name'],
                            'model_description':d['model_description'],
                            'model_file':d['model_file'],
                            'file_type':d['file_type'],
                            'date':d['date']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_modelReactions(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_modelReactions'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_modelReactions).filter(
                            #sample.sample_name.like(d['sample_name'])
                            ).update(
                            {'model_id':d['model_id'],
                            'rxn_id':d['rxn_id'],
                            'equation':d['equation'],
                            'subsystem':d['subsystem'],
                            'gpr':d['gpr'],
                            'genes':d['genes'],
                            'reactants_stoichiometry':d['reactants_stoichiometry'],
                            'products_stoichiometry':d['products_stoichiometry'],
                            'reactants_ids':d['reactants_ids'],
                            'products_ids':d['products_ids'],
                            'lower_bound':d['lower_bound'],
                            'upper_bound':d['upper_bound'],
                            'objective_coefficient':d['objective_coefficient'],
                            'flux_units':d['flux_units'],
                            'fixed':d['fixed'],
                            'free':d['free'],
                            'reversibility':d['reversibility'],
                            'weight':d['weight'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_modelMetabolites(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_modelMetabolites'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_modelMetabolites).filter(
                            #sample.sample_name.like(d['sample_name'])
                            ).update(
                            {'model_id':d['model_id'],
                            'met_name':d['met_name'],
                            'met_id':d['met_id'],
                            'formula':d['formula'],
                            'charge':d['charge'],
                            'compartment':d['compartment'],
                            'bound':d['bound'],
                            'constraint_sense':d['constraint_sense'],
                            'lower_bound':d['lower_bound'],
                            'upper_bound':d['upper_bound'],
                            'balanced':d['balanced'],
                            'fixed':d['fixed'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_measuredFluxes(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_measuredFluxes'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_measuredFluxes).filter(
                            #sample.sample_name.like(d['sample_name'])
                            ).update(
                            {'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            #'time_point':d['time_point'],
                            'rxn_id':d['rxn_id'],
                            'flux_average':d['flux_average'],
                            'flux_stdev':d['flux_stdev'],
                            'flux_lb':d['flux_lb'],
                            'flux_ub':d['flux_ub'],
                            'flux_units':d['flux_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_measuredPools(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_measuredPools'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_measuredPools).filter(
                            #sample.sample_name.like(d['sample_name'])
                            ).update(
                            {'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'met_id':d['met_id'],
                            'pool_size':d['pool_size'],
                            'concentration_average':d['concentration_average'],
                            'concentration_var':d['concentration_var'],
                            'concentration_lb':d['concentration_lb'],
                            'concentration_ub':d['concentration_ub'],
                            'concentration_units':d['concentration_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_measuredFragments(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_measuredFragments'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_measuredFragments).filter(
                            #sample.sample_name.like(d['sample_name'])
                            ).update(
                            {'experiment_id':d['experiment_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'met_id':d['met_id'],
                            'fragment_id':d['fragment_id'],
                            'fragment_formula':d['fragment_formula'],
                            'intensity_normalized_average':d['intensity_normalized_average'],
                            'intensity_normalized_cv':d['intensity_normalized_cv'],
                            'intensity_normalized_stdev':d['intensity_normalized_stdev'],
                            'intensity_normalized_units':d['intensity_normalized_units'],
                            'scan_type':d['scan_type'],
                            'met_elements':d['met_elements'],
                            'met_atompositions':d['met_atompositions'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def import_data_stage02_isotopomer_atomMappingReactions_update(self, filename):
        '''table updates'''
        data = base_importData();
        data.read_csv(settings.workspace_data+filename);
        #data.read_json(filename);
        data.format_data();
        self.update_data_stage02_isotopomer_atomMappingReactions(data.data);
        data.clear_data();
    def update_data_stage02_isotopomer_atomMappingReactions(self,data_I):
        '''update rows of data_stage02_isotopomer_atomMappingReactions'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_atomMappingReactions).filter(
                            data_stage02_isotopomer_atomMappingReactions.id == d['id']
                            ).update(
                            {'mapping_id':d['mapping_id'],
                            'rxn_id':d['rxn_id'],
                            'rxn_description':d['rxn_description'],
                            'reactants_stoichiometry_tracked':d['reactants_stoichiometry_tracked'],
                            'products_stoichiometry_tracked':d['products_stoichiometry_tracked'],
                            'reactants_ids_tracked':d['reactants_ids_tracked'],
                            'products_ids_tracked':d['products_ids_tracked'],
                            'reactants_elements_tracked':d['reactants_elements_tracked'],
                            'products_elements_tracked':d['products_elements_tracked'],
                            'reactants_positions_tracked':d['reactants_positions_tracked'],
                            'products_positions_tracked':d['products_positions_tracked'],
                            'reactants_mapping':d['reactants_mapping'],
                            'products_mapping':d['products_mapping'],
                            'rxn_equation':d['rxn_equation'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def import_data_stage02_isotopomer_atomMappingMetabolites_update(self, filename):
        '''table updates'''
        data = base_importData();
        data.read_csv(settings.workspace_data+filename);
        #data.read_json(filename);
        data.format_data();
        self.update_data_stage02_isotopomer_atomMappingMetabolites(data.data);
        data.clear_data();
    def update_data_stage02_isotopomer_atomMappingMetabolites(self,data_I):
        '''update rows of data_stage02_isotopomer_atomMappingMetabolites'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_atomMappingMetabolites).filter(
                            data_stage02_isotopomer_atomMappingMetabolites.id == d['id']
                            ).update(
                            {'mapping_id':d['mapping_id'],
                            'met_id':d['met_id'],
                            'met_elements':d['met_elements'],
                            'met_atompositions':d['met_atompositions'],
                            'met_symmetry_elements':d['met_symmetry_elements'],
                            'met_symmetry_atompositions':d['met_symmetry_atompositions'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],
                            'met_mapping':d['met_mapping'],
                            'base_met_ids':d['base_met_ids'],
                            'base_met_elements':d['base_met_elements'],
                            'base_met_atompositions':d['base_met_atompositions'],
                            'base_met_symmetry_elements':d['base_met_symmetry_elements'],
                            'base_met_symmetry_atompositions':d['base_met_symmetry_atompositions'],
                            'base_met_indices':d['base_met_indices']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_modelReactionsAtomMapping(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_modelReactionsAtomMapping'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_modelReactionsAtomMapping).filter(
                            #sample.sample_name.like(d['sample_name'])
                            ).update(
                            {'model_id':d['model_id'],
                            'mapping_id':d['mapping_id'],
                            'rxn_id':d['rxn_id'],
                            'equation':d['equation'],
                            'subsystem':d['subsystem'],
                            'gpr':d['gpr'],
                            'genes':d['genes'],
                            'reactants_stoichiometry':d['reactants_stoichiometry'],
                            'products_stoichiometry':d['products_stoichiometry'],
                            'reactants_ids':d['reactants_ids'],
                            'products_ids':d['products_ids'],
                            'reactants_stoichiometry_tracked':d['reactants_stoichiometry_tracked'],
                            'products_stoichiometry_tracked':d['products_stoichiometry_tracked'],
                            'reactants_ids_tracked':d['reactants_ids_tracked'],
                            'products_ids_tracked':d['products_ids_tracked'],
                            'reactants_elements_tracked':d['reactants_elements_tracked'],
                            'products_elements_tracked':d['products_elements_tracked'],
                            'reactants_mapping':d['reactants_mapping'],
                            'products_mapping':d['products_mapping'],
                            'rxn_equation':d['rxn_equation'],
                            'lower_bound':d['lower_bound'],
                            'upper_bound':d['upper_bound'],
                            'objective_coefficient':d['objective_coefficient'],
                            'flux_units':d['flux_units'],
                            'fixed':d['fixed'],
                            'free':d['free'],
                            'reversibility':d['reversibility'],
                            'weight':d['weight'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_modelMetabolitesAtomMapping(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_modelMetabolitesAtomMapping'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_modelMetabolitesAtomMapping).filter(
                            #sample.sample_name.like(d['sample_name'])
                            ).update(
                            {'model_id':d['model_id'],
                            'mapping_id':d['mapping_id'],
                            'met_name':d['met_name'],
                            'met_id':d['met_id'],
                            'formula':d['formula'],
                            'charge':d['charge'],
                            'compartment':d['compartment'],
                            'met_elements':d['met_elements'],
                            'met_atompositions':d['met_atompositions'],
                            'balanced':d['balanced'],
                            'met_symmetry_elements':d['met_symmetry_elements'],
                            'met_symmetry_atompositions':d['met_symmetry_atompositions'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],
                            'met_mapping':d['met_mapping'],
                            'base_met_ids':d['base_met_ids'],
                            'base_met_elements':d['base_met_elements'],
                            'base_met_atompositions':d['base_met_atompositions'],
                            'base_met_symmetry_elements':d['base_met_symmetry_elements'],
                            'base_met_symmetry_atompositions':d['base_met_symmetry_atompositions']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_fittedFluxes(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_fittedFluxes'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_fittedFluxes).filter(
                            #data_stage02_isotopomer_fittedFluxes.sample_name.like(d['sample_name'])
                            ).update(
                            {'simulation_id':d['simulation_id'],
                            'simulation_dateAndTime':d['simulation_dateAndTime'],
                            #'experiment_id':d['experiment_id'],
                            #'model_id':d['model_id'],
                            #'mapping_id':d['mapping_id'],
                            #'sample_name_abbreviation':d['sample_name_abbreviation'],
                            #'time_point':d['time_point'],
                            'rxn_id':d['rxn_id'],
                            'flux':d['flux'],
                            'flux_stdev':d['flux_stdev'],
                            'flux_lb':d['flux_lb'],
                            'flux_ub':d['flux_ub'],
                            'flux_units':d['flux_units'],
                            'fit_alf':d['fit_alf'],
                            'fit_chi2s':d['fit_chi2s'],
                            'fit_cor':d['fit_cor'],
                            'fit_cov':d['fit_cov'],
                            'free':d['free'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_fittedFragments(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_fittedFragments'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_fittedFragments).filter(
                            #data_stage02_isotopomer_fittedFragments.sample_name.like(d['sample_name'])
                            ).update(
                            {'simulation_id':d['simulation_id'],
                            'simulation_dateAndTime':d['simulation_dateAndTime'],
                            'experiment_id':d['experiment_id'],
                            #'model_id':d['model_id'],
                            #'mapping_id':d['mapping_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'fragment_id':d['fragment_id'],
                            #'fragment_formula':d['fragment_formula'],
                            'fragment_mass':d['fragment_mass'],
                            'fit_val':d['fit_val'],
                            'fit_stdev':d['fit_stdev'],
                            'fit_units':d['fit_units'],
                            'fit_alf':d['fit_alf'],
                            'fit_chi2s':d['fit_chi2s'],
                            'fit_cor':d['fit_cor'],
                            'fit_cov':d['fit_cov'],
                            'free':d['free'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_fittedData(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_fittedData'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_fittedData).filter(
                            #data_stage02_isotopomer_fittedData.sample_name.like(d['sample_name'])
                            ).update(
                            {'simulation_id':d['simulation_id'],
                            'simulation_dateAndTime':d['simulation_dateAndTime'],
                            #'experiment_id':d['experiment_id'],
                            #'model_id':d['model_id'],
                            #'mapping_id':d['mapping_id'],
                            #'sample_name_abbreviation':d['sample_name_abbreviation'],
                            #'time_point':d['time_point'],
                            'fitted_echi2':d['fitted_echi2'],
                            'fitted_alf':d['fitted_alf'],
                            'fitted_chi2':d['fitted_chi2'],
                            'fitted_dof':d['fitted_dof'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_fittedMeasuredFluxes(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_fittedMeasuredFluxes'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_fittedMeasuredFluxes).filter(
                            #data_stage02_isotopomer_fittedMeasuredFluxes.sample_name.like(d['sample_name'])
                            ).update(
                            {'simulation_id':d['simulation_id'],
                            'simulation_dateAndTime':d['simulation_dateAndTime'],
                            'experiment_id':d['experiment_id'],
                            #'model_id':d['model_id'],
                            #'mapping_id':d['mapping_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            #'time_point':d['time_point'],
                            'rxn_id':d['rxn_id'],
                            'fitted_sres':d['fitted_sres'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_fittedMeasuredFragments(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_fittedMeasuredFragments'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_fittedMeasuredFragments).filter(
                            #data_stage02_isotopomer_fittedMeasuredFragments.sample_name.like(d['sample_name'])
                            ).update(
                            {'simulation_id':d['simulation_id'],
                            'simulation_dateAndTime':d['simulation_dateAndTime'],
                            'experiment_id':d['experiment_id'],
                            #'model_id':d['model_id'],
                            #'mapping_id':d['mapping_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            #'time_point':d['time_point'],
                            #'met_id':d['met_id'],
                            'fragment_id':d['fragment_id'],
                            #'fragment_formula':d['fragment_formula'],
                            'fitted_sres':d['fitted_sres'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_fittedMeasuredFluxResiduals(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_fittedMeasuredFluxResiduals'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_fittedMeasuredFluxResiduals).filter(
                            #data_stage02_isotopomer_fittedMeasuredFluxResiduals.sample_name.like(d['sample_name'])
                            ).update(
                            {'simulation_id':d['simulation_id'],
                            'simulation_dateAndTime':d['simulation_dateAndTime'],
                            'experiment_id':d['experiment_id'],
                            #'model_id':d['model_id'],
                            #'mapping_id':d['mapping_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'rxn_id':d['rxn_id'],
                            'res_data':d['res_data'],
                            'res_esens':d['res_esens'],
                            'res_fit':d['res_fit'],
                            'res_msens':d['res_msens'],
                            'res_peak':d['res_peak'],
                            'res_stdev':d['res_stdev'],
                            'res_val':d['res_val'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_fittedMeasuredFragmentResiduals(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_fittedMeasuredFragmentResiduals'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_fittedMeasuredFragmentResiduals).filter(
                            #data_stage02_isotopomer_fittedMeasuredFragmentResiduals.sample_name.like(d['sample_name'])
                            ).update(
                            {'simulation_id':d['simulation_id'],
                            'simulation_dateAndTime':d['simulation_dateAndTime'],
                            'experiment_id':d['experiment_id'],
                            #'model_id':d['model_id'],
                            #'mapping_id':d['mapping_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'fragment_id':d['fragment_id'],
                            #'fragment_formula':d['fragment_formula'],
                            'fragment_mass':d['fragment_mass'],
                            'res_data':d['res_data'],
                            'res_esens':d['res_esens'],
                            'res_fit':d['res_fit'],
                            'res_msens':d['res_msens'],
                            'res_peak':d['res_peak'],
                            'res_stdev':d['res_stdev'],
                            'res_val':d['res_val'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_data_stage02_isotopomer_simulationParameters(self,data_I):
        #TODO:
        '''update rows of data_stage02_isotopomer_simulationParameters'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_isotopomer_simulationParameters).filter(
                            #data_stage02_isotopomer_simulationParameters.sample_name.like(d['sample_name'])
                            ).update(
                            {'simulation_id':d['simulation_id'],
                            'simulation_dateAndTime':d['simulation_dateAndTime'],
                            'cont_alpha':d['cont_alpha'],
                            'cont_reltol':d['cont_reltol'],
                            'cont_steps':d['cont_steps'],
                            'fit_nudge':d['fit_nudge'],
                            'fit_reinit':d['fit_reinit'],
                            'fit_reltol':d['fit_reltol'],
                            'fit_starts':d['fit_starts'],
                            'fit_tau':d['fit_tau'],
                            'hpc_mcr':d['hpc_mcr'],
                            'hpc_on':d['hpc_on'],
                            'hpc_serve':d['hpc_serve'],
                            'int_maxstep':d['int_maxstep'],
                            'int_reltol':d['int_reltol'],
                            'int_senstol':d['int_senstol'],
                            'int_timeout':d['int_timeout'],
                            'int_tspan':d['int_tspan'],
                            'ms_correct':d['ms_correct'],
                            'oed_crit':d['oed_crit'],
                            'oed_reinit':d['oed_reinit'],
                            'oed_tolf':d['oed_tolf'],
                            'oed_tolx':d['oed_tolx'],
                            'sim_more':d['sim_more'],
                            'sim_na':d['sim_na'],
                            'sim_sens':d['sim_sens'],
                            'sim_ss':d['sim_ss'],
                            'sim_tunit':d['sim_tunit']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    # model input:
    def import_dataStage02IsotopomerModel_sbml(self, model_id_I, date_I, model_sbml):
        '''import isotopomer model from file'''
        dataStage02IsotopomerModelRxns_data = [];
        dataStage02IsotopomerModelMets_data = [];
        dataStage02IsotopomerModels_data,\
            dataStage02IsotopomerModelRxns_data,\
            dataStage02IsotopomerModelMets_data = self._parse_model_sbml(model_id_I, date_I, model_sbml)
        self.add_data_stage02_isotopomer_modelMetabolites(dataStage02IsotopomerModelMets_data);
        self.add_data_stage02_isotopomer_modelReactions(dataStage02IsotopomerModelRxns_data);
        self.add_data_stage02_isotopomer_models(dataStage02IsotopomerModels_data);
    def import_dataStage02IsotopomerModelAtomMapping_sbmlAndCsv(self, model_id_I, date_I, model_sbml, isotopomer_mapping):
        '''import isotopomer model from file'''
        dataStage02IsotopomerModels_data = [];
        dataStage02IsotopomerModelRxns_data_tmp = [];
        dataStage02IsotopomerModelMets_data = [];
        dataStage02IsotopomerModels_data,\
            dataStage02IsotopomerModelRxns_data_tmp,\
            dataStage02IsotopomerModelMets_data = self._parse_model_sbml(model_sbml)
        isotopomer_mapping_data = self._parse_isotopomer_mapping_csvToDict(isotopomer_mapping)
        # combine model_data and isotopomer_mapping_data
        dataStage02IsotopomerModelRxns_data = [];
        for r in dataStage02IsotopomerModelRxns_data_tmp:
            if isotopomer_mapping_data.has_key(r['rxn_id']):
                r['reactants_stoichiometry_tracked'] = isotopomer_mapping_data[r['rxn_id']]['reactants_stoichiometry_tracked'];
                r['products_stoichiometry_tracked'] = isotopomer_mapping_data[r['rxn_id']]['products_stoichiometry_tracked'];
                r['reactants_ids_tracked'] = isotopomer_mapping_data[r['rxn_id']]['reactants_ids_tracked'];
                r['products_ids_tracked'] = isotopomer_mapping_data[r['rxn_id']]['products_ids_tracked'];
                r['reactants_mapping'] = isotopomer_mapping_data[r['rxn_id']]['reactants_mapping'];
                r['products_mapping'] = isotopomer_mapping_data[r['rxn_id']]['products_mapping'];
                r['reactants_elements_tracked'] = isotopomer_mapping_data[r['rxn_id']]['reactants_elements_tracked'];
                r['products_elements_tracked'] = isotopomer_mapping_data[r['rxn_id']]['products_elements_tracked'];
                r['mapping_id'] = isotopomer_mapping_data[r['rxn_id']]['mapping_id'];
                r['rxn_equation'] = isotopomer_mapping_data[r['rxn_id']]['rxn_equation'];
                dataStage02sotopomerModelRxns_data.append(r);
        self.add_data_stage02_isotopomer_models(dataStage02IsotopomerModels_data);
        self.add_data_stage02_isotopomer_modelReactions(dataStage02IsotopomerModelRxns_tmp);
        self.add_data_stage02_isotopomer_modelMetabolites(dataStage02IsotopomerModelMets);
        self.add_data_stage02_isotopomer_atomMappingReactions(isotopomer_mapping_data);
    def import_dataStage02IsotopomerAtomMapping_csv(self, isotopomer_mapping):
        '''import isotopomer atom mapping from file'''
        isotopomer_mapping_data = self._parse_isotopomer_mapping_csv(isotopomer_mapping)
        self.add_data_stage02_isotopomer_atomMappingReactions(isotopomer_mapping_data);
    def _parse_model_sbml(self,model_id_I,date_I,filename_I):
        # Read in the sbml file and define the model conditions
        cobra_model = create_cobra_model_from_sbml_file(filename_I, print_time=True)
        model_data = [];
        model_data_tmp = {};
        # parse out model metadata
        model_data_tmp['model_id'] = model_id_I;
        model_data_tmp['model_name'] = None;
        model_data_tmp['date'] = date_I;
        model_data_tmp['model_description'] = cobra_model.description;
        with open(filename_I, 'r') as f:
            model_data_tmp['model_file'] = f.read();
        model_data_tmp['file_type'] = 'sbml'
        model_data.append(model_data_tmp)
        reaction_data = [];
        # parse out reaction data
        for r in cobra_model.reactions:
            reaction_data_dict = {};
            reaction_data_dict['model_id'] = model_id_I
            reaction_data_dict['rxn_id'] = r.id
            reaction_data_dict['rxn_name'] = r.name
            reaction_data_dict['equation'] = r.build_reaction_string()
            reaction_data_dict['subsystem'] = r.subsystem
            reaction_data_dict['gpr'] = r.gene_reaction_rule
            reaction_data_dict['genes'] = []
            genes = r.genes;
            for g in genes:
                reaction_data_dict['genes'].append(g.id);
            reaction_data_dict['reactants_stoichiometry'] = [];
            reaction_data_dict['reactants_ids'] = [];
            reactants = r.reactants;
            for react in reactants:
                reaction_data_dict['reactants_stoichiometry'].append(r.get_coefficient(react.id));
                reaction_data_dict['reactants_ids'].append(react.id);
            reaction_data_dict['products_stoichiometry'] = [];
            reaction_data_dict['products_ids'] = [];
            products = r.products;
            for prod in products:
                reaction_data_dict['products_stoichiometry'].append(r.get_coefficient(prod.id));
                reaction_data_dict['products_ids'].append(prod.id);
            reaction_data_dict['lower_bound'] = r.lower_bound
            reaction_data_dict['upper_bound'] = r.upper_bound
            reaction_data_dict['objective_coefficient'] = r.objective_coefficient
            reaction_data_dict['flux_units'] = 'mmol*gDW-1*hr-1'
            reaction_data_dict['reversibility'] = r.reversibility
            #reaction_data_dict['reactants_stoichiometry_tracked'] = None;
            #reaction_data_dict['products_stoichiometry_tracked'] = None;
            #reaction_data_dict['reactants_ids_tracked'] = None;
            #reaction_data_dict['products_ids_tracked'] = None;
            #reaction_data_dict['reactants_mapping'] = None;
            #reaction_data_dict['products_mapping'] = None;
            #reaction_data_dict['rxn_equation'] = None;
            reaction_data_dict['fixed'] = None;
            reaction_data_dict['free'] = None;
            reaction_data_dict['weight'] = None;
            reaction_data_dict['used_'] = True
            reaction_data_dict['comment_'] = None;
            reaction_data.append(reaction_data_dict);
        metabolite_data = [];
        # parse out metabolite data
        for met in cobra_model.metabolites:
            metabolite_data_tmp = {};
            metabolite_data_tmp['model_id'] = model_id_I
            metabolite_data_tmp['met_name'] = met.name;
            metabolite_data_tmp['met_id'] = met.id;
            formula = {};
            for k,v in met.formula.elements.iteritems():
                formula[k] = {0:v};
            tmp = Formula()
            tmp._elements=formula
            metabolite_data_tmp['formula'] = tmp.formula;
            metabolite_data_tmp['charge'] = met.charge
            metabolite_data_tmp['compartment'] = met.compartment
            metabolite_data_tmp['bound'] = met._bound
            metabolite_data_tmp['constraint_sense'] = met._constraint_sense
            #metabolite_data_tmp['met_elements'] = None;
            #metabolite_data_tmp['met_atompositions'] = None;
            #metabolite_data_tmp['balanced'] = None;
            #metabolite_data_tmp['met_symmetry'] = None;
            #metabolite_data_tmp['met_symmetry_atompositions'] = None;
            metabolite_data_tmp['used_'] = True
            metabolite_data_tmp['comment_'] = None;
            metabolite_data.append(metabolite_data_tmp);

        return model_data,reaction_data,metabolite_data
    def _parse_isotopomer_mapping_csvToDict(self,filename_I):
        #Read in the isotopomer mappings
        # Output:
        # isotopomer_mapping = {
        #    'rxn_id':{'reactants_mapping':reactants_mapping,
        #              'reactants_stoichiometry_tracked':reactants_stoichiometry_tracked,
        #              'reactants_ids_tracked':reactants_ids_tracked,
        #              'products_mapping':products_mapping,
        #              'products_stoichiometry_tracked':products_stoichiometry_tracked,
        #              'products_ids_tracked':products_ids_tracked};
        
        isotopomer_mapping = {};
        with open(filename_I,mode='r') as infile:
            reader = csv.DictReader(infile);
            for r in reader:
                reactants_mapping = r['reactants_mapping'].strip().split('+');
                reactants_stoichiometry_tracked = [];
                reactants_ids_tracked = [];
                #print r['reactants_ids_tracked']
                reactants = r['reactants_ids_tracked'].strip().split('+');
                reactants_elements_tracked = [];
                if reactants and reactants[0]:
                    for react in reactants:
                        tmp = react.split('*');
                        reactants_stoichiometry_tracked.append(-abs(float(tmp[0]))); #ensure it is negative!
                        reactants_ids_tracked.append(tmp[1]);
                        reactants_elements_tracked.append(r['reactants_elements_tracked']);
                products_mapping = r['products_mapping'].strip().split('+');
                products_stoichiometry_tracked = [];
                products_ids_tracked = [];
                products = r['products_ids_tracked'].strip().split('+');
                #print r['products_ids_tracked']
                products_elements_tracked = [];
                if products and products[0]:
                    for prod in products:
                        tmp = prod.split('*');
                        products_stoichiometry_tracked.append(float(tmp[0]));
                        products_ids_tracked.append(tmp[1]);
                        products_elements_tracked.append(r['products_elements_tracked']);
                isotopomer_mapping[r['rxn_id']] = {'reactants_mapping':reactants_mapping,
                                                   'rxn_id':r['rxn_id'],
                                                   'reactants_stoichiometry_tracked':reactants_stoichiometry_tracked,
                                                   'reactants_ids_tracked':reactants_ids_tracked,
                                                   'reactants_elements_tracked':reactants_elements_tracked,
                                                   'products_mapping':products_mapping,
                                                   'products_stoichiometry_tracked':products_stoichiometry_tracked,
                                                   'products_ids_tracked':products_ids_tracked,
                                                   'products_elements_tracked':products_ids_tracked,
                                                   'mapping_id':r['mapping_id'],
                                                   'rxn_equation':r['rxn_equation'],
                                                   'rxn_description':r['rxn_description'],
                                                   'used_':r['used_'],
                                                   'comment_':r['comment_']};
        return isotopomer_mapping
    def _parse_isotopomer_mapping_csv(self,filename_I):
        #Read in the isotopomer mappings
        
        isotopomer_mapping = [];
        with open(filename_I,mode='r') as infile:
            reader = csv.DictReader(infile);
            for r in reader:
                reactants_mapping = r['reactants_mapping'].strip().split('+');
                reactants_stoichiometry_tracked = [];
                reactants_ids_tracked = [];
                #print r['reactants_ids_tracked']
                reactants = r['reactants_ids_tracked'].strip().split('+');
                reactants_elements_tracked = [];
                if reactants and reactants[0]:
                    for react in reactants:
                        tmp = react.split('*');
                        reactants_stoichiometry_tracked.append(-abs(float(tmp[0]))); #ensure it is negative!
                        reactants_ids_tracked.append(tmp[1]);
                        reactants_elements_tracked.append(r['reactants_elements_tracked']);
                products_mapping = r['products_mapping'].strip().split('+');
                products_stoichiometry_tracked = [];
                products_ids_tracked = [];
                products = r['products_ids_tracked'].strip().split('+');
                #print r['products_ids_tracked']
                products_elements_tracked = [];
                if products and products[0]:
                    for prod in products:
                        tmp = prod.split('*');
                        products_stoichiometry_tracked.append(float(tmp[0]));
                        products_ids_tracked.append(tmp[1]);
                        products_elements_tracked.append(r['products_elements_tracked']);
                isotopomer_mapping.append({'reactants_mapping':reactants_mapping,
                                                   'rxn_id':r['rxn_id'],
                                                   'reactants_stoichiometry_tracked':reactants_stoichiometry_tracked,
                                                   'reactants_ids_tracked':reactants_ids_tracked,
                                                   'reactants_elements_tracked':reactants_elements_tracked,
                                                   'products_mapping':products_mapping,
                                                   'products_stoichiometry_tracked':products_stoichiometry_tracked,
                                                   'products_ids_tracked':products_ids_tracked,
                                                   'products_elements_tracked':products_elements_tracked,
                                                   'mapping_id':r['mapping_id'],
                                                   'rxn_equation':r['rxn_equation'],
                                                   'rxn_description':r['rxn_description'],
                                                   'used_':r['used_'],
                                                   'comment_':r['comment_']});
        return isotopomer_mapping
    def import_dataStage02IsotopomerModelAndAtomMappingReactions_mat(self,model_id_I='iJS2012',mapping_id_I='iJS2012_01', date_I='120101', model_mat_I='data\iJS2012_centralMets.mat',model_mat_name_I='iJS2012'):
        '''load and parse matlab isotopomer model (i.e., iJS2012)'''

        '''DELETE previous uploads of iJS2012:
        DELETE FROM data_stage02_isotopomer_models WHERE model_id LIKE 'iJS2012';
        DELETE FROM "data_stage02_isotopomer_modelReactions" WHERE model_id LIKE 'iJS2012';
        DELETE FROM "data_stage02_isotopomer_modelMetabolites" WHERE model_id LIKE 'iJS2012';
        DELETE FROM "data_stage02_isotopomer_atomMappingMetabolites" WHERE mapping_id LIKE 'iJS2012_01';
        DELETE FROM "data_stage02_isotopomer_atomMappingReactions" WHERE mapping_id LIKE 'iJS2012_01';'''

        #load the matlab model
        cobra_model = load_matlab_model(model_mat_I)
        #check and correct the reaction ids
        rxn_ids = [];
        for rxn in cobra_model.reactions:
            rxn_id_old = copy(rxn.id)
            rxn_id_new = copy(rxn.id)
            rxn_id_new = rxn_id_new.replace('_Full','');
            rxn_id_new = rxn_id_new.replace("'",'');
            rxn_id_new = rxn_id_new.replace("_noMatch",'');
            rxn_id_new = rxn_id_new.replace("_nomatch",'');
            cobra_model.reactions.get_by_id(rxn_id_old).id = rxn_id_new;
            cobra_model.repair();
            rxn_ids.append(rxn_id_new);
        #load the isotopomer data
        isotopomer_data = scipy.io.loadmat(model_mat_I)[model_mat_name_I]['isotopomer'][0][0]
        atomMappingReactions=[];
        #parse the isotopomer data
        for rxn,mapping_numpy in enumerate(isotopomer_data):
            #intialize the row
            row={}
            row['mapping_id']=mapping_id_I;
            row['rxn_id']=rxn_ids[rxn];
            row['rxn_description']='';
            row['rxn_equation']='';
            row['reactants_stoichiometry_tracked']=[]
            row['products_stoichiometry_tracked']=[]
            row['reactants_ids_tracked']=[]
            row['products_ids_tracked']=[]
            row['reactants_elements_tracked']=[]
            row['products_elements_tracked']=[]
            row['reactants_positions_tracked']=[]
            row['products_positions_tracked']=[]
            row['reactants_mapping']=[]
            row['products_mapping']=[]
            row['used_']=True
            row['comment_']=None
            if not mapping_numpy:
                # append
                atomMappingReactions.append(row);
            else:
                mapping = mapping_numpy[0][0];
                # parse into tracked metabolites and their mapping
                mapping_list = mapping.split('!');
                mets_info_list = mapping_list[0].split('>'); # parse each into reactants and products
                mapping_info_list = mapping_list[1].split('>'); # parse each into reactants and products
                                                                #only the first mapping will be used
                # parse tracked metabolite information
                mets_info_list[0] = mets_info_list[0].strip().split(' ')
                mets_info_list[1] = mets_info_list[1].strip().split(' ')
                stoich = True;
                for cnt,c in enumerate(mets_info_list[0]):
                    c.strip()
                    if not c or cnt==0: continue #first string is the reaction id
                    if stoich:#c.isnumeric():
                        row['reactants_stoichiometry_tracked'].append(-abs(float(c)))
                        stoich=False;
                    else:
                        row['reactants_ids_tracked'].append(c[1:]) #first character is always an 'x'
                        stoich = True;
                for cnt,c in enumerate(mets_info_list[1]):
                    c.strip()
                    if not c: continue
                    if stoich:#c.isnumeric():
                        row['products_stoichiometry_tracked'].append(float(c))
                        stoich=False;
                    else:
                        row['products_ids_tracked'].append(c[1:])
                        stoich = True;
                # parse mapping information
                mapping_info_list[0] = mapping_info_list[0].strip().split(' ')
                mapping_info_list[1] = mapping_info_list[1].strip().split(' ')
                for cnt,m in enumerate(mapping_info_list[0]):
                    if not m: continue
                    row['reactants_mapping'].append(m.strip('#'))
                    elements = [];
                    positions = [];
                    for pos,element in enumerate(m.strip('#')):
                        positions.append(pos);
                        elements.append('C');
                    row['reactants_positions_tracked'].append(positions);
                    row['reactants_elements_tracked'].append(elements);
                for cnt,m in enumerate(mapping_info_list[1]):
                    if not m: continue
                    row['products_mapping'].append(m.strip('#'))
                    elements = [];
                    positions = [];
                    for pos,element in enumerate(m.strip('#')):
                        positions.append(pos);
                        elements.append('C');
                    row['products_positions_tracked'].append(positions);
                    row['products_elements_tracked'].append(elements);
                # append
                atomMappingReactions.append(row);
        # update selected reactions to account for new metabolites
        acon = Metabolite('acon_DASH_C_c','C6H3O6','cis-Aconitate','c');
        cit = cobra_model.metabolites.get_by_id('cit_c')
        icit = cobra_model.metabolites.get_by_id('icit_c')
        for rxn,row in enumerate(atomMappingReactions):
            if rxn_ids[rxn] == 'ACONTa':
                # Update ACONTa
                aconta_mets = {};
                aconta_mets[cit] = -1;
                aconta_mets[acon] = 1;
                aconta = Reaction('ACONTa');
                aconta.add_metabolites(aconta_mets);
                cobra_model.remove_reactions(['ACONTa']);
                cobra_model.add_reactions([aconta]);
                cobra_model.repair();
                # Update the mapping ids
                atomMappingReactions[rxn]['products_ids_tracked']=['acon_DASH_C_c']
                atomMappingReactions[rxn]['comment_']='updated'
            elif rxn_ids[rxn] == 'ACONTa_reverse':
                aconta_reverse_mets = {};
                aconta_reverse_mets[cit] = 1;
                aconta_reverse_mets[acon] = -1;
                aconta_reverse = Reaction('ACONTa_reverse');
                aconta_reverse.add_metabolites(aconta_reverse_mets);
                cobra_model.remove_reactions(['ACONTa_reverse']);
                cobra_model.add_reactions([aconta_reverse]);
                cobra_model.repair();
                # Update the mapping ids
                atomMappingReactions[rxn]['reactants_ids_tracked']=['acon_DASH_C_c']
                atomMappingReactions[rxn]['comment_']='updated'
            elif rxn_ids[rxn] == 'EX_co2_LPAREN_e_RPAREN__reverse':
                # Correct atomMapping
                atomMappingReactions[rxn]['mapping_id']=mapping_id_I;
                atomMappingReactions[rxn]['rxn_id']=rxn_ids[rxn];
                atomMappingReactions[rxn]['rxn_description']='';
                atomMappingReactions[rxn]['rxn_equation']='';
                atomMappingReactions[rxn]['reactants_stoichiometry_tracked']=[]
                atomMappingReactions[rxn]['products_stoichiometry_tracked']=[1]
                atomMappingReactions[rxn]['reactants_ids_tracked']=[]
                atomMappingReactions[rxn]['products_ids_tracked']=['co2_e']
                atomMappingReactions[rxn]['reactants_elements_tracked']=[]
                atomMappingReactions[rxn]['products_elements_tracked']=[["C"]]
                atomMappingReactions[rxn]['reactants_positions_tracked']=[]
                atomMappingReactions[rxn]['products_positions_tracked']=[[0]]
                atomMappingReactions[rxn]['reactants_mapping']=[]
                atomMappingReactions[rxn]['products_mapping']=['a']
                atomMappingReactions[rxn]['used_']=True
                atomMappingReactions[rxn]['comment_']=None
        # add in ACONTb
        acontb_mets = {};
        acontb_mets[acon] = -1;
        acontb_mets[icit] = 1;
        acontb = Reaction('ACONTb');
        acontb.add_metabolites(acontb_mets);
        cobra_model.add_reactions([acontb]);
        cobra_model.repair();
        # add in ACONTb mapping
        row={};
        row['mapping_id']=mapping_id_I;
        row['rxn_id']='ACONTb';
        row['rxn_description']='';
        row['rxn_equation']='';
        row['reactants_stoichiometry_tracked']=[-1]
        row['products_stoichiometry_tracked']=[1]
        row['reactants_ids_tracked']=['acon_DASH_C_c']
        row['products_ids_tracked']=['icit_c']
        row['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row['products_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row['products_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row['reactants_mapping']=['abcdef']
        row['products_mapping']=['abcdef']
        row['used_']=True
        row['comment_']='added'
        atomMappingReactions.append(row)
        # add in ACONTb_reverse
        acontb_reverse_mets = {};
        acontb_reverse_mets[acon] = 1;
        acontb_reverse_mets[icit] = -1;
        acontb_reverse = Reaction('ACONTb_reverse');
        acontb_reverse.add_metabolites(acontb_reverse_mets);
        cobra_model.add_reactions([acontb_reverse]);
        cobra_model.repair();
        # add in ACONTb_reverse mapping
        row={};
        row['mapping_id']=mapping_id_I;
        row['rxn_id']='ACONTb_reverse';
        row['rxn_description']='';
        row['rxn_equation']='';
        row['reactants_stoichiometry_tracked']=[-1]
        row['products_stoichiometry_tracked']=[1]
        row['reactants_ids_tracked']=['icit_c']
        row['products_ids_tracked']=['acon_DASH_C_c']
        row['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row['products_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row['products_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row['reactants_mapping']=['abcdef']
        row['products_mapping']=['abcdef']
        row['used_']=True
        row['comment_']='added'
        atomMappingReactions.append(row)
        # update exchanges
        cobra_model_sbml = None; # get the cobra model
        cobra_model_sbml = self.stage02_isotopomer_query.get_row_modelID_dataStage02IsotopomerModels('140407_iDM2014');
        if cobra_model_sbml['file_type'] == 'sbml':
            with open('data/cobra_model_tmp.xml','wb') as file:
                file.write(cobra_model_sbml['model_file']);
                file.close()
            cobra_model1 = None;
            cobra_model1 = create_cobra_model_from_sbml_file('data/cobra_model_tmp.xml', print_time=True);
        elif cobra_model_sbml['file_type'] == 'json':
            with open('data/cobra_model_tmp.json','wb') as file:
                file.write(cobra_model_sbml['model_file']);
                file.close()
            cobra_model1 = None;
            cobra_model1 = load_json_model('data/cobra_model_tmp.json');
        else:
            print 'file_type not supported'
        # delete exchange reactions:
        cobra_model.remove_reactions([cobra_model.reactions.get_by_id('EX_h_LPAREN_e_RPAREN_'),
                                   cobra_model.reactions.get_by_id('EX_h2o_LPAREN_e_RPAREN_'),
                                   cobra_model.reactions.get_by_id('EX_nh4_LPAREN_e_RPAREN_'),
                                   cobra_model.reactions.get_by_id('EX_o2_LPAREN_e_RPAREN_'),
                                   cobra_model.reactions.get_by_id('EX_pi_LPAREN_e_RPAREN_'),
                                   cobra_model.reactions.get_by_id('EX_so4_LPAREN_e_RPAREN_')]);
        cobra_model.repair();
        # add in exchange reactions:
        cobra_model.add_reactions([cobra_model1.reactions.get_by_id('EX_h_LPAREN_e_RPAREN_'),
                                   cobra_model1.reactions.get_by_id('EX_h_LPAREN_e_RPAREN__reverse'),
                                   cobra_model1.reactions.get_by_id('EX_h2o_LPAREN_e_RPAREN_'),
                                   cobra_model1.reactions.get_by_id('EX_h2o_LPAREN_e_RPAREN__reverse'),
                                   cobra_model1.reactions.get_by_id('EX_nh4_LPAREN_e_RPAREN__reverse'),
                                   cobra_model1.reactions.get_by_id('EX_o2_LPAREN_e_RPAREN__reverse'),
                                   cobra_model1.reactions.get_by_id('EX_pi_LPAREN_e_RPAREN__reverse'),
                                   cobra_model1.reactions.get_by_id('EX_so4_LPAREN_e_RPAREN__reverse')]);
        cobra_model.repair();
        # ensure that there are no reversible reactions
        #NOTE: reactions do not involved tracked metabolites, so there is no need to update the atomMappingReactions
        convert_to_irreversible(cobra_model);
        # repair EX_glc_LPAREN_e_RPAREN__reverse
        if cobra_model.reactions.has_id('EX_glc_LPAREN_e_RPAREN__reverse'):
            cobra_model.remove_reactions(['EX_glc_LPAREN_e_RPAREN_'])
            lb,ub = cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN__reverse').lower_bound,cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN__reverse').upper_bound;
            EX_glc_mets = {};
            EX_glc_mets[cobra_model.metabolites.get_by_id('glc_DASH_D_e')] = -1;
            EX_glc = Reaction('EX_glc_LPAREN_e_RPAREN_');
            EX_glc.add_metabolites(EX_glc_mets);
            cobra_model.add_reaction(EX_glc)
            cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN_').lower_bound = -ub;
            cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN_').upper_bound = lb;
            cobra_model.remove_reactions(['EX_glc_LPAREN_e_RPAREN__reverse'])
        # lookup metabolite information from the database
        for met in cobra_model.metabolites:
            met_info = {};
            met_info = self.stage02_isotopomer_query.get_row_modelIDAndMetID_dataStage02PhysiologyModelMetabolites('iJO1366',met.id);
            if met_info:
                cobra_model.metabolites.get_by_id(met.id).charge = met_info['charge'];
                cobra_model.metabolites.get_by_id(met.id).compartment = met_info['compartment'];
                cobra_model.metabolites.get_by_id(met.id).formula = met_info['formula'];
                cobra_model.metabolites.get_by_id(met.id).name = met_info['met_name'];
                cobra_model.repair();
            elif met.id == '2kmb_c':
                cobra_model.metabolites.get_by_id(met.id).charge = -1;
                cobra_model.metabolites.get_by_id(met.id).compartment = 'c';
                cobra_model.metabolites.get_by_id(met.id).formula = 'C5H7O3S';
                cobra_model.metabolites.get_by_id(met.id).name = '2-keto-4-methylthiobutyrate';
                cobra_model.repair();
            elif met.id == 'dkmpp_c':
                cobra_model.metabolites.get_by_id(met.id).charge = -2;
                cobra_model.metabolites.get_by_id(met.id).compartment = 'c';
                cobra_model.metabolites.get_by_id(met.id).formula = 'C6H9O6PS';
                cobra_model.metabolites.get_by_id(met.id).name = '2,3-diketo-5-methylthio-1-phosphopentane';
                cobra_model.repair();
            else:
                # correct for 'EC'
                if 'EC' in met.id:
                    met_id_old = met.id
                    met_id_new_list = met.id.split('_')[:-1]
                    met_id_new = '_'.join(met_id_new_list)
                    met_id_new += '_e';
                    cobra_model.metabolites.get_by_id(met_id_old).id = met_id_new;
                    cobra_model.repair();
                compartment = met.id.split('_')[-1];
                cobra_model.metabolites.get_by_id(met.id).compartment = compartment;
                cobra_model.metabolites.get_by_id(met.id).charge = 0;
                cobra_model.metabolites.get_by_id(met.id).formula = '';
                cobra_model.metabolites.get_by_id(met.id).name = '';
                cobra_model.repair();
        # write the model to a temporary file
        #write_cobra_model_to_sbml_file(cobra_model,'data/cobra_model_tmp.xml')
        save_json_model(cobra_model,'data/cobra_model_tmp.json')
        # add the model information to the database
        dataStage02IsotopomerModelRxns_data = [];
        dataStage02IsotopomerModelMets_data = [];
        dataStage02IsotopomerModels_data,\
            dataStage02IsotopomerModelRxns_data,\
            dataStage02IsotopomerModelMets_data = self._parse_model_json(model_id_I, date_I, 'data/cobra_model_tmp.json')
        self.add_data_stage02_isotopomer_modelMetabolites(dataStage02IsotopomerModelMets_data);
        self.add_data_stage02_isotopomer_modelReactions(dataStage02IsotopomerModelRxns_data);
        self.add_data_stage02_isotopomer_models(dataStage02IsotopomerModels_data);
        # add the mapping information to the database
        self.add_data_stage02_isotopomer_atomMappingReactions(atomMappingReactions);
    def _parse_model_json(self,model_id_I,date_I,filename_I):
        # Read in the sbml file and define the model conditions
        cobra_model = load_json_model(filename_I);
        model_data = [];
        model_data_tmp = {};
        # parse out model metadata
        model_data_tmp['model_id'] = model_id_I;
        model_data_tmp['model_name'] = None;
        model_data_tmp['date'] = date_I;
        model_data_tmp['model_description'] = cobra_model.description;
        with open(filename_I, 'r') as f:
            model_data_tmp['model_file'] = f.read();
        model_data_tmp['file_type'] = 'json'
        model_data.append(model_data_tmp)
        reaction_data = [];
        # parse out reaction data
        for r in cobra_model.reactions:
            reaction_data_dict = {};
            reaction_data_dict['model_id'] = model_id_I
            reaction_data_dict['rxn_id'] = r.id
            reaction_data_dict['rxn_name'] = r.name
            reaction_data_dict['equation'] = r.build_reaction_string()
            reaction_data_dict['subsystem'] = r.subsystem
            reaction_data_dict['gpr'] = r.gene_reaction_rule
            reaction_data_dict['genes'] = []
            genes = r.genes;
            for g in genes:
                reaction_data_dict['genes'].append(g.id);
            reaction_data_dict['reactants_stoichiometry'] = [];
            reaction_data_dict['reactants_ids'] = [];
            reactants = r.reactants;
            for react in reactants:
                reaction_data_dict['reactants_stoichiometry'].append(r.get_coefficient(react.id));
                reaction_data_dict['reactants_ids'].append(react.id);
            reaction_data_dict['products_stoichiometry'] = [];
            reaction_data_dict['products_ids'] = [];
            products = r.products;
            for prod in products:
                reaction_data_dict['products_stoichiometry'].append(r.get_coefficient(prod.id));
                reaction_data_dict['products_ids'].append(prod.id);
            reaction_data_dict['lower_bound'] = r.lower_bound
            reaction_data_dict['upper_bound'] = r.upper_bound
            reaction_data_dict['objective_coefficient'] = r.objective_coefficient
            reaction_data_dict['flux_units'] = 'mmol*gDW-1*hr-1'
            reaction_data_dict['reversibility'] = r.reversibility
            #reaction_data_dict['reactants_stoichiometry_tracked'] = None;
            #reaction_data_dict['products_stoichiometry_tracked'] = None;
            #reaction_data_dict['reactants_ids_tracked'] = None;
            #reaction_data_dict['products_ids_tracked'] = None;
            #reaction_data_dict['reactants_mapping'] = None;
            #reaction_data_dict['products_mapping'] = None;
            #reaction_data_dict['rxn_equation'] = None;
            reaction_data_dict['fixed'] = None;
            reaction_data_dict['free'] = None;
            reaction_data_dict['weight'] = None;
            reaction_data_dict['used_'] = True
            reaction_data_dict['comment_'] = None;
            reaction_data.append(reaction_data_dict);
        metabolite_data = [];
        # parse out metabolite data
        for met in cobra_model.metabolites:
            metabolite_data_tmp = {};
            metabolite_data_tmp['model_id'] = model_id_I
            metabolite_data_tmp['met_name'] = met.name;
            metabolite_data_tmp['met_id'] = met.id;
            if met.formula:
                if met.formula != 'None' and not 'X' in met.formula:
                    try:
                        tmp = Formula(met.formula)
                        metabolite_data_tmp['formula'] = tmp.formula;
                    except Exception as e:
                        print e;
                        print met.id
                        metabolite_data_tmp['formula']= met.formula
                else: 
                    metabolite_data_tmp['formula'] = met.formula;
            else: 
                metabolite_data_tmp['formula'] = None;
            metabolite_data_tmp['charge'] = met.charge
            metabolite_data_tmp['compartment'] = met.compartment
            metabolite_data_tmp['bound'] = met._bound
            metabolite_data_tmp['constraint_sense'] = met._constraint_sense
            #metabolite_data_tmp['met_elements'] = None;
            #metabolite_data_tmp['met_atompositions'] = None;
            metabolite_data_tmp['balanced'] = None;
            metabolite_data_tmp['fixed'] = None;
            #metabolite_data_tmp['met_symmetry'] = None;
            #metabolite_data_tmp['met_symmetry_atompositions'] = None;
            metabolite_data_tmp['used_'] = True
            metabolite_data_tmp['comment_'] = None;
            metabolite_data_tmp['lower_bound'] = None;
            metabolite_data_tmp['upper_bound'] = None;

            metabolite_data.append(metabolite_data_tmp);

        return model_data,reaction_data,metabolite_data
    def import_dataStage02IsotopomerModelAndAtomMappingReactions_INCA(self,model_id_I=None,mapping_id_I=None, date_I=None,
                                                                      model_INCA_I=None, model_rxn_conversion_I=None,
                                                                      model_met_conversion_I=None,model_rxn_CBM_I=None,
                                                                      element_tracked_I = 'C',
                                                                      add_model_I = True, add_rxns_I = True,
                                                                      add_mets_I = True, add_rxn_mappings_I=True,
                                                                      update_model_I = False, update_rxns_I = False,
                                                                      update_mets_I = False, update_rxn_mappings_I=False,
                                                                      addunique_mets_I = False):
        '''load and parse INCA isotopomer model (i.e., ecoli_inca01)
        TODO: add in ability to parse elements/mapping in use cases such as '(C1:a,C2:b1,C3:c2)' or '(C1:a,C2:b3,H1:d)' '''

        '''DELETE previous uploads of ecoli_inca01:
        DELETE FROM data_stage02_isotopomer_models WHERE model_id LIKE 'ecoli_inca01';
        DELETE FROM "data_stage02_isotopomer_modelReactions" WHERE model_id LIKE 'ecoli_inca01';
        DELETE FROM "data_stage02_isotopomer_modelMetabolites" WHERE model_id LIKE 'ecoli_inca01';
        DELETE FROM "data_stage02_isotopomer_atomMappingMetabolites" WHERE mapping_id LIKE 'ecoli_inca01';
        DELETE FROM "data_stage02_isotopomer_atomMappingReactions" WHERE mapping_id LIKE 'ecoli_inca01';'''

        #read in the data:
        model_INCA = {};
        model_rxn_conversion = {};
        model_met_conversion = {};
        model_rxn_cbm = {};

        data = base_importData();
        data.read_csv(model_INCA_I);
        for d in data.data:
            model_INCA[d['rxn_id_INCA']]=d['rxn_equation_INCA'];
            #model_INCA.append(d);
        data.clear_data();

        if model_rxn_conversion_I:
            data = base_importData();
            data.read_csv(model_rxn_conversion_I);
            for d in data.data:
                model_rxn_conversion[d['rxn_id_INCA']]=d['rxn_id'];
            data.clear_data();

        if model_met_conversion_I:
            data = base_importData();
            data.read_csv(model_met_conversion_I);
            for d in data.data:
                model_met_conversion[d['met_id_INCA']]=d['met_id'];
            data.clear_data();

        if model_rxn_CBM_I:
            data = base_importData();
            data.read_csv(model_rxn_CBM_I);
            for d in data.data:
                genes = [];
                genes_str = d['genes'];
                genes = genes_str.replace('{','').replace('}','').split(',');
                fixed =None;
                if d['fixed']: fixed = d['fixed']
                free= None;
                if d['free']: free = d['free']
                weight = None;
                if d['weight']:  weight = d['weight']
                model_rxn_cbm[d['rxn_id_INCA']]={'comment_':d['comment_'],
                    'lower_bound':float(d['lower_bound']),
                    'upper_bound':float(d['upper_bound']),
                    'objective_coefficient':float(d['objective_coefficient']),
                    'subsystem':d['subsystem'],'gpr':d['gpr'],'genes':genes,
                    'flux_units':d['flux_units'],'fixed':fixed,'free':free,'weight': weight,
                    'used_':d['used_'],'reversibility':d['reversibility'],
                    };
            data.clear_data();

        modelReactions = [];
        atomMappingReactions = [];
        atomMappingReactions_reverse = [];
        model_met_ids = [];
        #parse the rxn network into modelReactions and atomMappingReactions
        for id,rxn_eqn in model_INCA.iteritems():
            #if id == 'HEX1':
            #    print 'check'
            #initialize the data structure for modelReactions:
            modelReactions_row = {};
            modelReactions_row['model_id']=model_id_I;
            if model_rxn_conversion_I: modelReactions_row['rxn_id']=model_rxn_conversion[id];
            else: modelReactions_row['rxn_id']=id;
            modelReactions_row['equation']=None;
            modelReactions_row['subsystem']=None;
            modelReactions_row['gpr']=None;
            modelReactions_row['genes']=None;
            modelReactions_row['reactants_stoichiometry']=[];
            modelReactions_row['products_stoichiometry']=[];
            modelReactions_row['reactants_ids']=[];
            modelReactions_row['products_ids']=[];
            if model_rxn_CBM_I:
                modelReactions_row['subsystem']=model_rxn_cbm[id]['subsystem'];
                modelReactions_row['gpr']=model_rxn_cbm[id]['gpr'];
                modelReactions_row['genes']=model_rxn_cbm[id]['genes'];
                modelReactions_row['lower_bound']=model_rxn_cbm[id]['lower_bound'];
                modelReactions_row['upper_bound']=model_rxn_cbm[id]['upper_bound'];
                modelReactions_row['objective_coefficient']=model_rxn_cbm[id]['objective_coefficient'];
                modelReactions_row['flux_units']=model_rxn_cbm[id]['flux_units'];
                modelReactions_row['fixed']=model_rxn_cbm[id]['fixed'];
                modelReactions_row['free']=model_rxn_cbm[id]['free'];
                modelReactions_row['reversibility']=model_rxn_cbm[id]['reversibility'];
                modelReactions_row['weight']=model_rxn_cbm[id]['weight'];
                modelReactions_row['used_']=model_rxn_cbm[id]['used_'];
                modelReactions_row['comment_']=model_rxn_cbm[id]['comment_'];
            else:
                modelReactions_row['lower_bound']=-1000;
                modelReactions_row['upper_bound']=1000;
                if model_rxn_conversion[id]=='Ec_Biomass_INCA':
                    modelReactions_row['objective_coefficient']=1.0;
                else:
                    modelReactions_row['objective_coefficient']=0.0;
                modelReactions_row['flux_units']='mmol*gDW-1*hr-1';
                modelReactions_row['fixed']=None;
                modelReactions_row['free']=None;
                modelReactions_row['reversibility']=None;
                modelReactions_row['weight']=None;
                modelReactions_row['used_']=True;
                modelReactions_row['comment_']=None
            #initialize the data structure for atomMappingReactions:
            atomMappingReactions_row = {};
            atomMappingReactions_row['mapping_id']=mapping_id_I;
            if model_rxn_conversion_I: atomMappingReactions_row['rxn_id']=model_rxn_conversion[id];
            else: atomMappingReactions_row['rxn_id']=id;
            atomMappingReactions_row['rxn_description']='';
            atomMappingReactions_row['rxn_equation']=rxn_eqn;
            atomMappingReactions_row['reactants_stoichiometry_tracked']=[]
            atomMappingReactions_row['products_stoichiometry_tracked']=[]
            atomMappingReactions_row['reactants_ids_tracked']=[]
            atomMappingReactions_row['products_ids_tracked']=[]
            atomMappingReactions_row['reactants_elements_tracked']=[]
            atomMappingReactions_row['products_elements_tracked']=[]
            atomMappingReactions_row['reactants_positions_tracked']=[]
            atomMappingReactions_row['products_positions_tracked']=[]
            atomMappingReactions_row['reactants_mapping']=[]
            atomMappingReactions_row['products_mapping']=[]
            atomMappingReactions_row['used_']=True
            atomMappingReactions_row['comment_']=None
            #split into reactants and products and determine the reversibility
            model_INCA_reactants = '';
            model_INCA_products = '';
            rxn_eqn.strip();
            if '<->' in rxn_eqn or '<=>' in rxn_eqn:
                modelReactions_row['reversibility'] = True;
                if '<->' in rxn_eqn and rxn_eqn.split('<->')[0]: model_INCA_reactants = rxn_eqn.split('<->')[0];
                if '<->' in rxn_eqn and rxn_eqn.split('<->')[1]: model_INCA_products = rxn_eqn.split('<->')[1];
                if '<=>' in rxn_eqn and rxn_eqn.split('<=>')[0]: model_INCA_reactants = rxn_eqn.split('<=>')[0];
                if '<=>' in rxn_eqn and rxn_eqn.split('<=>')[1]: model_INCA_products = rxn_eqn.split('<=>')[1];
                if not model_rxn_CBM_I: 
                    modelReactions_row['lower_bound']=-1000;
                    modelReactions_row['upper_bound']=1000;
            elif '->' in rxn_eqn or '-->' in rxn_eqn:
                modelReactions_row['reversibility'] = False;
                if '-->' in rxn_eqn:
                    if rxn_eqn.split('-->')[0]: model_INCA_reactants = rxn_eqn.split('-->')[0];
                    if rxn_eqn.split('-->')[1]: model_INCA_products = rxn_eqn.split('-->')[1];
                else:
                    if rxn_eqn.split('->')[0]: model_INCA_reactants = rxn_eqn.split('->')[0];
                    if rxn_eqn.split('->')[1]: model_INCA_products = rxn_eqn.split('->')[1];
                if not model_rxn_CBM_I: 
                    modelReactions_row['lower_bound']=0;
                    modelReactions_row['upper_bound']=1000;
            else:
                print 'no valid forward/reverse reaction identifier found'
            #parse the reactants
            met_id_tmp = None;
            met_stoichiometry_tmp = None;
            model_INCA_reactants_list = model_INCA_reactants.replace('*',' ').split(' ')
            rxn_mapping_bool = False;
            rxn_mapping_str = '';
            pos_cnt = 0;
            positions = [];
            elements = [];
            for rxn_token in model_INCA_reactants_list:
                #check for extra whitespace
                if rxn_token == '' or rxn_token == ' ': continue;
                #check for mapping
                elif ')' in rxn_token:
                    rxn_mapping = rxn_token.strip(')');
                    #TODO: will break on use cases such as '(C1:a C2:b1 C3:c2)'
                    if ':' in rxn_mapping:
                        rxn_mapping = rxn_mapping.split(':')[1];
                    atomMappingReactions_row['reactants_ids_tracked'].append(met_id_tmp);
                    atomMappingReactions_row['reactants_stoichiometry_tracked'].append(met_stoichiometry_tmp);
                    rxn_mapping_str+= '['+rxn_mapping+']';
                    elements.append(element_tracked_I);
                    positions.append(pos_cnt);
                    atomMappingReactions_row['reactants_positions_tracked'].append(positions)
                    atomMappingReactions_row['reactants_elements_tracked'].append(elements)
                    rxn_mapping_bool = False;
                    atomMappingReactions_row['reactants_mapping'].append(rxn_mapping_str);
                    rxn_mapping_str='';
                    pos_cnt=0;
                elif rxn_mapping_bool:
                    #TODO: will break on use cases such as '(C1:a C2:b1 C3:c2)'
                    if ':' in rxn_mapping:
                        rxn_mapping = rxn_mapping.split(':')[1];
                    atomMappingReactions_row['reactants_ids_tracked'].append(met_id_tmp);
                    atomMappingReactions_row['reactants_stoichiometry_tracked'].append(met_stoichiometry_tmp);
                    rxn_mapping_str+= '['+rxn_mapping+']';
                    elements.append(element_tracked_I);
                    positions.append(pos_cnt);
                    pos_cnt+=1;
                elif '(' in rxn_token:
                    rxn_mapping = rxn_token.strip('(');
                    #TODO: will break on use cases such as '(C1:a C2:b1 C3:c2)'
                    if ':' in rxn_mapping:
                        rxn_mapping = rxn_mapping.split(':')[1];
                    atomMappingReactions_row['reactants_ids_tracked'].append(met_id_tmp);
                    atomMappingReactions_row['reactants_stoichiometry_tracked'].append(met_stoichiometry_tmp);
                    rxn_mapping_str+= '['+rxn_mapping+']';
                    elements.append(element_tracked_I);
                    positions.append(pos_cnt);
                    rxn_mapping_bool = True;
                    pos_cnt+=1;
                #check for stoichiometry
                elif rxn_token.replace('.','').replace('-','').replace('E','').isdigit():
                    met_stoichiometry_tmp = -abs(float(rxn_token));
                    modelReactions_row['reactants_stoichiometry'].append(met_stoichiometry_tmp)
                #check for the next metabolite
                elif '+' in rxn_token:
                    met_id_tmp = None;
                    met_stoichiometry_tmp = None;
                #met_id
                else:
                    if model_met_conversion_I: met_id_tmp = model_met_conversion[rxn_token.strip()];
                    else: met_id_tmp = rxn_token.strip();
                    modelReactions_row['reactants_ids'].append(met_id_tmp)
                    model_met_ids.append(met_id_tmp)
                    if not met_stoichiometry_tmp: #implicit stoichiometry of 1
                        met_stoichiometry_tmp = -1.0;
                        modelReactions_row['reactants_stoichiometry'].append(met_stoichiometry_tmp);
            #parse the products
            met_id_tmp = None;
            met_stoichiometry_tmp = None;
            model_INCA_products_list = model_INCA_products.replace('*',' ').split(' ')
            rxn_mapping_bool = False;
            rxn_mapping_str = '';
            pos_cnt = 0;
            positions = [];
            elements = [];
            for rxn_token in model_INCA_products_list:
                #check for extra whitespace
                if rxn_token == '' or rxn_token == ' ': continue;
                #check for mapping
                elif ')' in rxn_token:
                    rxn_mapping = rxn_token.strip(')');
                    #TODO: will break on use cases such as '(C1:a C2:b1 C3:c2)'
                    if ':' in rxn_mapping:
                        rxn_mapping = rxn_mapping.split(':')[1];
                    atomMappingReactions_row['products_ids_tracked'].append(met_id_tmp);
                    atomMappingReactions_row['products_stoichiometry_tracked'].append(met_stoichiometry_tmp);
                    rxn_mapping_str+= '['+rxn_mapping+']';
                    elements.append(element_tracked_I);
                    positions.append(pos_cnt);
                    atomMappingReactions_row['products_positions_tracked'].append(positions)
                    atomMappingReactions_row['products_elements_tracked'].append(elements)
                    rxn_mapping_bool = False;
                    atomMappingReactions_row['products_mapping'].append(rxn_mapping_str);
                    rxn_mapping_str='';
                    pos_cnt=0;
                elif rxn_mapping_bool:
                    #TODO: will break on use cases such as '(C1:a C2:b1 C3:c2)'
                    if ':' in rxn_mapping:
                        rxn_mapping = rxn_mapping.split(':')[1];
                    atomMappingReactions_row['products_ids_tracked'].append(met_id_tmp);
                    atomMappingReactions_row['products_stoichiometry_tracked'].append(met_stoichiometry_tmp);
                    rxn_mapping_str+= '['+rxn_mapping+']';
                    elements.append(element_tracked_I);
                    positions.append(pos_cnt);
                    pos_cnt+=1;
                elif '(' in rxn_token:
                    rxn_mapping = rxn_token.strip('(');
                    #TODO: will break on use cases such as '(C1:a C2:b1 C3:c2)'
                    if ':' in rxn_mapping:
                        rxn_mapping = rxn_mapping.split(':')[1];
                    atomMappingReactions_row['products_ids_tracked'].append(met_id_tmp);
                    atomMappingReactions_row['products_stoichiometry_tracked'].append(met_stoichiometry_tmp);
                    rxn_mapping_str+= '['+rxn_mapping+']';
                    elements.append(element_tracked_I);
                    positions.append(pos_cnt);
                    rxn_mapping_bool = True;
                    pos_cnt+=1;
                #check for stoichiometry
                elif rxn_token.replace('.','').replace('-','').replace('E','').isdigit():
                    met_stoichiometry_tmp = abs(float(rxn_token));
                    modelReactions_row['products_stoichiometry'].append(met_stoichiometry_tmp)
                #check for the next metabolite
                elif '+' in rxn_token:
                    met_id_tmp = None;
                    met_stoichiometry_tmp = None;
                #met_id
                else:
                    if model_met_conversion_I: met_id_tmp = model_met_conversion[rxn_token.strip()];
                    else: met_id_tmp = rxn_token.strip();
                    modelReactions_row['products_ids'].append(met_id_tmp)
                    model_met_ids.append(met_id_tmp)
                    if not met_stoichiometry_tmp: #implicit stoichiometry of 1
                        met_stoichiometry_tmp = 1.0;
                        modelReactions_row['products_stoichiometry'].append(met_stoichiometry_tmp);
            #met_id_tmp = None;
            #met_stoichiometry_tmp = None;
            #for rxn_token in model_INCA_products.replace('*',' ').split(' '):
            #    #check for extra whitespace
            #    if rxn_token == '' or rxn_token == ' ': continue;
            #    #check for mapping
            #    elif '(' in rxn_token or ')' in rxn_token:
            #        rxn_mapping = rxn_token.strip('(').strip(')');
            #        #TODO: will break on use cases such as '(C1:a,C2:b1,C3:c2)'
            #        if ':' in rxn_mapping:
            #            rxn_mapping = rxn_mapping.split(':')[1];
            #        atomMappingReactions_row['products_ids_tracked'].append(met_id_tmp);
            #        atomMappingReactions_row['products_stoichiometry_tracked'].append(met_stoichiometry_tmp);
            #        atomMappingReactions_row['products_mapping'].append(rxn_mapping);
            #        elements = [];
            #        positions = [];
            #        for pos,mapping in enumerate(rxn_mapping):
            #            positions.append(pos);
            #            elements.append(element_tracked_I);
            #        atomMappingReactions_row['products_positions_tracked'].append(positions)
            #        atomMappingReactions_row['products_elements_tracked'].append(elements)
            #    #check for stoichiometry
            #    elif rxn_token.replace('.','').replace('-','').replace('E','').isdigit():
            #        met_stoichiometry_tmp = abs(float(rxn_token));
            #        modelReactions_row['products_stoichiometry'].append(met_stoichiometry_tmp)
            #    #check for the next metabolite
            #    elif '+' in rxn_token:
            #        met_id_tmp = None;
            #        met_stoichiometry_tmp = None;
            #    #met_id
            #    else:
            #        if model_met_conversion_I: met_id_tmp = model_met_conversion[rxn_token.strip()];
            #        else: met_id_tmp = rxn_token.strip();
            #        modelReactions_row['products_ids'].append(met_id_tmp)
            #        model_met_ids.append(met_id_tmp)
            #        if not met_stoichiometry_tmp: #implicit stoichiometry of 1
            #            met_stoichiometry_tmp = 1.0;
            #            modelReactions_row['products_stoichiometry'].append(met_stoichiometry_tmp);
            #append to list
            modelReactions.append(modelReactions_row);
            atomMappingReactions.append(atomMappingReactions_row);
            #check for a potential reverse reaction:
            if modelReactions_row['reversibility']:
                #initialize the data structure for atomMappingReactions_reverse:
                atomMappingReactions_reverse_row = {};
                atomMappingReactions_reverse_row['mapping_id']=mapping_id_I;
                if model_rxn_conversion_I: atomMappingReactions_reverse_row['rxn_id']=model_rxn_conversion[id]+'_reverse';
                else: atomMappingReactions_reverse_row['rxn_id']=id+'_reverse';
                atomMappingReactions_reverse_row['rxn_description']=atomMappingReactions_row['rxn_description'];
                atomMappingReactions_reverse_row['rxn_equation']=atomMappingReactions_row['rxn_equation'];
                atomMappingReactions_reverse_row['reactants_stoichiometry_tracked']=[-abs(s) for s in atomMappingReactions_row['products_stoichiometry_tracked']]
                atomMappingReactions_reverse_row['products_stoichiometry_tracked']=[abs(s) for s in atomMappingReactions_row['reactants_stoichiometry_tracked']]
                atomMappingReactions_reverse_row['reactants_ids_tracked']=atomMappingReactions_row['products_ids_tracked']
                atomMappingReactions_reverse_row['products_ids_tracked']=atomMappingReactions_row['reactants_ids_tracked']
                atomMappingReactions_reverse_row['reactants_elements_tracked']=atomMappingReactions_row['products_elements_tracked']
                atomMappingReactions_reverse_row['products_elements_tracked']=atomMappingReactions_row['reactants_elements_tracked']
                atomMappingReactions_reverse_row['reactants_positions_tracked']=atomMappingReactions_row['products_positions_tracked']
                atomMappingReactions_reverse_row['products_positions_tracked']=atomMappingReactions_row['reactants_positions_tracked']
                atomMappingReactions_reverse_row['reactants_mapping']=atomMappingReactions_row['products_mapping']
                atomMappingReactions_reverse_row['products_mapping']=atomMappingReactions_row['reactants_mapping']
                atomMappingReactions_reverse_row['used_']=True
                atomMappingReactions_reverse_row['comment_']=None
                atomMappingReactions_reverse.append(atomMappingReactions_reverse_row)

        #lookup the metabolite information from the database to generate modelMetabolites
        model_met_ids_unique = list(set(model_met_ids));
        modelMetabolites = [];
        for model_met_id in model_met_ids_unique:
            met_id = model_met_id.split('.')[0]
            INCA_compartment = None;
            if '.' in model_met_id:
                INCA_compartment = model_met_id.split('.')[1]
            modelMetabolites_row = {};
            modelMetabolites_row = self.stage02_isotopomer_query.get_row_modelIDAndMetID_dataStage02PhysiologyModelMetabolites('iJO1366',met_id);
            if not modelMetabolites_row:
                modelMetabolites_row['met_name']='';
                modelMetabolites_row['formula']='';
                modelMetabolites_row['charge']=0;
                modelMetabolites_row['bound']=0;
                modelMetabolites_row['constraint_sense']='E';
                modelMetabolites_row['lower_bound']=None;
                modelMetabolites_row['upper_bound']=None;
                modelMetabolites_row['fixed']=None;
                modelMetabolites_row['used_']=True;
                modelMetabolites_row['comment_']='INCA-specific metabolite'
            if INCA_compartment:
                modelMetabolites_row['balanced']=False;
                modelMetabolites_row['met_id']=met_id + '.' + INCA_compartment;
                modelMetabolites_row['compartment']=INCA_compartment;
            else:
                modelMetabolites_row['balanced']=True;
                modelMetabolites_row['met_id']=met_id
                compartment = met_id.split('_')[-1]
                modelMetabolites_row['compartment']=compartment;
            modelMetabolites_row['model_id']=model_id_I;
            modelMetabolites.append(modelMetabolites_row);

        #create the model from modelReactions and modelMetabolites
        cobra_model = self.create_modelFromReactionsAndMetabolitesTables(modelReactions,modelMetabolites)
        convert_to_irreversible(cobra_model);
        save_json_model(cobra_model,settings.workspace_data+'/cobra_model_tmp.json')

        # add the model information to the database
        dataStage02IsotopomerModelRxns_data = [];
        dataStage02IsotopomerModelMets_data = [];
        dataStage02IsotopomerModels_data,\
            dataStage02IsotopomerModelRxns_data,\
            dataStage02IsotopomerModelMets_data = self._parse_model_json(model_id_I, date_I, settings.workspace_data+'/cobra_model_tmp.json')

        # add modelReactions to the database
        #if add_rxns_I: self.add_data_stage02_isotopomer_modelReactions(dataStage02IsotopomerModelRxns_data);
        # add in equations to modelReactions:
        for rxn1_cnt,rxn1 in enumerate(modelReactions):
            for rxn2_cnt,rxn2 in enumerate(dataStage02IsotopomerModelRxns_data):
                if rxn1['rxn_id']==rxn2['rxn_id']:
                    modelReactions[rxn1_cnt]['equation'] = rxn2['equation'];
        if add_rxns_I: self.add_data_stage02_isotopomer_modelReactions(modelReactions);
        elif update_rxns_I: self.update_data_stage02_isotopomer_modelReactions(modelReactions);
        
        # add modelMetabolites to the database
        #self.add_data_stage02_isotopomer_modelMetabolites(modelMetabolites);
        if add_mets_I: self.add_data_stage02_isotopomer_modelMetabolites(dataStage02IsotopomerModelMets_data);
        elif update_mets_I: self.update_data_stage02_isotopomer_modelMetabolites(dataStage02IsotopomerModelMets_data);
        elif addunique_mets_I: 
            existing_mets = [];
            existing_mets = self.stage02_isotopomer_query.get_metIDs_modelID_dataStage02IsotopomerModelMetabolites(model_id_I);
            all_mets = self.stage02_isotopomer_query.get_metIDs_modelID_dataStage02IsotopomerModelReactions(model_id_I);
            new_mets = [];
            for met in all_mets:
                if not met in existing_mets:
                    new_mets.append(met);
            new_mets_add = [];
            for row in dataStage02IsotopomerModelMets_data:
                if row['met_id'] in new_mets:
                    new_mets_add.append(row);
            self.add_data_stage02_isotopomer_modelMetabolites(new_mets_add);

        # add model to the database
        if add_model_I: self.add_data_stage02_isotopomer_models(dataStage02IsotopomerModels_data);
        elif update_model_I: self.update_data_stage02_isotopomer_models(dataStage02IsotopomerModels_data);

        #add atomMappingReactions to the database
        if add_rxn_mappings_I: 
            self.add_data_stage02_isotopomer_atomMappingReactions(atomMappingReactions);
            self.add_data_stage02_isotopomer_atomMappingReactions(atomMappingReactions_reverse);
        elif update_rxn_mappings_I: 
            self.update_data_stage02_isotopomer_atomMappingReactions(atomMappingReactions);
            self.update_data_stage02_isotopomer_atomMappingReactions(atomMappingReactions_reverse);

        print 'model and mapping added';
    def create_modelFromReactionsAndMetabolitesTables(self,rxns_table_I,mets_table_I):
        '''generate a cobra model from isotopomer_modelReactions and isotopomer_modelMetabolites tables'''
        
        cobra_model = Model(rxns_table_I[0]['model_id']);
        for rxn_cnt,rxn_row in enumerate(rxns_table_I):
            #if rxn_row['rxn_id'] == 'HEX1':
            #    print 'check'
            mets = {}
            print rxn_row['rxn_id']
            # parse the reactants
            for rxn_met_cnt,rxn_met in enumerate(rxn_row['reactants_ids']):
                for met_cnt,met_row in enumerate(mets_table_I):
                    if met_row['met_id']==rxn_met:# and met_row['balanced']:
                        compartment = met_row['compartment']
                        if not compartment:
                            met_id_tmp = met_row['met_id'].split('.')[0]
                            compartment = met_id_tmp.split('_')[-1];
                        met_tmp = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],compartment)
                        met_tmp.charge = met_row['charge']
                        # check for duplicate metabolites
                        met_keys = mets.keys();
                        met_keys_ids = {};
                        if met_keys: 
                            for cnt,met in enumerate(met_keys):
                                met_keys_ids[met.id]=cnt;
                        if met_tmp.id in met_keys_ids.keys():
                            mets[met_keys[met_keys_ids[met_tmp.id]]]-=1
                        else:
                            mets[met_tmp] = rxn_row['reactants_stoichiometry'][rxn_met_cnt];
                        break;
            # parse the products
            for rxn_met_cnt,rxn_met in enumerate(rxn_row['products_ids']):
                for met_cnt,met_row in enumerate(mets_table_I):
                    if met_row['met_id']==rxn_met:# and met_row['balanced']:
                        compartment = met_row['compartment']
                        if not compartment:
                            met_id_tmp = met_row['met_id'].split('.')[0]
                            compartment = met_id_tmp.split('_')[-1];
                        met_tmp = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],compartment)
                        met_tmp.charge = met_row['charge']
                        # check for duplicate metabolites
                        met_keys = mets.keys();
                        met_keys_ids = {};
                        if met_keys: 
                            for cnt,met in enumerate(met_keys):
                                met_keys_ids[met.id]=cnt;
                        if met_tmp.id in met_keys_ids.keys():
                            mets[met_keys[met_keys_ids[met_tmp.id]]]+=1
                        else:
                            mets[met_tmp] = rxn_row['products_stoichiometry'][rxn_met_cnt];
                        break;
            rxn = None;
            rxn = Reaction(rxn_row['rxn_id']);
            rxn.add_metabolites(mets);
            rxn.lower_bound=rxn_row['lower_bound'];
            rxn.upper_bound=rxn_row['upper_bound'];
            rxn.subsystem=rxn_row['subsystem'];
            rxn.gpr=rxn_row['gpr'];
            rxn.objective_coefficient=rxn_row['objective_coefficient'];
            cobra_model.add_reactions([rxn]);
            cobra_model.repair();
        return cobra_model
    def import_isotopomerSimulationResults_INCA(self, simulation_id, filename, model_rxn_conversion_I=None):
        '''import results from a fluxomics simulation using INCA1.3
        Please reference the model, fitdata, and simdata class structures in the INCA documentation'''
        #TODO
        '''table adds'''
        # extract information about the file
        import os, time
        from datetime import datetime
        from stat import ST_SIZE, ST_MTIME
        try:
            st = os.stat(filename)
        except IOError:
            print "failed to get information about", filename
            return;
        else:
            file_size = st[ST_SIZE]
            simulation_dateAndTime_struct = time.localtime(st[ST_MTIME])
            simulation_dateAndTime = datetime.fromtimestamp(time.mktime(simulation_dateAndTime_struct))
        # lookup information about the simulation:
        simulation_info = {};
        simulation_info = self.stage02_isotopomer_query.get_simulation_simulationID_dataStage02IsotopomerSimulation(simulation_id);
        # determine if the simulation is a parallel labeling experiment, non-stationary, or both
        parallel = False;
        non_stationary = False;
        if len(simulation_info['experiment_id'])>1 or len(simulation_info['sample_name_abbreviation'])>1:
            parallel = True;
        if len(simulation_info['time_point'])>1:
            non_stationary = True;
        # extract out simulation data
        m = scipy.io.loadmat(filename)['m']; #model
        f = scipy.io.loadmat(filename)['f']; #fitdata
        s = scipy.io.loadmat(filename)['s']; #simdata
        # extract out model information (not currently recorded)
        m_ms_id = [];
        m_ms_on = [];
        m_ms_expt = [];
        for exp in m['expts']:
            exp_id = exp[0][0]['id'][0][0]
            for d in exp[0][0]['data_ms'][0]['id'][0]:
                m_ms_expt.append(exp_id);
                m_ms_id.append(d[0]);
                m_ms_on.append(bool(d[0][0]));
        # extract out simulation parameters (options)
        m_options = {
                    'cont_alpha':float(m['options'][0][0][0]['cont_alpha'][0][0][0]),
                    'cont_reltol':float(m['options'][0][0][0]['cont_reltol'][0][0][0]),
                    'cont_steps':float(m['options'][0][0][0]['cont_steps'][0][0][0]),
                    'fit_nudge':float(m['options'][0][0][0]['fit_nudge'][0][0][0]),
                    'fit_reinit':bool(m['options'][0][0][0]['fit_reinit'][0][0][0]),
                    'fit_reltol':float(m['options'][0][0][0]['fit_reltol'][0][0][0]),
                    'fit_starts':float(m['options'][0][0][0]['fit_starts'][0][0][0]),
                    'fit_tau':float(m['options'][0][0][0]['fit_tau'][0][0][0]),
                    'hpc_mcr':m['options'][0][0][0]['hpc_mcr'][0][0],
                    'hpc_on':bool(m['options'][0][0][0]['hpc_on'][0][0][0]),
                    'hpc_serve':m['options'][0][0][0]['hpc_serve'][0][0],
                    'int_maxstep':float(m['options'][0][0][0]['int_maxstep'][0][0][0]),
                    'int_reltol':float(m['options'][0][0][0]['int_reltol'][0][0][0]),
                    'int_senstol':float(m['options'][0][0][0]['int_senstol'][0][0][0]),
                    'int_timeout':float(m['options'][0][0][0]['int_timeout'][0][0][0]),
                    'int_tspan':float(m['options'][0][0][0]['int_tspan'][0][0][0]),
                    'ms_correct':bool(m['options'][0][0][0]['ms_correct'][0][0][0]),
                    'oed_crit':m['options'][0][0][0]['oed_crit'][0][0],
                    'oed_reinit':bool(m['options'][0][0][0]['oed_reinit'][0][0][0]),
                    'oed_tolf':float(m['options'][0][0][0]['oed_tolf'][0][0][0]),
                    'oed_tolx':float(m['options'][0][0][0]['oed_tolx'][0][0][0]),
                    'sim_more':bool(m['options'][0][0][0]['sim_more'][0][0][0]),
                    'sim_na':bool(m['options'][0][0][0]['sim_na'][0][0][0]),
                    'sim_sens':bool(m['options'][0][0][0]['sim_sens'][0][0][0]),
                    'sim_ss':bool(m['options'][0][0][0]['sim_ss'][0][0][0]),
                    'sim_tunit':m['options'][0][0][0]['sim_tunit'][0][0]}
        simulationParameters = [];
        m_options.update({'simulation_id':simulation_id,'simulation_dateAndTime':simulation_dateAndTime,
                    'used_':True,
                    'comment_':None});
        simulationParameters.append(m_options);
        # extract out fit information
        fittedData = [];
        f_Echi2 = None;
        if not isnan(f['Echi2'][0][0][0][0]):
            if len(f['Echi2'][0][0][0])>1:
                f_Echi2 = [f['Echi2'][0][0][0][0],f['Echi2'][0][0][0][1]];
            else:
                f_Echi2 = [f['Echi2'][0][0][0][0]];
        f_alf = f['alf'][0][0][0][0];
        f_chi2 = f['chi2'][0][0][0][0];
        f_dof = int(f['dof'][0][0][0][0]);
        f_ = {'fitted_echi2':f_Echi2,
        'fitted_alf':f_alf,
        'fitted_chi2':f_chi2,
        'fitted_dof':f_dof};
        f_.update({'simulation_id':simulation_id,'simulation_dateAndTime':simulation_dateAndTime,
                    'used_':True,
                    'comment_':None})
        fittedData.append(f_);
        # extract out sum of the squared residuals of the fitted measurements
        f_mnt_id = [];
        f_mnt_sres = [];
        f_mnt_expt = [];
        f_mnt_type = []; #Flux or MS
        for d in f['mnt'][0][0][0]['id']:
            f_mnt_id.append(d[0]);
        for d in f['mnt'][0][0][0]['sres']:
            f_mnt_sres.append(float(d[0][0]));
        for d in f['mnt'][0][0][0]['expt']:
            f_mnt_expt.append(d[0]);
        for d in f['mnt'][0][0][0]['type']:
            f_mnt_type.append(d[0]);
        # seperate into appropriate table rows
        fittedMeasuredFluxes = [];
        fittedMeasuredFragments = [];
        for cnt,type in enumerate(f_mnt_type):
            if type=='Flux':
                if f_mnt_expt[cnt] in simulation_info['experiment_id']:
                    fittedMeasuredFluxes.append({'simulation_id':simulation_id,
                    'simulation_dateAndTime':simulation_dateAndTime,
                    'experiment_id':f_mnt_expt[cnt],
                    'sample_name_abbreviation':simulation_info['sample_name_abbreviation'][0],
                    'rxn_id':f_mnt_id[cnt],
                    'fitted_sres':f_mnt_sres[cnt],
                    'used_':True,
                    'comment_':None})
                elif f_mnt_expt[cnt] in simulation_info['sample_name_abbreviation']:
                    fittedMeasuredFluxes.append({'simulation_id':simulation_id,
                    'simulation_dateAndTime':simulation_dateAndTime,
                    'experiment_id':simulation_info['experiment_id'][0],
                    'sample_name_abbreviation':f_mnt_expt[cnt],
                    'rxn_id':f_mnt_id[cnt],
                    'fitted_sres':f_mnt_sres[cnt],
                    'used_':True,
                    'comment_':None})
            elif type=='MS':
                if f_mnt_expt[cnt] in simulation_info['experiment_id']:
                    fittedMeasuredFragments.append({'simulation_id':simulation_id,
                    'simulation_dateAndTime':simulation_dateAndTime,
                    'experiment_id':f_mnt_expt[cnt],
                    'sample_name_abbreviation':simulation_info['sample_name_abbreviation'][0],
                    'fragment_id':f_mnt_id[cnt],
                    'fitted_sres':f_mnt_sres[cnt],
                    'used_':True,
                    'comment_':None})
                elif f_mnt_expt[cnt] in simulation_info['sample_name_abbreviation']:
                    fittedMeasuredFragments.append({'simulation_id':simulation_id,
                    'simulation_dateAndTime':simulation_dateAndTime,
                    'experiment_id':simulation_info['experiment_id'][0],
                    'sample_name_abbreviation':f_mnt_expt[cnt],
                    'fragment_id':f_mnt_id[cnt],
                    'fitted_sres':f_mnt_sres[cnt],
                    'used_':True,
                    'comment_':None})
            else:
                print 'type not recognized';
        # extract out the residuals of the fitted measurements
        f_mnt_res_val = [];
        f_mnt_res_fit = [];
        f_mnt_res_type = []; #Flux or MS
        f_mnt_res_id = [];
        f_mnt_res_std = [];
        f_mnt_res_time = [];
        f_mnt_res_expt = [];
        f_mnt_res_data = [];
        #f_mnt_res_esens = [];
        #f_mnt_res_msens = [];
        f_mnt_res_peak = [];
        for d in f['mnt'][0][0][0]['res']: 
            f_mnt_res_val.append(float(d[0][0]['val'][0][0]));
            f_mnt_res_fit.append(float(d[0][0]['fit'][0][0]));
            f_mnt_res_type.append(d[0][0]['type'][0]);
            f_mnt_res_id.append(d[0][0]['id'][0]);
            f_mnt_res_std.append(float(d[0][0]['std'][0][0]));
            #change default of time inf to 0
            if isinf(d[0][0]['time'][0][0]):
                f_mnt_res_time.append('0');
            else:
                f_mnt_res_time.append(str(d[0][0]['time'][0][0]));
            if d[0][0]['expt'][0] == 'Expt #1':
                f_mnt_res_expt.append(simulation_info['experiment_id'][0]);
            else:
                f_mnt_res_expt.append(d[0][0]['expt'][0]);
            f_mnt_res_data.append(d[0][0]['data'][0][0]);
            #f_mnt_res_esens.append(d[0][0]['esens'].data); #not needed, and matlab->python conversion has several bugs
            #f_mnt_res_msens.append(d[0][0]['msens'].data);
            if d[0][0]['peak']: f_mnt_res_peak.append(d[0][0]['peak'][0]);
            else: f_mnt_res_peak.append(None);
        # seperate into appropriate table rows
        fittedMeasuredFluxResiduals = [];
        fittedMeasuredFragmentResiduals = [];
        for cnt,type in enumerate(f_mnt_res_type):
            if type=='Flux':
                if f_mnt_res_expt[cnt] in simulation_info['experiment_id']:
                    fittedMeasuredFluxResiduals.append({'simulation_id':simulation_id,
                    'simulation_dateAndTime':simulation_dateAndTime,
                    'experiment_id':f_mnt_res_expt[cnt],
                    'sample_name_abbreviation':simulation_info['sample_name_abbreviation'][0],
                    'time_point':f_mnt_res_time[cnt],
                    'rxn_id':f_mnt_res_id[cnt],
                    'res_data':float(f_mnt_res_data[cnt]),
                    #'res_esens':f_mnt_res_esens[cnt],
                    'res_fit':float(f_mnt_res_fit[cnt]),
                    #'res_msens':f_mnt_res_msens[cnt],
                    'res_peak':f_mnt_res_peak[cnt],
                    'res_stdev':float(f_mnt_res_std[cnt]),
                    'res_val':float(f_mnt_res_val[cnt]),
                    'res_msens':None,
                    'res_esens':None,
                    'used_':True,
                    'comment_':None})
                elif f_mnt_res_expt[cnt] in simulation_info['sample_name_abbreviation']:
                    fittedMeasuredFluxResiduals.append({'simulation_id':simulation_id,
                    'simulation_dateAndTime':simulation_dateAndTime,
                    'experiment_id':simulation_info['experiment_id'][0],
                    'sample_name_abbreviation':f_mnt_res_expt[cnt],
                    'time_point':f_mnt_res_time[cnt],
                    'rxn_id':f_mnt_res_id[cnt],
                    'res_data':float(f_mnt_res_data[cnt]),
                    #'res_esens':f_mnt_res_esens[cnt],
                    'res_fit':float(f_mnt_res_fit[cnt]),
                    #'res_msens':f_mnt_res_msens[cnt],
                    'res_peak':f_mnt_res_peak[cnt],
                    'res_stdev':float(f_mnt_res_std[cnt]),
                    'res_val':float(f_mnt_res_val[cnt]),
                    'res_msens':None,
                    'res_esens':None,
                    'used_':True,
                    'comment_':None})
            elif type=='MS':
                # parse the id into fragment_id and mass
                fragment_string = f_mnt_res_id[cnt]
                fragment_string = re.sub('_DASH_','-',fragment_string)
                fragment_string = re.sub('_LPARANTHES_','[(]',fragment_string)
                fragment_string = re.sub('_RPARANTHES_','[)]',fragment_string)
                fragment_list = fragment_string.split('_');
                if not len(fragment_list)>5 or not ('MRM' in fragment_list or 'EPI' in fragment_list):
                    fragment_id = '_'.join([fragment_list[0],fragment_list[1],fragment_list[2]])
                    fragment_mass = Formula(fragment_list[2]).mass + float(fragment_list[3]);
                    time_point = fragment_list[4];
                else:
                    fragment_id = '_'.join([fragment_list[0],fragment_list[1],fragment_list[2],fragment_list[3]])
                    fragment_mass = Formula(fragment_list[2]).mass + float(fragment_list[4]);
                    time_point = fragment_list[5];
                #exp_id = fragment_list[5];
                #exp_id = fragment_list[6];
                fragment_id = re.sub('-','_DASH_',fragment_id)
                fragment_id = re.sub('[(]','_LPARANTHES_',fragment_id)
                fragment_id = re.sub('[)]','_RPARANTHES_',fragment_id)
                if f_mnt_res_expt[cnt] in simulation_info['experiment_id']:
                    fittedMeasuredFragmentResiduals.append({'simulation_id':simulation_id,
                    'simulation_dateAndTime':simulation_dateAndTime,
                    'experiment_id':f_mnt_res_expt[cnt],
                    'sample_name_abbreviation':simulation_info['sample_name_abbreviation'][0],
                    'time_point':f_mnt_res_time[cnt],
                    'fragment_id':fragment_id,
                    'fragment_mass':fragment_mass,
                    'res_data':float(f_mnt_res_data[cnt]),
                    #'res_esens':f_mnt_res_esens[cnt],
                    'res_fit':float(f_mnt_res_fit[cnt]),
                    #'res_msens':f_mnt_res_msens[cnt],
                    'res_peak':f_mnt_res_peak[cnt], #'res_peak':float(f_mnt_res_peak[cnt]),
                    'res_stdev':float(f_mnt_res_std[cnt]),
                    'res_val':float(f_mnt_res_val[cnt]),
                    'res_msens':None,
                    'res_esens':None,
                    'used_':True,
                    'comment_':None})
                elif f_mnt_res_expt[cnt] in simulation_info['sample_name_abbreviation']:
                    fittedMeasuredFragmentResiduals.append({'simulation_id':simulation_id,
                    'simulation_dateAndTime':simulation_dateAndTime,
                    'experiment_id':simulation_info['experiment_id'][0],
                    'sample_name_abbreviation':f_mnt_res_expt[cnt],
                    'time_point':f_mnt_res_time[cnt],
                    'fragment_id':fragment_id,
                    'fragment_mass':fragment_mass,
                    'res_data':float(f_mnt_res_data[cnt]),
                    #'res_esens':f_mnt_res_esens[cnt],
                    'res_fit':float(f_mnt_res_fit[cnt]),
                    #'res_msens':f_mnt_res_msens[cnt],
                    'res_peak':f_mnt_res_peak[cnt], #'res_peak':float(f_mnt_res_peak[cnt]),
                    'res_stdev':float(f_mnt_res_std[cnt]),
                    'res_val':float(f_mnt_res_val[cnt]),
                    'res_msens':None,
                    'res_esens':None,
                    'used_':True,
                    'comment_':None})
            else:
                print 'type not recognized';
        # extract out the fitted parameters
        f_par_id = [];
        f_par_val = [];
        f_par_std = [];
        f_par_type = []; # 'Net flux' or 'Norm'
        f_par_lb = [];
        f_par_ub = [];
        f_par_unit = [];
        f_par_alf = [];
        f_par_chi2s = [];
        f_par_cor = [];
        f_par_cov = [];
        f_par_free = [];
        for d in f['par'][0][0][0]['id']:
            if 'Expt #1' in d[0]:
                id_str = d[0].astype('str')
                f_par_id.append(id_str.replace('Expt #1',simulation_info['experiment_id'][0]))
            else:
                f_par_id.append(d[0])
        # ensure that there are no negative values or infinite values
        for d in f['par'][0][0][0]['val']:
            if not d:
                f_par_val.append(0.0)
            elif isnan(d[0][0]) or d[0][0]<1.0e-6:
                f_par_val.append(0.0)
            elif isinf(d[0][0]) or d[0][0]>1e3:
                f_par_val.append(1.0e3)
            else:
                f_par_val.append(float(d[0][0]))
        for d in f['par'][0][0][0]['std']:
            if not d:
                f_par_std.append(0.0)
            elif isnan(d[0][0]):
                f_par_val.append(0.0)
            else:
                f_par_std.append(float(d[0][0]))
        for d in f['par'][0][0][0]['type']:
            f_par_type.append(d[0])
        #adjust the lb and ub to [0,1000];
        for cnt,d in enumerate(f['par'][0][0][0]['lb']):
            if not d:
                f_par_lb.append(0.0)
            elif isnan(d[0][0]) or d[0][0]<1.0e-6:
                f_par_lb.append(0.0)
            else:
                f_par_lb.append(float(d[0][0]))
        for d in f['par'][0][0][0]['ub']:
            if not d:
                f_par_ub.append(1.0e3)
            elif isinf(d[0][0]) or isnan(d[0][0]) or d[0][0]>1.0e3:
                f_par_ub.append(1.0e3)
            else:
                f_par_ub.append(float(d[0][0]))
        for d in f['par'][0][0][0]['unit']:
            if not d:
                #f_par_unit.append(None);
                #use default: mmol*gDCW-1*hr-1
                f_par_unit.append('mmol*gDCW-1*hr-1');
            else:
                f_par_unit.append(d[0])
        for d in f['par'][0][0][0]['alf']:
            f_par_alf.append(float(d[0][0]))
        for d in f['par'][0][0][0]['chi2s']:
            f_par_chi2s.append(d)
        for d in f['par'][0][0][0]['cor']:
            f_par_cor.append(d)
        for d in f['par'][0][0][0]['cov']:
            f_par_cov.append(d)
        for d in f['par'][0][0][0]['free']:
            f_par_free.append(bool(d[0][0]))
        # seperate into appropriate table rows
        fittedFluxes = [];
        fittedFragments = [];
        for cnt,type in enumerate(f_par_type):
            if type=='Net flux':
                fittedFluxes.append({'simulation_id':simulation_id,
                'simulation_dateAndTime':simulation_dateAndTime,
                'rxn_id':f_par_id[cnt],
                'flux':f_par_val[cnt],
                'flux_stdev':f_par_std[cnt],
                'flux_lb':f_par_lb[cnt],
                'flux_ub':f_par_ub[cnt],
                'flux_units':f_par_unit[cnt],
                'fit_alf':f_par_alf[cnt],
                'fit_chi2s':None,
                #'fit_chi2s':f_par_chi2s[cnt],
                'fit_cor':None,
                'fit_cov':None,
                #'fit_cor':f_par_cor[cnt],
                #'fit_cov':f_par_cov[cnt],
                'free':f_par_free[cnt],
                'used_':True,
                'comment_':None})
            elif type=='Norm':
                # parse the id 
                id_list = f_par_id[cnt].split(' ');
                expt = id_list[0];
                fragment_id = id_list[1];
                fragment_string = id_list[2];
                units = id_list[3];
                # parse the id into fragment_id and mass
                fragment_string = re.sub('_DASH_','-',fragment_string)
                fragment_string = re.sub('_LPARANTHES_','[(]',fragment_string)
                fragment_string = re.sub('_RPARANTHES_','[)]',fragment_string)
                fragment_list = fragment_string.split('_');
                if not len(fragment_list)>5 or not ('MRM' in fragment_list or 'EPI' in fragment_list):
                    fragment_mass = Formula(fragment_list[2]).mass + float(fragment_list[3]);
                    time_point = fragment_list[4];
                else:
                    fragment_mass = Formula(fragment_list[2]).mass + float(fragment_list[4]);
                    time_point = fragment_list[5];
                #fragment_id = '_'.join([fragment_list[0],fragment_list[1],fragment_list[2],fragment_list[3]])
                #fragment_id = re.sub('-','_DASH_',fragment_id)
                #fragment_id = re.sub('[(]','_LPARANTHES_',fragment_id)
                #fragment_id = re.sub('[)]','_RPARANTHES_',fragment_id)
                #expt_id = fragment_list[5];
                #expt_id = fragment_list[6];
                if expt in simulation_info['experiment_id']:
                    fittedFragments.append({'simulation_id':simulation_id,
                    'simulation_dateAndTime':simulation_dateAndTime,
                    'experiment_id':expt,
                    'sample_name_abbreviation':simulation_info['sample_name_abbreviation'][0],
                    'time_point':time_point,
                    'fragment_id':fragment_id,
                    'fragment_mass':fragment_mass,
                    'fit_val':f_par_val[cnt],
                    'fit_stdev':f_par_std[cnt],
                    'fit_units':units,
                    'fit_alf':f_par_alf[cnt],
                    'fit_cor':None,
                    'fit_cov':None,
                    #'fit_cor':f_par_cor[cnt],
                    #'fit_cov':f_par_cov[cnt],
                    'free':f_par_free[cnt],
                    'used_':True,
                    'comment_':None})
                elif expt in simulation_info['sample_name_abbreviation']:
                    fittedFragments.append({'simulation_id':simulation_id,
                    'simulation_dateAndTime':simulation_dateAndTime,
                    'experiment_id':simulation_info['experiment_id'][0],
                    'sample_name_abbreviation':expt,
                    'time_point':time_point,
                    'fragment_id':fragment_id,
                    'fragment_mass':fragment_mass,
                    'fit_val':f_par_val[cnt],
                    'fit_stdev':f_par_std[cnt],
                    'fit_units':units,
                    'fit_alf':f_par_alf[cnt],
                    'fit_cor':None,
                    'fit_cov':None,
                    #'fit_cor':f_par_cor[cnt],
                    #'fit_cov':f_par_cov[cnt],
                    'free':f_par_free[cnt],
                    'used_':True,
                    'comment_':None})
            else:
                print 'type not recognized';
        # add data to the database
        self.add_data_stage02_isotopomer_fittedData(fittedData);
        self.add_data_stage02_isotopomer_fittedFluxes(fittedFluxes);
        self.add_data_stage02_isotopomer_fittedFragments(fittedFragments);
        self.add_data_stage02_isotopomer_fittedMeasuredFluxes(fittedMeasuredFluxes);
        self.add_data_stage02_isotopomer_fittedMeasuredFragments(fittedMeasuredFragments);
        self.add_data_stage02_isotopomer_fittedMeasuredFluxResiduals(fittedMeasuredFluxResiduals);
        self.add_data_stage02_isotopomer_fittedMeasuredFragmentResiduals(fittedMeasuredFragmentResiduals);
        self.add_data_stage02_isotopomer_simulationParameters(simulationParameters)

    # TODO:
    def export_data_stage02_isotopomer_models(self,model_id_I,filename_I):
        cobra_model_sbml = None;
        cobra_model_sbml = self.stage02_isotopomer_query.get_row_modelID_dataStage02IsotopomerModels(model_id_I);
        # write the model to a temporary file
        with open(filename_I,'wb') as file:
            file.write(cobra_model_sbml['sbml_file']);
    def export_isotopomerModel_cobraMAT(self, filename):
        '''export isotopomer model for fluxomics simulation using the cobratoolbox 2.0 fluxomics module'''
        #TODO
        return
    def export_isotopomerModel_INCA(self, filename):
        '''export isotopomer model for fluxomics simulation using INCA1.1'''
        #TODO
        return
    def export_isotopomerExperiment_cobraMAT(self, filename):
        '''export isotopomer experiment for fluxomics simulation using the cobratoolbox 2.0 fluxomics module'''
        #TODO
        return
    def export_isotopomerExperiment_INCA(self, filename):
        '''export isotopomer experiment for fluxomics simulation using INCA1.1'''
        #TODO
        return
    def import_isotopomerSimulationResults_cobraMAT(self, filename):
        '''import results from a fluxomics simulation using the cobratoolbox 2.0 fluxomics module'''
        #TODO
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_(data.data);
        data.clear_data();
        return

    # Internal
    def convert_netRxn2IndividualRxns(self,net_rxn_I,flux_I):
        '''Convert a net rxn into individual rxns,
        and update the direction of the flux for each individual reactions
        accordingly'''

        #Input:
        #   net_rxn_I = string, rxn_id
        #   flux_I = flux, float
        #Output:
        #   rxns_O = list, rxn_ids
        #   fluxes_O = list, floats
        #   fluxes_O_dict = dict, rxn_id:flux
        

        from stage02_isotopomer_dependencies import isotopomer_netRxns
        netRxns = isotopomer_netRxns();

        rxns_O = [];
        fluxes_O = [];
        fluxes_O_dict = {};

        if not flux_I:
            #print 'reaction has no flux';
            return fluxes_O_dict;
        elif net_rxn_I in netRxns.isotopomer_rxns_net.keys():
            rxns_O = netRxns.isotopomer_rxns_net[net_rxn_I]['reactions'];
            stoichiometry = netRxns.isotopomer_rxns_net[net_rxn_I]['stoichiometry'];
            # change the direction of the fluxes according to the stoichiometry of the reactions
            fluxes_O = [s*flux_I for s in stoichiometry];
        else:
            #print 'net reaction not found';
            return fluxes_O_dict;

        #return rxns_O,fluxes_O;
        # wrap into a dictionary
        fluxes_O_dict = dict(zip(rxns_O,fluxes_O));
        return fluxes_O_dict;

    # Visualization
    def export_fluxomicsAnalysis_escher(self,experiment_id_I,model_ids_I=[],
                         model_ids_dict_I={},
                     mapping_ids_I=[],
                     sample_name_abbreviations_I=[],
                     map_ids_I=[],
                     filename=[settings.visualization_data,'/isotopomer/metabolicmap/','fluxomics/']):
        '''export estimated fluxes for visualization'''
        
        # get the model ids:
        filter_O = {};
        filter_O['model_id'] = [];
        filter_O['mapping_id'] = [];
        filter_O['sample'] = [];
        filter_O['map_id'] = [];
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage02_isotopomer_query.get_modelID_experimentID_dataStage02IsotopomerSimulation(experiment_id_I);
        for model_id in model_ids:
            filter_mi_str = 'model_id/'+ model_id.replace('_','');
            filter_O['model_id'].append(filter_mi_str);
            print 'exporting fluxomics analysis for model_id ' + model_id;
            # get the cobra model
            if model_ids_dict_I:
                cobra_model = model_ids_dict_I[model_id];
            else:
                # get the cobra model
                cobra_model_sbml = None;
                cobra_model_sbml = self.stage02_isotopomer_query.get_row_modelID_dataStage02IsotopomerModels(model_id);
                # write the model to a temporary file
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
            # get the time-points
            if mapping_ids_I:
                mapping_ids = mapping_ids_I;
            else:
                mapping_ids = [];
                mapping_ids = self.stage02_isotopomer_query.get_mappingID_experimentIDAndModelID_dataStage02IsotopomerSimulation(experiment_id_I,model_id);
            for mapping in mapping_ids:
                filter_mapping_str = 'model_id/'+ model_id.replace('_','') +'/mapping_id/'+mapping.replace('_','');
                filter_O['mapping_id'].append(filter_mapping_str);
                print 'exporting fluxomic analysis for mapping_id ' + mapping;
                # get sample_name_abbreviations
                if sample_name_abbreviations_I:
                    sample_name_abbreviations = sample_name_abbreviations_I;
                else:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.stage02_isotopomer_query.get_sampleNameAbbreviations_experimentIDAndModelIDAndMappingID_dataStage02IsotopomerSimulation(experiment_id_I,model_id,mapping);
                for sna in sample_name_abbreviations:
                    filter_sna_str = 'model_id/'+ model_id.replace('_','') +'/mapping_id/'+mapping.replace('_','')+'/sample/'+sna.replace('_','');
                    filter_O['sample'].append(filter_sna_str);
                    print 'exporting fluxomic analysis for sample_name_abbreviation ' + sna;
                    # get the simulation_id
                    simulation_ids = [];
                    simulation_ids = self.stage02_isotopomer_query.get_simulationID_experimentIDAndSampleNameAbbreviationsAndModelIDAndMappingID_dataStage02IsotopomerSimulation(experiment_id_I,sna,model_id,mapping);
                    if len(simulation_ids)>1:
                        print 'more than 1 simulation found'
                        return;
                    else: simulation_id = simulation_ids[0];
                    # calculated fluxes
                    flux_lbub = [];
                    flux_lbub = self.stage02_isotopomer_query.get_rowsEscherFluxLbUb_simulationID_dataStage02IsotopomerfittedNetFluxes(simulation_id);
                    flux = {};
                    flux = self.stage02_isotopomer_query.get_rowsEscherFlux_simulationID_dataStage02IsotopomerfittedNetFluxes(simulation_id);
                    # break lumped reactions into individual reactions
                    fluxes = {};
                    for k,v in flux.iteritems():
                        fluxes_O = {};
                        fluxes_O = self.convert_netRxn2IndividualRxns(k,v);
                        if fluxes_O:
                            fluxes.update(fluxes_O);
                        else:
                            fluxes.update({k:v});
                    # map_ids
                    if map_ids_I:
                        map_ids = map_ids_I;
                    else:
                        map_ids = [
                        'AlternateCarbonMetabolism',\
                        'AminoAcidMetabolism',\
                        'CofactorBiosynthesis',\
                        'InorganicIonMetabolism',\
                        'NucleotideMetabolism',\
                        'CentralMetabolism'
                        ];
                    for map_id in map_ids:
                        filter_map_str = 'model_id/'+ model_id.replace('_','') +'/mapping_id/'+mapping.replace('_','')+'/sample/'+sna.replace('_','')+'/map_id/'+map_id.replace('_','');
                        filter_O['map_id'].append(filter_map_str);
                        print 'exporting fluxomics analysis for map_id ' + map_id;
                        # generate the map html using escher
                        map_json = json.load(open(settings.sbaas + '/data/escher_maps/' + map_id + '.json','rb'));
                        map = Builder(map_json=json.dumps(map_json), reaction_data=fluxes);
                        #html_file = map._get_html(scroll_behavior='zoom')
                        #html_file = map._get_html(menu='all',
                        #  # make the output a standalone HTML file
                        #  html_wrapper=True,
                        #  # make sure the application fills the screen
                        #  fill_screen=True,
                        #  # choose whether to enable map editing
                        #  enable_editing=True,
                        #  # choose whether to enable keyboard shortcuts
                        #  enable_keys=True)
                        filename_str = filename[0] + '/' + experiment_id_I.replace('_','') + filename[1] + filename[2] + model_id.replace('_','') + '_' + mapping.replace('_','') + '_' + sna.replace('_','') + '_' + map_id.replace('_','') + '.html';
                        #with open(filename_str,'wb') as file:
                        #    file.write(html_file);
                        map.save_html(filename_str)
        # dump the filter data to a json file
        json_str = 'var ' + 'data_filter' + ' = ' + json.dumps(filter_O);
        filename_str = filename[0]+ '/' +experiment_id_I.replace('_','') + filename[1] + filename[2] + 'filter.js'
        with open(filename_str,'wb') as file:
            file.write(json_str);
    def export_dataStage02IsotopomerFittedNetFluxes_js(self,analysis_id_I = None, simulation_ids_I = [],data_dir_I="tmp"):
        '''Plot the flux precision for a given set of simulations and a given set of reactions
        Default: plot the flux precision for each simulation on a single plot for a single reaction'''

        #Input:
        # analysis_id_I or
        # simulation_ids_I

        if simulation_ids_I:
            simulation_ids = simulation_ids_I;
        else:
            simulation_ids = [];
            simulation_ids = self.stage02_isotopomer_query.get_simulationID_analysisID_dataStage02IsotopomerAnalysis(analysis_id_I);
        data_O =[]; 
        for simulation_id in simulation_ids:
            # get the flux information for each simulation
            flux_data = [];
            flux_data = self.stage02_isotopomer_query.get_rows_simulationID_dataStage02IsotopomerfittedNetFluxes(simulation_id);
            for i,row in enumerate(flux_data):
                row['simulation_dateAndTime'] = self.convert_datetime2string(row['simulation_dateAndTime']);
                row['flux_units'] = row['flux_units'].replace('*','x');
                data_O.append(row);
        # dump chart parameters to a js files
        data1_keys = ['simulation_id','rxn_id','simulation_dateAndTime','flux_units'
                    ];
        data1_nestkeys = ['rxn_id'];
        data1_keymap = {'xdata':'rxn_id',
                        'ydata':'flux',
                        'ydatalb':'flux_lb',
                        'ydataub':'flux_ub',
                        'serieslabel':'simulation_id',
                        'featureslabel':'rxn_id'};
        # make the data object
        dataobject_O = [{"data":data_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys}];
        # make the tile parameter objects
        formtileparameters_O = {'tileheader':'Filter menu','tiletype':'html','tileid':"filtermenu1",'rowid':"row1",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"};
        formparameters_O = {'htmlid':'filtermenuform1',"htmltype":'form_01',"formsubmitbuttonidtext":{'id':'submit1','text':'submit'},"formresetbuttonidtext":{'id':'reset1','text':'reset'},"formupdatebuttonidtext":{'id':'update1','text':'update'}};
        formtileparameters_O.update(formparameters_O);
        svgparameters_O = {"svgtype":'boxandwhiskersplot2d_01',"svgkeymap":[data1_keymap,data1_keymap],
                            'svgid':'svg1',
                            "svgmargin":{ 'top': 50, 'right': 350, 'bottom': 50, 'left': 50 },
                            "svgwidth":500,"svgheight":350,
                            "svgx1axislabel":"rxn_id","svgy1axislabel":"flux",
    						'svgformtileid':'filtermenu1','svgresetbuttonid':'reset1','svgsubmitbuttonid':'submit1'};
        svgtileparameters_O = {'tileheader':'Flux precision','tiletype':'svg','tileid':"tile2",'rowid':"row1",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"};
        svgtileparameters_O.update(svgparameters_O);
        tableparameters_O = {"tabletype":'responsivetable_01',
                    'tableid':'table1',
                    "tablefilters":None,
                    "tableclass":"table  table-condensed table-hover",
    			    'tableformtileid':'filtermenu1','tableresetbuttonid':'reset1','tablesubmitbuttonid':'submit1'};
        tabletileparameters_O = {'tileheader':'Flux precision','tiletype':'table','tileid':"tile3",'rowid':"row1",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"};
        tabletileparameters_O.update(tableparameters_O);
        parametersobject_O = [formtileparameters_O,svgtileparameters_O,tabletileparameters_O];
        tile2datamap_O = {"filtermenu1":[0],"tile2":[0],"tile3":[0]};
        # dump the data to a json file
        data_str = 'var ' + 'data' + ' = ' + json.dumps(dataobject_O) + ';';
        parameters_str = 'var ' + 'parameters' + ' = ' + json.dumps(parametersobject_O) + ';';
        tile2datamap_str = 'var ' + 'tile2datamap' + ' = ' + json.dumps(tile2datamap_O) + ';';
        if data_dir_I=='tmp':
            filename_str = settings.visualization_data + '/tmp/ddt_data.js'
        elif data_dir_I=='project':
            filename_str = settings.visualization_data + '/project/' + analysis_id_I + '_data_stage02_isotopomer_fittedNetFluxes' + '.js'
        elif data_dir_I=='data_json':
            data_json_O = data_str + '\n' + parameters_str + '\n' + tile2datamap_str;
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(data_str);
            file.write(parameters_str);
            file.write(tile2datamap_str);
    def export_dataStage02IsotopomerFluxMap_js(self,simulation_id_I = None,data_dir_I="tmp"):
        '''Export flux map for viewing'''

        iomod = models_query(self.session);

        # Get the flux information
        flux = [];
        #flux = self.stage02_isotopomer_query.get_rowsEscherFluxList_simulationID_dataStage02IsotopomerfittedNetFluxes(simulation_id_I);
        flux = self.stage02_isotopomer_query.get_rows_simulationID_dataStage02IsotopomerfittedNetFluxes(simulation_id_I);
        for i,row in enumerate(flux):
            flux[i]['simulation_dateAndTime'] = self.convert_datetime2string(row['simulation_dateAndTime']);
            flux[i]['flux_units'] = self.remove_jsRegularExpressions(row['flux_units']);
        # Get the map information
        map = [];
        map = iomod.get_rows_modelID_modelsEschermaps('iJO1366');
        # dump chart parameters to a js files
        data1_keys = ['simulation_id','rxn_id','simulation_dateAndTime','flux_units'
                    ];
        data1_nestkeys = ['simulation_id'];
        data1_keymap = {'values':'flux','key':'rxn_id'};
        data2_keys = ['model_id','eschermap_id'
                    ];
        data2_nestkeys = ['model_id'];
        data2_keymap = {'data':'eschermap_json'};
        # make the data object
        dataobject_O = [{"data":flux,"datakeys":data1_keys,"datanestkeys":data1_nestkeys},
                        {"data":map,"datakeys":data2_keys,"datanestkeys":data2_nestkeys}];
        # make the tile parameter objects
        formtileparameters1_O = {'tileheader':'Filter menu','tiletype':'html','tileid':"filtermenu1",'rowid':"row1",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-6"};
        formparameters1_O = {'htmlid':'filtermenuform1',"htmltype":'form_01',"formsubmitbuttonidtext":{'id':'submit1','text':'submit'},"formresetbuttonidtext":{'id':'reset1','text':'reset'},"formupdatebuttonidtext":{'id':'update1','text':'update'}};
        formtileparameters1_O.update(formparameters1_O);
        formtileparameters2_O = {'tileheader':'Filter menu','tiletype':'html','tileid':"filtermenu2",'rowid':"row1",'colid':"col2",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-6"};
        formparameters2_O = {'htmlid':'filtermenuform2',"htmltype":'form_01',"formsubmitbuttonidtext":{'id':'submit2','text':'submit'},"formresetbuttonidtext":{'id':'reset2','text':'reset'},"formupdatebuttonidtext":{'id':'update2','text':'update'}};
        formtileparameters2_O.update(formparameters2_O);
        htmlparameters_O = {"htmlkeymap":[data1_keymap,data2_keymap],
                        'htmltype':'escher_01','htmlid':'html1',
                        'escherdataindex':{"reactiondata":0,"mapdata":1},
                        'escherembeddedcss':None,
                        'escheroptions':None};
        htmltileparameters_O = {'tileheader':'Escher map','tiletype':'html','tileid':"tile1",'rowid':"row2",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"};
        htmltileparameters_O.update(htmlparameters_O);
        tableparameters_O = {"tabletype":'responsivetable_01',
                    'tableid':'table1',
                    "tablefilters":None,
                    "tableclass":"table  table-condensed table-hover",
    			    'tableformtileid':'filtermenu1','tableresetbuttonid':'reset1','tablesubmitbuttonid':'submit1'};
        tabletileparameters_O = {'tileheader':'Flux precision','tiletype':'table','tileid':"tile2",'rowid':"row3",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"};
        tabletileparameters_O.update(tableparameters_O);
        parametersobject_O = [formtileparameters1_O,formtileparameters2_O,htmltileparameters_O,tabletileparameters_O];
        tile2datamap_O = {"filtermenu1":[0],"filtermenu2":[1],"tile1":[0,1],"tile2":[0]};
        filtermenuobject_O = [{"filtermenuid":"filtermenu1","filtermenuhtmlid":"filtermenuform1",
                "filtermenusubmitbuttonid":"submit1","filtermenuresetbuttonid":"reset1",
                "filtermenuupdatebuttonid":"update1"},{"filtermenuid":"filtermenu2","filtermenuhtmlid":"filtermenuform2",
                "filtermenusubmitbuttonid":"submit2","filtermenuresetbuttonid":"reset2",
                "filtermenuupdatebuttonid":"update2"}];
        # dump the data to a json file
        data_str = 'var ' + 'data' + ' = ' + json.dumps(dataobject_O) + ';';
        parameters_str = 'var ' + 'parameters' + ' = ' + json.dumps(parametersobject_O) + ';';
        tile2datamap_str = 'var ' + 'tile2datamap' + ' = ' + json.dumps(tile2datamap_O) + ';';
        filtermenu_str = 'var ' + 'filtermenu' + ' = ' + json.dumps(filtermenuobject_O) + ';';
        if data_dir_I=='tmp':
            filename_str = settings.visualization_data + '/tmp/ddt_data.js'
        elif data_dir_I=='project':
            filename_str = settings.visualization_data + '/project/' + analysis_id_I + '_data_stage02_isotopomer_fittedNetFluxes' + '.js'
        elif data_dir_I=='data_json':
            data_json_O = data_str + '\n' + parameters_str + '\n' + tile2datamap_str + '\n' + filtermenu_str;
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(data_str);
            file.write(parameters_str);
            file.write(tile2datamap_str);
            file.write(filtermenu_str);