from analysis.analysis_base import *

class stage00_query(base_analysis):
    def get_structureFile_standards(self,met_id_I):
        '''Querry structure file and extension from metabolomics standards'''
        try:
            structure = self.session.query(standards.structure_file,
                    standards.structure_file_extention).filter(
                    standards.met_id.like(met_id_I)).all();
            struct_file_O = '';
            struct_file_ext_O = '';
            if structure:
                struct_file_O = structure[0][0];
                struct_file_ext_O = structure[0][1];
            else: 
                print('no structure file found for ' + met_id_I);
                exit(-1);
            return struct_file_O, struct_file_ext_O
        except SQLAlchemyError as e:
            print(e);

    def get_exactMassAndFormula_standards(self,met_id_I):
        '''Querry exact mass and formula from metabolomics standards'''
        try:
            massformula = self.session.query(standards.exactmass,
                    standards.formula).filter(
                    standards.met_id.like(met_id_I)).all();
            mass_O = '';
            formula_O = '';
            if massformula:
                mass_O = massformula[0][0];
                formula_O = massformula[0][1];
            else: 
                print('no mass and formula found for ' + met_id_I);
                exit(-1);
            return mass_O, formula_O
        except SQLAlchemyError as e:
            print(e);

    def get_Q1AndQ3MassAndMode_MSComponents(self,met_id_I):
        '''Querry q1 mass, q3 mass, and ms_mode from ms_components'''
        try:
            mscomponents = self.session.query(MS_components.q1_mass,
                    MS_components.q3_mass,
                    MS_components.ms_mode).filter(
                    MS_components.met_id.like(met_id_I)).order_by(
                    MS_components.ms_mode.asc(),
                    MS_components.q1_mass.asc(),
                    MS_components.q3_mass.asc()).all();
            mscomponents_O = [];
            for msc in mscomponents: 
                mscomponents_1 = {};
                mscomponents_1['met_id'] = met_id_I;
                mscomponents_1['q1_mass'] = msc.q1_mass;
                mscomponents_1['q3_mass'] = msc.q3_mass;
                mscomponents_1['ms_mode'] = msc.ms_mode;
                mscomponents_O.append(mscomponents_1);
            return mscomponents_O;
        except SQLAlchemyError as e:
            print(e);

    def get_row_MSComponents(self,met_id_I,ms_mode_I,ms_methodtype_I):
        '''Querry row from ms_components by met_id, ms_mode, and ms_methodtype'''
        try:
            mscomponents = self.session.query(MS_components.q1_mass,MS_components.q3_mass,
                    MS_components.ms3_mass,MS_components.met_name,MS_components.dp,
                    MS_components.ep,MS_components.ce,MS_components.cxp,MS_components.af,
                    MS_components.quantifier,MS_components.ms_mode,MS_components.ion_intensity_rank,
                    MS_components.ion_abundance,MS_components.precursor_formula,
                    MS_components.product_ion_reference,MS_components.product_formula,
                    MS_components.production_ion_notes,MS_components.met_id,
                    MS_components.external_reference,MS_components.q1_mass_units,
                    MS_components.q3_mass_units,MS_components.ms3_mass_units,
                    MS_components.threshold_units,MS_components.dp_units,
                    MS_components.ep_units,MS_components.ce_units,
                    MS_components.cxp_units,MS_components.af_units,
                    MS_components.ms_group,MS_components.threshold,
                    MS_components.dwell_weight,MS_components.component_name,
                    MS_components.ms_include,MS_components.ms_is,MS_components.precursor_fragment,
                    MS_components.product_fragment,MS_components.precursor_exactmass,
                    MS_components.product_exactmass,MS_components.ms_methodtype).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.ms_mode.like(ms_mode_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I)).all();
            mscomponents_O = [];
            if not mscomponents:
                print('bad query for row in ms_components: ')
                print('met_id: ' + met_id_I + ', ms_mode_I: ' + ms_mode_I + ', ms_methodtype_I: ' + ms_methodtype_I);
                exit(-1)
            for msc in mscomponents: 
                mscomponents_1 = {};
                mscomponents_1["q1_mass"] = msc.q1_mass;
                mscomponents_1["q3_mass"] = msc.q3_mass;
                mscomponents_1["ms3_mass"] = msc.ms3_mass;
                mscomponents_1["met_name"] = msc.met_name;
                mscomponents_1["dp"] = msc.dp;
                mscomponents_1["ep"] = msc.ep;
                mscomponents_1["ce"] = msc.ce;
                mscomponents_1["cxp"] = msc.cxp;
                mscomponents_1["af"] = msc.af;
                mscomponents_1["quantifier"] = msc.quantifier;
                mscomponents_1["ms_mode"] = msc.ms_mode;
                mscomponents_1["ion_intensity_rank"] = msc.ion_intensity_rank;
                mscomponents_1["ion_abundance"] = msc.ion_abundance;
                mscomponents_1["precursor_formula"] = msc.precursor_formula;
                mscomponents_1["product_ion_reference"] = msc.product_ion_reference;
                mscomponents_1["product_formula"] = msc.product_formula;
                mscomponents_1["production_ion_notes"] = msc.production_ion_notes;
                mscomponents_1["met_id"] = msc.met_id;
                mscomponents_1["external_reference"] = msc.external_reference;
                mscomponents_1["q1_mass_units"] = msc.q1_mass_units;
                mscomponents_1["q3_mass_units"] = msc.q3_mass_units;
                mscomponents_1["ms3_mass_units"] = msc.ms3_mass_units;
                mscomponents_1["threshold_units"] = msc.threshold_units;
                mscomponents_1["dp_units"] = msc.dp_units;
                mscomponents_1["ep_units"] = msc.ep_units;
                mscomponents_1["ce_units"] = msc.ce_units;
                mscomponents_1["cxp_units"] = msc.cxp_units;
                mscomponents_1["af_units"] = msc.af_units;
                mscomponents_1["ms_group"] = msc.ms_group;
                mscomponents_1["threshold"] = msc.threshold;
                mscomponents_1["dwell_weight"] = msc.dwell_weight;
                mscomponents_1["component_name"] = msc.component_name;
                mscomponents_1["ms_include"] = msc.ms_include;
                mscomponents_1["ms_is"] = msc.ms_is;
                mscomponents_1["precursor_fragment"] = msc.precursor_fragment;
                mscomponents_1["product_fragment"] = msc.product_fragment;
                mscomponents_1["precursor_exactmass"] = msc.precursor_exactmass;
                mscomponents_1["product_exactmass"] = msc.product_exactmass;
                mscomponents_1["ms_methodtype"] = msc.ms_methodtype;
                mscomponents_O.append(mscomponents_1);
            return mscomponents_O;
        except SQLAlchemyError as e:
            print(e);

    def get_row_MSComponents_metIDAndFormula(self,met_id_I,precursor_formula_I,
                                             product_formula_I,ms_methodtype_I):
        '''Querry row from ms_components by met_id, precursor_formula, product_formula'''
        try:
            mscomponents = self.session.query(MS_components.q1_mass,MS_components.q3_mass,
                    MS_components.ms3_mass,MS_components.met_name,MS_components.dp,
                    MS_components.ep,MS_components.ce,MS_components.cxp,MS_components.af,
                    MS_components.quantifier,MS_components.ms_mode,MS_components.ion_intensity_rank,
                    MS_components.ion_abundance,MS_components.precursor_formula,
                    MS_components.product_ion_reference,MS_components.product_formula,
                    MS_components.production_ion_notes,MS_components.met_id,
                    MS_components.external_reference,MS_components.q1_mass_units,
                    MS_components.q3_mass_units,MS_components.ms3_mass_units,
                    MS_components.threshold_units,MS_components.dp_units,
                    MS_components.ep_units,MS_components.ce_units,
                    MS_components.cxp_units,MS_components.af_units,
                    MS_components.ms_group,MS_components.threshold,
                    MS_components.dwell_weight,MS_components.component_name,
                    MS_components.ms_include,MS_components.ms_is,MS_components.precursor_fragment,
                    MS_components.product_fragment,MS_components.precursor_exactmass,
                    MS_components.product_exactmass,MS_components.ms_methodtype).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.precursor_formula.like(precursor_formula_I),
                    MS_components.product_formula.like(product_formula_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I)).all();
            mscomponents_O = [];
            if not mscomponents:
                print('bad query for row in ms_components: ')
                print('met_id: ' + met_id_I + ', precursor_formula_I: ' + precursor_formula_I + ', product_formula_I: ' + product_formula_I + ', ms_methodtype_I: ' + ms_methodtype_I);
                exit(-1)
            for msc in mscomponents: 
                mscomponents_1 = {};
                mscomponents_1["q1_mass"] = msc.q1_mass;
                mscomponents_1["q3_mass"] = msc.q3_mass;
                mscomponents_1["ms3_mass"] = msc.ms3_mass;
                mscomponents_1["met_name"] = msc.met_name;
                mscomponents_1["dp"] = msc.dp;
                mscomponents_1["ep"] = msc.ep;
                mscomponents_1["ce"] = msc.ce;
                mscomponents_1["cxp"] = msc.cxp;
                mscomponents_1["af"] = msc.af;
                mscomponents_1["quantifier"] = msc.quantifier;
                mscomponents_1["ms_mode"] = msc.ms_mode;
                mscomponents_1["ion_intensity_rank"] = msc.ion_intensity_rank;
                mscomponents_1["ion_abundance"] = msc.ion_abundance;
                mscomponents_1["precursor_formula"] = msc.precursor_formula;
                mscomponents_1["product_ion_reference"] = msc.product_ion_reference;
                mscomponents_1["product_formula"] = msc.product_formula;
                mscomponents_1["production_ion_notes"] = msc.production_ion_notes;
                mscomponents_1["met_id"] = msc.met_id;
                mscomponents_1["external_reference"] = msc.external_reference;
                mscomponents_1["q1_mass_units"] = msc.q1_mass_units;
                mscomponents_1["q3_mass_units"] = msc.q3_mass_units;
                mscomponents_1["ms3_mass_units"] = msc.ms3_mass_units;
                mscomponents_1["threshold_units"] = msc.threshold_units;
                mscomponents_1["dp_units"] = msc.dp_units;
                mscomponents_1["ep_units"] = msc.ep_units;
                mscomponents_1["ce_units"] = msc.ce_units;
                mscomponents_1["cxp_units"] = msc.cxp_units;
                mscomponents_1["af_units"] = msc.af_units;
                mscomponents_1["ms_group"] = msc.ms_group;
                mscomponents_1["threshold"] = msc.threshold;
                mscomponents_1["dwell_weight"] = msc.dwell_weight;
                mscomponents_1["component_name"] = msc.component_name;
                mscomponents_1["ms_include"] = msc.ms_include;
                mscomponents_1["ms_is"] = msc.ms_is;
                mscomponents_1["precursor_fragment"] = msc.precursor_fragment;
                mscomponents_1["product_fragment"] = msc.product_fragment;
                mscomponents_1["precursor_exactmass"] = msc.precursor_exactmass;
                mscomponents_1["product_exactmass"] = msc.product_exactmass;
                mscomponents_1["ms_methodtype"] = msc.ms_methodtype;
                mscomponents_O.append(mscomponents_1);
            return mscomponents_O[0];
        except SQLAlchemyError as e:
            print(e);

    def get_nMaxBioReps_sampleDescription(self,experiment_id_I):
        '''Query the maximum number of biological replicates corresponding to a given experiment'''
        try:
            bioReps = self.session.query(sample_description.sample_replicate).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.istechnical != True).group_by(
                    sample_description.sample_replicate).order_by(
                    sample_description.sample_replicate.desc()).all();
            maxBioReps_O = 0;
            if bioReps:
                maxBioReps_O = max(bioReps[0]);
            else: 
                print('no biological replicates found for experiment ' + experiment_id_I);
                exit(-1);
            return maxBioReps_O;
        except SQLAlchemyError as e:
            print(e);

    def get_batchFileInfo_experimentID(self,experiment_id_I,sample_type_I):
        '''Query data from experiment and sample for batch file'''
        try:
            data = self.session.query(experiment.id,
                    sample.sample_name,
                    experiment.acquisition_method_id,
                    sample.sample_dilution,
                    sample.sample_type,
                    sample_description.sample_replicate,
                    sample_description.sample_desc,
                    sample_description.sample_name_abbreviation).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_type.like(sample_type_I),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    experiment.id,
                    sample.sample_name,
                    experiment.acquisition_method_id,
                    sample.sample_dilution,
                    sample.sample_type,
                    sample_description.sample_replicate,
                    sample_description.sample_desc,
                    sample_description.sample_name_abbreviation).order_by(
                    experiment.id.asc(),
                    sample.sample_dilution.desc(),
                    sample_description.sample_name_abbreviation.asc(),
                    #sample.sample_name.asc(),
                    sample_description.sample_replicate.asc(),
                    sample_description.sample_desc.desc()).all();
            #.order_by(
            #        experiment.id.asc(),
            #        sample.sample_dilution.desc(),
            #        sample_description.sample_replicate.asc(),
            #        sample_description.sample_desc.desc(),
            #        sample.sample_name.asc()).all();
            data_O = [];
            if data:
                for d in data:
                    data_tmp = {};
                    data_tmp['id']=d.id;
                    data_tmp['sample_name']=d.sample_name;
                    data_tmp['sample_type']=d.sample_type;
                    data_tmp['acquisition_method_id']=d.acquisition_method_id;
                    data_tmp['sample_dilution']=d.sample_dilution;
                    data_tmp['sample_replicate']=d.sample_replicate;
                    data_O.append(data_tmp);
            else: 
                print('no data found for experiment ' + experiment_id_I + ' and sample_type' + sample_type_I);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_batchFileInfo_experimentIDAndExpType(self,experiment_id_I,sample_type_I,exp_type_I):
        '''Query data from experiment and sample for batch file'''
        try:
            data = self.session.query(experiment.id,
                    sample.sample_name,
                    experiment.acquisition_method_id,
                    sample.sample_dilution,
                    sample.sample_type,
                    sample_description.sample_replicate,
                    sample_description.sample_desc,
                    sample_description.sample_name_abbreviation).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id==exp_type_I,
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_type.like(sample_type_I),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    experiment.id,
                    sample.sample_name,
                    experiment.acquisition_method_id,
                    sample.sample_dilution,
                    sample.sample_type,
                    sample_description.sample_replicate,
                    sample_description.sample_desc,
                    sample_description.sample_name_abbreviation).order_by(
                    experiment.id.asc(),
                    sample.sample_dilution.desc(),
                    sample_description.sample_name_abbreviation.asc(),
                    #sample.sample_name.asc(),
                    sample_description.sample_replicate.asc(),
                    sample_description.sample_desc.desc()).all();
            #.order_by(
            #        experiment.id.asc(),
            #        sample.sample_dilution.desc(),
            #        sample_description.sample_replicate.asc(),
            #        sample_description.sample_desc.desc(),
            #        sample.sample_name.asc()).all();
            data_O = [];
            if data:
                for d in data:
                    data_tmp = {};
                    data_tmp['id']=d.id;
                    data_tmp['sample_name']=d.sample_name;
                    data_tmp['sample_type']=d.sample_type;
                    data_tmp['acquisition_method_id']=d.acquisition_method_id;
                    data_tmp['sample_dilution']=d.sample_dilution;
                    data_tmp['sample_replicate']=d.sample_replicate;
                    data_O.append(data_tmp);
            else: 
                print('no data found for experiment ' + experiment_id_I + ' and sample_type' + sample_type_I);
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    def delete_sample_experimentIDAndSampleID_experiment(self,dataListDelete_I):
        '''Delete specific samples from an experiment by their sample ID from experiment'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(experiment).filter(
                        experiment.id.like(d['experiment_id']),
                        sample.sample_id.like(d['sample_id']),
                        experiment.sample_name.like(sample.sample_name)).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def delete_sample_experimentIDAndSampleID_sample(self,dataListDelete_I):
        '''Delete specific samples from an experiment by their sample ID from sample'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(sample).filter(
                        experiment.id.like(d['experiment_id']),
                        sample.sample_id.like(d['sample_id']),
                        experiment.sample_name.like(sample.sample_name)).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def delete_sample_experimentIDAndSampleID_sampleDescription(self,dataListDelete_I):
        '''Delete specific samples from an experiment by their sample ID from sample_description'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(sample_description).filter(
                        experiment.id.like(d['experiment_id']),
                        sample.sample_id.like(d['sample_id']),
                        experiment.sample_name.like(sample.sample_name),
                        sample_description.sample_id.like(sample.sample_id)).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def delete_sample_experimentIDAndSampleID_sampleStorage(self,dataListDelete_I):
        '''Delete specific samples from an experiment by their sample ID from sample_storage'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(sample_storage).filter(
                        experiment.id.like(d['experiment_id']),
                        sample.sample_id.like(d['sample_id']),
                        experiment.sample_name.like(sample.sample_name),
                        sample_storage.sample_id.like(sample.sample_id)).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def delete_sample_experimentIDAndSampleID_samplePhysiologicalParameters(self,dataListDelete_I):
        '''Delete specific samples from an experiment by their sample ID from sample_physiologicalparameters'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(sample_physiologicalParameters).filter(
                        experiment.id.like(d['experiment_id']),
                        sample.sample_id.like(d['sample_id']),
                        experiment.sample_name.like(sample.sample_name),
                        sample_physiologicalParameters.sample_id.like(sample.sample_id)).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def get_calibratorIDAndLevel_sampleNameAndSampleType_sample(self,sample_name_I,sample_type_I):
        '''Querry calibrator id and level from metabolomics sample'''
        try:
            calibratorInfo = self.session.query(sample.calibrator_id,
                    sample.calibrator_level).filter(
                    sample.sample_name.like(sample_name_I),
                    sample.sample_type.like(sample_type_I)).all();
            id_O = None;
            level_O = None;
            if calibratorInfo:
                id_O = calibratorInfo[0][0];
                level_O = calibratorInfo[0][1];
            else: 
                print('no calibrator id nor level found for sample_name/sample_type ' + sample_name_I + ' / ' + sample_type_I);
            return id_O, level_O
        except SQLAlchemyError as e:
            print(e);

    def get_calibratorConcentrationAndUnit_metIDAndCalibratorIDAndLevel_calibratorConcentrations(self, met_id_I, calibrator_id_I, calibrator_level_I):
        '''Querry calibrator id and level from metabolomics sample'''
        concentration_O = 0.0;
        unit_O = None;
        # 1. query the calibrator id for the metabolite
        try:
            calibratorID = self.session.query(
                    calibrator2mix.calibrator_id).filter(
                    mix2met_id.met_id.like(met_id_I),
                    mix2met_id.mix_id.like(calibrator2mix.mix_id)).all();
            calibrator_id_O = None;
            if calibratorID:
                calibrator_id_O = calibratorID[0][0];
            else: 
                print('no calibrator ID nor unit found for met_id ' + met_id_I);
        except SQLAlchemyError as e:
            print(e);
        # 2. check if the calibrator id matches
        if calibrator_id_O == calibrator_id_I:
            # 3. query the concentration and units
            try:
                calibratorInfo = self.session.query(
                        calibrator_concentrations.calibrator_concentration,
                        calibrator_concentrations.concentration_units).filter(
                        calibrator_concentrations.met_id.like(met_id_I),
                        calibrator_concentrations.calibrator_level == calibrator_level_I).all();
                if calibratorInfo:
                    concentration_O = calibratorInfo[0][0];
                    unit_O = calibratorInfo[0][1];
                else: 
                    print('no calibrator concentration nor unit found for met_id/calibrator_id/calibrator_level ' + met_id_I + ' / ' + str(calibrator_id_I) + ' / ' + str(calibrator_level_I));
                return concentration_O, unit_O
            except SQLAlchemyError as e:
                print(e);
        else: 
            return concentration_O, unit_O

    def get_acqusitionMethod(self,lc_method_I,ms_mode_I,ms_methodtype_I):
        '''Querry acqusition method (i.e., join tables lc_elution and ms_components)'''
        try:
            mscomponents = self.session.query(MS_components.component_name, 
                    MS_components.met_id, 
                    MS_components.met_name, 
                    MS_components.q1_mass, 
                    MS_components.q3_mass, 
                    MS_components.dp, 
                    MS_components.ep, 
                    MS_components.ce, 
                    MS_components.cxp, 
                    MS_components.precursor_formula, 
                    MS_components.product_formula, 
                    MS_components.quantifier, 
                    MS_components.ms_group, 
                    MS_components.threshold, 
                    MS_components.dwell_weight, 
                    lc_elution.rt, 
                    lc_elution.ms_window, 
                    lc_elution.rt_units, 
                    lc_elution.window_units).filter(
                    lc_elution.lc_method_id.like(lc_method_I),
                    MS_components.ms_mode.like(ms_mode_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.met_id.like(lc_elution.met_id),
                    MS_components.ms_include).group_by( # query only components that are included in the method
                    MS_components.component_name, 
                    MS_components.met_id, 
                    MS_components.met_name, 
                    MS_components.q1_mass, 
                    MS_components.q3_mass, 
                    MS_components.dp, 
                    MS_components.ep, 
                    MS_components.ce, 
                    MS_components.cxp, 
                    MS_components.precursor_formula, 
                    MS_components.product_formula, 
                    MS_components.quantifier, 
                    MS_components.ms_group, 
                    MS_components.threshold, 
                    MS_components.dwell_weight, 
                    lc_elution.rt, 
                    lc_elution.ms_window, 
                    lc_elution.rt_units, 
                    lc_elution.window_units).order_by(
                    lc_elution.rt.asc(),
                    MS_components.component_name.asc()).all();
            mscomponents_O = [];
            if not mscomponents:
                print('bad query for row in ms_components: ')
                print('lc_method_I: ' + lc_method_I + ', ms_mode_I: ' + ms_mode_I + ', ms_methodtype_I: ' + ms_methodtype_I);
                exit(-1)
            for msc in mscomponents: 
                mscomponents_1 = {};
                mscomponents_1["q1_mass"] = msc.q1_mass;
                mscomponents_1["q3_mass"] = msc.q3_mass;
                mscomponents_1["met_name"] = msc.met_name;
                mscomponents_1["dp"] = msc.dp;
                mscomponents_1["ep"] = msc.ep;
                mscomponents_1["ce"] = msc.ce;
                mscomponents_1["cxp"] = msc.cxp;
                mscomponents_1["quantifier"] = msc.quantifier;
                mscomponents_1["met_id"] = msc.met_id;
                mscomponents_1["ms_group"] = msc.ms_group;
                mscomponents_1["threshold"] = msc.threshold;
                mscomponents_1["dwell_weight"] = msc.dwell_weight;
                mscomponents_1["component_name"] = msc.component_name;
                mscomponents_1["rt"] = msc.rt;
                mscomponents_1["ms_window"] = msc.ms_window;
                mscomponents_1["rt_units"] = msc.rt_units;
                mscomponents_1["window_units"] = msc.window_units;
                mscomponents_O.append(mscomponents_1);
            return mscomponents_O;
        except SQLAlchemyError as e:
            print(e);

    def delete_sample_experimentID_experiment(self,dataListDelete_I):
        '''Delete samples from an experiment from experiment'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(experiment).filter(
                        experiment.id.like(d['experiment_id'])).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def delete_sample_experimentID_sample(self,dataListDelete_I):
        '''Delete an experiment from sample'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(sample).filter(
                        experiment.id.like(d['experiment_id']),
                        experiment.sample_name.like(sample.sample_name)).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();
  
    def get_nMaxBioReps_experimentIDAndSampleName_sampleDescription(self,experiment_id_I,sample_name_I):
        '''Query the maximum number of biological replicates corresponding to a given experiment'''
        try:
            bioReps = self.session.query(sample_description.sample_replicate).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample_name_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.istechnical != True).group_by(
                    sample_description.sample_replicate).order_by(
                    sample_description.sample_replicate.desc()).all();
            maxBioReps_O = 0;
            if bioReps:
                maxBioReps_O = max(bioReps[0]);
            else: 
                print('no biological replicates found for experiment ' + experiment_id_I);
                exit(-1);
            return maxBioReps_O;
        except SQLAlchemyError as e:
            print(e);

    def get_nMaxBioReps_experimentIDAndSampleID_sampleDescription(self,experiment_id_I,sample_id_I):
        '''Query the maximum number of biological replicates corresponding to a given experiment'''
        try:
            bioReps = self.session.query(sample_description.sample_replicate).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_desc.like('Broth'),
                    sample_description.istechnical != True).group_by(
                    sample_description.sample_replicate).order_by(
                    sample_description.sample_replicate.desc()).all();
            maxBioReps_O = 0;
            if bioReps:
                maxBioReps_O = max(bioReps[0]);
            else: 
                print('no biological replicates found for experiment ' + experiment_id_I);
                exit(-1);
            return maxBioReps_O;
        except SQLAlchemyError as e:
            print(e);

    def get_nMaxBioReps_experimentIDAndSampleNameAbbreviation_sampleDescription(self,experiment_id_I,sample_name_abbreviation_I):
        '''Query the maximum number of biological replicates corresponding to a given experiment'''
        try:
            bioReps = self.session.query(sample_description.sample_replicate).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.sample_desc.like('Broth')
                    #sample_description.istechnical != True
                    ).group_by(
                    sample_description.sample_replicate).order_by(
                    sample_description.sample_replicate.desc()).all();
            maxBioReps_O = 0;
            if bioReps:
                maxBioReps_O = max(bioReps[0]);
            else: 
                print('no biological replicates found for experiment ' + experiment_id_I);
                exit(-1);
            return maxBioReps_O;
        except SQLAlchemyError as e:
            print(e);

    def get_nMaxBioReps_experimentIDAndSampleNameAbbreviationAndExpType_sampleDescription(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I):
        '''Query the maximum number of biological replicates corresponding to a given experiment'''
        try:
            bioReps = self.session.query(sample_description.sample_replicate).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id==exp_type_I,
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.sample_desc.like('Broth')
                    #sample_description.istechnical != True
                    ).group_by(
                    sample_description.sample_replicate).order_by(
                    sample_description.sample_replicate.desc()).all();
            maxBioReps_O = 0;
            if bioReps:
                maxBioReps_O = max(bioReps[0]);
            else: 
                print('no biological replicates found for experiment ' + experiment_id_I);
                exit(-1);
            return maxBioReps_O;
        except SQLAlchemyError as e:
            print(e);
       
    def get_sampleIDs_experimentID_experiment(self,experiment_id_I):
        '''Querry sample IDs that are used from the experiment'''
        try:
            sample_names = self.session.query(sample.sample_id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name)).group_by(
                    sample.sample_id).order_by(
                    sample.sample_id.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_id);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);

    def get_sampleNameAbbreviation_experimentIDAndSampleID(self,experiment_id_I,sample_id_I):
        '''Querry sample name abbreviation from the experiment'''
        try:
            sample_name_abbreviations = self.session.query(sample_description.sample_name_abbreviation).filter(
                    sample.sample_id.like(sample_id_I),
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = None;
            sample_name_abbreviations_O = sample_name_abbreviations[0][0];
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);

    def get_sampleNameAbbreviation_experimentIDAndSampleName(self,experiment_id_I,sample_name_I):
        '''Querry sample name abbreviation from the experiment'''
        try:
            sample_name_abbreviations = self.session.query(sample_description.sample_name_abbreviation).filter(
                    sample.sample_name.like(sample_name_I),
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = None;
            sample_name_abbreviations_O = sample_name_abbreviations[0][0];
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);

    def get_sampleLabelAndBoxAndPos_experimentIDAndExperimentTypeID_sampleStorage(self,experiment_id_I,exp_type_id_I):
        '''Querry sample name abbreviation from the experiment'''
        try:
            data = self.session.query(sample_storage.sample_id,
                    sample_storage.sample_label,
                    sample_storage.box,
                    sample_storage.pos).filter(
                    experiment.exp_type_id == exp_type_id_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_storage.sample_id)).group_by(
                    sample_storage.sample_id,
                    sample_storage.sample_label,
                    sample_storage.box,
                    sample_storage.pos).order_by(
                    sample_storage.sample_id.asc()).all();
            sampleStorage_O = [];
            if data:
                for d in data:
                    sampleStorage_O.append({'sample_id':d.sample_id,
                    'sample_label':d.sample_label,
                    'box':d.box,
                    'pos':d.pos});
            return sampleStorage_O;
        except SQLAlchemyError as e:
            print(e);