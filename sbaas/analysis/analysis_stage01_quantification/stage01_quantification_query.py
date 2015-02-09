from analysis.analysis_base import *

class stage01_quantification_query(base_analysis):
    # query sample names from data_stage01_quantification_mqresultstable
    def get_sampleNames_experimentIDAndSampleType(self,experiment_id_I,sample_type_I,exp_type_I=4):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_quantification_MQResultsTable.sample_name).filter(
                    data_stage01_quantification_MQResultsTable.sample_type.like(sample_type_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_quantification_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name)).group_by(
                    data_stage01_quantification_MQResultsTable.sample_name).order_by(
                    data_stage01_quantification_MQResultsTable.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleID(self,experiment_id_I,sample_id_I,exp_type_I=4):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample.sample_name).filter(
                    sample.sample_id.like(sample_id_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_quantification_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name)).group_by(
                    sample.sample_name).order_by(
                    sample.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleIDAndSampleDilution(self,experiment_id_I,sample_id_I,sample_dilution_I,exp_type_I=4):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample.sample_name).filter(
                    sample.sample_id.like(sample_id_I),
                    sample.sample_dilution == sample_dilution_I,
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_quantification_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name)).group_by(
                    sample.sample_name).order_by(
                    sample.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleNameShortAndSampleDescription(self,experiment_id_I,sample_name_short_I,sample_decription_I,exp_type_I=4):
        '''Querry sample names that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample.sample_name).filter(
                    sample_description.sample_name_short.like(sample_name_short_I),
                    sample_description.sample_description.like(sample_decription_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name),
                    data_stage01_quantification_MQResultsTable.used_.is_(True)).group_by(
                    sample.sample_name).order_by(
                    sample.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleNameAbbreviationAndSampleDescription(self,experiment_id_I,sample_name_abbreviation_I,sample_decription_I,exp_type_I=4):
        '''Querry sample names that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample.sample_name).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.sample_description.like(sample_decription_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name),
                    data_stage01_quantification_MQResultsTable.used_.is_(True)).group_by(
                    sample.sample_name).order_by(
                    sample.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleNameAbbreviationAndSampleDilution(self,experiment_id_I,sample_name_abbreviation_I,sample_dilution_I,exp_type_I=4):
        '''Querry sample names that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample.sample_name).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample.sample_dilution == sample_dilution_I,
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name),
                    data_stage01_quantification_MQResultsTable.used_.is_(True)).group_by(
                    sample.sample_name).order_by(
                    sample.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample ids from data_stage01_quantification_mqresultstable
    def get_sampleIDs_experimentIDAndSampleType(self,experiment_id_I,sample_type_I,exp_type_I=4):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_ids = self.session.query(sample.sample_id).filter(
                    data_stage01_quantification_MQResultsTable.sample_type.like(sample_type_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_quantification_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name)).group_by(
                    sample.sample_id).order_by(
                    sample.sample_id.asc()).all();
            sample_ids_O = [];
            for si in sample_ids: sample_ids_O.append(si.sample_id);
            return sample_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleIDs_experimentID(self,experiment_id_I,exp_type_I=4):
        '''Querry sample names that are used from the experiment'''
        try:
            sample_ids = self.session.query(sample.sample_id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_quantification_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name)).group_by(
                    sample.sample_id).order_by(
                    sample.sample_id.asc()).all();
            sample_ids_O = [];
            for si in sample_ids: sample_ids_O.append(si.sample_id);
            return sample_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleID_experimentIDAndSampleName(self,experiment_id_I,sample_name_I,exp_type_I=4):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_id = self.session.query(sample.sample_id).filter(
                    sample.sample_name.like(sample_name_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_quantification_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name)).group_by(
                    sample.sample_id).all();
            sample_id_O = sample_id[0];
            return sample_id_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample name short from data_stage01_quantification_mqresultstable
    def get_sampleNameShort_experimentIDAndSampleType(self,experiment_id_I,sample_type_I,exp_type_I=4):
        '''Querry sample name short that are used from
        the experiment'''
        try:
            sample_name_short = self.session.query(sample_description.sample_name_short).filter(
                    sample.sample_type.like(sample_type_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_quantification_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name)).group_by(
                    sample_description.sample_name_short).order_by(
                    sample_description.sample_name_short.asc()).all();
            sample_name_short_O = [];
            for sns in sample_name_short: sample_name_short_O.append(sns.sample_name_short);
            return sample_name_short_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameShort_experimentIDAndSampleName(self,experiment_id_I,sample_name_I,exp_type_I=4):
        '''Querry sample name short that are used from
        the experiment'''
        try:
            sample_name_short = self.session.query(sample_description.sample_name_short).filter(
                    sample.sample_name.like(sample_name_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_quantification_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name)).group_by(
                    sample_description.sample_name_short).all();
            sample_name_short_O = sample_name_short[0];
            return sample_name_short_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample name abbreviations from data_stage01_quantification_mqresultstable
    def get_sampleNameAbbreviations_experimentIDAndSampleType(self,experiment_id_I,sample_type_I,exp_type_I=4):
        '''Querry sample name abbreviations that are used from
        the experiment'''
        try:
            sample_name_abbreviations = self.session.query(sample_description.sample_name_abbreviation).filter(
                    sample.sample_type.like(sample_type_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_quantification_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            for sna in sample_name_abbreviations: sample_name_abbreviations_O.append(sna.sample_name_abbreviation);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    # query dilutions from data_stage01_quantification_mqresultstable
    def get_sampleDilution_experimentIDAndSampleID(self,experiment_id_I,sample_id_I,exp_type_I=4):
        '''Querry dilutions that are used from the experiment'''
        try:
            sample_dilutions = self.session.query(sample.sample_dilution).filter(
                    sample.sample_id.like(sample_id_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_quantification_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name)).group_by(
                    sample.sample_dilution).order_by(
                    sample.sample_dilution.asc()).all();
            sample_dilutions_O = [];
            for sd in sample_dilutions: sample_dilutions_O.append(sd.sample_dilution);
            return sample_dilutions_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleDilution_experimentIDAndSampleNameAbbreviation(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I=4):
        '''Querry dilutions that are used from the experiment'''
        try:
            sample_dilutions = self.session.query(sample.sample_dilution).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name)).group_by(
                    sample.sample_dilution).order_by(
                    sample.sample_dilution.asc()).all();
            sample_dilutions_O = [];
            for sd in sample_dilutions: sample_dilutions_O.append(sd.sample_dilution);
            return sample_dilutions_O;
        except SQLAlchemyError as e:
            print(e);
    # query time points from data_stage01_quantification_mqresultstable
    def get_timePoint_experimentIDAndSampleNameAbbreviation(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I=4):
        '''Querry time points that are used from the experiment and sample name abbreviation'''
        try:
            time_points = self.session.query(sample_description.time_point).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_quantification_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name)).group_by(
                    sample_description.time_point).order_by(
                    sample_description.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # query component names from data_stage01_quantification_mqresultstable
    def get_componentsNames_experimentIDAndSampleID(self,experiment_id_I,sample_id_I,exp_type_I=4):
        '''Querry component names that are used and are not IS from
        the experiment and sample_id'''
        try:
            component_names = self.session.query(data_stage01_quantification_MQResultsTable.component_name).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_quantification_MQResultsTable.used_.is_(True),                   
                    data_stage01_quantification_MQResultsTable.is_.is_(False),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name)).group_by(
                    data_stage01_quantification_MQResultsTable.component_name).order_by(
                    data_stage01_quantification_MQResultsTable.component_name.asc()).all();
            component_names_O = [];
            for cn in component_names: component_names_O.append(cn.component_name);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentsNames_experimentIDAndSampleNameAbbreviation(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I=4):
        '''Querry component names that are used from
        the experiment and sample_name_abbreviation'''
        try:
            component_names = self.session.query(data_stage01_quantification_MQResultsTable.component_name).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name),                   
                    data_stage01_quantification_MQResultsTable.used_.is_(True),                   
                    data_stage01_quantification_MQResultsTable.is_.is_(False)).group_by(
                    data_stage01_quantification_MQResultsTable.component_name).order_by(
                    data_stage01_quantification_MQResultsTable.component_name.asc()).all();
            component_names_O = [];
            for cn in component_names: component_names_O.append(cn.component_name);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentsNames_experimentIDAndSampleName(self,experiment_id_I,sample_name_I,exp_type_I=4):
        '''Querry component names that are used and not internal standards from
        the experiment and sample_name'''
        try:
            component_names = self.session.query(data_stage01_quantification_MQResultsTable.component_name).filter(
                    experiment.sample_name.like(sample_name_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name),                   
                    data_stage01_quantification_MQResultsTable.used_.is_(True),                   
                    data_stage01_quantification_MQResultsTable.is_.is_(False)).group_by(
                    data_stage01_quantification_MQResultsTable.component_name).order_by(
                    data_stage01_quantification_MQResultsTable.component_name.asc()).all();
            component_names_O = [];
            for cn in component_names: component_names_O.append(cn.component_name);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query component group names from data_stage01_quantification_mqresultstable
    def get_componentGroupNames_sampleName(self,sample_name_I):
        '''Querry component group names that are used from the sample name
        NOTE: intended to be used within a for loop'''
        try:
            component_group_names = self.session.query(data_stage01_quantification_MQResultsTable.component_group_name).filter(
                    data_stage01_quantification_MQResultsTable.sample_name.like(sample_name_I),
                    data_stage01_quantification_MQResultsTable.used_.is_(True)).group_by(
                    data_stage01_quantification_MQResultsTable.component_group_name).order_by(
                    data_stage01_quantification_MQResultsTable.component_group_name.asc()).all();
            component_group_names_O = [];
            for cgn in component_group_names: component_group_names_O.append(cgn.component_group_name);
            return component_group_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentGroupName_experimentIDAndComponentName(self,experiment_id_I,component_name_I,exp_type_I=4):
        '''Querry component group names that are used from the component name
        NOTE: intended to be used within a for loop'''
        try:
            component_group_name = self.session.query(data_stage01_quantification_MQResultsTable.component_group_name).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name),
                    data_stage01_quantification_MQResultsTable.component_name.like(component_name_I),
                    data_stage01_quantification_MQResultsTable.used_.is_(True)).group_by(
                    data_stage01_quantification_MQResultsTable.component_group_name).all();
            if len(component_group_name)>1:
                print('more than 1 component_group_name retrieved per component_name')
            component_group_name_O = component_group_name[0];
            return component_group_name_O;
        except SQLAlchemyError as e:
            print(e);
    # query physiological parameters from data_stage01_quantification_mqresultstable
    def get_CVSAndCVSUnitsAndODAndDilAndDilUnits_sampleName(self,sample_name_I):
        '''Querry culture volume sampled, culture volume sampled units, and OD600 from sample name
        NOTE: intended to be used within a for loop'''
        try:
            physiologicalParameters = self.session.query(sample_physiologicalParameters.culture_volume_sampled,
                    sample_physiologicalParameters.culture_volume_sampled_units,
                    sample_physiologicalParameters.od600,
                    sample_description.reconstitution_volume,
                    sample_description.reconstitution_volume_units).filter(
                    sample.sample_name.like(sample_name_I),
                    sample.sample_id.like(sample_physiologicalParameters.sample_id),
                    sample.sample_id.like(sample_description.sample_id)).all();
            cvs_O = physiologicalParameters[0][0];
            cvs_units_O = physiologicalParameters[0][1];
            od600_O = physiologicalParameters[0][2];
            dil_O = physiologicalParameters[0][3];
            dil_units_O = physiologicalParameters[0][4];
            return cvs_O, cvs_units_O, od600_O, dil_O, dil_units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_CVSAndCVSUnitsAndODAndDilAndDilUnits_sampleNameShort(self,experiment_id_I,sample_name_short_I,exp_type_I=4):
        '''Querry culture volume sampled, culture volume sampled units, and OD600 from sample name
        NOTE: intended to be used within a for loop'''
        try:
            physiologicalParameters = self.session.query(sample_physiologicalParameters.culture_volume_sampled,
                    sample_physiologicalParameters.culture_volume_sampled_units,
                    sample_physiologicalParameters.od600,
                    sample_description.reconstitution_volume,
                    sample_description.reconstitution_volume_units).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_short.like(sample_name_short_I),
                    sample_description.sample_id.like(sample_physiologicalParameters.sample_id)).all();
            cvs_O = physiologicalParameters[0][0];
            cvs_units_O = physiologicalParameters[0][1];
            od600_O = physiologicalParameters[0][2];
            dil_O = physiologicalParameters[0][3];
            dil_units_O = physiologicalParameters[0][4];
            return cvs_O, cvs_units_O, od600_O, dil_O, dil_units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_conversionAndConversionUnits_biologicalMaterialAndConversionName(self,biological_material_I,conversion_name_I):
        '''Querry conversion and conversion units from
        biological material and conversion name
        NOTE: intended to be used within a for loop'''
        try:
            physiologicalParameters = self.session.query(sample_massVolumeConversion.conversion_factor,
                    sample_massVolumeConversion.conversion_units).filter(
                    sample_massVolumeConversion.biological_material.like(biological_material_I),
                    sample_massVolumeConversion.conversion_name.like(conversion_name_I)).all();
            conversion_O = physiologicalParameters[0][0];
            conversion_units_O = physiologicalParameters[0][1];
            return conversion_O, conversion_units_O;
        except SQLAlchemyError as e:
            print(e);
    # query data from data_stage01_quantification_mqresultstable
    def get_concAndConcUnits_sampleNameAndComponentName(self,sample_name_I,component_name_I):
        '''Querry data (i.e. concentration, area/peak height ratio) from sample name and component name
        NOTE: intended to be used within a for loop'''
        # check for absolute or relative quantitation (i.e. area/peak height ratio)
        try:
            use_conc = self.session.query(data_stage01_quantification_MQResultsTable.use_calculated_concentration).filter(
                    data_stage01_quantification_MQResultsTable.sample_name.like(sample_name_I),
                    data_stage01_quantification_MQResultsTable.component_name.like(component_name_I),
                    data_stage01_quantification_MQResultsTable.used_.is_(True)).all();
            if use_conc:
                use_conc_O = use_conc[0][0];
            else: 
                use_conc_O = None;
        except SQLAlchemyError as e:
            print(e);

        if use_conc_O:
            try:
                data = self.session.query(data_stage01_quantification_MQResultsTable.calculated_concentration,
                        data_stage01_quantification_MQResultsTable.conc_units).filter(
                        data_stage01_quantification_MQResultsTable.sample_name.like(sample_name_I),
                        data_stage01_quantification_MQResultsTable.component_name.like(component_name_I),
                        data_stage01_quantification_MQResultsTable.used_.is_(True)).all();
                if data:
                    conc_O = data[0][0];
                    conc_units_O = data[0][1];
                else: 
                    conc_O = None;
                    conc_units_O = None;
                return conc_O, conc_units_O;
            except SQLAlchemyError as e:
                print(e);

        else:
            # check for area or peak height ratio from quantitation_method
            try:
                data = self.session.query(quantitation_method.use_area).filter(
                        experiment.sample_name.like(sample_name_I),
                        experiment.quantitation_method_id.like(quantitation_method.id),
                        quantitation_method.component_name.like(component_name_I)).all();
                if data:
                    ratio_O = data[0][0];
                else: 
                    ratio_O = None;
            except SQLAlchemyError as e:
                print(e);

            if ratio_O:
                try:
                    data = self.session.query(data_stage01_quantification_MQResultsTable.area_ratio).filter(
                            data_stage01_quantification_MQResultsTable.sample_name.like(sample_name_I),
                            data_stage01_quantification_MQResultsTable.component_name.like(component_name_I),
                            data_stage01_quantification_MQResultsTable.used_.is_(True)).all();
                    if data:
                        conc_O = data[0][0];
                        conc_units_O = 'area_ratio';
                    else: 
                        conc_O = None;
                        conc_units_O = None;
                    return conc_O, conc_units_O;
                except SQLAlchemyError as e:
                    print(e);
            else:
                try:
                    data = self.session.query(data_stage01_quantification_MQResultsTable.height_ratio).filter(
                            data_stage01_quantification_MQResultsTable.sample_name.like(sample_name_I),
                            data_stage01_quantification_MQResultsTable.component_name.like(component_name_I),
                            data_stage01_quantification_MQResultsTable.used_.is_(True)).all();
                    if data:
                        conc_O = data[0][0];
                        conc_units_O = 'height_ratio';
                    else: 
                        conc_O = None;
                        conc_units_O = None;
                    return conc_O, conc_units_O;
                except SQLAlchemyError as e:
                    print(e);
    def get_peakHeight_sampleNameAndComponentName(self,sample_name_I,component_name_I):
        '''Querry peak height from sample name and component name
        NOTE: intended to be used within a for loop'''

        try:
            data = self.session.query(data_stage01_quantification_MQResultsTable.height).filter(
                    data_stage01_quantification_MQResultsTable.sample_name.like(sample_name_I),
                    data_stage01_quantification_MQResultsTable.component_name.like(component_name_I),
                    data_stage01_quantification_MQResultsTable.used_.is_(True)).all();
            if data:
                conc_O = data[0][0];
                conc_units_O = 'height';
            else: 
                conc_O = None;
                conc_units_O = None;
            return conc_O, conc_units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_used_sampleNameAndComponentName(self,sample_name_I,component_name_I):
        '''Querry used from sample name and component name
        NOTE: intended to be used within a for loop'''
        try:
            data = self.session.query(data_stage01_quantification_MQResultsTable.used_).filter(
                    data_stage01_quantification_MQResultsTable.sample_name.like(sample_name_I),
                    data_stage01_quantification_MQResultsTable.component_name_name.like(component_name_name_I)).all();
            if data:
                used_O = data[0];
            else: used_O = None;
            return used_O;
        except SQLAlchemyError as e:
            print(e);
    def get_row_sampleNameAndComponentName(self,sample_name_I,component_name_I):
        '''Query peak information from sample name and component name
        NOTE: intended to be used within a for loop'''
        try:
            data = self.session.query(data_stage01_quantification_MQResultsTable).filter(
                    data_stage01_quantification_MQResultsTable.sample_name.like(sample_name_I),
                    data_stage01_quantification_MQResultsTable.component_name_name.like(component_name_I),
                    data_stage01_quantification_MQResultsTable.used_.is_(True)).all();
            data_O = {};
            if data:
                for d in data:
                    used_O={'index_':d.index_,
            'sample_index':d.sample_index,
            'original_filename':d.original_filename,
            'sample_name':d.sample_name,
            'sample_id':d.sample_id,
            'sample_comment':d.sample_comment,
            'sample_type':d.sample_type,
            'acquisition_date_and_time':d.acquisition_date_and_time,
            'rack_number':d.rack_number,
            'plate_number':d.plate_number,
            'vial_number':d.vial_number,
            'dilution_factor':d.dilution_factor,
            'injection_volume':d.injection_volume,
            'operator_name':d.operator_name,
            'acq_method_name':d.acq_method_name,
            'is_':d.is_,
            'component_name':d.component_name,
            'component_index':d.component_index,
            'component_comment':d.component_comment,
            'is_comment':d.is_comment,
            'mass_info':d.mass_info,
            'is_mass':d.is_mass,
            'is_name':d.is_name,
            'component_group_name':d.component_group_name,
            'conc_units':d.conc_units,
            'failed_query':d.failed_query,
            'is_failed_query':d.is_failed_query,
            'peak_comment':d.peak_comment,
            'is_peak_comment':d.is_peak_comment,
            'actual_concentration':d.actual_concentration,
            'is_actual_concentration':d.is_actual_concentration,
            'concentration_ratio':d.concentration_ratio,
            'expected_rt':d.expected_rt,
            'is_expected_rt':d.is_expected_rt,
            'integration_type':d.integration_type,
            'is_integration_type':d.is_integration_type,
            'area':d.area,
            'is_area':d.is_area,
            'corrected_area':d.corrected_area,
            'is_corrected_area':d.is_corrected_area,
            'area_ratio':d.area_ratio,
            'height':d.height,
            'is_height':d.is_height,
            'corrected_height':d.corrected_height,
            'is_corrected_height':d.is_corrected_height,
            'height_ratio':d.height_ratio,
            'area_2_height':d.area_2_height,
            'is_area_2_height':d.is_area_2_height,
            'corrected_area2height':d.corrected_area2height,
            'is_corrected_area2height':d.is_corrected_area2height,
            'region_height':d.region_height,
            'is_region_height':d.is_region_height,
            'quality':d.quality,
            'is_quality':d.is_quality,
            'retention_time':d.retention_time,
            'is_retention_time':d.is_retention_time,
            'start_time':d.start_time,
            'is_start_time':d.is_start_time,
            'end_time':d.end_time,
            'is_end_time':d.is_end_time,
            'total_width':d.total_width,
            'is_total_width':d.is_total_width,
            'width_at_50':d.width_at_50,
            'is_width_at_50':d.is_width_at_50,
            'signal_2_noise':d.signal_2_noise,
            'is_signal_2_noise':d.is_signal_2_noise,
            'baseline_delta_2_height':d.baseline_delta_2_height,
            'is_baseline_delta_2_height':d.is_baseline_delta_2_height,
            'modified_':d.modified_,
            'relative_rt':d.relative_rt,
            'used_':d.used_,
            'calculated_concentration':d.calculated_concentration,
            'accuracy_':d.accuracy_,
            'comment_':d.comment_,
            'use_calculated_concentration':d.use_calculated_concentration};
            else: used_O = None;
            return used_O;
        except SQLAlchemyError as e:
            print(e);
    def get_peakInfo_sampleNameAndComponentName(self,sample_name_I,component_name_I,acquisition_date_and_time_I):
        '''Query peak information from sample name and component name
        NOTE: intended to be used within a for loop'''
        try:
            if acquisition_date_and_time_I[0] and acquisition_date_and_time_I[1]:
                data = self.session.query(data_stage01_quantification_MQResultsTable).filter(
                    data_stage01_quantification_MQResultsTable.sample_name.like(sample_name_I),
                    data_stage01_quantification_MQResultsTable.component_name.like(component_name_I),
                    data_stage01_quantification_MQResultsTable.acquisition_date_and_time>=acquisition_date_and_time_I[0],
                    data_stage01_quantification_MQResultsTable.acquisition_date_and_time<=acquisition_date_and_time_I[1],
                    data_stage01_quantification_MQResultsTable.used_.is_(True)).all();
            else:
                data = self.session.query(data_stage01_quantification_MQResultsTable).filter(
                    data_stage01_quantification_MQResultsTable.sample_name.like(sample_name_I),
                    data_stage01_quantification_MQResultsTable.component_name.like(component_name_I),
                    data_stage01_quantification_MQResultsTable.used_.is_(True)).all();
            data_O = {};
            if data:
                for d in data:
                    used_O={'acquisition_date_and_time':d.acquisition_date_and_time,
                    'component_name':d.component_name,
                    'component_group_name':d.component_group_name,
                    'area':d.area,
                    'height':d.height,
                    'retention_time':d.retention_time,
                    'start_time':d.start_time,
                    'end_time':d.end_time,
                    'total_width':d.total_width,
                    'width_at_50':d.width_at_50,
                    'signal_2_noise':d.signal_2_noise,
                    'baseline_delta_2_height':d.baseline_delta_2_height,
                    'relative_rt':d.relative_rt};
            else: used_O = None;
            return used_O;
        except SQLAlchemyError as e:
            print(e);
    # delet data from data_stage01_quantification_mqresultstable
    def delete_row_sampleName(self,sampleNames_I):
        '''Delete specific samples from an experiment by their sample ID from sample_physiologicalparameters'''
        deletes = [];
        for d in sampleNames_I:
            try:
                delete = self.session.query(data_stage01_quantification_MQResultsTable).filter(
                        data_stage01_quantification_MQResultsTable.sample_name.like(d['sample_name'])).delete(
                        synchronize_session=False);
                if delete == 0:
                    print 'row not found'
                    print d;
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();
        
    # query description from sample_description
    def get_description_experimentIDAndSampleID_sampleDescription(self,experiment_id_I,sample_id_I):
        '''Query description by sample id from sample_description'''
        try:
            data = self.session.query(sample_description).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_description.sample_id)).first();
            desc = {};
            if data: 
                desc['sample_id']=data.sample_id;
                desc['sample_name_short']=data.sample_name_short;
                desc['sample_name_abbreviation']=data.sample_name_abbreviation;
                desc['sample_date']=data.sample_date;
                desc['time_point']=data.time_point;
                desc['sample_condition']=data.sample_condition;
                desc['extraction_method_id']=data.extraction_method_id;
                desc['biological_material']=data.biological_material;
                desc['sample_description']=data.sample_description;
                desc['sample_replicate']=data.sample_replicate;
                desc['is_added']=data.is_added;
                desc['is_added_units']=data.is_added_units;
                desc['reconstitution_volume']=data.reconstitution_volume;
                desc['reconstitution_volume_units']=data.reconstitution_volume_units;
                desc['istechnical']=data.istechnical;
                desc['sample_replicate_biological']=data.sample_replicate_biological;
                desc['notes']=data.notes;
            return desc;
        except SQLAlchemyError as e:
            print(e);

    # QC queries from data_stage01_quantification_normalized
    def get_LLOQAndULOQ(self,experiment_id_I,exp_type_I=4):
        '''query to populate the "checkLLOQAndULOQ" view'''
        try:
            check = self.session.query(data_stage01_quantification_MQResultsTable.sample_name, 
                        data_stage01_quantification_MQResultsTable.component_group_name, 
                        data_stage01_quantification_MQResultsTable.component_name, 
                        data_stage01_quantification_MQResultsTable.calculated_concentration, 
                        data_stage01_quantification_MQResultsTable.conc_units, 
                        quantitation_method.correlation, 
                        quantitation_method.lloq, 
                        quantitation_method.uloq, 
                        quantitation_method.points,
                        data_stage01_quantification_MQResultsTable.used_).filter(
                        experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                        experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name),
                        experiment.quantitation_method_id.like(quantitation_method.id),
                        data_stage01_quantification_MQResultsTable.component_name.like(quantitation_method.component_name),
                        data_stage01_quantification_MQResultsTable.used_.is_(True),
                        data_stage01_quantification_MQResultsTable.is_.is_(False),
                        quantitation_method.points > 0,
                        or_(data_stage01_quantification_MQResultsTable.sample_type.like('Unknown'),
                        data_stage01_quantification_MQResultsTable.sample_type.like('Quality Control'))).order_by(
                        data_stage01_quantification_MQResultsTable.component_name.asc(),
                        data_stage01_quantification_MQResultsTable.sample_name.asc()).all();
            check_O = [];
            for c in check: 
                check_1 = {};
                check_1['sample_name'] = c.sample_name;
                check_1['component_group_name'] = c.component_group_name;
                check_1['component_name'] = c.component_name;
                check_1['calculated_concentration'] = c.calculated_concentration;
                check_1['conc_units'] = c.conc_units;
                check_1['correlation'] = c.correlation;
                check_1['lloq'] = c.lloq;
                check_1['uloq'] = c.uloq;
                check_1['points'] = c.points;
                check_1['used'] = c.used_;
                check_O.append(check_1);
            return  check_O;
        except SQLAlchemyError as e:
            print(e);
        return
    def get_checkLLOQAndULOQ(self,experiment_id_I,exp_type_I=4):
        '''query to populate the "checkLLOQAndULOQ" view'''
        try:
            check = self.session.query(data_stage01_quantification_MQResultsTable.sample_name, 
                        data_stage01_quantification_MQResultsTable.component_group_name, 
                        data_stage01_quantification_MQResultsTable.component_name, 
                        data_stage01_quantification_MQResultsTable.calculated_concentration, 
                        data_stage01_quantification_MQResultsTable.conc_units, 
                        quantitation_method.correlation, 
                        quantitation_method.lloq, 
                        quantitation_method.uloq, 
                        quantitation_method.points,
                        data_stage01_quantification_MQResultsTable.used_).filter(
                        experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                        experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name),
                        experiment.quantitation_method_id.like(quantitation_method.id),
                        data_stage01_quantification_MQResultsTable.component_name.like(quantitation_method.component_name),
                        data_stage01_quantification_MQResultsTable.used_.is_(True),
                        data_stage01_quantification_MQResultsTable.is_.is_(False),
                        quantitation_method.points > 0,
                        or_(data_stage01_quantification_MQResultsTable.sample_type.like('Unknown'),
                        data_stage01_quantification_MQResultsTable.sample_type.like('Quality Control')),
                        or_(data_stage01_quantification_MQResultsTable.calculated_concentration < quantitation_method.lloq,
                        data_stage01_quantification_MQResultsTable.calculated_concentration > quantitation_method.uloq)).order_by(
                        data_stage01_quantification_MQResultsTable.component_name.asc(),
                        data_stage01_quantification_MQResultsTable.sample_name.asc()).all();
            check_O = [];
            for c in check: 
                check_1 = {};
                check_1['sample_name'] = c.sample_name;
                check_1['component_group_name'] = c.component_group_name;
                check_1['component_name'] = c.component_name;
                check_1['calculated_concentration'] = c.calculated_concentration;
                check_1['conc_units'] = c.conc_units;
                check_1['correlation'] = c.correlation;
                check_1['lloq'] = c.lloq;
                check_1['uloq'] = c.uloq;
                check_1['points'] = c.points;
                check_1['used'] = c.used_;
                check_O.append(check_1);
            return  check_O;
        except SQLAlchemyError as e:
            print(e);
        return
    def get_checkISMatch(self,experiment_id_I,exp_type_I=4):
        '''query to populate the "checkISMatch" view'''
        try:
            check = self.session.query(data_stage01_quantification_MQResultsTable.sample_name, 
                        data_stage01_quantification_MQResultsTable.component_name, 
                        data_stage01_quantification_MQResultsTable.calculated_concentration, 
                        data_stage01_quantification_MQResultsTable.is_name.label('IS_name_samples'), 
                        quantitation_method.is_name.label('IS_name_calibrators')).filter(
                        experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                        experiment.sample_name.like(data_stage01_quantification_MQResultsTable.sample_name),
                        experiment.quantitation_method_id.like(quantitation_method.id),
                        data_stage01_quantification_MQResultsTable.component_name.like(quantitation_method.component_name),
                        data_stage01_quantification_MQResultsTable.used_.is_(True),
                        data_stage01_quantification_MQResultsTable.is_.is_(False),
                        or_(data_stage01_quantification_MQResultsTable.sample_type.like('Unknown'),
                        data_stage01_quantification_MQResultsTable.sample_type.like('Quality Control')),
                        ~(data_stage01_quantification_MQResultsTable.is_name.like(quantitation_method.is_name)),
                        quantitation_method.component_name.like(data_stage01_quantification_MQResultsTable.component_name)).order_by(
                        data_stage01_quantification_MQResultsTable.component_name.asc(),
                        data_stage01_quantification_MQResultsTable.sample_name.asc()).all();
            check_O = [];
            for c in check: 
                check_1 = {};
                check_1['sample_name'] = c.sample_name;
                check_1['component_name'] = c.component_name;
                check_1['IS_name_samples'] = c.IS_name_samples;
                check_1['IS_name_calibrators'] = c.IS_name_calibrators;
                check_O.append(check_1);
            return  check_O;
        except SQLAlchemyError as e:
            print(e);
        return
    def get_checkCV_dilutions(self,experiment_id_I):
        '''query to populate the "checkCV_dilutions" view'''
        cv_threshold = 20;
        try:
            check = self.session.query(data_stage01_quantification_dilutions).filter(
                        data_stage01_quantification_dilutions.experiment_id.like(experiment_id_I),
                        data_stage01_quantification_dilutions.calculated_concentration_cv > cv_threshold).all();
            check_O = [];
            for c in check: 
                check_1 = {};
                check_1['experiment_id'] = c.experiment_id;
                check_1['sample_id'] = c.sample_id;
                check_1['component_group_name'] = c.component_group_name;
                check_1['component_name'] = c.component_name;
                check_1['n_replicates'] = c.n_replicates;
                check_1['calculated_concentration_average'] = c.calculated_concentration_average;
                check_1['calculated_concentration_cv'] = c.calculated_concentration_cv;
                check_1['calculated_concentration_units'] = c.calculated_concentration_units;
                check_O.append(check_1);
            return  check_O;
        except SQLAlchemyError as e:
            print(e);
    def get_checkCVAndExtracellular_averages(self,experiment_id_I):
        '''query to populate the "checkCVAndExtracellular_averages" view'''
        cv_threshold = 20;
        extracellular_threshold = 50;
        try:
            check = self.session.query(data_stage01_quantification_averages).filter(
                        data_stage01_quantification_averages.experiment_id.like(experiment_id_I),
                        or_(data_stage01_quantification_averages.calculated_concentration_cv > cv_threshold,
                        data_stage01_quantification_averages.extracellular_percent > extracellular_threshold)).all();
            check_O = [];
            for c in check: 
                check_1 = {};
                check_1['experiment_id'] = c.experiment_id;
                check_1['sample_name_abbreviation'] = c.sample_name_abbreviation;
                check_1['time_point'] = c.time_point;
                check_1['component_group_name'] = c.component_group_name;
                check_1['component_name'] = c.component_name;
                check_1['n_replicates_broth'] = c.n_replicates_broth;
                check_1['calculated_concentration_broth_average'] = c.calculated_concentration_broth_average;
                check_1['calculated_concentration_broth_cv'] = c.calculated_concentration_broth_cv;
                check_1['n_replicates_filtrate'] = c.n_replicates_filtrate;
                check_1['calculated_concentration_filtrate_average'] = c.calculated_concentration_filtrate_average;
                check_1['calculated_concentration_filtrate_cv'] = c.calculated_concentration_filtrate_cv;
                check_1['n_replicates'] = c.n_replicates;
                check_1['calculated_concentration_average'] = c.calculated_concentration_average;
                check_1['calculated_concentration_cv'] = c.calculated_concentration_cv;
                check_1['calculated_concentration_units'] = c.calculated_concentration_units;
                check_1['extracellular_percent'] = c.extracellular_percent;
                check_1['used'] = c.used_;
                check_O.append(check_1);
            return  check_O;
        except SQLAlchemyError as e:
            print(e);

    # query samples from data_stage01_quantification_normalized
    def get_sampleIDs_experimentID_dataStage01Normalized(self,experiment_id_I):
        '''Querry sample ids that are used from
        the experiment'''
        try:
            sample_ids = self.session.query(data_stage01_quantification_normalized.sample_id).filter(
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_normalized.used_.is_(True)).group_by(
                    data_stage01_quantification_normalized.sample_id).order_by(
                    data_stage01_quantification_normalized.sample_id.asc()).all();
            sample_ids_O = [];
            for si in sample_ids: sample_ids_O.append(si.sample_id);
            return sample_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentID_dataStage01Normalized(self,experiment_id_I):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_quantification_normalized.sample_name).filter(
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_normalized.used_.is_(True)).group_by(
                    data_stage01_quantification_normalized.sample_name).order_by(
                    data_stage01_quantification_normalized.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleNameAbbreviationAndSampleDescriptionAndComponentName_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,sample_decription_I,component_name_I,exp_type_I=4):
        '''Querry sample names that are used from the experiment by sample name abbreviation and sample description'''
        try:
            sample_names = self.session.query(data_stage01_quantification_normalized.sample_name).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.sample_description.like(sample_decription_I),
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    data_stage01_quantification_normalized.component_name.like(component_name_I),
                    sample.sample_id.like(sample_description.sample_id),
                    sample.sample_name.like(data_stage01_quantification_normalized.sample_name),
                    data_stage01_quantification_normalized.used_.is_(True)).group_by(
                    data_stage01_quantification_normalized.sample_name).order_by(
                    data_stage01_quantification_normalized.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleNameAbbreviationAndSampleDescriptionAndComponentNameAndTimePoint_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,sample_decription_I,component_name_I,time_point_I,exp_type_I=4):
        '''Querry sample names that are used from the experiment by sample name abbreviation and sample description'''
        try:
            sample_names = self.session.query(data_stage01_quantification_normalized.sample_name).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.time_point.like(time_point_I),
                    sample_description.sample_description.like(sample_decription_I),
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_normalized.component_name.like(component_name_I),
                    sample.sample_id.like(sample_description.sample_id),
                    sample.sample_name.like(data_stage01_quantification_normalized.sample_name),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_quantification_normalized.used_.is_(True)).group_by(
                    data_stage01_quantification_normalized.sample_name).order_by(
                    data_stage01_quantification_normalized.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleName_experimentIDAndSampleIDAndSampleDilution_dataStage01Normalized(self,experiment_id_I,sample_id_I, sample_dilution_I):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_name = self.session.query(data_stage01_quantification_normalized.sample_name).filter(
                    data_stage01_quantification_normalized.sample_id.like(sample_id_I),
                    sample.sample_dilution == sample_dilution_I,
                    data_stage01_quantification_normalized.sample_name.like(sample.sample_name),
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_normalized.used_.is_(True)).all();
            sample_name_O = sample_name[0];
            return sample_name_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameShort_experimentIDAndSampleName_dataStage01Normalized(self,experiment_id_I,sample_name_I):
        '''Querry sample name short that are used from
        the experiment'''
        try:
            sample_name_short = self.session.query(sample_description.sample_name_short).filter(
                    sample.sample_name.like(sample_name_I),
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_normalized.used_.is_(True),
                    data_stage01_quantification_normalized.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.sample_name_short).all();
            sample_name_short_O = sample_name_short[0];
            return sample_name_short_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameShort_experimentIDAndSampleDescription_dataStage01Normalized(self,experiment_id_I,sample_description_I,exp_type_I=4):
        '''Querry sample name short that are in the experiment'''
        try:
            sample_name_short = self.session.query(sample_description.sample_name_short).filter(
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_normalized.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(sample.sample_name),
                    sample_description.sample_description.like(sample_description_I)).group_by(
                    sample_description.sample_name_short).all();
            sample_name_short_O = [];
            if sample_name_short:
                for sns in sample_name_short:
                    sample_name_short_O.append(sns[0]);
            return sample_name_short_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameShort_experimentID_dataStage01Normalized(self,experiment_id_I):
        '''Querry sample name short that are in the experiment'''
        try:
            sample_name_short = self.session.query(sample_description.sample_name_short).filter(
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_normalized.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.sample_name_short).all();
            sample_name_short_O = [];
            if sample_name_short:
                for sns in sample_name_short:
                    sample_name_short_O.append(sns[0]);
            return sample_name_short_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentID_dataStage01Normalized(self,experiment_id_I):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample_description.sample_name_abbreviation).filter(
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_normalized.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_quantification_normalized.used_.is_(True)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_abbreviation);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query components from data_stage01_quantification_normalized
    def get_componentsNames_experimentIDAndSampleID_dataStage01Normalized(self,experiment_id_I,sample_id_I):
        '''Querry component names that are used and not internal standards from
        the experiment and sample_id'''
        try:
            component_names = self.session.query(data_stage01_quantification_normalized.component_name).filter(
                    data_stage01_quantification_normalized.sample_id.like(sample_id_I),
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),                  
                    data_stage01_quantification_normalized.used_.is_(True)).group_by(
                    data_stage01_quantification_normalized.component_name).order_by(
                    data_stage01_quantification_normalized.component_name.asc()).all();
            component_names_O = [];
            for cn in component_names: component_names_O.append(cn.component_name);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentsNames_experimentIDAndSampleName_dataStage01Normalized(self,experiment_id_I,sample_name_I):
        '''Querry component names that are used and not internal standards from
        the experiment and sample_name'''
        try:
            component_names = self.session.query(data_stage01_quantification_normalized.component_name).filter(
                    data_stage01_quantification_normalized.sample_name.like(sample_name_I),
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),                  
                    data_stage01_quantification_normalized.used_.is_(True)).group_by(
                    data_stage01_quantification_normalized.component_name).order_by(
                    data_stage01_quantification_normalized.component_name.asc()).all();
            component_names_O = [];
            for cn in component_names: component_names_O.append(cn.component_name);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentsNames_experimentIDAndSampleNameAbbreviation_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I=4):
        '''Querry component names that are used and not internal standards from
        the experiment and sample abbreviation'''
        try:
            component_names = self.session.query(data_stage01_quantification_normalized.component_name).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_normalized.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.exp_type_id == exp_type_I,  
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),                
                    data_stage01_quantification_normalized.used_.is_(True)).group_by(
                    data_stage01_quantification_normalized.component_name).order_by(
                    data_stage01_quantification_normalized.component_name.asc()).all();
            component_names_O = [];
            for cn in component_names: component_names_O.append(cn.component_name);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentGroupName_experimentIDAndComponentName_dataStage01Normalized(self,experiment_id_I,component_name_I):
        '''Querry component group names that are used from the component name
        NOTE: intended to be used within a for loop'''
        try:
            component_group_name = self.session.query(data_stage01_quantification_normalized.component_group_name).filter(
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_normalized.component_name.like(component_name_I),
                    data_stage01_quantification_normalized.used_.is_(True)).group_by(
                    data_stage01_quantification_normalized.component_group_name).all();
            if len(component_group_name)>1:
                print('more than 1 component_group_name retrieved per component_name')
            component_group_name_O = component_group_name[0];
            return component_group_name_O;
        except SQLAlchemyError as e:
            print(e);
    # query dilutions from data_stage01_quantification_normalized
    def get_sampleDilutions_experimentIDAndSampleIDAndComponentName_dataStage01Normalized(self,experiment_id_I,sample_id_I,component_name_I):
        '''Querry dilutions that are used from the experiment'''
        try:
            sample_dilutions = self.session.query(sample.sample_dilution).filter(
                    sample.sample_id.like(sample_id_I),
                    data_stage01_quantification_normalized.sample_name.like(sample.sample_name),
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_normalized.used_.is_(True),
                    data_stage01_quantification_normalized.component_name.like(component_name_I)).group_by(
                    sample.sample_dilution).order_by(
                    sample.sample_dilution.asc()).all();
            sample_dilutions_O = [];
            for sd in sample_dilutions: sample_dilutions_O.append(sd.sample_dilution);
            return sample_dilutions_O;
        except SQLAlchemyError as e:
            print(e);
    # query time points
    def get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I=4):
        '''Querry time points that are used from the experiment and sample name abbreviation'''
        try:
            time_points = self.session.query(sample_description.time_point).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_normalized.experiment_id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_quantification_normalized.used_.is_(True),
                    data_stage01_quantification_normalized.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.time_point).order_by(
                    sample_description.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # query data from data_stage01_quantification_normalized    
    def get_concAndConcUnits_sampleNameAndComponentName_dataStage01Normalized(self,sample_name_I,component_name_I):
        '''Querry data (i.e. concentration) from sample name and component name
        NOTE: intended to be used within a for loop'''
        try:
            data = self.session.query(data_stage01_quantification_normalized.calculated_concentration,
                    data_stage01_quantification_normalized.calculated_concentration_units).filter(
                    data_stage01_quantification_normalized.sample_name.like(sample_name_I),
                    data_stage01_quantification_normalized.component_name.like(component_name_I),
                    data_stage01_quantification_normalized.used_.is_(True)).all();
            if data:
                conc_O = data[0][0];
                conc_units_O = data[0][1];
            else: 
                conc_O = None;
                conc_units_O = None;
            return conc_O, conc_units_O;
        except SQLAlchemyError as e:
            print(e);
        
    # Query samples from data_stage01_quantification_replicates
    def get_sampleNameAbbreviations_experimentID_dataStage01Replicates(self,experiment_id_I,exp_type_I=4):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample_description.sample_name_abbreviation).filter(
                    data_stage01_quantification_replicates.experiment_id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    data_stage01_quantification_replicates.sample_name_short.like(sample_description.sample_name_short),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_quantification_replicates.used_.is_(True)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_abbreviation);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_SampleNameShort_experimentIDAndSampleNameAbbreviationAndTimePoint_dataStage01Replicates(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,exp_type_I=4):
        '''Querry sample names short that are used from the experiment and sample name abbreviation and time point'''
        try:
            sample_names = self.session.query(sample_description.sample_name_short).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.time_point.like(time_point_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    sample_description.sample_id.like(sample.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    data_stage01_quantification_replicates.experiment_id.like(experiment_id_I),
                    sample_description.sample_description.like('Broth')
                    #data_stage01_quantification_replicates.used_.is_(True),
                    #data_stage01_quantification_replicates.sample_name_short.like(sample_description.sample_name_short)
                    ).group_by(
                    sample_description.sample_name_short).order_by(
                    sample_description.sample_name_short.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_short);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query time points
    def get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01Replicates(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I=4):
        '''Querry time points that are used from the experiment and sample name abbreviation'''
        try:
            time_points = self.session.query(sample_description.time_point).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_replicates.experiment_id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    data_stage01_quantification_replicates.used_.is_(True),
                    data_stage01_quantification_replicates.sample_name_short.like(sample_description.sample_name_short)).group_by(
                    sample_description.time_point).order_by(
                    sample_description.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # Query data data_stage01_quantification_replicates:
    def get_data_experimentID_dataStage01Replicates(self, experiment_id_I):
        """write query results to csv"""
        try:
            data = self.session.query(data_stage01_quantification_replicates.sample_name_short,
                    data_stage01_quantification_replicates.calculated_concentration,
                    data_stage01_quantification_replicates.component_group_name).filter(
                    data_stage01_quantification_replicates.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicates.used_.is_(True)).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['component_group_name'] = d.component_group_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_data_experimentIDAndSampleNameShortAndTimePoint_dataStage01Replicates(self, experiment_id_I, sample_name_short_I, time_point_I):
        """write query results to csv"""
        try:
            data = self.session.query(data_stage01_quantification_replicates.sample_name_short,
                    data_stage01_quantification_replicates.calculated_concentration,
                    data_stage01_quantification_replicates.component_name).filter(
                    data_stage01_quantification_replicates.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicates.used_.is_(True),
                    data_stage01_quantification_replicates.sample_name_short.like(sample_name_short_I),
                    data_stage01_quantification_replicates.time_point.like(time_point_I),
                    data_stage01_quantification_replicates.used_.is_(True)).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentGroupNameAndConcUnits_experimentIDAndComponentName_dataStage01Replicates(self,experiment_id_I, component_name_I):
        '''Querry data (i.e. concentration) from component name
        NOTE: intended to be used within a for loop'''
        try:
            data = self.session.query(data_stage01_quantification_replicates.component_group_name,
                    data_stage01_quantification_replicates.calculated_concentration_units).filter(
                    data_stage01_quantification_replicates.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicates.component_name.like(component_name_I)).group_by(
                    data_stage01_quantification_replicates.component_group_name,
                    data_stage01_quantification_replicates.calculated_concentration_units).all();
            if len(data)>1:
                print('more than 1 component_group_name retrieved per component_name')
            if data:
                cgn_O = data[0][0];
                conc_units_O = data[0][1];
            else: 
                conc_O = None;
                conc_units_O = None;
            return cgn_O, conc_units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentGroupNameAndConcUnits_experimentIDAndComponentNameAndSampleNameAbbreviationAndTimePoint_dataStage01Replicates(self,experiment_id_I, component_name_I, sample_name_abbreviation_I,time_point_I,exp_type_I=4):
        '''Querry data (i.e. concentration) from component name and sample name abbreviation and time points
        NOTE: intended to be used within a for loop'''
        try:
            data = self.session.query(data_stage01_quantification_replicates.component_group_name,
                    data_stage01_quantification_replicates.calculated_concentration_units).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.time_point.like(time_point_I),
                    sample_description.sample_id.like(sample.sample_id),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    data_stage01_quantification_replicates.sample_name_short.like(sample_description.sample_name_short),
                    data_stage01_quantification_replicates.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicates.component_name.like(component_name_I)).group_by(
                    data_stage01_quantification_replicates.component_group_name,
                    data_stage01_quantification_replicates.calculated_concentration_units).all();
            if len(data)>1:
                print('more than 1 component_group_name retrieved per component_name')
            if data:
                cgn_O = data[0][0];
                conc_units_O = data[0][1];
            else: 
                conc_O = None;
                conc_units_O = None;
            return cgn_O, conc_units_O;
        except SQLAlchemyError as e:
            print(e);

    # Query sample names from data_stage01_quantification_replicatesMI:
    def get_sampleNameShort_experimentIDAndSampleNameAbbreviationAndComponentNameAndTimePoint_dataStage01ReplicatesMI(self,experiment_id_I,sample_name_abbreviation_I,component_name_I,time_point_I,exp_type_I=4):
        '''Querry sample names that are used from the experiment by sample name abbreviation and sample description'''
        try:
            sample_names = self.session.query(data_stage01_quantification_replicatesMI.sample_name_short).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.time_point.like(time_point_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_quantification_replicatesMI.time_point.like(time_point_I),
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.component_name.like(component_name_I),
                    data_stage01_quantification_replicatesMI.sample_name_short.like(sample_description.sample_name_short),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).group_by(
                    data_stage01_quantification_replicatesMI.sample_name_short).order_by(
                    data_stage01_quantification_replicatesMI.sample_name_short.asc()).all();
            sample_names_short_O = [];
            for sn in sample_names: sample_names_short_O.append(sn.sample_name_short);
            return sample_names_short_O;
        except SQLAlchemyError as e:
            print(e);
    def get_SampleNameShort_experimentID_dataStage01ReplicatesMI(self,experiment_id_I):
        '''Querry sample names short that are used from the experiment'''
        try:
            sample_names = self.session.query(data_stage01_quantification_replicatesMI.sample_name_short).filter(
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).group_by(
                    data_stage01_quantification_replicatesMI.sample_name_short).order_by(
                    data_stage01_quantification_replicatesMI.sample_name_short.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_short);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentID_dataStage01ReplicatesMI(self,experiment_id_I,exp_type_I=4):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample_description.sample_name_abbreviation).filter(
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.sample_name_short.like(sample_description.sample_name_short),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_abbreviation);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndTimePointAndComponentName_dataStage01ReplicatesMI(self,experiment_id_I,time_point_I,component_name_I,exp_type_I=4):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample_description.sample_name_abbreviation).filter(
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.time_point.like(time_point_I),
                    data_stage01_quantification_replicatesMI.component_name.like(component_name_I),
                    data_stage01_quantification_replicatesMI.sample_name_short.like(sample_description.sample_name_short),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_abbreviation);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # Query component names from data_stage01_quantification_replicatesMI:
    def get_componentNames_experimentID_dataStage01ReplicatesMI(self,experiment_id_I):
        '''Querry component Names that are used from the experiment'''
        try:
            component_names = self.session.query(data_stage01_quantification_replicatesMI.component_name).filter(
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).group_by(
                    data_stage01_quantification_replicatesMI.component_name).order_by(
                    data_stage01_quantification_replicatesMI.component_name.asc()).all();
            component_names_O = [];
            for cn in component_names: component_names_O.append(cn.component_name);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentNames_experimentIDAndSampleNameAbbreviation_dataStage01ReplicatesMI(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I=4):
        '''Querry component names that are used and not internal standards from
        the experiment and sample abbreviation'''
        try:
            component_names = self.session.query(data_stage01_quantification_replicatesMI.component_name).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.sample_name_short.like(sample_description.sample_name_short),   
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),            
                    data_stage01_quantification_replicatesMI.used_.is_(True)).group_by(
                    data_stage01_quantification_replicatesMI.component_name).order_by(
                    data_stage01_quantification_replicatesMI.component_name.asc()).all();
            component_names_O = [];
            for cn in component_names: component_names_O.append(cn.component_name);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentNames_experimentIDAndTimePoint_dataStage01ReplicatesMI(self,experiment_id_I,time_point_I):
        '''Querry component names that are used and not internal standards from
        the experiment and time point'''
        try:
            component_names = self.session.query(data_stage01_quantification_replicatesMI.component_name).filter(
                    data_stage01_quantification_replicatesMI.time_point.like(time_point_I),
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),            
                    data_stage01_quantification_replicatesMI.used_.is_(True)).group_by(
                    data_stage01_quantification_replicatesMI.component_name).order_by(
                    data_stage01_quantification_replicatesMI.component_name.asc()).all();
            component_names_O = [];
            for cn in component_names: component_names_O.append(cn.component_name);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    # Query time points from data_stage01_quantification_replicatesMI
    def get_timePoint_experimentID_dataStage01ReplicatesMI(self,experiment_id_I):
        '''Querry time points that are used from the experiment'''
        try:
            time_points = self.session.query(data_stage01_quantification_replicatesMI.time_point).filter(
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).group_by(
                    data_stage01_quantification_replicatesMI.time_point).order_by(
                    data_stage01_quantification_replicatesMI.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_experimentIDAndSampleNameShort_dataStage01ReplicatesMI(self,experiment_id_I,sample_name_short_I):
        '''Querry time points that are used from the experiment'''
        try:
            time_points = self.session.query(data_stage01_quantification_replicatesMI.time_point).filter(
                    data_stage01_quantification_replicatesMI.sample_name_short.like(sample_name_short_I),
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).group_by(
                    data_stage01_quantification_replicatesMI.time_point).order_by(
                    data_stage01_quantification_replicatesMI.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01ReplicatesMI(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I=4):
        '''Querry time points that are used from the experiment'''
        try:
            time_points = self.session.query(data_stage01_quantification_replicatesMI.time_point).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_short.like(data_stage01_quantification_replicatesMI.sample_name_short),
                    sample_description.time_point.like(data_stage01_quantification_replicatesMI.time_point),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).group_by(
                    data_stage01_quantification_replicatesMI.time_point).order_by(
                    data_stage01_quantification_replicatesMI.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # Query data from data_stage01_quantification_replicatesMI:
    def get_data_experimentID_dataStage01ReplicatesMI(self, experiment_id_I):
        """get data from experiment ID"""
        try:
            data = self.session.query(data_stage01_quantification_replicatesMI.sample_name_short,
                    data_stage01_quantification_replicatesMI.calculated_concentration,
                    data_stage01_quantification_replicatesMI.component_group_name).filter(
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['component_group_name'] = d.component_group_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentrations_experimentIDAndSampleNameAbbreviationAndTimePointAndComponentName_dataStage01ReplicatesMI(self, experiment_id_I, sample_name_abbreviation_I, time_point_I, component_name_I,exp_type_I=4):
        """Query calculatedConcentrations"""
        try:
            data = self.session.query(data_stage01_quantification_replicatesMI.calculated_concentration).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.time_point.like(time_point_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_quantification_replicatesMI.sample_name_short.like(sample_description.sample_name_short),
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.time_point.like(time_point_I),
                    data_stage01_quantification_replicatesMI.component_name.like(component_name_I),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).group_by(
                    data_stage01_quantification_replicatesMI.calculated_concentration).all();
            ratios_O = [];
            for d in data:
                ratios_O.append(d[0]);
            return ratios_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentration_experimentIDAndSampleNameShortAndTimePointAndComponentName_dataStage01ReplicatesMI(self, experiment_id_I, sample_name_short_I, time_point_I, component_name_I):
        """Query calculated concentrations"""
        try:
            data = self.session.query(data_stage01_quantification_replicatesMI.calculated_concentration).filter(
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.sample_name_short.like(sample_name_short_I),
                    data_stage01_quantification_replicatesMI.time_point.like(time_point_I),
                    data_stage01_quantification_replicatesMI.component_name.like(component_name_I),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).all();
            if len(data)>1:
                print('more than 1 calculated_concentration retrieved per component_name')
            if data:
                calc_conc_O = data[0];
            else: 
                calc_conc_O = None;
            return calc_conc_O;
        except SQLAlchemyError as e:
            print(e);
    def get_concAndConcUnits_experimentIDAndSampleNameShortAndTimePointAndComponentName_dataStage01ReplicatesMI(self, experiment_id_I, sample_name_short_I, time_point_I, component_name_I):
        """Query calculated concentrations"""
        try:
            data = self.session.query(data_stage01_quantification_replicatesMI.calculated_concentration,
                    data_stage01_quantification_replicatesMI.calculated_concentration_units).filter(
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.sample_name_short.like(sample_name_short_I),
                    data_stage01_quantification_replicatesMI.time_point.like(time_point_I),
                    data_stage01_quantification_replicatesMI.component_name.like(component_name_I),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).all();
            if len(data)>1:
                print('more than 1 calculated_concentration retrieved per component_name')
            if data:
                conc_O = data[0][0];
                conc_units_O = data[0][1];
            else: 
                conc_O = None;
                conc_units_O = None;
            return conc_O, conc_units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_concAndConcUnits_experimentIDAndSampleNameShortAndTimePointAndComponentGroupName_dataStage01ReplicatesMI(self, experiment_id_I, sample_name_short_I, time_point_I, component_group_name_I):
        """Query calculated concentrations"""
        try:
            data = self.session.query(data_stage01_quantification_replicatesMI.calculated_concentration,
                    data_stage01_quantification_replicatesMI.calculated_concentration_units).filter(
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.sample_name_short.like(sample_name_short_I),
                    data_stage01_quantification_replicatesMI.time_point.like(time_point_I),
                    data_stage01_quantification_replicatesMI.component_group_name.like(component_group_name_I),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).all();
            if len(data)>1:
                print('more than 1 calculated_concentration retrieved per component_name')
            if data:
                conc_O = data[0][0];
                conc_units_O = data[0][1];
            else: 
                conc_O = None;
                conc_units_O = None;
            return conc_O, conc_units_O;
        except SQLAlchemyError as e:
            print(e);
   # Query information from calibrators based on data_stage01_quantification_replicatesMI
    def get_lloq_ExperimentIDAndComponentName_dataStage01LLOQAndULOQ(self, experiment_id_I, component_name_I):
        '''Query lloq for a given component and experiment
        NOTE: intended to be used in a loop'''

        try:
            calibrators_parameters = self.session.query(data_stage01_quantification_LLOQAndULOQ.lloq,
                                                   data_stage01_quantification_LLOQAndULOQ.calculated_concentration_units).filter(
                                data_stage01_quantification_LLOQAndULOQ.experiment_id.like(experiment_id_I),
                                data_stage01_quantification_LLOQAndULOQ.component_name.like(component_name_I)).first();
            if calibrators_parameters:
                lloq_O = calibrators_parameters.lloq;
                calculated_concentration_units_O = calibrators_parameters.calculated_concentration_units;
                return lloq_O, calculated_concentration_units_O;
            else:
                return None,None;

        except SQLAlchemyError as e:
            print(e);

    # Query data from data_stage01_quantification_averagesMI:
    def get_concentrations_experimentIDAndSampleNameAbbreviationAndTimePoint_dataStage01AveragesMI(self, experiment_id_I, sample_name_abbreviation_I, time_point_I):
        """get data from experiment ID, sample name abbreviation, and time point"""
        try:
            data = self.session.query(data_stage01_quantification_averagesMI.calculated_concentration_average,
                    data_stage01_quantification_averagesMI.calculated_concentration_cv,
                    data_stage01_quantification_averagesMI.calculated_concentration_units,
                    data_stage01_quantification_averagesMI.component_group_name).filter(
                    data_stage01_quantification_averagesMI.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_averagesMI.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_averagesMI.time_point.like(time_point_I),
                    data_stage01_quantification_averagesMI.used_.is_(True)).all();
            data_O = {};
            for d in data: 
                data_O[d.component_group_name] = {'concentration':d.calculated_concentration_average,
                      'concentration_cv':d.calculated_concentration_cv,
                      'concentration_units':d.calculated_concentration_units};
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    
    # Query sample names from data_stage01_quantification_averagesMIgeo:
    def get_sampleNameAbbreviations_experimentIDAndTimePointAndComponentName_dataStage01AveragesMIgeo(self,experiment_id_I,time_point_I,component_name_I):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_quantification_averagesMIgeo.sample_name_abbreviation).filter(
                    data_stage01_quantification_averagesMIgeo.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_averagesMIgeo.time_point.like(time_point_I),
                    data_stage01_quantification_averagesMIgeo.component_name.like(component_name_I),
                    data_stage01_quantification_averagesMIgeo.used_.is_(True)).group_by(
                    data_stage01_quantification_averagesMIgeo.sample_name_abbreviation).order_by(
                    data_stage01_quantification_averagesMIgeo.sample_name_abbreviation.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_abbreviation);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # Query data from data_stage01_quantification_averagesMIgeo:
    def get_concentrations_experimentIDAndSampleNameAbbreviationAndTimePoint_dataStage01AveragesMIgeo(self, experiment_id_I, sample_name_abbreviation_I, time_point_I):
        """get data from experiment ID, sample name abbreviation, and time point"""
        try:
            data = self.session.query(data_stage01_quantification_averagesMIgeo.calculated_concentration_average,
                    data_stage01_quantification_averagesMIgeo.calculated_concentration_var,
                    data_stage01_quantification_averagesMIgeo.calculated_concentration_lb,
                    data_stage01_quantification_averagesMIgeo.calculated_concentration_ub,
                    data_stage01_quantification_averagesMIgeo.calculated_concentration_units,
                    data_stage01_quantification_averagesMIgeo.component_group_name).filter(
                    data_stage01_quantification_averagesMIgeo.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_averagesMIgeo.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_averagesMIgeo.time_point.like(time_point_I),
                    data_stage01_quantification_averagesMIgeo.used_.is_(True)).all();
            data_O = {};
            for d in data: 
                data_O[d.component_group_name] = {'concentration':d.calculated_concentration_average,
                      'concentration_var':d.calculated_concentration_var,
                      'concentration_lb':d.calculated_concentration_lb,
                      'concentration_ub':d.calculated_concentration_ub,
                      'concentration_units':d.calculated_concentration_units};
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_data_experimentIDAndSampleNameAbbreviationAndTimePointAndComponentName_dataStage01AveragesMIgeo(self, experiment_id_I, sample_name_abbreviation_I, time_point_I, component_name_I):
        """get data from experiment ID, sample name abbreviation, and time point"""
        try:
            data = self.session.query(data_stage01_quantification_averagesMIgeo).filter(
                    data_stage01_quantification_averagesMIgeo.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_averagesMIgeo.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_averagesMIgeo.component_name.like(component_name_I),
                    data_stage01_quantification_averagesMIgeo.time_point.like(time_point_I),
                    data_stage01_quantification_averagesMIgeo.used_.is_(True)).all();
            data_O = {};
            if data: 
                data_O={"experiment_id":data[0].experiment_id,
                "sample_name_abbreviation":data[0].sample_name_abbreviation,
                "time_point":data[0].time_point,
                "component_group_name":data[0].component_group_name,
                "component_name":data[0].component_name,
                "calculated_concentration_average":data[0].calculated_concentration_average,
                "calculated_concentration_var":data[0].calculated_concentration_var,
                "calculated_concentration_lb":data[0].calculated_concentration_lb,
                "calculated_concentration_ub":data[0].calculated_concentration_ub,
                "calculated_concentration_units":data[0].calculated_concentration_units,
                "used_":data[0].used_};
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    # Query time points from data_stage01_quantification_averagesMIgeo
    def get_timePoint_experimentID_dataStage01AveragesMIgeo(self,experiment_id_I):
        '''Querry time points that are used from the experiment'''
        try:
            time_points = self.session.query(data_stage01_quantification_averagesMIgeo.time_point).filter(
                    data_stage01_quantification_averagesMIgeo.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_averagesMIgeo.used_.is_(True)).group_by(
                    data_stage01_quantification_averagesMIgeo.time_point).order_by(
                    data_stage01_quantification_averagesMIgeo.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # Query component names from data_stage01_quantification_averagesMIgeo:
    def get_componentNames_experimentIDAndTimePoint_dataStage01AveragesMIgeo(self,experiment_id_I,time_point_I):
        '''Querry component Names that are used from the experiment'''
        try:
            component_names = self.session.query(data_stage01_quantification_averagesMIgeo.component_name).filter(
                    data_stage01_quantification_averagesMIgeo.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_averagesMIgeo.time_point.like(time_point_I),
                    data_stage01_quantification_averagesMIgeo.used_.is_(True)).group_by(
                    data_stage01_quantification_averagesMIgeo.component_name).order_by(
                    data_stage01_quantification_averagesMIgeo.component_name.asc()).all();
            component_names_O = [];
            for cn in component_names: component_names_O.append(cn.component_name);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    
    # Query data from ms_components:data_stage01_quantification_physiologicalRatios_replicates
    def get_msGroup_componentName_MSComponents(self,component_name_I):
        '''Querry component group names from the component name
        NOTE: intended to be used within a for loop'''
        try:
            component_group_name = self.session.query(MS_components.ms_group).filter(
                    MS_components.component_name.like(component_name_I)).group_by(
                    MS_components.ms_group).all();
            if len(component_group_name)>1:
                print('more than 1 component_group_name retrieved per component_name')
            component_group_name_O = component_group_name[0];
            return component_group_name_O;
        except SQLAlchemyError as e:
            print(e);

    # Query sample names from data_stage01_quantification_physiologicalRatios_replicates
    def get_sampleNameAbbreviations_experimentID_dataStage01PhysiologicalRatiosReplicates(self,experiment_id_I,exp_type_I=4):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample_description.sample_name_abbreviation).filter(
                    data_stage01_quantification_physiologicalRatios_replicates.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_physiologicalRatios_replicates.sample_name_short.like(sample_description.sample_name_short),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_quantification_physiologicalRatios_replicates.used_.is_(True)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_abbreviation);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameShort_experimentIDAndSampleNameAbbreviationAndRatioIDAndTimePoint_dataStage01PhysiologicalRatiosReplicates(self,experiment_id_I,sample_name_abbreviation_I,physiologicalratio_id_I,time_point_I,exp_type_I=4):
        '''Querry sample names that are used from the experiment by sample name abbreviation and sample description'''
        try:
            sample_names = self.session.query(data_stage01_quantification_physiologicalRatios_replicates.sample_name_short).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.time_point.like(time_point_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_quantification_physiologicalRatios_replicates.time_point.like(time_point_I),
                    data_stage01_quantification_physiologicalRatios_replicates.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_physiologicalRatios_replicates.physiologicalratio_id.like(physiologicalratio_id_I),
                    data_stage01_quantification_physiologicalRatios_replicates.sample_name_short.like(sample_description.sample_name_short),
                    data_stage01_quantification_physiologicalRatios_replicates.used_.is_(True)).group_by(
                    data_stage01_quantification_physiologicalRatios_replicates.sample_name_short).order_by(
                    data_stage01_quantification_physiologicalRatios_replicates.sample_name_short.asc()).all();
            sample_names_short_O = [];
            for sn in sample_names: sample_names_short_O.append(sn.sample_name_short);
            return sample_names_short_O;
        except SQLAlchemyError as e:
            print(e);
    # Query time points from data_stage01_quantification_physiologicalRatios_replicates
    def get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01PhysiologicalRatiosReplicates(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I=4):
        '''Querry time points that are used from the experiment'''
        try:
            time_points = self.session.query(data_stage01_quantification_physiologicalRatios_replicates.time_point).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_physiologicalRatios_replicates.experiment_id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_short.like(data_stage01_quantification_physiologicalRatios_replicates.sample_name_short),
                    sample_description.time_point.like(data_stage01_quantification_physiologicalRatios_replicates.time_point),
                    data_stage01_quantification_physiologicalRatios_replicates.used_.is_(True)).group_by(
                    data_stage01_quantification_physiologicalRatios_replicates.time_point).order_by(
                    data_stage01_quantification_physiologicalRatios_replicates.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_experimentID_dataStage01PhysiologicalRatiosReplicates(self,experiment_id_I):
        '''Querry time points that are used from the experiment'''
        try:
            time_points = self.session.query(data_stage01_quantification_physiologicalRatios_replicates.time_point).filter(
                    data_stage01_quantification_physiologicalRatios_replicates.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_physiologicalRatios_replicates.used_.is_(True)).group_by(
                    data_stage01_quantification_physiologicalRatios_replicates.time_point).order_by(
                    data_stage01_quantification_physiologicalRatios_replicates.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # Query data from data_stage01_quantification_physiologicalRatios_replicates
    def get_ratio_experimentIDAndSampleNameShortAndTimePointAndRatioID_dataStage01PhysiologicalRatiosReplicates(self, experiment_id_I, sample_name_short_I, time_point_I, physiologicalratio_id_I):
        """Query calculated ratios"""
        try:
            data = self.session.query(data_stage01_quantification_physiologicalRatios_replicates.physiologicalratio_value).filter(
                    data_stage01_quantification_physiologicalRatios_replicates.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_physiologicalRatios_replicates.sample_name_short.like(sample_name_short_I),
                    data_stage01_quantification_physiologicalRatios_replicates.time_point.like(time_point_I),
                    data_stage01_quantification_physiologicalRatios_replicates.physiologicalratio_id.like(physiologicalratio_id_I),
                    data_stage01_quantification_physiologicalRatios_replicates.used_.is_(True)).all();
            if len(data)>1:
                print('more than 1 calculated_concentration retrieved per component_name')
            if data:
                ratio_O = data[0][0];
            else: 
                ratio_O = None;
            return ratio_O;
        except SQLAlchemyError as e:
            print(e);
    def get_ratios_experimentIDAndSampleNameAbbreviationAndTimePointAndRatioID_dataStage01PhysiologicalRatiosReplicates(self, experiment_id_I, sample_name_abbreviation_I, time_point_I, physiologicalratio_id_I,exp_type_I=4):
        """Query calculated ratios"""
        try:
            data = self.session.query(data_stage01_quantification_physiologicalRatios_replicates.physiologicalratio_value).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.time_point.like(time_point_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_quantification_physiologicalRatios_replicates.sample_name_short.like(sample_description.sample_name_short),
                    data_stage01_quantification_physiologicalRatios_replicates.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_physiologicalRatios_replicates.time_point.like(time_point_I),
                    data_stage01_quantification_physiologicalRatios_replicates.physiologicalratio_id.like(physiologicalratio_id_I),
                    data_stage01_quantification_physiologicalRatios_replicates.used_.is_(True)).group_by(
                    data_stage01_quantification_physiologicalRatios_replicates.physiologicalratio_value).all();
            ratios_O = [];
            for d in data:
                ratios_O.append(d[0]);
            return ratios_O;
        except SQLAlchemyError as e:
            print(e);
    # Query ratio_id information from data_stage01_quantificaton_physiologicalRatios_replicates
    def get_ratioIDs_experimentIDAndTimePoint_dataStage01PhysiologicalRatiosReplicates(self,experiment_id_I,time_point_I):
        '''Querry sample names that are used from the experiment by sample name abbreviation and sample description'''
        try:
            ratios = self.session.query(data_stage01_quantification_physiologicalRatios_replicates.physiologicalratio_id,
                    data_stage01_quantification_physiologicalRatios_replicates.physiologicalratio_name,
                    data_stage01_quantification_physiologicalRatios_replicates.physiologicalratio_description).filter(
                    data_stage01_quantification_physiologicalRatios_replicates.time_point.like(time_point_I),
                    data_stage01_quantification_physiologicalRatios_replicates.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_physiologicalRatios_replicates.used_.is_(True)).group_by(
                    data_stage01_quantification_physiologicalRatios_replicates.physiologicalratio_id,
                    data_stage01_quantification_physiologicalRatios_replicates.physiologicalratio_name,
                    data_stage01_quantification_physiologicalRatios_replicates.physiologicalratio_description).order_by(
                    data_stage01_quantification_physiologicalRatios_replicates.physiologicalratio_id.asc()).all();
            ratios_O = {};
            for r in ratios:
                ratios_O[r.physiologicalratio_id] = {'name':r.physiologicalratio_name,
                                                     'description':r.physiologicalratio_description};
            return ratios_O;
        except SQLAlchemyError as e:
            print(e);
    
    # Query time points from data_stage01_quantification_physiologicalRatios_averages
    def get_timePoint_experimentID_dataStage01PhysiologicalRatiosAverages(self,experiment_id_I):
        '''Querry time points that are used from the experiment'''
        try:
            time_points = self.session.query(data_stage01_quantification_physiologicalRatios_averages.time_point).filter(
                    data_stage01_quantification_physiologicalRatios_averages.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_physiologicalRatios_averages.used_.is_(True)).group_by(
                    data_stage01_quantification_physiologicalRatios_averages.time_point).order_by(
                    data_stage01_quantification_physiologicalRatios_averages.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # Query sample names from data_stage01_quantification_physiologicalRatios_averages
    def get_sampleNameAbbreviations_experimentIDAndTimePoint_dataStage01PhysiologicalRatiosAverages(self,experiment_id_I,time_point_I):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_quantification_physiologicalRatios_averages.sample_name_abbreviation).filter(
                    data_stage01_quantification_physiologicalRatios_averages.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_physiologicalRatios_averages.time_point.like(time_point_I),
                    data_stage01_quantification_physiologicalRatios_averages.used_.is_(True)).group_by(
                    data_stage01_quantification_physiologicalRatios_averages.sample_name_abbreviation).order_by(
                    data_stage01_quantification_physiologicalRatios_averages.sample_name_abbreviation.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_abbreviation);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndTimePointAndRatioID_dataStage01PhysiologicalRatiosAverages(self,experiment_id_I,time_point_I,physiologicalratio_id_I):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_quantification_physiologicalRatios_averages.sample_name_abbreviation).filter(
                    data_stage01_quantification_physiologicalRatios_averages.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_physiologicalRatios_averages.time_point.like(time_point_I),
                    data_stage01_quantification_physiologicalRatios_averages.physiologicalratio_id.like(physiologicalratio_id_I),
                    data_stage01_quantification_physiologicalRatios_averages.used_.is_(True)).group_by(
                    data_stage01_quantification_physiologicalRatios_averages.sample_name_abbreviation).order_by(
                    data_stage01_quantification_physiologicalRatios_averages.sample_name_abbreviation.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_abbreviation);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # Query data from data_stage01_quantification_physiologicalRatios_averages:
    def get_data_experimentIDAndTimePointAndSampleNameAbbreviation_dataStage01PhysiologicalRatiosAverages(self, experiment_id_I,time_point_I,sample_name_abbreviation_I):
        """get data from experiment ID"""
        try:
            data = self.session.query(data_stage01_quantification_physiologicalRatios_averages).filter(
                    data_stage01_quantification_physiologicalRatios_averages.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_physiologicalRatios_averages.time_point.like(time_point_I),
                    data_stage01_quantification_physiologicalRatios_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_physiologicalRatios_averages.used_.is_(True)).all();
            data_O = [];
            for d in data: 
                data_1 = {'experiment_id':d.experiment_id,
                'sample_name_abbreviation':d.sample_name_abbreviation,
                'time_point':d.time_point,
                'physiologicalratio_id':d.physiologicalratio_id,
                'physiologicalratio_name':d.physiologicalratio_name,
                'physiologicalratio_value_ave':d.physiologicalratio_value_ave,
                'physiologicalratio_value_cv':d.physiologicalratio_value_cv,
                'physiologicalratio_value_lb':d.physiologicalratio_value_lb,
                'physiologicalratio_value_ub':d.physiologicalratio_value_ub,
                'physiologicalratio_description':d.physiologicalratio_description,
                'used_':d.used_,
                'comment_':d.comment_};
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_data_experimentIDAndTimePointAndRatioIDAndSampleNameAbbreviation_dataStage01PhysiologicalRatiosAverages(self, experiment_id_I,time_point_I,physiologicalratio_id_I,sample_name_abbreviation_I):
        """get data from experiment ID"""
        try:
            data = self.session.query(data_stage01_quantification_physiologicalRatios_averages).filter(
                    data_stage01_quantification_physiologicalRatios_averages.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_physiologicalRatios_averages.time_point.like(time_point_I),
                    data_stage01_quantification_physiologicalRatios_averages.physiologicalratio_id.like(physiologicalratio_id_I),
                    data_stage01_quantification_physiologicalRatios_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_physiologicalRatios_averages.used_.is_(True)).all();
            data_O = {};
            if data: 
                data_O = {'experiment_id':data[0].experiment_id,
                'sample_name_abbreviation':data[0].sample_name_abbreviation,
                'time_point':data[0].time_point,
                'physiologicalratio_id':data[0].physiologicalratio_id,
                'physiologicalratio_name':data[0].physiologicalratio_name,
                'physiologicalratio_value_ave':data[0].physiologicalratio_value_ave,
                'physiologicalratio_value_cv':data[0].physiologicalratio_value_cv,
                'physiologicalratio_value_lb':data[0].physiologicalratio_value_lb,
                'physiologicalratio_value_ub':data[0].physiologicalratio_value_ub,
                'physiologicalratio_description':data[0].physiologicalratio_description,
                'used_':data[0].used_,
                'comment_':data[0].comment_};
            return data_O;
        except SQLAlchemyError as e:
            print(e);    
    def get_ratio_experimentIDAndTimePointAndRatioIDAndSampleNameAbbreviation_dataStage01PhysiologicalRatiosAverages(self, experiment_id_I,time_point_I,physiologicalratio_id_I,sample_name_abbreviation_I):
        """get data from experiment ID"""
        try:
            data = self.session.query(data_stage01_quantification_physiologicalRatios_averages).filter(
                    data_stage01_quantification_physiologicalRatios_averages.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_physiologicalRatios_averages.time_point.like(time_point_I),
                    data_stage01_quantification_physiologicalRatios_averages.physiologicalratio_id.like(physiologicalratio_id_I),
                    data_stage01_quantification_physiologicalRatios_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_physiologicalRatios_averages.used_.is_(True)).all();
            ratio_O = None;
            if data: 
                ratio_O = data[0].physiologicalratio_value_ave;
            return ratio_O;
        except SQLAlchemyError as e:
            print(e);

    # Query peakInfo_parameter from data_stage01_quantificaton_peakInformation
    def get_peakInfoParameter_experimentID_dataStage01PeakInformation(self,experiment_id_I):
        '''Query component_names that are used for the experiment'''
        try:
            names = self.session.query(data_stage01_quantification_peakInformation.peakInfo_parameter).filter(
                    data_stage01_quantification_peakInformation.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_peakInformation.used_.is_(True)).group_by(
                    data_stage01_quantification_peakInformation.component_name).order_by(
                    data_stage01_quantification_peakInformation.component_name.asc()).all();
            names_O = [];
            for n in names:
                names_O.append(n.peakInfo_parameter);
            return names_O;
        except SQLAlchemyError as e:
            print(e);
    # Query data from data_stage01_quantification_peakInformation
    def get_row_experimentIDAndComponentName_dataStage01PeakInformation(self, experiment_id_I, component_name_I):
        """Query rows"""
        try:
            data = self.session.query(data_stage01_quantification_peakInformation).filter(
                    data_stage01_quantification_peakInformation.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_peakInformation.component_name.like(component_name_I),
                    data_stage01_quantification_peakInformation.used_.is_(True)).all();
            data_O = {};
            if len(data)>1:
                print('more than 1 calculated_concentration retrieved per component_name')
            if data:
                for d in data:
                    data_O = {'experiment_id':d.experiment_id,
            'component_group_name':d.component_group_name,
            'component_name':d.component_name,
            'peakInfo_parameter':d.peakInfo_parameter,
            'peakInfo_ave':d.peakInfo_ave,
            'peakInfo_cv':d.peakInfo_cv,
            'peakInfo_lb':d.peakInfo_lb,
            'peakInfo_ub':d.peakInfo_ub,
            'peakInfo_units':d.peakInfo_units,
            'sample_names':d.sample_names,
            'sample_types':d.sample_types,
            'acqusition_date_and_times':d.acqusition_date_and_times,
            'peakInfo_data':d.peakInfo_data};
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_row_experimentIDAndPeakInfoParameterComponentName_dataStage01PeakInformation(self, experiment_id_I, peakInfo_parameter_I, component_name_I):
        """Query rows"""
        try:
            data = self.session.query(data_stage01_quantification_peakInformation).filter(
                    data_stage01_quantification_peakInformation.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_peakInformation.component_name.like(component_name_I),
                    data_stage01_quantification_peakInformation.peakInfo_parameter.like(peakInfo_parameter_I),
                    data_stage01_quantification_peakInformation.used_.is_(True)).all();
            data_O = {};
            if len(data)>1:
                print('more than 1 calculated_concentration retrieved per component_name')
            if data:
                for d in data:
                    data_O = {'experiment_id':d.experiment_id,
            'component_group_name':d.component_group_name,
            'component_name':d.component_name,
            'peakInfo_parameter':d.peakInfo_parameter,
            'peakInfo_ave':d.peakInfo_ave,
            'peakInfo_cv':d.peakInfo_cv,
            'peakInfo_lb':d.peakInfo_lb,
            'peakInfo_ub':d.peakInfo_ub,
            'peakInfo_units':d.peakInfo_units,
            'sample_names':d.sample_names,
            'sample_types':d.sample_types,
            'acqusition_date_and_times':d.acqusition_date_and_times,
            'peakInfo_data':d.peakInfo_data};
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    # Query component_names from data_stage01_quantificaton_peakInformation
    def get_componentNames_experimentID_dataStage01PeakInformation(self,experiment_id_I):
        '''Query component_names that are used for the experiment'''
        try:
            names = self.session.query(data_stage01_quantification_peakInformation.component_name).filter(
                    data_stage01_quantification_peakInformation.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_peakInformation.used_.is_(True)).group_by(
                    data_stage01_quantification_peakInformation.component_name).order_by(
                    data_stage01_quantification_peakInformation.component_name.asc()).all();
            names_O = [];
            for n in names:
                names_O.append(n.component_name);
            return names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentNames_experimentIDAndPeakInfoParameter_dataStage01PeakInformation(self,experiment_id_I,peakInfo_parameter_I):
        '''Query component_names that are used for the experiment'''
        try:
            names = self.session.query(data_stage01_quantification_peakInformation.component_name).filter(
                    data_stage01_quantification_peakInformation.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_peakInformation.peakInfo_parameter.like(peakInfo_parameter_I),
                    data_stage01_quantification_peakInformation.used_.is_(True)).group_by(
                    data_stage01_quantification_peakInformation.component_name).order_by(
                    data_stage01_quantification_peakInformation.component_name.asc()).all();
            names_O = [];
            for n in names:
                names_O.append(n.component_name);
            return names_O;
        except SQLAlchemyError as e:
            print(e);
            
    # Query peakInfo_parameter from data_stage01_quantification_peakResolution
    def get_peakInfoParameter_experimentID_dataStage01PeakResolution(self,experiment_id_I):
        '''Query component_names that are used for the experiment'''
        try:
            names = self.session.query(data_stage01_quantification_peakResolution.peakInfo_parameter).filter(
                    data_stage01_quantification_peakResolution.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_peakResolution.used_.is_(True)).group_by(
                    data_stage01_quantification_peakResolution.component_name).order_by(
                    data_stage01_quantification_peakResolution.component_name.asc()).all();
            names_O = [];
            for n in names:
                names_O.append(n.peakInfo_parameter);
            return names_O;
        except SQLAlchemyError as e:
            print(e);
    # Query data from data_stage01_quantification_peakResolution
    def get_row_experimentIDAndComponentName_dataStage01PeakResolution(self, experiment_id_I, component_name_I):
        """Query rows"""
        try:
            data = self.session.query(data_stage01_quantification_peakResolution).filter(
                    data_stage01_quantification_peakResolution.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_peakResolution.component_name.like(component_name_I),
                    data_stage01_quantification_peakResolution.used_.is_(True)).all();
            data_O = {};
            if len(data)>1:
                print('more than 1 calculated_concentration retrieved per component_name')
            if data:
                for d in data:
                    data_O = {'experiment_id':d.experiment_id,
            'component_group_name_pair':d.component_group_name_pair,
            'component_name_pair':d.component_name_pair,
            'peakInfo_parameter':d.peakInfo_parameter,
            'peakInfo_ave':d.peakInfo_ave,
            'peakInfo_cv':d.peakInfo_cv,
            'peakInfo_lb':d.peakInfo_lb,
            'peakInfo_ub':d.peakInfo_ub,
            'peakInfo_units':d.peakInfo_units,
            'sample_names':d.sample_names,
            'sample_types':d.sample_types,
            'acqusition_date_and_times':d.acqusition_date_and_times,
            'peakInfo_data':d.peakInfo_data};
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_row_experimentIDAndPeakInfoParameterComponentName_dataStage01PeakResolution(self, experiment_id_I, peakInfo_parameter_I, component_name_pair_I):
        """Query rows"""
        try:
            data = self.session.query(data_stage01_quantification_peakResolution).filter(
                    data_stage01_quantification_peakResolution.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_peakResolution.component_name_pair.any(component_name_pair_I[0]),
                    data_stage01_quantification_peakResolution.component_name_pair.any(component_name_pair_I[1]),
                    data_stage01_quantification_peakResolution.peakInfo_parameter.like(peakInfo_parameter_I),
                    data_stage01_quantification_peakResolution.used_.is_(True)).all();
            data_O = {};
            if len(data)>1:
                print('more than 1 calculated_concentration retrieved per component_name')
            if data:
                for d in data:
                    data_O = {'experiment_id':d.experiment_id,
            'component_group_name_pair':d.component_group_name_pair,
            'component_name_pair':d.component_name_pair,
            'peakInfo_parameter':d.peakInfo_parameter,
            'peakInfo_ave':d.peakInfo_ave,
            'peakInfo_cv':d.peakInfo_cv,
            'peakInfo_lb':d.peakInfo_lb,
            'peakInfo_ub':d.peakInfo_ub,
            'peakInfo_units':d.peakInfo_units,
            'sample_names':d.sample_names,
            'sample_types':d.sample_types,
            'acqusition_date_and_times':d.acqusition_date_and_times,
            'peakInfo_data':d.peakInfo_data};
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    # Query component_names from data_stage01_quantification_peakResolution
    def get_componentNamePairs_experimentID_dataStage01PeakResolution(self,experiment_id_I):
        '''Query component_names that are used for the experiment'''
        try:
            names = self.session.query(data_stage01_quantification_peakResolution.component_name_pair).filter(
                    data_stage01_quantification_peakResolution.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_peakResolution.used_.is_(True)).group_by(
                    data_stage01_quantification_peakResolution.component_name_pair).order_by(
                    data_stage01_quantification_peakResolution.component_name_pair.asc()).all();
            names_O = [];
            for n in names:
                names_O.append(n.component_name_pair);
            return names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentNamePairs_experimentIDAndPeakInfoParameter_dataStage01PeakResolution(self,experiment_id_I,peakInfo_parameter_I):
        '''Query component_names that are used for the experiment'''
        try:
            names = self.session.query(data_stage01_quantification_peakResolution.component_name_pair).filter(
                    data_stage01_quantification_peakResolution.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_peakResolution.peakInfo_parameter.like(peakInfo_parameter_I),
                    data_stage01_quantification_peakResolution.used_.is_(True)).group_by(
                    data_stage01_quantification_peakResolution.component_name_pair).order_by(
                    data_stage01_quantification_peakResolution.component_name_pair.asc()).all();
            names_O = [];
            for n in names:
                names_O.append(n.component_name_pair);
            return names_O;
        except SQLAlchemyError as e:
            print(e);