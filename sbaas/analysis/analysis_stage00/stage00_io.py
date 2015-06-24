from sbaas.analysis.analysis_base import *
from .stage00_query import stage00_query
from sqlalchemy.exc import IntegrityError

class stage00_io(base_analysis):

    def import_standards_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_standards(data.data);
        data.clear_data();

    def add_standards(self, data_I):
        '''add rows of metabolomics_standard'''
        if data_I:
            for d in data_I:
                try:
                    data_add = standards(d['met_id'],
                            d['met_name'],
                            d['formula'],
                            d['hmdb'],
                            d['solubility'],
                            d['solubility_units'],
                            d['mass'],
                            d['cas_number'],
                            d['keggid'],
                            d['structure_file'],
                            d['structure_file_extention']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_standards_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_standards(data.data);
        data.clear_data();

    def update_standards(self,data_I):
        '''update rows of standards'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(standards).filter(
                            standards.met_id.like(d['met_id'])).update(
                            {'met_id':d['met_id'],
                            'met_name':d['met_name'],
                            'formula':d['formula'],
                            'hmdb':d['hmdb'],
                            'solubility':d['solubility'],
                            'solubility_units':d['solubility_units'],
                            'mass':d['mass'],
                            'cas_number':d['cas_number'],
                            'keggid':d['keggid'],
                            'structure_file':d['structure_file'],
                            'structure_file_extention':d['structure_file_extention']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def update_standards_structureFile(self,data_I):
        '''update rows of standards'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(standards).filter(
                            standards.met_id.like(d['met_id'])).update(
                            {'structure_file':d['structure_file'],
                            'structure_file_extention':d['structure_file_extention']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def update_standards_formulaAndMass(self,data_I):
        '''update rows of standards'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(standards).filter(
                            standards.met_id.like(d['met_id'])).update(
                            {'formula':d['formula'],
                            'mass':d['mass'],
                            'exactmass':d['exactmass']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_standardsOrdering_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_standardsOrdering(data.data);
        data.clear_data();

    def add_standardsOrdering(self, data_I):
        '''add rows of standards_ordering'''
        if data_I:
            for d in data_I:
                try:
                    data_add = standards_ordering(d['met_id'],
                            d['met_name'],
                            d['hillcrest'],
                            d['provider'],
                            d['provider_reference'],
                            d['price'],
                            d['amount'],
                            d['amount_units'],
                            d['purity'],
                            d['mw'],
                            d['notes'],
                            d['powderdate_received'],
                            d['powderdate_opened'],
                            d['order_standard'],
                            d['standards_storage'],
                            d['purchase']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_standardsOrdering_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_standardsOrdering(data.data);
        data.clear_data();

    def update_standardsOrdering(self,data_I):
        '''update rows of standards_ordering'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(standards_ordering).filter(
                           standards_ordering.met_id.like(d['met_id'])).update(
                            {'met_id':d['met_id'],
                            'met_name':d['met_name'],
                            'hillcrest':d['hillcrest'],
                            'provider':d['provider'],
                            'provider_reference':d['provider_reference'],
                            'price':d['price'],
                            'amount':d['amount'],
                            'amount_units':d['amount_units'],
                            'purity':d['purity'],
                            'mw':d['mw'],
                            'notes':d['notes'],
                            'powderdate_received':d['powderdate_received'],
                            'powderdate_opened':d['powderdate_opened'],
                            'order_standard':d['order_standard'],
                            'standards_storage':d['standards_storage'],
                            'purchase':d['purchase']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def update_MSComponents_precursorFormulaAndMass(self,data_I):
        '''update rows of ms_components
        for columns of precursor_formula and precursor_exact_mass'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(MS_components).filter(
                           MS_components.met_id.like(d['met_id']),
                           MS_components.q1_mass == d['q1_mass'],
                           MS_components.q3_mass == d['q3_mass']).update(
                            {'precursor_formula':d['precursor_formula'],
                            'precursor_exactmass':d['precursor_exactmass']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_MSComponents_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_MSComponents(data.data);
        data.clear_data();

    def add_MSComponents(self, data_I):
        '''add rows of ms_components'''
        if data_I:
            for d in data_I:
                try:
                    data_add = MS_components(d['q1_mass'],
                                                    d['q3_mass'],
                                                    d['ms3_mass'],
                                                    d['met_name'],
                                                    d['dp'],
                                                    d['ep'],
                                                    d['ce'],
                                                    d['cxp'],
                                                    d['af'],
                                                    d['quantifier'],
                                                    d['ms_mode'],
                                                    d['ion_intensity_rank'],
                                                    d['ion_abundance'],
                                                    d['precursor_formula'],
                                                    d['product_ion_reference'],
                                                    d['product_formula'],
                                                    d['production_ion_notes'],
                                                    d['met_id'],
                                                    d['external_reference'],
                                                    d['q1_mass_units'],
                                                    d['q3_mass_units'],
                                                    d['ms3_mass_units'],
                                                    d['threshold_units'],
                                                    d['dp_units'],
                                                    d['ep_units'],
                                                    d['ce_units'],
                                                    d['cxp_units'],
                                                    d['af_units'],
                                                    d['ms_group'],
                                                    d['threshold'],
                                                    d['dwell_weight'],
                                                    d['component_name'],
                                                    d['ms_include'],
                                                    d['ms_is'],
                                                    d['precursor_fragment'],
                                                    d['product_fragment'],
                                                    d['precursor_exactmass'],
                                                    d['product_exactmass'],
                                                    d['ms_methodtype'],
                                                    d['precursor_fragment_elements'],
                                                    d['product_fragment_elements']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_oligosStorage_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_oligosStorage(data.data);
        data.clear_data();

    def add_oligosStorage(self, data_I):
        '''add rows of oligos_storage'''
        if data_I:
            for d in data_I:
                try:
                    data_add = oligos_storage(d['oligos_id'],
                                                    d['oligos_label'],
                                                    d['oligos_box'],
                                                    d['oligos_posstart'],
                                                    d['oligos_posend'],
                                                    d['oligos_date'],
                                                    d['oligos_storagebuffer'],
                                                    d['oligos_concentration'],
                                                    d['oligos_concentration_units']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_oligosDescription_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_oligosDescription(data.data);
        data.clear_data();

    def add_oligosDescription(self, data_I):
        '''add rows of oligos_description'''
        if data_I:
            for d in data_I:
                try:
                    data_add = oligos_description(d['oligos_id'],
                                                    d['oligos_sequence'],
                                                    d['oligos_purification'],
                                                    d['oligos_description'],
                                                    d['oligos_notes']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_MSComponentList_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_MSComponentList(data.data);
        data.clear_data();

    def add_MSComponentList(self, data_I):
        '''add rows of ms_component_list'''
        if data_I:
            for d in data_I:
                try:
                    data_add = MS_component_list(d['ms_method_id'],
                                                    d['q1_mass'],
                                                    d['q3_mass'],
                                                    d['met_id'],
                                                    d['component_name'],
                                                    d['ms_methodtype']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_MSMethod_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_MSMethod(data.data);
        data.clear_data();

    def add_MSMethod(self, data_I):
        '''add rows of ms_method'''
        if data_I:
            for d in data_I:
                try:
                    data_add = MS_method(d['id'],
                                         d['ms_sourceparameters_id'],
                                         d['ms_information_id'],
                                         d['ms_experiment_id']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_AcquisitionMethod_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_AcquisitionMethod(data.data);
        data.clear_data();

    def add_AcquisitionMethod(self, data_I):
        '''add rows of acquisition_method'''
        if data_I:
            for d in data_I:
                try:
                    data_add = acquisition_method(d['id'],
                                         d['ms_method_id'],
                                         d['autosampler_method_id'],
                                         d['lc_method_id']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_sampleFile_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        # split into seperate data structures based on the destined table add
        sampleDescription_data = [];
        samplePhysiologicalParameters_data = [];
        sampleStorage_data = [];
        sample_data = [];
        experiment_data = [];
        for d in data.data:
            sampleDescription_data.append({'sample_id':d['sample_id'],
                                        'sample_name_short':d['sample_name_short'],
                                        'sample_name_abbreviation':d['sample_name_abbreviation'],
                                        'sample_date':d['sample_date'],
                                        'time_point':d['time_point'],
                                        'sample_condition':d['sample_condition'],
                                        'extraction_method_id':d['extraction_method_id'],
                                        'biological_material':d['biological_material'],
                                        'sample_desc':d['sample_description'],
                                        'sample_replicate':d['sample_replicate'],
                                        'is_added':d['is_added'],
                                        'is_added_units':d['is_added_units'],
                                        'reconstitution_volume':d['reconstitution_volume'],
                                        'reconstitution_volume_units':d['reconstitution_volume_units'],
                                        #'sample_replicate_biological':d['sample_replicate'],
                                        #'istechnical':False});
                                        'sample_replicate_biological':d['sample_replicate_biological'],
                                        'istechnical':d['istechnical'],
                                        'notes':d['notes']});
            samplePhysiologicalParameters_data.append({'sample_id':d['sample_id'],
                                        'growth_condition_short':d['growth_condition_short'],
                                        'growth_condition_long':d['growth_condition_long'],
                                        'media_short':d['media_short'],
                                        'media_long':d['media_long'],
                                        'isoxic':d['isoxic'],
                                        'temperature':d['temperature'],
                                        'supplementation':d['supplementation'],
                                        'od600':d['od600'],
                                        'vcd':d['vcd'],
                                        'culture_density':d['culture_density'],
                                        'culture_volume_sampled':d['culture_volume_sampled'],
                                        'cells':d['cells'],
                                        'dcw':d['dcw'],
                                        'wcw':d['wcw'],
                                        'vcd_units':d['vcd_units'],
                                        'culture_density_units':d['culture_density_units'],
                                        'culture_volume_sampled_units':d['culture_volume_sampled_units'],
                                        'dcw_units':d['dcw_units'],
                                        'wcw_units':d['wcw_units']});
            sampleStorage_data.append({'sample_id':d['sample_id'],
                                        'sample_label':d['sample_label'],
                                        'ph':d['ph'],
                                        'box':d['box'],
                                        'pos':d['pos']});
            sample_data.append({'sample_name':d['sample_id'],
                                        #'sample_name':d['sample_name'],
                                        'sample_type':d['sample_type'],
                                        #'sample_type':'Unknown',
                                        'calibrator_id':None,
                                        'calibrator_level':None,
                                        #'calibrator_id':d['calibrator_id'],
                                        #'calibrator_level':d['calibrator_level'],
                                        'sample_id':d['sample_id'],
                                        'sample_dilution':1.0});
                                        #'sample_dilution':d['sample_dilution']});
            experiment_data.append({'exp_type_id':d['exp_type_id'],
                                        'id':d['experiment_id'],
                                        'sample_name':d['sample_id'],
                                        #'sample_name':d['sample_name'],
                                        'experimentor_id':d['experimentor_id'],
                                        'extraction_method_id':d['extraction_method_id'],
                                        'acquisition_method_id':d['acquisition_method_id'],
                                        'quantitation_method_id':d['quantitation_method_id'],
                                        'internal_standard_id':d['is_id']});
        # add data to the database:
        self.add_sampleDescription(sampleDescription_data);
        self.add_samplePhysiologicalParameters(samplePhysiologicalParameters_data);
        self.add_sampleStorage(sampleStorage_data);
        self.add_sample(sample_data);
        self.add_experiment(experiment_data);
        # deallocate memory
        data.clear_data();

        return sampleDescription_data,samplePhysiologicalParameters_data,sampleStorage_data,sample_data,experiment_data;

    def import_sampleFile_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        # split into seperate data structures based on the destined table add
        sampleDescription_data = [];
        samplePhysiologicalParameters_data = [];
        sampleStorage_data = [];
        sample_data = [];
        experiment_data = [];
        for d in data.data:
            sampleDescription_data.append({'sample_id':d['sample_id'],
                                        'sample_name_short':d['sample_name_short'],
                                        'sample_name_abbreviation':d['sample_name_abbreviation'],
                                        'sample_date':d['sample_date'],
                                        'time_point':d['time_point'],
                                        'sample_condition':d['sample_condition'],
                                        'extraction_method_id':d['extraction_method_id'],
                                        'biological_material':d['biological_material'],
                                        'sample_desc':d['sample_description'],
                                        'sample_replicate':d['sample_replicate'],
                                        'is_added':d['is_added'],
                                        'is_added_units':d['is_added_units'],
                                        'reconstitution_volume':d['reconstitution_volume'],
                                        'reconstitution_volume_units':d['reconstitution_volume_units'],
                                        #'sample_replicate_biological':d['sample_replicate'],
                                        #'istechnical':False});
                                        'sample_replicate_biological':d['sample_replicate_biological'],
                                        'istechnical':d['istechnical'],
                                        'notes':d['notes']});
            samplePhysiologicalParameters_data.append({'sample_id':d['sample_id'],
                                        'growth_condition_short':d['growth_condition_short'],
                                        'growth_condition_long':d['growth_condition_long'],
                                        'media_short':d['media_short'],
                                        'media_long':d['media_long'],
                                        'isoxic':d['isoxic'],
                                        'temperature':d['temperature'],
                                        'supplementation':d['supplementation'],
                                        'od600':d['od600'],
                                        'vcd':d['vcd'],
                                        'culture_density':d['culture_density'],
                                        'culture_volume_sampled':d['culture_volume_sampled'],
                                        'cells':d['cells'],
                                        'dcw':d['dcw'],
                                        'wcw':d['wcw'],
                                        'vcd_units':d['vcd_units'],
                                        'culture_density_units':d['culture_density_units'],
                                        'culture_volume_sampled_units':d['culture_volume_sampled_units'],
                                        'dcw_units':d['dcw_units'],
                                        'wcw_units':d['wcw_units']});
            sampleStorage_data.append({'sample_id':d['sample_id'],
                                        'sample_label':d['sample_label'],
                                        'ph':d['ph'],
                                        'box':d['box'],
                                        'pos':d['pos']});
            sample_data.append({'sample_name':d['sample_id'],
                                        #'sample_name':d['sample_name'],
                                        'sample_type':d['sample_type'],
                                        #'sample_type':'Unknown',
                                        'calibrator_id':None,
                                        'calibrator_level':None,
                                        #'calibrator_id':d['calibrator_id'],
                                        #'calibrator_level':d['calibrator_level'],
                                        'sample_id':d['sample_id'],
                                        'sample_dilution':1.0});
                                        #'sample_dilution':d['sample_dilution']});
            experiment_data.append({'exp_type_id':d['exp_type_id'],
                                        'id':d['experiment_id'],
                                        'sample_name':d['sample_id'],
                                        #'sample_name':d['sample_name'],
                                        'experimentor_id':d['experimentor_id'],
                                        'extraction_method_id':d['extraction_method_id'],
                                        'acquisition_method_id':d['acquisition_method_id'],
                                        'quantitation_method_id':d['quantitation_method_id'],
                                        'internal_standard_id':d['is_id']});
        # add data to the database:
        self.update_sampleDescription(sampleDescription_data);
        self.update_samplePhysiologicalParameters(samplePhysiologicalParameters_data);
        self.update_sampleStorage(sampleStorage_data);
        self.update_sample(sample_data);
        self.update_experiment(experiment_data);
        # deallocate memory
        data.clear_data();

        return sampleDescription_data,samplePhysiologicalParameters_data,sampleStorage_data,sample_data,experiment_data;

    def add_sample(self, data_I):
        '''add rows of sample'''
        if data_I:
            for d in data_I:
                try:
                    data_add = sample(d['sample_name'],
                            d['sample_type'],
                            d['calibrator_id'],
                            d['calibrator_level'],
                            d['sample_id'],
                            d['sample_dilution']);
                    self.session.add(data_add);
                    self.session.commit();
                except IntegrityError as e:
                    print(e);
                    self.session.rollback();
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    
    def update_sample(self,data_I):
        '''update rows of sample'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(sample).filter(
                            sample.sample_name.like(d['sample_name'])).update(
                            {'sample_type':d['sample_type'],
                            'calibrator_id':d['calibrator_id'],
                            'calibrator_level':d['calibrator_level'],
                            'sample_id':d['sample_id'],
                            'sample_dilution':d['sample_dilution']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_sampleDescription_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_sampleDescription(data.data);
        data.clear_data();

    def add_sampleDescription(self, data_I):
        '''add rows of sample_description'''
        if data_I:
            for d in data_I:
                try:
                    data_add = sample_description(d['sample_id'],
                            d['sample_name_short'],
                            d['sample_name_abbreviation'],
                            d['sample_date'],
                            d['time_point'],
                            d['sample_condition'],
                            d['extraction_method_id'],
                            d['biological_material'],
                            d['sample_desc'],
                            d['sample_replicate'],
                            d['is_added'],
                            d['is_added_units'],
                            d['reconstitution_volume'],
                            d['reconstitution_volume_units'],
                            d['sample_replicate_biological'],
                            d['istechnical'],
                            d['notes']);
                    self.session.add(data_add);
                    self.session.commit();
                except IntegrityError as e:
                    print(e);
                    self.session.rollback();
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_sampleDescription_update(self, filename):
        '''table updates'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_sampleDescription(data.data);
        data.clear_data();
    
    def update_sampleDescription(self,data_I):
        '''update rows of sample_description'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(sample_description).filter(
                            sample_description.sample_id.like(d['sample_id'])).update(
                            {'sample_name_short':d['sample_name_short'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'sample_date':d['sample_date'],
                            'time_point':d['time_point'],
                            'sample_condition':d['sample_condition'],
                            'extraction_method_id':d['extraction_method_id'],
                            'biological_material':d['biological_material'],
                            'sample_desc':d['sample_desc'],
                            'sample_replicate':d['sample_replicate'],
                            'is_added':d['is_added'],
                            'is_added_units':d['is_added_units'],
                            'reconstitution_volume':d['reconstitution_volume'],
                            'reconstitution_volume_units':d['reconstitution_volume_units'],
                            'sample_replicate_biological':d['sample_replicate_biological'],
                            'istechnical':d['istechnical'],
                            'notes':d['notes']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_samplePhysiologicalParameters(self, data_I):
        '''add rows of sample_physiologicalparameters'''
        if data_I:
            for d in data_I:
                try:
                    data_add = sample_physiologicalParameters(d['sample_id'],
                            d['growth_condition_short'],
                            d['growth_condition_long'],
                            d['media_short'],
                            d['media_long'],
                            d['isoxic'],
                            d['temperature'],
                            d['supplementation'],
                            d['od600'],
                            d['vcd'],
                            d['culture_density'],
                            d['culture_volume_sampled'],
                            d['cells'],
                            d['dcw'],
                            d['wcw'],
                            d['vcd_units'],
                            d['culture_density_units'],
                            d['culture_volume_sampled_units'],
                            d['dcw_units'],
                            d['wcw_units']);
                    self.session.add(data_add);
                    self.session.commit();
                except IntegrityError as e:
                    print(e);
                    self.session.rollback();
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_sampleStorage(self, data_I):
        '''add rows of sample_storage'''
        if data_I:
            for d in data_I:
                try:
                    data_add = sample_storage(d['sample_id'],
                            d['sample_label'],
                            d['ph'],
                            d['box'],
                            d['pos']);
                    self.session.add(data_add);
                    self.session.commit();
                except IntegrityError as e:
                    print(e);
                    self.session.rollback();
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_experiment(self, data_I):
        '''add rows of experiment'''
        if data_I:
            for d in data_I:
                try:
                    data_add = experiment(d['exp_type_id'],
                        d['id'],
                        d['sample_name'],
                        d['experimentor_id'],
                        d['extraction_method_id'],
                        d['acquisition_method_id'],
                        d['quantitation_method_id'],
                        d['internal_standard_id']);
                    self.session.add(data_add);
                    self.session.commit();
                except IntegrityError as e:
                    print(e);
                    self.session.rollback();
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def export_batchFile(self, data_I, header_I, filename):
        export = base_exportData(data_I)
        export.write_headersAndElements2txt(header_I,filename)
        return;

    def import_calibrationFile_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        # split into seperate data structures based on the destined table add
        sample_data = [];
        experiment_data = [];
        for d in data.data:
            sample_data.append({'sample_name':d['sample_name'],
                                        'sample_type':d['sample_type'],
                                        'calibrator_id':d['calibrator_id'],
                                        'calibrator_level':d['calibrator_level'],
                                        'sample_id':d['sample_id'],
                                        'sample_dilution':d['sample_dilution']});
            experiment_data.append({'exp_type_id':d['exp_type_id'],
                                        'id':d['experiment_id'],
                                        'sample_name':d['sample_name'],
                                        'experimentor_id':d['experimentor_id'],
                                        'extraction_method_id':d['extraction_method_id'],
                                        'acquisition_method_id':d['acquisition_method_id'],
                                        'quantitation_method_id':d['quantitation_method_id'],
                                        'internal_standard_id':d['is_id']});
        # add data to the database:
        self.add_sample(sample_data);
        self.add_experiment(experiment_data);
        # deallocate memory
        data.clear_data();

    def import_calibration_sampleAndComponents(self, filename):
        '''import calibration curve sample and component information'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        # split into separate data structures
        samplesComponents_data = [];
        for d in data.data:
            samplesComponents_data.append({'sample_name':d['Sample Name'],
                                           'sample_type':d['Sample Type'],
                                           'met_id':d['Component Group Name']});

        data.clear_data();
        return samplesComponents_data;

    def export_calibrationConcentrations(self, data, filename):
        '''export calibration curve concentrations'''

        # write calibration curve concentrations to file
        export = base_exportData(data);
        export.write_dict2csv(filename);

    def import_calibratorConcentrations_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_calibratorConcentrations(data.data);
        data.clear_data();

    def add_calibratorConcentrations(self, data_I):
        '''add rows of calibrator_concentrations'''
        if data_I:
            for d in data_I:
                try:
                    data_add = calibrator_concentrations(d['met_id'],
                                                d['calibrator_level'],
                                                d['dilution_factor'],
                                                d['calibrator_concentration'],
                                                d['concentration_units']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_metabolomicsModels_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_metabolomicsModels(data.data);
        data.clear_data();

    def import_biologicalMaterialGeneReferences_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_biologicalMaterialGeneReferences(data.data);
        data.clear_data();

    def add_biologicalMaterialGeneReferences(self, data_I):
        '''add rows of biologicalMaterial_geneReferences'''
        if data_I:
            for d in data_I:
                try:
                    data_add = biologicalMaterial_geneReferences(d['biologicalmaterial_id'],
                        d['ordered_locus_name'],
                        d['ordered_locus_name2'],
                        d['swissprot_entry_name'],
                        d['ac'],
                        d['ecogene_accession_number'],
                        d['gene_name']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_biologicalMaterialGeneReferences_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_biologicalMaterialGeneReferences(data.data);
        data.clear_data();

    def update_biologicalMaterialGeneReferences(self,data_I):
        '''update rows of biologicalMaterial_geneReferences'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(biologicalMaterial_geneReferences).filter(
                           biologicalMaterial_geneReferences.id==d['id']).update(
                            {'biologicalmaterial_id':d['biologicalmaterial_id'],
                                'ordered_locus_name':d['ordered_locus_name'],
                                'ordered_locus_name2':d['ordered_locus_name2'],
                                'swissprot_entry_name':d['swissprot_entry_name'],
                                'ac':d['ac'],
                                'ecogene_accession_number':d['ecogene_accession_number'],
                                'gene_name':d['gene_name']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_MSComponents_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_MSComponents(data.data);
        data.clear_data();

    def update_MSComponents(self, data_I):
        '''update rows of ms_components'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(MS_components).filter(
                            MS_components.id==d['id']).update(
                            {'q1_mass':d['q1_mass'],
                            'q3_mass':d['q3_mass'],
                            'ms3_mass':d['ms3_mass'],
                            'met_name':d['met_name'],
                            'dp':d['dp'],
                            'ep':d['ep'],
                            'ce':d['ce'],
                            'cxp':d['cxp'],
                            'af':d['af'],
                            'quantifier':d['quantifier'],
                            'ms_mode':d['ms_mode'],
                            'ion_intensity_rank':d['ion_intensity_rank'],
                            'ion_abundance':d['ion_abundance'],
                            'precursor_formula':d['precursor_formula'],
                            'product_ion_reference':d['product_ion_reference'],
                            'product_formula':d['product_formula'],
                            'production_ion_notes':d['production_ion_notes'],
                            'met_id':d['met_id'],
                            'external_reference':d['external_reference'],
                            'q1_mass_units':d['q1_mass_units'],
                            'q3_mass_units':d['q3_mass_units'],
                            'ms3_mass_units':d['ms3_mass_units'],
                            'threshold_units':d['threshold_units'],
                            'dp_units':d['dp_units'],
                            'ep_units':d['ep_units'],
                            'ce_units':d['ce_units'],
                            'cxp_units':d['cxp_units'],
                            'af_units':d['af_units'],
                            'ms_group':d['ms_group'],
                            'threshold':d['threshold'],
                            'dwell_weight':d['dwell_weight'],
                            'component_name':d['component_name'],
                            'ms_include':d['ms_include'],
                            'ms_is':d['ms_is'],
                            'precursor_fragment':d['precursor_fragment'],
                            'product_fragment':d['product_fragment'],
                            'precursor_exactmass':d['precursor_exactmass'],
                            'product_exactmass':d['product_exactmass'],
                            'ms_methodtype':d['ms_methodtype'],
                            'precursor_fragment_elements':d['precursor_fragment_elements'],
                            'product_fragment_elements':d['product_fragment_elements']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    #Need to test:
    def add_metabolomicsModels(self, data_I):
        '''add rows of metabolomics_models'''
        if data_I:
            for d in data_I:
                try:
                    data_add = metabolomics_models(d['model_id'],
                                    d['model_date'],
                                    d['model_file'],
                                    d['model_file_extension']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
            
    def import_modelsAtomMapping_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_modelsAtomMapping(data.data);
        data.clear_data();

    def add_modelsAtomMapping(self, data_I):
        '''add rows of models_atomMapping'''
        if data_I:
            for d in data_I:
                try:
                    data_add = models_atomMapping(d['mapping_id'],
                                d['mapping_date'],
                                d['mapping_description'],
                                d['rxn_id_old'],
                                d['rxn_id'],
                                d['ctrack'],
                                d['mapping'],
                                d['notes']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
            
    def import_modelsLumpedRxns_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_modelsLumpedRxns(data.data);
        data.clear_data();

    def add_modelsLumpedRxns(self, data_I):
        '''add rows of models_lumpedRxns'''
        if data_I:
            for d in data_I:
                try:
                    data_add = models_lumpedRxns(d['lumped_id'],
                                d['lumped_date'],
                                d['lumped_description'],
                                d['rxn_id'],
                                d['reactions'],
                                d['stoichiometry']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
            
    def export_acquisitionMethod(self, data, filename):
        '''export acquisition method'''

        # write acquisition method to file
        export = base_exportData(data);
        export.write_dict2csv(filename);

    def update_samplePhysiologicalParameters(self,data_I):
        '''update rows of sample_physiologicalParameters'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(sample_physiologicalParameters).filter(
                           sample_physiologicalParameters.sample_id==d['sample_id']).update(
                            {
                            'growth_condition_short':d['growth_condition_short'],
                            'growth_condition_long':d['growth_condition_long'],
                            'media_short':d['media_short'],
                            'media_long':d['media_long'],
                            'isoxic':d['isoxic'],
                            'temperature':d['temperature'],
                            'supplementation':d['supplementation'],
                            'od600':d['od600'],
                            'vcd':d['vcd'],
                            'culture_density':d['culture_density'],
                            'culture_volume_sampled':d['culture_volume_sampled'],
                            'cells':d['cells'],
                            'dcw':d['dcw'],
                            'wcw':d['wcw'],
                            'vcd_units':d['vcd_units'],
                            'culture_density_units':d['culture_density_units'],
                            'culture_volume_sampled_units':d['culture_volume_sampled_units'],
                            'dcw_units':d['dcw_units'],
                            'wcw_units':d['wcw_units']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def update_sampleStorage(self,data_I):
        '''update rows of sample_storage'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(sample_storage).filter(
                           sample_storage.sample_id==d['sample_id']).update(
                            {
                            'sample_label':d['sample_label'],
                            'ph':d['ph'],
                            'box':d['box'],
                            'pos':d['pos']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def update_experiment(self,data_I):
        '''update rows of experiment'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(experiment).filter(
                           experiment.sample_name==d['sample_name'],
                           experiment.id==d['id']).update(
                            {#'wid ':d['wid '],
                            'exp_type_id':d['exp_type_id'],
                            #'id':d['id'],
                            #'sample_name':d['sample_name'],
                            'experimentor_id':d['experimentor_id'],
                            'extraction_method_id':d['extraction_method_id'],
                            'acquisition_method_id':d['acquisition_method_id'],
                            'quantitation_method_id':d['quantitation_method_id'],
                            'internal_standard_id':d['internal_standard_id']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();