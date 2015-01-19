# Dependencies
from analysis.analysis_base import *
from stage03_quantification_query import stage03_quantification_query
from resources.molmass import Formula
# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file, write_cobra_model_to_sbml_file
from cobra.io import load_matlab_model
# Dependencies from escher
from escher import Builder

class stage03_quantification_io(base_analysis):
    def __init__(self):
        self.session = Session();
        self.stage03_quantification_query = stage03_quantification_query();
    def import_dataStage03MetabolomicsData_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03MetabolomicsData(data.data);
        data.clear_data();

    def add_dataStage03MetabolomicsData(self, data_I):
        '''add rows of data_stage03_quantification_metabolomicsData'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage03_quantification_metabolomicsData(d['experiment_id'],
                            d['sample_name_abbreviation'],
                            d['time_point'],
                            d['met_id'],
                            d['concentration'],
                            d['concentration_var'],
                            d['concentration_units'],
                            d['concentration_lb'],
                            d['concentration_ub'],
                            d['measured'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03MetabolomicsData_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03MetabolomicsData(data.data);
        data.clear_data();

    def update_dataStage03MetabolomicsData(self,data_I):
        #Not yet tested
        '''update rows of data_stage03_quantification_metabolomicsData'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_metabolomicsData).filter(
                            data_stage03_quantification_metabolomicsData.id.like(d['id'])).update(
                            {'experiment_id':d['experiment_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'met_id':d['met_id'],
                            'concentration':d['concentration'],
                            'concentration_var':d['concentration_var'],
                            'concentration_units':d['concentration_units'],
                            'concentration_lb':d['concentration_lb'],
                            'concentration_ub':d['concentration_ub'],
                            'measured':d['measured'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
            
    def import_dataStage03SimulatedData_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03SimulatedData(data.data);
        data.clear_data();

    def add_dataStage03SimulatedData(self, data_I):
        '''add rows of data_stage03_quantification_simulatedData'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage03_quantification_simulatedData(d['experiment_id'],
                                d['model_id'],
                                d['rxn_id'],
                                d['fba_flux'],
                                d['fva_minimum'],
                                d['fva_maximum'],
                                d['flux_units'],
                                d['sra_gr'],
                                d['sra_gr_ratio'],
                                d['used_'],
                                d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03SimulatedData_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03SimulatedData(data.data);
        data.clear_data();

    def update_dataStage03SimulatedData(self,data_I):
        #Not yet tested
        '''update rows of data_stage03_quantification_simulatedData'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_simulatedData).filter(
                            data_stage03_quantification_simulatedData.id.like(d['id'])).update(
                            {'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'rxn_id':d['rxn_id'],
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

    def import_dataStage03OtherData_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03OtherData(data.data);
        data.clear_data();

    def add_dataStage03OtherData(self, data_I):
        '''add rows of data_stage03_quantification_otherData'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage03_quantification_otherData(d['experiment_id'],
                        d['sample_name_abbreviation'],
                        d['time_point'],
                        d['compartment_id'],
                        d['pH'],
                        d['temperature'],
                        d['temperature_units'],
                        d['ionic_strength'],
                        d['ionic_strength_units'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03OtherData_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03OtherData(data.data);
        data.clear_data();

    def update_dataStage03OtherData(self,data_I):
        #Not yet tested
        '''update rows of data_stage03_quantification_otherData'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_otherData).filter(
                            data_stage03_quantification_otherData.id.like(d['id'])).update(
                            {'experiment_id':d['experiment_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'compartment_id':d['compartment_id'],
                            'pH':d['pH'],
                            'temperature':d['temperature'],
                            'temperature_units':d['temperature_units'],
                            'ionic_strength':d['ionic_strength'],
                            'ionic_strength_units':d['ionic_strength_units'],
                            'used_':d['used_'],
                            'comment_I':d['comment_I']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
            
    def import_dataStage03dG0r_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03dG0r(data.data);
        data.clear_data();

    def add_dataStage03dG0r(self, data_I):
        '''add rows of data_stage03_quantification_dG0_r'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage03_quantification_dG0_r(d['experiment_id'],
                        d['model_id'],
                        d['sample_name_abbreviation'],
                        d['time_point'],
                        d['rxn_id'],
                        d['Keq_lb'],
                        d['Keq_ub'],
                        d['dG0_r'],
                        d['dG0_r_var'],
                        d['dG0_r_units'],
                        d['dG0_r_lb'],
                        d['dG0_r_ub'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03dG0r_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03dG0r(data.data);
        data.clear_data();

    def update_dataStage03dG0r(self,data_I):
        #Not yet tested
        '''update rows of data_stage03_quantification_dG0_r'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_dG0_r).filter(
                            standards.id.like(d['id'])).update(
                            {'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'rxn_id':d['rxn_id'],
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

    def import_dataStage03dGr_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03dGr(data.data);
        data.clear_data();

    def add_dataStage03dGr(self, data_I):
        '''add rows of data_stage03_quantification_dG_r'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage03_quantification_dG_r(d['experiment_id'],
                        d['model_id'],
                        d['sample_name_abbreviation'],
                        d['time_point'],
                        d['rxn_id'],
                        d['Keq_lb'],
                        d['Keq_ub'],
                        d['dG_r'],
                        d['dG_r_var'],
                        d['dG_r_units'],
                        d['dG_r_lb'],
                        d['dG_r_ub'],
                        d['displacement_lb'],
                        d['displacement_ub'],
                        d['Q_lb'],
                        d['Q_ub'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03dGr_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03dGr(data.data);
        data.clear_data();

    def update_dataStage03dGr(self,data_I):
        #Not yet tested
        '''update rows of data_stage03_quantification_dG_r'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_dG_r).filter(
                            standards.id.like(d['id'])).update(
                            {'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'rxn_id':d['rxn_id'],
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
            
    def import_dataStage03dGf_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03dGf(data.data);
        data.clear_data();

    def add_dataStage03dGf(self, data_I):
        '''add rows of data_stage03_quantification_dG_f'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage03_quantification_dG_f(d['experiment_id'],
                        d['model_id'],
                        d['sample_name_abbreviation'],
                        d['time_point'],
                        d['met_name'],
                        d['met_id'],
                        d['dG_f'],
                        d['dG_f_units'],
                        d['dG_f_lb'],
                        d['dG_f_ub'],
                        d['temperature'],
                        d['temperature_units'],
                        d['ionic_strength'],
                        d['ionic_strength_units'],
                        d['pH'],
                        d['pH_units'],
                        d['measured'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03dGf_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03dGf(data.data);
        data.clear_data();

    def update_dataStage03dGf(self,data_I):
        #Not yet tested
        '''update rows of data_stage03_quantification_dG_f'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_dG_f).filter(
                            standards.id.like(d['id'])).update(
                            {'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'met_name':d['met_name'],
                            'met_id':d['met_id'],
                            'dG_f':d['dG_f'],
                            'dG_f_units':d['dG_f_units'],
                            'dG_f_lb':d['dG_f_lb'],
                            'dG_f_ub':d['dG_f_ub'],
                            'temperature':d['temperature'],
                            'temperature_units':d['temperature_units'],
                            'ionic_strength':d['ionic_strength'],
                            'ionic_strength_units':d['ionic_strength_units'],
                            'pH':d['pH'],
                            'pH_units':d['pH_units'],
                            'measured':d['measured'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03dG0f_add(self, filename):
        '''table adds'''
        data = base_importData();
        #data.read_csv(filename);
        data.read_json(filename);
        #data.format_data();
        self.add_dataStage03dG0f(data.data);
        #data.clear_data();

    def add_dataStage03dG0f(self, data_I):
        '''add rows of data_stage03_quantification_dG0_f'''
        if data_I:
            #for d in data_I:
            #    try:
            #        data_add = data_stage03_quantification_dG0_f(d['reference_id'],
            #            d['met_name'],
            #            d['met_id'],
            #            d['KEGG_id'],
            #            d['priority'],
            #            d['dG0_f'],
            #            d['dG0_f_units'],
            #            d['temperature'],
            #            d['temperature_units'],
            #            d['ionic_strength'],
            #            d['ionic_strength_units'],
            #            d['pH'],
            #            d['pH_units'],
            #            d['used_'],
            #            d['comment_']);
            #        self.session.add(data_add);
            #    except SQLAlchemyError as e:
            #        print(e);
            for k,v in data_I.iteritems():
                for d in v:
                    try:
                        data_add = data_stage03_quantification_dG0_f(d['source'],
                            None,
                            None,
                            k,
                            d['priority'],
                            d['dG0_f'],
                            d['dG0_f_var'],
                            d['dG0_f_units'],
                            298.15,
                            'K',
                            0.0,
                            'M',
                            0.0,
                            None,
                            True,
                            None);
                        self.session.add(data_add);
                    except SQLAlchemyError as e:
                        print(e);
            self.session.commit();

    def import_dataStage03dG0f_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03dG0f(data.data);
        data.clear_data();

    def update_dataStage03dG0f(self,data_I):
        #Not yet tested
        '''update rows of data_stage03_quantification_dG0_f'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_dG0_f).filter(
                            data_stage03_quantification_dG0_f.id.like(d['id'])).update(
                            {'reference_id':d['reference_id'],
                            'met_name':d['met_name'],
                            'met_id':d['met_id'],
                            'KEGG_id':d['KEGG_id'],
                            'priority':d['priority'],
                            'dG0_f':d['dG0_f'],
                            'dG0_f_var':d['dG0_f_var'],
                            'dG0_f_units':d['dG0_f_units'],
                            'temperature':d['temperature'],
                            'temperature_units':d['temperature_units'],
                            'ionic_strength':d['ionic_strength'],
                            'ionic_strength_units':d['ionic_strength_units'],
                            'pH':d['pH'],
                            'pH_units':d['pH_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03tcc_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03tcc(data.data);
        data.clear_data();

    def add_dataStage03tcc(self, data_I):
        '''add rows of data_stage03_quantification_tcc'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage03_quantification_tcc(d['experiment_id'],
                    d['model_id'],
                    d['sample_name_abbreviation'],
                    d['time_point'],
                    d['rxn_id'],
                    d['feasible'],
                    d['measured_concentration_coverage_criteria'],
                    d['measured_dG_f_coverage_criteria'],
                    d['measured_concentration_coverage'],
                    d['measured_dG_f_coverage'],
                    d['used_'],
                    d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03tcc_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03tcc(data.data);
        data.clear_data();

    def update_dataStage03tcc(self,data_I):
        #Not yet tested
        '''update rows of data_stage03_quantification_tcc'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_tcc).filter(
                            standards.id.like(d['id'])).update(
                            {'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'rxn_id':d['rxn_id'],
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

    def import_dataStage03dGp_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03dGp(data.data);
        data.clear_data();

    def add_dataStage03dGp(self, data_I):
        '''add rows of data_stage03_quantification_dG_p'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage03_quantification_dG_p(d['experiment_id'],
                        d['model_id'],
                        d['sample_name_abbreviation'],
                        d['time_point'],
                        d['pathway_id'],
                        d['dG_p'],
                        d['dG_p_var'],
                        d['dG_p_units'],
                        d['dG_p_lb'],
                        d['dG_p_ub'],
                        d['reactions'],
                        d['stoichiometry'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03dGp_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03dGp(data.data);
        data.clear_data();

    def update_dataStage03dGp(self,data_I):
        #Not yet tested
        '''update rows of data_stage03_quantification_dG_p'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_dG_p).filter(
                            data_stage03_quantification_dG_p.id.like(d['id'])).update(
                            {'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'pathway_id':d['pathway_id'],
                            'dG_p':d['dG_p'],
                            'dG_p_var':d['dG_p_var'],
                            'dG_p_units':d['dG_p_units'],
                            'dG_p_lb':d['dG_p_lb'],
                            'dG_p_ub':d['dG_p_ub'],
                            'reactions':d['reactions'],
                            'stoichiometry':d['stoichiometry'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03metid2keggid_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03metid2keggid(data.data);
        data.clear_data();

    def add_dataStage03metid2keggid(self, data_I):
        '''add rows of data_stage03_quantification_metid2keggid'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage03_quantification_metid2keggid(
                        d['met_id'],
                        d['KEGG_id'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03metid2keggid_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03metid2keggid(data.data);
        data.clear_data();

    def update_dataStage03metid2keggid(self,data_I):
        #Not yet tested
        '''update rows of data_stage03_quantification_metid2keggid'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_metid2keggid).filter(
                            data_stage03_quantification_metid2keggid.id.like(d['id'])).update(
                            {
                            'met_id':d['met_id'],
                            'KEGG_id':d['KEGG_id'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    
    def import_dataStage03QuantificationModel_sbml(self, model_id_I, date_I, model_sbml):
        '''import isotopomer model from file'''
        dataStage03QuantificationModelRxns_data = [];
        dataStage03QuantificationModelMets_data = [];
        dataStage03QuantificationModels_data,\
            dataStage03QuantificationModelRxns_data,\
            dataStage03QuantificationModelMets_data = self._parse_model_sbml(model_id_I, date_I, model_sbml)
        self.add_dataStage03ModelMetabolites(dataStage03QuantificationModelMets_data);
        self.add_dataStage03ModelReactions(dataStage03QuantificationModelRxns_data);
        self.add_dataStage03Models(dataStage03QuantificationModels_data);

    def _parse_model_sbml(self,model_id_I,date_I,filename_I):
        # Read in the sbml file
        cobra_model = create_cobra_model_from_sbml_file(filename_I, print_time=True)
        model_data = [];
        model_data_tmp = {};
        # parse out model metadata
        model_data_tmp['model_id'] = model_id_I;
        model_data_tmp['model_name'] = None;
        model_data_tmp['date'] = date_I;
        model_data_tmp['model_description'] = cobra_model.description;
        with open(filename_I, 'r') as f:
            model_data_tmp['sbml_file'] = f.read();
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
            metabolite_data_tmp['used_'] = True
            metabolite_data_tmp['comment_'] = None;
            metabolite_data.append(metabolite_data_tmp);

        return model_data,reaction_data,metabolite_data

    def import_dataStage03Models_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03Models(data.data);
        data.clear_data();

    def add_dataStage03Models(self, data_I):
        '''add rows of data_stage03_quantification_models'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage03_quantification_models(d['model_id'],
                        d['model_name'],
                        d['model_description'],
                        d['sbml_file'],
                        d['date']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03Models_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03Models(data.data);
        data.clear_data();

    def update_dataStage03Models(self,data_I):
        #Not yet tested
        '''update rows of data_stage03_quantification_models'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_models).filter(
                            data_stage03_quantification_models.id.like(d['id'])).update(
                            {'model_id':d['model_id'],
                            'model_name':d['model_name'],
                            'model_description':d['model_description'],
                            'sbml_file':d['sbml_file'],
                            'date':d['date']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03ModelReactions_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03ModelReactions(data.data);
        data.clear_data();

    def add_dataStage03ModelReactions(self, data_I):
        '''add rows of data_stage03_quantification_modelReactions'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage03_quantification_modelReactions(d['model_id'],
                            d['rxn_id'],
                            d['rxn_name'],
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
                            d['reversibility'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03ModelReactions_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03ModelReactions(data.data);
        data.clear_data();

    def update_dataStage03ModelReactions(self,data_I):
        #Not yet tested
        '''update rows of data_stage03_quantification_modelReactions'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_modelReactions).filter(
                            data_stage03_quantification_modelReactions.id.like(d['id'])).update(
                            {'model_id':d['model_id'],
                                'rxn_id':d['rxn_id'],
                                'rxn_name':d['rxn_name'],
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
                                'reversibility':d['reversibility'],
                                'used_':d['used_'],
                                'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03ModelMetabolites_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03ModelMetabolites(data.data);
        data.clear_data();

    def add_dataStage03ModelMetabolites(self, data_I):
        '''add rows of data_stage03_quantification_modelMetabolites'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage03_quantification_modelMetabolites(d['model_id'],
                        d['met_name'],
                        d['met_id'],
                        d['formula'],
                        d['charge'],
                        d['compartment'],
                        d['bound'],
                        d['constraint_sense'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03ModelMetabolites_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03ModelMetabolites(data.data);
        data.clear_data();

    def update_dataStage03ModelMetabolites(self,data_I):
        '''update rows of data_stage03_quantification_modelMetabolites'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_modelMetabolites).filter(
                            data_stage03_quantification_modelMetabolites.id.like(d['id'])).update(
                            {'model_id':d['model_id'],
                                'met_name':d['met_name'],
                                'met_id':d['met_id'],
                                'formula':d['formula'],
                                'charge':d['charge'],
                                'compartment':d['compartment'],
                                'bound':d['bound'],
                                'constraint_sense':d['constraint_sense'],
                                'used_':d['used_'],
                                'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03Experiment_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03Experiment(data.data);
        data.clear_data();

    def add_dataStage03Experiment(self, data_I):
        '''add rows of data_stage03_quantification_simulation'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage03_quantification_simulation(d['experiment_id'],
                        d['model_id'],
                        d['sample_name_abbreviation'],
                        d['time_point'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03Experiment_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03Experiment(data.data);
        data.clear_data();

    def update_dataStage03Experiment(self,data_I):
        '''update rows of data_stage03_quantification_simulation'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_simulation).filter(
                            data_stage03_quantification_simulation.id.like(d['id'])).update(
                            {'experiment_id':d['experiment_id'],
                            'model_id':d['model_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            'compartment_id':d['compartment_id'],
                            'pH':d['pH'],
                            'temperature':d['temperature'],
                            'temperature_units':d['temperature_units'],
                            'ionic_strength':d['ionic_strength'],
                            'ionic_strength_units':d['ionic_strength_units'],
                            'used_':d['used_'],
                            'comment_I':d['comment_I']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
            
    def import_dataStage03modelPathways_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage03modelPathways(data.data);
        data.clear_data();

    def add_dataStage03modelPathways(self, data_I):
        '''add rows of data_stage03_quantification_modelPathways'''
        if data_I:
            for d in data_I:
                try:
                    d['reactions'] = d['reactions'].replace(' ','');
                    d['reactions'] = d['reactions'].split(',');
                    d['stoichiometry'] = d['stoichiometry'].replace(' ','');
                    d['stoichiometry'] = numpy.array(d['stoichiometry'].split(','));
                    d['stoichiometry'] = [float(x) for x in d['stoichiometry']];
                    data_add = data_stage03_quantification_modelPathways(
                        d['model_id'],
                        d['pathway_id'],
                        d['reactions'],
                        d['stoichiometry'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage03modelPathways_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage03modelPathways(data.data);
        data.clear_data();

    def update_dataStage03modelPathways(self,data_I):
        #Not yet tested
        '''update rows of data_stage03_quantification_modelPathways'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage03_quantification_modelPathways).filter(
                            data_stage03_quantification_modelPathways.id.like(d['id'])).update(
                            {
                            'model_id':d['model_id'],
                            'pathway_id':d['pathway_id'],
                            'reactions':d['reactions'],
                            'stoichiometry':d['stoichiometry'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def export_thermodynamicAnalysis_escher(self,experiment_id_I,model_ids_I=[],
                         model_ids_dict_I={},
                     time_points_I=[],
                     sample_name_abbreviations_I=[],
                     measured_concentration_coverage_criteria_I=0.49,
                     measured_dG_f_coverage_criteria_I=0.99,
                     filename=['visualization/data/','/quantification/metabolicmap/','thermodynamics/']):
        '''export concentration and dG_r data for visualization'''
        
        # get the model ids:
        filter_O = {};
        filter_O['model_id'] = [];
        filter_O['time_point'] = [];
        filter_O['sample'] = [];
        filter_O['map_id'] = [];
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage03_quantification_query.get_modelID_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
        for model_id in model_ids:
            filter_mi_str = 'model_id/'+ model_id;
            filter_O['model_id'].append(filter_mi_str);
            print 'exporting thermodynamic analysis for model_id ' + model_id;
            # get the cobra model
            if model_ids_dict_I:
                cobra_model = model_ids_dict_I[model_id];
            else:
                cobra_model_sbml = None;
                cobra_model_sbml = self.stage03_quantification_query.get_row_modelID_dataStage03QuantificationModels(model_id);
                # write the model to a temporary file
                with open('data/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['sbml_file']);
                # Read in the sbml file and define the model conditions
                cobra_model = create_cobra_model_from_sbml_file('data/cobra_model_tmp.xml', print_time=True);
            # get the time-points
            if time_points_I:
                time_points = time_points_I;
            else:
                time_points = [];
                time_points = self.stage03_quantification_query.get_timePoints_experimentIDAndModelID_dataStage03QuantificationSimulation(experiment_id_I,model_id);
            for tp in time_points:
                filter_tp_str = 'model_id/'+ model_id +'/time_point/'+tp;
                filter_O['time_point'].append(filter_tp_str);
                print 'exporting thermodynamic analysis for time_point ' + tp;
                # get sample_name_abbreviations
                if sample_name_abbreviations_I:
                    sample_name_abbreviations = sample_name_abbreviations_I;
                else:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.stage03_quantification_query.get_sampleNameAbbreviations_experimentIDAndModelIDAndTimePoint_dataStage03QuantificationSimulation(experiment_id_I,model_id,tp);
                for sna in sample_name_abbreviations:
                    filter_sna_str = 'model_id/'+ model_id +'/time_point/'+tp+'/sample/'+sna;
                    filter_O['sample'].append(filter_sna_str);
                    print 'exporting thermodynamic analysis for sample_name_abbreviation ' + sna;
                    # get metabolomicsData
                    #concentrations_lbub = [];
                    #concentrations_lbub = self.stage03_quantification_query.get_rowsEscherLbUb_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationMetabolomicsData(experiment_id_I,tp,sna);
                    concentrations = {};
                    concentrations = self.stage03_quantification_query.get_rowsEscher_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationMetabolomicsData(experiment_id_I,tp,sna);
                    # get dGr
                    #dG_r_lbub = [];
                    #dG_r_lbub = self.stage03_quantification_query.get_rowsEscherDGrLbUb_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDGr(experiment_id_I,model_id,tp,sna,measured_concentration_coverage_criteria_I,measured_dG_f_coverage_criteria_I);
                    dG_r = {};
                    dG_r = self.stage03_quantification_query.get_rowsEscherDGr_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDGr(experiment_id_I,model_id,tp,sna,measured_concentration_coverage_criteria_I,measured_dG_f_coverage_criteria_I);
                    for map_id in ['Alternate Carbon Metabolism',\
                        'Amino Acid Metabolism',\
                        'Central Metabolism',\
                        'Cofactor Biosynthesis',\
                        'Inorganic Ion Metabolism',\
                        'Nucleotide Metabolism']:
                        filter_map_str = 'model_id/'+ model_id +'/time_point/'+tp+'/sample/'+sna+'/map_id/'+map_id;
                        filter_O['map_id'].append(filter_map_str);
                        print 'exporting thermodynamic analysis for map_id ' + map_id;
                        # generate the map html using escher
                        map_json = json.load(open('data/escher_maps/' + map_id + '.json','rb'));
                        #map = Builder(map_json=, metabolite_data=concentrations_lbub, reaction_data=dG_r_lbub)
                        map = Builder(map_json=json.dumps(map_json), metabolite_data=concentrations, reaction_data=dG_r);
                        #html_file = map._get_html(scroll_behavior='zoom')
                        html_file = map._get_html(menu='all')
                        filename_str = filename[0] + experiment_id_I + filename[1] + filename[2] + model_id + '_' + tp + '_' + sna + '_' + map_id + '.html';
                        with open(filename_str,'w') as file:
                            file.write(html_file);
        # dump the filter data to a json file
        json_str = 'var ' + 'data_filter' + ' = ' + json.dumps(filter_O);
        filename_str = filename[0] + experiment_id_I + filename[1] + filename[2] + 'filter.js'
        with open(filename_str,'w') as file:
            file.write(json_str);

    def export_thermodynamicAnalysisComparison_escher(self,experiment_id_I,sample_name_abbreviation_base,
                    model_ids_I=[],
                    model_ids_dict_I={},
                     time_points_I=[],
                     sample_name_abbreviations_I=[],
                     measured_concentration_coverage_criteria_I=0.49,
                     measured_dG_f_coverage_criteria_I=0.99,
                     filename=['visualization/data/','/quantification/metabolicmap/','thermodynamics/']):
        '''export concentration and dG_r data for visualization'''
        
        # get the model ids:
        filter_O = {};
        filter_O['model_id'] = [];
        filter_O['time_point'] = [];
        filter_O['sample'] = [];
        filter_O['map_id'] = [];
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage03_quantification_query.get_modelID_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
        for model_id in model_ids:
            filter_mi_str = 'model_id/'+ model_id;
            filter_O['model_id'].append(filter_mi_str);
            print 'exporting thermodynamic analysis for model_id ' + model_id;
            # get the cobra model
            if model_ids_dict_I:
                cobra_model = model_ids_dict_I[model_id];
            else:
                cobra_model_sbml = None;
                cobra_model_sbml = self.stage03_quantification_query.get_row_modelID_dataStage03QuantificationModels(model_id);
                # write the model to a temporary file
                with open('data/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['sbml_file']);
                # Read in the sbml file and define the model conditions
                cobra_model = create_cobra_model_from_sbml_file('data/cobra_model_tmp.xml', print_time=True);
            # get the time-points
            if time_points_I:
                time_points = time_points_I;
            else:
                time_points = [];
                time_points = self.stage03_quantification_query.get_timePoints_experimentIDAndModelID_dataStage03QuantificationSimulation(experiment_id_I,model_id);
            for tp in time_points:
                filter_tp_str = 'model_id/'+ model_id +'/time_point/'+tp;
                filter_O['time_point'].append(filter_tp_str);
                print 'exporting thermodynamic analysis for time_point ' + tp;
                # get sample_name_abbreviations
                if sample_name_abbreviations_I:
                    sample_name_abbreviations = sample_name_abbreviations_I;
                else:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.stage03_quantification_query.get_sampleNameAbbreviations_experimentIDAndModelIDAndTimePoint_dataStage03QuantificationSimulation(experiment_id_I,model_id,tp);
                sample_name_abbreviations = [sna for sna in sample_name_abbreviations if sna !=sample_name_abbreviation_base]
                # get information about the sample to be compared
                # get metabolomicsData
                concentrations_base = {};
                concentrations_base = self.stage03_quantification_query.get_rowsEscher_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationMetabolomicsData(experiment_id_I,tp,sample_name_abbreviation_base);
                # get dGr
                dG_r_base = {};
                dG_r_base = self.stage03_quantification_query.get_rowsEscherDGr_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDGr(experiment_id_I,model_id,tp,sample_name_abbreviation_base,measured_concentration_coverage_criteria_I,measured_dG_f_coverage_criteria_I);

                for sna in sample_name_abbreviations:
                    filter_sna_str = 'model_id/'+ model_id +'/time_point/'+tp+'/sample/'+sample_name_abbreviation_base+'_vs_'+sna;
                    filter_O['sample'].append(filter_sna_str);
                    print 'exporting thermodynamic analysis for sample_name_abbreviation ' + sample_name_abbreviation_base+'_vs_'+sna;
                    # get metabolomicsData
                    #concentrations_lbub = [];
                    #concentrations_lbub = self.stage03_quantification_query.get_rowsEscherLbUb_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationMetabolomicsData(experiment_id_I,tp,sna);
                    concentrations = {};
                    concentrations = self.stage03_quantification_query.get_rowsEscher_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationMetabolomicsData(experiment_id_I,tp,sna);
                    # get dGr
                    #dG_r_lbub = [];
                    #dG_r_lbub = self.stage03_quantification_query.get_rowsEscherDGrLbUb_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDGr(experiment_id_I,model_id,tp,sna,measured_concentration_coverage_criteria_I,measured_dG_f_coverage_criteria_I);
                    dG_r = {};
                    dG_r = self.stage03_quantification_query.get_rowsEscherDGr_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationDGr(experiment_id_I,model_id,tp,sna,measured_concentration_coverage_criteria_I,measured_dG_f_coverage_criteria_I);
                    # make the data structure
                    concentrations_diff = [concentrations_base,concentrations];
                    dG_r_diff = [dG_r_base,dG_r];
                    for map_id in ['Alternate Carbon Metabolism',\
                        'Amino Acid Metabolism',\
                        'Central Metabolism',\
                        'Cofactor Biosynthesis',\
                        'Inorganic Ion Metabolism',\
                        'Nucleotide Metabolism']:
                        filter_map_str = 'model_id/'+ model_id +'/time_point/'+tp+'/sample/'+sample_name_abbreviation_base+'_vs_'+sna+'/map_id/'+map_id;
                        filter_O['map_id'].append(filter_map_str);
                        print 'exporting thermodynamic analysis for map_id ' + map_id;
                        # generate the map html using escher
                        map_json = json.load(open('data/escher_maps/' + map_id + '.json','rb'));
                        #map = Builder(map_json=, metabolite_data=concentrations_lbub, reaction_data=dG_r_lbub)
                        map = Builder(map_json=json.dumps(map_json), metabolite_data=concentrations_diff, reaction_data=dG_r_diff);
                        #html_file = map._get_html(scroll_behavior='zoom')
                        html_file = map._get_html(menu='all',enable_editing=True)
                        filename_str = filename[0] + experiment_id_I + filename[1] + filename[2] + model_id + '_' + tp + '_' + sample_name_abbreviation_base+'_vs_'+sna + '_' + map_id + '.html';
                        with open(filename_str,'w') as file:
                            file.write(html_file);
        # dump the filter data to a json file
        json_str = 'var ' + 'data_filter' + ' = ' + json.dumps(filter_O);
        filename_str = filename[0] + experiment_id_I + filename[1] + filename[2] + 'filter.js'
        with open(filename_str,'w') as file:
            file.write(json_str);

    def export_thermodynamicAnalysisComparison_csv(self,experiment_id_I,sample_name_abbreviation_base,
                    model_ids_I=[],
                    model_ids_dict_I={},
                     time_points_I=[],
                     sample_name_abbreviations_I=[],
                     measured_concentration_coverage_criteria_I=0.5,
                     measured_dG_f_coverage_criteria_I=0.99,
                     filename=['data/_output/','tacomparison.csv']):
        '''export concentration and dG_r data for visualization'''
        
        # get the model ids:
        data_O = [];
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage03_quantification_query.get_modelID_experimentID_dataStage03QuantificationSimulation(experiment_id_I);
        for model_id in model_ids:
            print 'exporting thermodynamic analysis for model_id ' + model_id;
            # get the cobra model
            if model_ids_dict_I:
                cobra_model = model_ids_dict_I[model_id];
            else:
                cobra_model_sbml = None;
                cobra_model_sbml = self.stage03_quantification_query.get_row_modelID_dataStage03QuantificationModels(model_id);
                # write the model to a temporary file
                with open('data/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['sbml_file']);
                # Read in the sbml file and define the model conditions
                cobra_model = create_cobra_model_from_sbml_file('data/cobra_model_tmp.xml', print_time=True);
            # get the time-points
            if time_points_I:
                time_points = time_points_I;
            else:
                time_points = [];
                time_points = self.stage03_quantification_query.get_timePoints_experimentIDAndModelID_dataStage03QuantificationSimulation(experiment_id_I,model_id);
            for tp in time_points:
                print 'exporting thermodynamic analysis for time_point ' + tp;
                # get sample_name_abbreviations
                if sample_name_abbreviations_I:
                    sample_name_abbreviations = sample_name_abbreviations_I;
                else:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.stage03_quantification_query.get_sampleNameAbbreviations_experimentIDAndModelIDAndTimePoint_dataStage03QuantificationSimulation(experiment_id_I,model_id,tp);
                sample_name_abbreviations = [sna for sna in sample_name_abbreviations if sna !=sample_name_abbreviation_base]
                # get information about the sample to be compared
                concentrations_base = {};
                concentrations_base = self.stage03_quantification_query.get_rowsEscher_experimentIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationMetabolomicsData(experiment_id_I,tp,sample_name_abbreviation_base);
                # get tcc
                tcc_base = [];
                tcc_base = self.stage03_quantification_query.get_rows_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationTCC(experiment_id_I,model_id,tp,sample_name_abbreviation_base,measured_concentration_coverage_criteria_I,measured_dG_f_coverage_criteria_I);
                for sna in sample_name_abbreviations:
                    print 'exporting thermodynamic analysis for sample_name_abbreviation ' + sample_name_abbreviation_base+'_vs_'+sna;
                    for tcc_b in tcc_base:
                        # get tcc
                        tcc = {};
                        tcc = self.stage03_quantification_query.get_row_experimentIDAndModelIDAndTimePointAndSampleNameAbbreviations_dataStage03QuantificationTCC(experiment_id_I,model_id,tp,sna,tcc_b['rxn_id'],tcc_b['dG_r_lb'],tcc_b['dG_r_ub'],measured_concentration_coverage_criteria_I,measured_dG_f_coverage_criteria_I);
                        # record data
                        if tcc:
                            data_O.append({'experiment_id':experiment_id_I,
                            'model_id':model_id,
                            'sample_name_abbreviation':sna,
                            'time_point':tp,
                            'rxn_id':tcc['rxn_id'],
                            'dG_r_units':tcc['dG_r_units'],
                            'dG_r_lb_base':tcc_b['dG_r_lb'],
                            'dG_r_lb':tcc['dG_r_lb'],
                            'dG_r_ub_base':tcc_b['dG_r_ub'],
                            'dG_r_ub':tcc['dG_r_ub'],
                            'displacement_lb_base':tcc_b['displacement_lb'],
                            'displacement_lb':tcc['displacement_lb'],
                            'displacement_ub_base':tcc_b['displacement_ub'],
                            'displacement_ub':tcc['displacement_ub'],
                            'feasible_base':tcc_b['feasible'],
                            'feasible':tcc['feasible']});
        # write data to csv
        headers = ['experiment_id',
                            'model_id',
                            'sample_name_abbreviation',
                            'time_point',
                            'rxn_id',
                            'dG_r_units',
                            'dG_r_lb_base',
                            'dG_r_lb',
                            'dG_r_ub_base',
                            'dG_r_ub',
                            'displacement_lb_base',
                            'displacement_lb',
                            'displacement_ub_base',
                            'displacement_ub',
                            'feasible_base',
                            'feasible']
        io = base_exportData(data_O);
        filename_str = filename[0] + experiment_id_I + filename[1];
        io.write_dict2csv(filename_str,headers);
                    