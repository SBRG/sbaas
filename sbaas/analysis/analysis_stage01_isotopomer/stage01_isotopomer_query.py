from sbaas.analysis.analysis_base import *
from collections import OrderedDict

class stage01_isotopomer_query(base_analysis):
    # query sample names from data_stage01_isotopomer_mqresultstable
    def get_sampleNames_experimentIDAndSampleType(self,experiment_id_I,sample_type_I,exp_type_I=5):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_isotopomer_MQResultsTable.sample_name).filter(
                    data_stage01_isotopomer_MQResultsTable.sample_type.like(sample_type_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    data_stage01_isotopomer_MQResultsTable.sample_name).order_by(
                    data_stage01_isotopomer_MQResultsTable.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allSampleNames_experimentIDAndSampleType(self,experiment_id_I,sample_type_I,exp_type_I=5):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_isotopomer_MQResultsTable.sample_name).filter(
                    data_stage01_isotopomer_MQResultsTable.sample_type.like(sample_type_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    data_stage01_isotopomer_MQResultsTable.sample_name).order_by(
                    data_stage01_isotopomer_MQResultsTable.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleID(self,experiment_id_I,sample_id_I,exp_type_I=5):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample.sample_name).filter(
                    sample.sample_id.like(sample_id_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    sample.sample_name).order_by(
                    sample.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleIDAndSampleDilution(self,experiment_id_I,sample_id_I,sample_dilution_I,exp_type_I=5):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample.sample_name).filter(
                    sample.sample_id.like(sample_id_I),
                    sample.sample_dilution == sample_dilution_I,
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    sample.sample_name).order_by(
                    sample.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleNameShortAndSampleDescription(self,experiment_id_I,sample_name_short_I,sample_decription_I,exp_type_I=5):
        '''Querry sample names that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample.sample_name).filter(
                    sample_description.sample_name_short.like(sample_name_short_I),
                    sample_description.sample_desc.like(sample_decription_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True)).group_by(
                    sample.sample_name).order_by(
                    sample.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleNameAbbreviationAndSampleDescription(self,experiment_id_I,sample_name_abbreviation_I,sample_decription_I,exp_type_I=5):
        '''Querry sample names that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample.sample_name).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.sample_desc.like(sample_decription_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True)).group_by(
                    sample.sample_name).order_by(
                    sample.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleNameAbbreviationAndSampleDilution(self,experiment_id_I,sample_name_abbreviation_I,sample_dilution_I,exp_type_I=5):
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
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True)).group_by(
                    sample.sample_name).order_by(
                    sample.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNamesAndReplicateNumbersAndSampleTypes_experimentIDAndSampleNameAbbreviationAndSampleDescriptionAndComponentNameAndTimePointAndDilution(\
        self,experiment_id_I,sample_name_abbreviation_I,sample_description_I,component_name_I,time_point_I,sample_dilution_I,exp_type_I=5):
        '''Querry sample names that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample.sample_name,
                    sample_description.sample_replicate,
                    sample.sample_type).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.time_point.like(time_point_I),
                    sample_description.sample_desc.like(sample_description_I),
                    sample.sample_id.like(sample_description.sample_id),
                    sample.sample_dilution == sample_dilution_I,
                    experiment.sample_name.like(sample.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name),
                    data_stage01_isotopomer_MQResultsTable.component_name.like(component_name_I),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True)).group_by(
                    sample.sample_name,
                    sample_description.sample_replicate,
                    sample.sample_type).order_by(
                    sample.sample_name.asc()).all();
            sample_names_O = [];
            sample_replicates_O = [];
            sample_types_O = [];
            for sn in sample_names:
                sample_names_O.append(sn.sample_name);
                sample_replicates_O.append(sn.sample_replicate);
                sample_types_O.append(sn.sample_type);
            return sample_names_O,sample_replicates_O,sample_types_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNamesAndReplicateNumbersAndSampleTypes_experimentIDAndSampleNameAbbreviationAndSampleDescriptionAndTimePointAndDilution(\
        self,experiment_id_I,sample_name_abbreviation_I,sample_description_I,time_point_I,sample_dilution_I,exp_type_I=5):
        '''Querry sample names that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample.sample_name,
                    sample_description.sample_replicate,
                    sample.sample_type).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.time_point.like(time_point_I),
                    sample_description.sample_desc.like(sample_description_I),
                    sample.sample_id.like(sample_description.sample_id),
                    sample.sample_dilution == sample_dilution_I,
                    experiment.sample_name.like(sample.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True)).group_by(
                    sample.sample_name,
                    sample_description.sample_replicate,
                    sample.sample_type).order_by(
                    sample.sample_name.asc()).all();
            sample_names_O = [];
            sample_replicates_O = [];
            sample_types_O = [];
            for sn in sample_names:
                sample_names_O.append(sn.sample_name);
                sample_replicates_O.append(sn.sample_replicate);
                sample_types_O.append(sn.sample_type);
            return sample_names_O,sample_replicates_O,sample_types_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleNameAbbreviationAndSampleDescriptionAndComponentNameAndTimePointAndDilution(\
        self,experiment_id_I,sample_name_abbreviation_I,sample_description_I,component_name_I,time_point_I,sample_dilution_I,exp_type_I=5):
        '''Querry sample names that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample.sample_name).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.time_point.like(time_point_I),
                    sample_description.sample_desc.like(sample_description_I),
                    sample.sample_id.like(sample_description.sample_id),
                    sample.sample_dilution == sample_dilution_I,
                    experiment.sample_name.like(sample.sample_name),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I)).group_by(
                    sample.sample_name).order_by(
                    sample.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample ids from data_stage01_isotopomer_mqresultstable
    def get_sampleIDs_experimentIDAndSampleType(self,experiment_id_I,sample_type_I,exp_type_I=5):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_ids = self.session.query(sample.sample_id).filter(
                    data_stage01_isotopomer_MQResultsTable.sample_type.like(sample_type_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    sample.sample_id).order_by(
                    sample.sample_id.asc()).all();
            sample_ids_O = [];
            for si in sample_ids: sample_ids_O.append(si.sample_id);
            return sample_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleIDs_experimentID(self,experiment_id_I,exp_type_I=5):
        '''Querry sample names that are used from the experiment'''
        try:
            sample_ids = self.session.query(sample.sample_id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    sample.sample_id).order_by(
                    sample.sample_id.asc()).all();
            sample_ids_O = [];
            for si in sample_ids: sample_ids_O.append(si.sample_id);
            return sample_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleID_experimentIDAndSampleName(self,experiment_id_I,sample_name_I,exp_type_I=5):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_id = self.session.query(sample.sample_id).filter(
                    sample.sample_name.like(sample_name_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    sample.sample_id).all();
            sample_id_O = sample_id[0];
            return sample_id_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample names and sample name short
    def get_sampleNamesAndShortName_experimentIDAndSampleTypeAndTimePointAndDilution(experiment_id_I,sample_type_I,tp,dilution_I,exp_type_I=5):
        '''Querry sample name and sample name short that are used from
        the experimentfor specific time-points and dilutions'''
        try:
            sample_name_short = self.session.query(sample.sample_name,
                    sample_description.sample_name_short).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.sample_name.like(experiment.sample_name),
                    data_stage01_isotopomer_MQResultsTable.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    sample.sample_name.like(experiment.sample_name),
                    sample.sample_type.like(sample_type_I),
                    sample.sample_dilution == dilution_I,
                    sample_description.sample_id.like(sample.sample_id),
                    sample_description.time_point.like(time_point_I)).group_by(
                    sample.sample_name).order_by(
                    sample.sample_name).all();
            sample_name_O = [];
            sample_name_short_O = [];
            for sn in sample_name_short:
                sample_name_O.append(sn.sample_name);
                sample_name_short_O.append(sn.sample_name_short);
            return sample_name_short_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample names and sample name abbreviations
    def get_sampleNamesAndAbbreviations_experimentIDAndSampleTypeAndTimePointAndDilution(experiment_id_I,sample_type_I,tp,dilution_I,exp_type_I=5):
        '''Querry sample name and sample abbreviation that are used from
        the experimentfor specific time-points and dilutions'''
        try:
            sample_name_abbreviation = self.session.query(sample.sample_name,
                    sample_description.sample_name_abbreviation).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.sample_name.like(experiment.sample_name),
                    data_stage01_isotopomer_MQResultsTable.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    sample.sample_name.like(experiment.sample_name),
                    sample.sample_type.like(sample_type_I),
                    sample.sample_dilution == dilution_I,
                    sample_description.sample_id.like(sample.sample_id),
                    sample_description.time_point.like(time_point_I)).group_by(
                    sample.sample_name).order_by(
                    sample.sample_name).all();
            sample_name_O = [];
            sample_name_abbreviation_O = [];
            for sn in sample_name_abbreviation:
                sample_name_O.append(sn.sample_name);
                sample_name_abbreviation_O.append(sn.sample_name_abbreviation);
            return sample_name_O, sample_name_abbreviation_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample name short from data_stage01_isotopomer_mqresultstable
    def get_sampleNameShort_experimentIDAndSampleType(self,experiment_id_I,sample_type_I,exp_type_I=5):
        '''Querry sample name short that are used from
        the experiment'''
        try:
            sample_name_short = self.session.query(sample_description.sample_name_short).filter(
                    sample.sample_type.like(sample_type_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    sample_description.sample_name_short).order_by(
                    sample_description.sample_name_short.asc()).all();
            sample_name_short_O = [];
            for sns in sample_name_short: sample_name_short_O.append(sns.sample_name_short);
            return sample_name_short_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameShort_experimentIDAndSampleName(self,experiment_id_I,sample_name_I,exp_type_I=5):
        '''Querry sample name short that are used from
        the experiment'''
        try:
            sample_name_short = self.session.query(sample_description.sample_name_short).filter(
                    sample.sample_name.like(sample_name_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    sample_description.sample_name_short).all();
            sample_name_short_O = sample_name_short[0];
            return sample_name_short_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample name abbreviations from data_stage01_isotopomer_mqresultstable
    def get_sampleNameAbbreviations_experimentID(self,experiment_id_I,exp_type_I=5):
        '''Querry sample name abbreviations that are used from
        the experiment'''
        try:
            sample_name_abbreviations = self.session.query(sample_description.sample_name_abbreviation).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            for sna in sample_name_abbreviations: sample_name_abbreviations_O.append(sna.sample_name_abbreviation);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndSampleType(self,experiment_id_I,sample_type_I,exp_type_I=5):
        '''Querry sample name abbreviations that are used from
        the experiment'''
        try:
            sample_name_abbreviations = self.session.query(sample_description.sample_name_abbreviation).filter(
                    sample.sample_type.like(sample_type_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.id.like(experiment_id_I),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            for sna in sample_name_abbreviations: sample_name_abbreviations_O.append(sna.sample_name_abbreviation);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndSampleName(self,experiment_id_I,sample_name_I,exp_type_I=5):
        '''Querry sample name abbreviations that are used from
        the experiment by sample name'''
        try:
            sample_name_abbreviations = self.session.query(sample_description.sample_name_abbreviation).filter(
                    sample.sample_name.like(sample_name_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            for sna in sample_name_abbreviations: sample_name_abbreviations_O.append(sna.sample_name_abbreviation);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePointAndDilution(self,experiment_id_I,sample_type_I,time_point_I,dilution_I,exp_type_I=5):
        '''Querry sample name abbreviations that are used from
        the experiment for specific time-points and dilutions'''
        try:
            sample_name_abbreviations = self.session.query(
                    sample_description.sample_name_abbreviation).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.sample_name.like(experiment.sample_name),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    sample.sample_name.like(experiment.sample_name),
                    sample.sample_type.like(sample_type_I),
                    sample.sample_dilution == dilution_I,
                    sample_description.sample_id.like(sample.sample_id),
                    sample_description.time_point.like(time_point_I)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation).all();
            sample_name_abbreviations_O = [];
            for sn in sample_name_abbreviations:
                sample_name_abbreviations_O.append(sn[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    # query dilutions from data_stage01_isotopomer_mqresultstable
    def get_sampleDilution_experimentIDAndSampleID(self,experiment_id_I,sample_id_I,exp_type_I=5):
        '''Querry dilutions that are used from the experiment'''
        try:
            sample_dilutions = self.session.query(sample.sample_dilution).filter(
                    sample.sample_id.like(sample_id_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    sample.sample_dilution).order_by(
                    sample.sample_dilution.asc()).all();
            sample_dilutions_O = [];
            for sd in sample_dilutions: sample_dilutions_O.append(sd.sample_dilution);
            return sample_dilutions_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleDilution_experimentIDAndSampleNameAbbreviation(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I=5):
        '''Querry dilutions that are used from the experiment'''
        try:
            sample_dilutions = self.session.query(sample.sample_dilution).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    sample.sample_dilution).order_by(
                    sample.sample_dilution.asc()).all();
            sample_dilutions_O = [];
            for sd in sample_dilutions: sample_dilutions_O.append(sd.sample_dilution);
            return sample_dilutions_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleDilution_experimentIDAndTimePoint(self,experiment_id_I,time_point_I,exp_type_I=5):
        '''Querry dilutions that are used from the experiment'''
        try:
            sample_dilutions = self.session.query(sample.sample_dilution).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(sample.sample_name),
                    data_stage01_isotopomer_MQResultsTable.sample_name.like(experiment.sample_name),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.time_point.like(time_point_I)).group_by(
                    sample.sample_dilution).order_by(
                    sample.sample_dilution.asc()).all();
            sample_dilutions_O = [];
            for sd in sample_dilutions: sample_dilutions_O.append(sd.sample_dilution);
            return sample_dilutions_O;
        except SQLAlchemyError as e:
            print(e);
    # query time points from data_stage01_isotopomer_mqresultstable
    def get_timePoint_experimentIDAndSampleNameAbbreviation(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I=5):
        '''Querry time points that are used from the experiment and sample name abbreviation'''
        try:
            time_points = self.session.query(sample_description.time_point).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    sample_description.time_point).order_by(
                    sample_description.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_experimentIDAndSampleName(self,experiment_id_I,sample_name_I,exp_type_I=5):
        '''Querry time points that are used from the experiment and sample name'''
        try:
            time_points = self.session.query(sample_description.time_point).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(sample_name_I),
                    experiment.sample_name.like(sample.sample_name),
                    data_stage01_isotopomer_MQResultsTable.sample_name.like(experiment.sample_name),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.time_point).order_by(
                    sample_description.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_experimentID(self,experiment_id_I,exp_type_I=5):
        '''Querry time points that are used from the experiment and sample name'''
        try:
            time_points = self.session.query(sample_description.time_point).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(sample.sample_name),
                    data_stage01_isotopomer_MQResultsTable.sample_name.like(experiment.sample_name),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.time_point).order_by(
                    sample_description.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # query component names from data_stage01_isotopomer_mqresultstable
    def get_componentsNames_experimentIDAndSampleID(self,experiment_id_I,sample_id_I,exp_type_I=5):
        '''Querry component names that are used and are not IS from
        the experiment and sample_id'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_MQResultsTable.component_name).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),                   
                    data_stage01_isotopomer_MQResultsTable.is_.is_(False),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name)).group_by(
                    data_stage01_isotopomer_MQResultsTable.component_name).order_by(
                    data_stage01_isotopomer_MQResultsTable.component_name.asc()).all();
            component_names_O = [];
            for cn in component_names: component_names_O.append(cn.component_name);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentsNames_experimentIDAndSampleNameAbbreviation(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I=5):
        '''Querry component names that are used from
        the experiment and sample_name_abbreviation'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_MQResultsTable.component_name).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name),                   
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),                   
                    data_stage01_isotopomer_MQResultsTable.is_.is_(False)).group_by(
                    data_stage01_isotopomer_MQResultsTable.component_name).order_by(
                    data_stage01_isotopomer_MQResultsTable.component_name.asc()).all();
            component_names_O = [];
            for cn in component_names: component_names_O.append(cn.component_name);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentsNames_experimentIDAndSampleName(self,experiment_id_I,sample_name_I,exp_type_I=5):
        '''Querry component names that are used and not internal standards from
        the experiment and sample_name'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_MQResultsTable.component_name).filter(
                    experiment.sample_name.like(sample_name_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name),                   
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),                   
                    data_stage01_isotopomer_MQResultsTable.is_.is_(False)).group_by(
                    data_stage01_isotopomer_MQResultsTable.component_name).order_by(
                    data_stage01_isotopomer_MQResultsTable.component_name.asc()).all();
            component_names_O = [];
            for cn in component_names: component_names_O.append(cn.component_name);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query component group names from data_stage01_isotopomer_mqresultstable
    def get_componentGroupNames_sampleName(self,sample_name_I):
        '''Querry component group names that are used from the sample name
        NOTE: intended to be used within a for loop'''
        try:
            component_group_names = self.session.query(data_stage01_isotopomer_MQResultsTable.component_group_name).filter(
                    data_stage01_isotopomer_MQResultsTable.sample_name.like(sample_name_I)).group_by(
                    data_stage01_isotopomer_MQResultsTable.component_group_name).order_by(
                    data_stage01_isotopomer_MQResultsTable.component_group_name.asc()).all();
            component_group_names_O = [];
            for cgn in component_group_names: component_group_names_O.append(cgn.component_group_name);
            return component_group_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentGroupName_experimentIDAndComponentName(self,experiment_id_I,component_name_I,exp_type_I=5):
        '''Querry component group names that are used from the component name
        NOTE: intended to be used within a for loop'''
        try:
            component_group_name = self.session.query(data_stage01_isotopomer_MQResultsTable.component_group_name).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name),
                    data_stage01_isotopomer_MQResultsTable.component_name.like(component_name_I)).group_by(
                    data_stage01_isotopomer_MQResultsTable.component_group_name).all();
            if len(component_group_name)>1:
                print('more than 1 component_group_name retrieved per component_name')
            component_group_name_O = component_group_name[0];
            return component_group_name_O;
        except SQLAlchemyError as e:
            print(e);
    # query component names, group names, intensity,
    #   precursor formula, product formula, precursor mass, product mass
    def get_componentsNamesAndData_experimentIDAndSampleNameAndMSMethodType(self,experiment_id_I,sample_name_I,ms_methodtype_I,exp_type_I=5):
        '''Querry component names, group names, fragment formula, and fragment mass
        that are used the experiment and sample_name'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_MQResultsTable.component_name,
                    data_stage01_isotopomer_MQResultsTable.component_group_name,
                    data_stage01_isotopomer_MQResultsTable.height, #peak height
                    MS_components.precursor_formula,
                    MS_components.precursor_exactmass,
                    MS_components.product_formula,
                    MS_components.product_exactmass).filter(
                    data_stage01_isotopomer_MQResultsTable.sample_name.like(sample_name_I),               
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_isotopomer_MQResultsTable.sample_name),
                    MS_components.component_name.like(data_stage01_isotopomer_MQResultsTable.component_name),
                    MS_components.ms_methodtype.like(ms_methodtype_I)).group_by(
                    data_stage01_isotopomer_MQResultsTable.component_name).order_by(
                    data_stage01_isotopomer_MQResultsTable.component_name.asc()).all();
            component_names_O = [];
            component_group_names_O = [];
            intensities_O = [];
            precursor_formulas_O = [];
            precursor_masses_O = [];
            product_formulas_O = [];
            product_masses_O = [];
            for cn in component_names:
                component_names_O.append(cn.component_name);
                component_group_names_O.append(cn. component_group_name);
                intensities_O.append(cn.height);
                precursor_formulas_O.append(cn.precursor_formula);
                precursor_masses_O.append(cn.precursor_exactmass);
                product_formulas_O.append(cn.product_formula);
                product_masses_O.append(cn.product_exactmass);
            return component_names_O, component_group_names_O, intensities_O,\
                    precursor_formulas_O, precursor_masses_O, product_formulas_O, product_masses_O;
        except SQLAlchemyError as e:
            print(e);
    # query component names, group names, precursor formula, product formula, precursor mass, product mass
    def get_componentsNamesAndOther_experimentIDAndSampleNameAndMSMethodTypeAndTimePointAndDilution(self,experiment_id_I,sample_name_abbreviation_I,ms_methodtype_I,time_point_I,dilution_I,exp_type_I=5):
        '''Querry component names, group names, fragment formula, and fragment mass
        that are used the experiment'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_MQResultsTable.component_name,
                    data_stage01_isotopomer_MQResultsTable.component_group_name,
                    MS_components.precursor_formula,
                    MS_components.precursor_exactmass,
                    MS_components.product_formula,
                    MS_components.product_exactmass).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.time_point.like(time_point_I),
                    sample.sample_id.like(sample_description.sample_id),
                    sample.sample_dilution == dilution_I,
                    experiment.sample_name.like(sample.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.sample_name.like(experiment.sample_name),               
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    MS_components.component_name.like(data_stage01_isotopomer_MQResultsTable.component_name),
                    MS_components.ms_methodtype.like(ms_methodtype_I)).group_by(
                    data_stage01_isotopomer_MQResultsTable.component_name,
                    data_stage01_isotopomer_MQResultsTable.component_group_name,
                    MS_components.precursor_formula,
                    MS_components.precursor_exactmass,
                    MS_components.product_formula,
                    MS_components.product_exactmass).order_by(
                    data_stage01_isotopomer_MQResultsTable.component_name.asc()).all();
            component_names_O = [];
            component_group_names_O = [];
            precursor_formulas_O = [];
            precursor_masses_O = [];
            product_formulas_O = [];
            product_masses_O = [];
            if not component_names: 
                print('No component information found for:');
                print('experiment_id\tsample_name_abbreviation\tms_methodtype\ttime_point,dilution');
                print(experiment_id_I,sample_name_abbreviation_I,ms_methodtype_I,time_point_I,dilution_I);
                return component_names_O, component_group_names_O,\
                        precursor_formulas_O, precursor_masses_O, product_formulas_O, product_masses_O;
            else:
                for cn in component_names:
                    component_names_O.append(cn.component_name);
                    component_group_names_O.append(cn. component_group_name);
                    precursor_formulas_O.append(cn.precursor_formula);
                    precursor_masses_O.append(cn.precursor_exactmass);
                    product_formulas_O.append(cn.product_formula);
                    product_masses_O.append(cn.product_exactmass);
                return component_names_O, component_group_names_O,\
                        precursor_formulas_O, precursor_masses_O, product_formulas_O, product_masses_O;
        except SQLAlchemyError as e:
            print(e);
    # query component names, group names, precursor formula, product formula, precursor mass, product mass
    def get_componentsNamesAndOther_experimentIDAndSampleNameAndMSMethodTypeAndTimePointAndDilutionAndMetID(self,experiment_id_I,sample_name_abbreviation_I,ms_methodtype_I,time_point_I,dilution_I,met_id_I,exp_type_I=5):
        '''Querry component names, group names, fragment formula, and fragment mass
        that are used the experiment'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_MQResultsTable.component_name,
                    data_stage01_isotopomer_MQResultsTable.component_group_name,
                    MS_components.precursor_formula,
                    MS_components.precursor_exactmass,
                    MS_components.product_formula,
                    MS_components.product_exactmass).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.time_point.like(time_point_I),
                    sample.sample_id.like(sample_description.sample_id),
                    sample.sample_dilution == dilution_I,
                    experiment.sample_name.like(sample.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage01_isotopomer_MQResultsTable.sample_name.like(experiment.sample_name),      
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True),
                    MS_components.component_name.like(data_stage01_isotopomer_MQResultsTable.component_name),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.met_id.like(met_id_I)).group_by(
                    data_stage01_isotopomer_MQResultsTable.component_name,
                    data_stage01_isotopomer_MQResultsTable.component_group_name,
                    MS_components.precursor_formula,
                    MS_components.precursor_exactmass,
                    MS_components.product_formula,
                    MS_components.product_exactmass).order_by(
                    data_stage01_isotopomer_MQResultsTable.component_name.asc()).all();
            component_names_O = [];
            component_group_names_O = [];
            precursor_formulas_O = [];
            precursor_masses_O = [];
            product_formulas_O = [];
            product_masses_O = [];
            #component_names_O = None;
            #component_group_names_O = None;
            #precursor_formulas_O = None;
            #precursor_masses_O = None;
            #product_formulas_O = None;
            #product_masses_O = None;
            if not component_names: 
                print('No component information found for:');
                print('experiment_id\tsample_name_abbreviation\tms_methodtype\ttime_point\tdilution\tmet_id');
                print(experiment_id_I,sample_name_abbreviation_I,ms_methodtype_I,time_point_I,dilution_I,met_id_I);
                return component_names_O, component_group_names_O,\
                        precursor_formulas_O, precursor_masses_O, product_formulas_O, product_masses_O;
            else:
                for cn in component_names:
                    component_names_O.append(cn.component_name);
                    component_group_names_O.append(cn. component_group_name);
                    precursor_formulas_O.append(cn.precursor_formula);
                    precursor_masses_O.append(cn.precursor_exactmass);
                    product_formulas_O.append(cn.product_formula);
                    product_masses_O.append(cn.product_exactmass);
                #component_names_O=component_names[0][0];
                #component_group_names_O=component_names[0][1];
                #precursor_formulas_O=component_names[0][2];
                #precursor_masses_O=component_names[0][3];
                #product_formulas_O=component_names[0][4];
                #product_masses_O=component_names[0][5];
                return component_names_O, component_group_names_O,\
                        precursor_formulas_O, precursor_masses_O, product_formulas_O, product_masses_O;
        except SQLAlchemyError as e:
            print(e);
    # query physiological parameters from data_stage01_isotopomer_mqresultstable
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
    def get_CVSAndCVSUnitsAndODAndDilAndDilUnits_sampleNameShort(self,sample_name_short_I):
        '''Querry culture volume sampled, culture volume sampled units, and OD600 from sample name
        NOTE: intended to be used within a for loop'''
        try:
            physiologicalParameters = self.session.query(sample_physiologicalParameters.culture_volume_sampled,
                    sample_physiologicalParameters.culture_volume_sampled_units,
                    sample_physiologicalParameters.od600,
                    sample_description.reconstitution_volume,
                    sample_description.reconstitution_volume_units).filter(
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
    # query data from data_stage01_isotopomer_mqresultstable
    def get_concAndConcUnits_sampleNameAndComponentName(self,sample_name_I,component_name_I):
        '''Querry data (i.e. concentration, area/peak height ratio) from sample name and component name
        NOTE: intended to be used within a for loop'''
        # check for absolute or relative quantitation (i.e. area/peak height ratio)
        try:
            use_conc = self.session.query(data_stage01_isotopomer_MQResultsTable.use_calculated_concentration).filter(
                    data_stage01_isotopomer_MQResultsTable.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_MQResultsTable.component_name.like(component_name_I),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True)).all();
            if use_conc:
                use_conc_O = use_conc[0][0];
            else: 
                use_conc_O = None;
        except SQLAlchemyError as e:
            print(e);

        if use_conc_O:
            try:
                data = self.session.query(data_stage01_isotopomer_MQResultsTable.calculated_concentration,
                        data_stage01_isotopomer_MQResultsTable.conc_units).filter(
                        data_stage01_isotopomer_MQResultsTable.sample_name.like(sample_name_I),
                        data_stage01_isotopomer_MQResultsTable.component_name.like(component_name_I),
                        data_stage01_isotopomer_MQResultsTable.used_.is_(True)).all();
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
                    data = self.session.query(data_stage01_isotopomer_MQResultsTable.area_ratio).filter(
                            data_stage01_isotopomer_MQResultsTable.sample_name.like(sample_name_I),
                            data_stage01_isotopomer_MQResultsTable.component_name.like(component_name_I),
                            data_stage01_isotopomer_MQResultsTable.used_.is_(True)).all();
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
                    data = self.session.query(data_stage01_isotopomer_MQResultsTable.height_ratio).filter(
                            data_stage01_isotopomer_MQResultsTable.sample_name.like(sample_name_I),
                            data_stage01_isotopomer_MQResultsTable.component_name.like(component_name_I),
                            data_stage01_isotopomer_MQResultsTable.used_.is_(True)).all();
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
        '''Querry peakHeight from sample name and component name
        NOTE: intended to be used within a for loop'''
        try:
            data = self.session.query(data_stage01_isotopomer_MQResultsTable.height).filter(
                    data_stage01_isotopomer_MQResultsTable.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_MQResultsTable.component_name.like(component_name_I),
                    data_stage01_isotopomer_MQResultsTable.used_.is_(True)).all();
            if data:
                height_O = data[0][0];
            else: 
                height_O = None;
            return height_O
        except SQLAlchemyError as e:
            print(e);
    # query if used
    def get_used_sampleNameAndComponentName(self,sample_name_I,component_name_I):
        '''Querry used from sample name and component name
        NOTE: intended to be used within a for loop'''
        try:
            data = self.session.query(data_stage01_isotopomer_MQResultsTable.used_).filter(
                    data_stage01_isotopomer_MQResultsTable.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_MQResultsTable.component_name_name.like(component_name_name_I)).all();
            if data:
                used_O = data[0];
            else: used_O = None;
            return used_O;
        except SQLAlchemyError as e:
            print(e);
    # delet data from data_stage01_isotopomer_mqresultstable
    def delete_row_sampleName(self,sampleNames_I):
        '''Delete specific samples from an experiment by their sample name'''
        deletes = [];
        for d in sampleNames_I:
            try:
                delete = self.session.query(data_stage01_isotopomer_MQResultsTable).filter(
                        data_stage01_isotopomer_MQResultsTable.sample_name.like(d['sample_name'])).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    # query precursor and product formulas from MS_components
    def get_precursorAndProductFormulas_metID(self,met_id_I,ms_mode_I,ms_methodtype_I):
        '''Querry product formulas for the ms_mode and ms_methodtype experiment'''
        try:
            component_names = self.session.query(MS_components.precursor_formula,
                    MS_components.product_formula).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.ms_mode.like(ms_mode_I)).group_by(
                    MS_components.precursor_formula,
                    MS_components.product_formula).order_by(
                    MS_components.precursor_formula.asc(),
                    MS_components.product_formula.asc()).all();
            precursor_formulas_O = [];
            product_formulas_O = [];
            if not component_names: exit('bad query result: get_productFormulas_metID');
            for cn in component_names:
                if cn.product_formula: # skip unknown fragments
                    precursor_formulas_O.append(cn.precursor_formula);
                    product_formulas_O.append(cn.product_formula);
            return precursor_formulas_O, product_formulas_O;
        except SQLAlchemyError as e:
            print(e);
    # query precursor formula from MS_components
    def get_precursorFormula_metID(self,met_id_I,ms_mode_I,ms_methodtype_I):
        '''Querry precursor formulas for the ms_mode and ms_methodtype experiment'''
        try:
            component_names = self.session.query(MS_components.precursor_formula).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.ms_mode.like(ms_mode_I)).group_by(
                    MS_components.precursor_formula).all();
            precursor_formula_O = None;
            if not component_names: exit('bad query result: get_precursorFormula_metID');
            for cn in component_names:
                precursor_formula_O = cn[0];
            return precursor_formula_O;
        except SQLAlchemyError as e:
            print(e);
    def get_precursorFormulaAndProductFormulaAndCMaps_metID(self,met_id_I,ms_mode_I,ms_methodtype_I):
        '''Querry precursor formulas for the ms_mode and ms_methodtype experiment'''
        try:
            component_names = self.session.query(MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.precursor_fragment,
                    MS_components.product_fragment).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.ms_mode.like(ms_mode_I)).group_by(
                    MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.precursor_fragment,
                    MS_components.product_fragment).all();
            data_O = {};
            if not component_names: exit('bad query result: get_precursorFormulaAndProductFormulaAndCMaps_metID');
            for cn in component_names:
                data_O[cn.product_formula] = cn.product_fragment;
                data_O[cn.precursor_formula] = cn.precursor_fragment;
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_precursorFormulaAndProductFormulaAndCMapsAndPositions_metID(self,met_id_I,ms_mode_I,ms_methodtype_I):
        '''Querry precursor formulas for the ms_mode and ms_methodtype experiment'''
        try:
            component_names = self.session.query(MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.precursor_fragment,
                    MS_components.product_fragment,
                    MS_components.precursor_fragment_elements,
                    MS_components.product_fragment_elements).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.ms_mode.like(ms_mode_I)).group_by(
                    MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.precursor_fragment,
                    MS_components.product_fragment,
                    MS_components.precursor_fragment_elements,
                    MS_components.product_fragment_elements).all();
            data_O = {};
            if not component_names: exit('bad query result: get_precursorFormulaAndProductFormulaAndCMaps_metID');
            for cn in component_names:
                data_O[cn.product_formula] = {'fragment':cn.product_fragment,
                                              'fragment_elements':cn.product_fragment_elements};
                data_O[cn.precursor_formula] = {'fragment':cn.precursor_fragment,
                                              'fragment_elements':cn.precursor_fragment_elements};
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_precursorFormulaAndProductFormula_metID(self,met_id_I,ms_mode_I,ms_methodtype_I):
        '''Querry precursor formulas for the ms_mode and ms_methodtype experiment'''
        try:
            component_names = self.session.query(MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.q1_mass,
                    MS_components.q3_mass).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.ms_mode.like(ms_mode_I)).group_by(
                    MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.q1_mass,
                    MS_components.q3_mass).order_by(
                    MS_components.q1_mass.asc(),
                    MS_components.q3_mass.asc(),
                    MS_components.precursor_formula.desc(),
                    MS_components.product_formula.desc()).all();
            data_O = {};
            product_formula_O = None;
            precursor_formula_O = None;
            if not component_names: exit('bad query result: get_precursorFormulaAndProductFormula');
            # only need the first precursor and product formulas (i.e. monoisotopic)
            product_formula_O = component_names[0].product_formula;
            precursor_formula_O = component_names[0].precursor_formula;
            for cn in component_names:
                data_O[cn.product_formula] = cn.q1_mass;
                data_O[cn.precursor_formula] = cn.q3_mass;
            return precursor_formula_O,product_formula_O;
        except SQLAlchemyError as e:
            print(e);

    # query sample names from data_stage01_isotopomer_peakData
    def get_sampleNames_experimentIDAndSampleType_peakData(self,experiment_id_I,sample_type_I):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_isotopomer_peakData.sample_name).filter(
                    data_stage01_isotopomer_peakData.experiment_id.like(experiment_id_I),
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(data_stage01_isotopomer_peakData.sample_name),
                    sample.sample_name.like( experiment.sample_name),
                    sample.sample_type.like(sample_type_I)).group_by(
                    data_stage01_isotopomer_peakData.sample_name).order_by(
                    data_stage01_isotopomer_peakData.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleTypeAndSampleNameAbbreviation_peakData(self,experiment_id_I,sample_type_I,sample_name_abbreviation_I):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_isotopomer_peakData.sample_name).filter(
                    data_stage01_isotopomer_peakData.experiment_id.like(experiment_id_I),
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(data_stage01_isotopomer_peakData.sample_name),
                    sample.sample_name.like( experiment.sample_name),
                    sample.sample_type.like(sample_type_I),
                    sample_description.sample_id.like(sample.sample_id),
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I)).group_by(
                    data_stage01_isotopomer_peakData.sample_name).order_by(
                    data_stage01_isotopomer_peakData.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample name abbreviations from data_stage01_isotopomer_peakData
    def get_sampleNameAbbreviationsAndOther_experimentIDAndSampleName_peakData(self,experiment_id_I,sample_name_I):
        '''Querry sample name abbreviations, time points and replicate numbers from
        the experiment by sample name'''
        try:
            sample_name_abbreviations = self.session.query(sample_description.sample_name_abbreviation,
                    sample_description.time_point,
                    sample_description.sample_replicate).filter(
                    data_stage01_isotopomer_peakData.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakData.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakData.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.sample_name_abbreviation,
                    sample_description.time_point,
                    sample_description.sample_replicate).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = None;
            time_points_O = None;
            sample_replicates_O = None;
            if not sample_name_abbreviations: exit('bad query result: get_sampleNameAbbreviationsAndOther_experimentIDAndSampleName_peakData');
            sample_name_abbreviations_O=sample_name_abbreviations[0][0];
            time_points_O=sample_name_abbreviations[0][1];
            sample_replicates_O=sample_name_abbreviations[0][2];
            return sample_name_abbreviations_O,time_points_O,sample_replicates_O;
        except SQLAlchemyError as e:
            print(e);
    # query met_id, precursor formula from data_stage01_isotopomer_peakData
    def get_metIDAndPrecursorFormulaAndScanType_experimentIDAndSampleName_peakData(self,experiment_id_I,sample_name_I):
        '''Querry met_id, precursor formula that are used for the experiment'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_peakData.met_id,
                    data_stage01_isotopomer_peakData.precursor_formula,
                    data_stage01_isotopomer_peakData.scan_type).filter(
                    data_stage01_isotopomer_peakData.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakData.experiment_id.like(experiment_id_I)).group_by(
                    data_stage01_isotopomer_peakData.met_id,
                    data_stage01_isotopomer_peakData.precursor_formula,
                    data_stage01_isotopomer_peakData.scan_type).order_by(
                    data_stage01_isotopomer_peakData.met_id.asc(),
                    data_stage01_isotopomer_peakData.precursor_formula).all();
            met_ids_O = [];
            precursor_formulas_O = [];
            scan_type_O = [];
            if not component_names: exit('bad query result: get_metIDAndPrecursorFormula_experimentIDAndSampleName_peakData');
            for cn in component_names:
                met_ids_O.append(cn.met_id);
                precursor_formulas_O.append(cn.precursor_formula);
                scan_type_O.append(cn.scan_type);
            return met_ids_O, precursor_formulas_O, scan_type_O;
        except SQLAlchemyError as e:
            print(e);
    def get_scanType_experimentIDAndSampleName_peakData(self,experiment_id_I,sample_name_I):
        '''Querry scan type that are used for the experiment'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_peakData.scan_type).filter(
                    data_stage01_isotopomer_peakData.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakData.experiment_id.like(experiment_id_I)).group_by(
                    data_stage01_isotopomer_peakData.scan_type).order_by(
                    data_stage01_isotopomer_peakData.scan_type.asc()).all();
            scan_type_O = [];
            if not component_names: exit('bad query result: get_metIDAndPrecursorFormula_experimentIDAndSampleName_peakData');
            for cn in component_names:
                scan_type_O.append(cn[0]);
            return scan_type_O;
        except SQLAlchemyError as e:
            print(e);
    def get_metIDAndPrecursorFormula_experimentIDAndSampleNameAndScanType_peakData(self,experiment_id_I,sample_name_I,scan_type_I):
        '''Querry met_id, precursor formula that are used for the experiment'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_peakData.met_id,
                    data_stage01_isotopomer_peakData.precursor_formula).filter(
                    data_stage01_isotopomer_peakData.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakData.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakData.scan_type.like(scan_type_I)).group_by(
                    data_stage01_isotopomer_peakData.met_id,
                    data_stage01_isotopomer_peakData.precursor_formula).order_by(
                    data_stage01_isotopomer_peakData.met_id.asc(),
                    data_stage01_isotopomer_peakData.precursor_formula).all();
            met_ids_O = [];
            precursor_formulas_O = [];
            if not component_names: exit('bad query result: get_metIDAndPrecursorFormula_experimentIDAndSampleNameAndScanType_peakData');
            for cn in component_names:
                met_ids_O.append(cn.met_id);
                precursor_formulas_O.append(cn.precursor_formula);
            return met_ids_O, precursor_formulas_O;
        except SQLAlchemyError as e:
            print(e);
    def get_metIDAndPrecursorFormula_experimentIDAndSampleNameAndScanTypeAndMetID_peakData(self,experiment_id_I,sample_name_I,scan_type_I,met_id_I):
        '''Querry met_id, precursor formula that are used for the experiment'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_peakData.met_id,
                    data_stage01_isotopomer_peakData.precursor_formula).filter(
                    data_stage01_isotopomer_peakData.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakData.met_id.like(met_id_I),
                    data_stage01_isotopomer_peakData.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakData.scan_type.like(scan_type_I)).group_by(
                    data_stage01_isotopomer_peakData.met_id,
                    data_stage01_isotopomer_peakData.precursor_formula).order_by(
                    data_stage01_isotopomer_peakData.met_id.asc(),
                    data_stage01_isotopomer_peakData.precursor_formula).all();
            met_ids_O = [];
            precursor_formulas_O = [];
            if not component_names: exit('bad query result: get_metIDAndPrecursorFormula_experimentIDAndSampleNameAndScanType_peakData');
            for cn in component_names:
                met_ids_O.append(cn.met_id);
                precursor_formulas_O.append(cn.precursor_formula);
            return met_ids_O, precursor_formulas_O;
        except SQLAlchemyError as e:
            print(e);
    # query data from data_stage01_isotopomer_peakData
    def get_data_experimentIDAndSampleNameAndMetIDAndPrecursorFormulaAndScanType_peakData(self,experiment_id_I,sample_name_I,met_id_I,precursor_formula_I,scan_type_I):
        '''Querry peak data for a specific experiment_id, sample_name, met_id, and precursor_formula'''
        try:
            data = self.session.query(data_stage01_isotopomer_peakData.mass,
                    data_stage01_isotopomer_peakData.mass_units,
                    data_stage01_isotopomer_peakData.intensity,
                    data_stage01_isotopomer_peakData.intensity_units).filter(
                    data_stage01_isotopomer_peakData.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakData.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakData.met_id.like(met_id_I),
                    data_stage01_isotopomer_peakData.precursor_formula.like(precursor_formula_I),
                    data_stage01_isotopomer_peakData.scan_type.like(scan_type_I)).order_by(
                    data_stage01_isotopomer_peakData.mass.asc()).all();
            data_O = {};
            if not data: exit('bad query result: get_data_experimentIDAndSampleNameAndMetIDAndPrecursorFormula_peakData');
            for d in data:
                data_O[d.mass] = d.intensity;
            return data_O;
        except SQLAlchemyError as e:
            print(e);
            
    # query sample names from data_stage01_isotopomer_peakSpectrum
    def get_sampleNames_experimentIDAndSampleType_peakSpectrum(self,experiment_id_I,sample_type_I):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_isotopomer_peakSpectrum.sample_name).filter(
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.sample_type.like(sample_type_I)).group_by(
                    data_stage01_isotopomer_peakSpectrum.sample_name).order_by(
                    data_stage01_isotopomer_peakSpectrum.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndSampleTypeAndSampleNameAbbreviation_peakSpectrum(self,experiment_id_I,sample_type_I,sample_name_abbreviation_I):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_isotopomer_peakSpectrum.sample_name).filter(
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_peakSpectrum.sample_name_abbreviation.like(sample_name_abbreviation_I)).group_by(
                    data_stage01_isotopomer_peakSpectrum.sample_name).order_by(
                    data_stage01_isotopomer_peakSpectrum.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAndDilution_experimentIDAndTimePointAndSampleNameAbbreviationAndScanType_peakSpectrum(self,experiment_id_I,time_point_I,sample_name_abbreviation_I,scan_type_I,sample_replicate_I):
        '''Querry sample name and dilution from the experiment
        by time-point, sample name abbreviation, scan type, and replicate numbers'''
        try:
            sample_name = self.session.query(data_stage01_isotopomer_peakSpectrum.sample_name,
                    sample.sample_dilution).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_peakSpectrum.time_point.like(time_point_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.replicate_number == sample_replicate_I,
                    data_stage01_isotopomer_peakSpectrum.used_,
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample.sample_name)).group_by(
                    data_stage01_isotopomer_peakSpectrum.sample_name,
                    sample.sample_dilution).all();
            sample_name_O = None;
            dilution_O = None;
            if not sample_name: 
                print('no sample name and dilution found for experiment_id\ttime_point\tsample_name_abbreviation\tscan_type\tsample_replicate');
                print((experiment_id_I + '\t'+ time_point_I + '\t'+ sample_name_abbreviation_I + '\t'+ scan_type_I + '\t'+ str(sample_replicate_I)));
            else:
                sample_name_O = sample_name[0][0];
                dilution_O = sample_name[0][1];
            return sample_name_O,dilution_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample name abbreviations from data_stage01_isotopomer_peakSpectrum
    def get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePoint_peakSpectrum(self,experiment_id_I,sample_type_I,time_point_I):
        '''Querry sample name abbreviations from the experiment by sample type and time point'''
        try:
            sample_name_abbreviations = self.session.query(sample_description.sample_name_abbreviation).filter(
                    data_stage01_isotopomer_peakSpectrum.time_point.like(time_point_I),
                    data_stage01_isotopomer_peakSpectrum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_isotopomer_peakSpectrum.used_).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            if not sample_name_abbreviations: print(('no sample name abbreviations found for experiment: ' + experiment_id_I\
                + ' and time-point: ' + time_point_I + ' and sample type: ' + sample_type_I));
            else:
                for sna in sample_name_abbreviations:
                    sample_name_abbreviations_O.append(sna[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviationsAndTimePointAndReplicateNumber_experimentIDAndSampleName_peakSpectrum(self,experiment_id_I,sample_name_I):
        '''Querry sample name abbreviations, time points and replicate numbers from
        the experiment by sample name'''
        try:
            sample_name_abbreviations = self.session.query(sample_description.sample_name_abbreviation,
                    sample_description.time_point,
                    sample_description.sample_replicate).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.sample_name_abbreviation,
                    sample_description.time_point,
                    sample_description.sample_replicate).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = None;
            time_points_O = None;
            sample_replicates_O = None;
            if not sample_name_abbreviations: exit('bad query result: get_sampleNameAbbreviationsAndOther_experimentIDAndSampleName_peakSpectrum');
            sample_name_abbreviations_O=sample_name_abbreviations[0][0];
            time_points_O=sample_name_abbreviations[0][1];
            sample_replicates_O=sample_name_abbreviations[0][2];
            return sample_name_abbreviations_O,time_points_O,sample_replicates_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviationsAndOther_experimentIDAndSampleName_peakSpectrum(self,experiment_id_I,sample_name_I):
        '''Querry sample name abbreviations, time points, dilutions, and replicate numbers from
        the experiment by sample name'''
        try:
            sample_name_abbreviations = self.session.query(sample_description.sample_name_abbreviation,
                    sample_description.time_point,
                    sample.sample_dilution,
                    sample_description.sample_replicate).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.sample_name_abbreviation,
                    sample_description.time_point,
                    sample.sample_dilution,
                    sample_description.sample_replicate).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = None;
            time_points_O = None;
            dilutions_O = None;
            sample_replicates_O = None;
            if not sample_name_abbreviations: exit('bad query result: get_sampleNameAbbreviationsAndOther_experimentIDAndSampleName_peakSpectrum');
            sample_name_abbreviations_O=sample_name_abbreviations[0][0];
            time_points_O=sample_name_abbreviations[0][1];
            dilutions_O=sample_name_abbreviations[0][2];
            sample_replicates_O=sample_name_abbreviations[0][3];
            return sample_name_abbreviations_O,time_points_O,dilutions_O,sample_replicates_O;
        except SQLAlchemyError as e:
            print(e);
    # query time_points from data_stage01_isotopomer_peakSpectrum
    def get_timePoints_experimentID_peakSpectrum(self,experiment_id_I):
        '''time points from the experiment'''
        try:
            timepoints = self.session.query(
                    sample_description.time_point).filter(
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_isotopomer_peakSpectrum.used_).group_by(
                    sample_description.time_point).order_by(
                    sample_description.time_point.asc()).all();
            time_points_O = [];
            sample_replicates_O = None;
            if not timepoints: print(('no time points found for experiment: ' + experiment_id_I));
            else:
                for tp in timepoints:
                    time_points_O.append(tp[0]);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # query met_id, precursor formula from data_stage01_isotopomer_peakSpectrum
    def get_metIDAndPrecursorFormulaAndScanType_experimentIDAndSampleName_peakSpectrum(self,experiment_id_I,sample_name_I):
        '''Querry met_id, precursor formula that are used for the experiment'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_peakSpectrum.met_id,
                    data_stage01_isotopomer_peakSpectrum.precursor_formula,
                    data_stage01_isotopomer_peakSpectrum.scan_type).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I)).group_by(
                    data_stage01_isotopomer_peakSpectrum.met_id,
                    data_stage01_isotopomer_peakSpectrum.precursor_formula,
                    data_stage01_isotopomer_peakSpectrum.scan_type).order_by(
                    data_stage01_isotopomer_peakSpectrum.met_id.asc(),
                    data_stage01_isotopomer_peakSpectrum.precursor_formula).all();
            met_ids_O = [];
            precursor_formulas_O = [];
            scan_type_O = [];
            if not component_names: exit('bad query result: get_metIDAndPrecursorFormula_experimentIDAndSampleName_peakSpectrum');
            for cn in component_names:
                met_ids_O.append(cn.met_id);
                precursor_formulas_O.append(cn.precursor_formula);
                scan_type_O.append(cn.scan_type);
            return met_ids_O, precursor_formulas_O, scan_type_O;
        except SQLAlchemyError as e:
            print(e);
    def get_metIDAndPrecursorFormula_experimentIDAndSampleNameAndScanType_peakSpectrum(self,experiment_id_I,sample_name_I,scan_type_I):
        '''Querry met_id, precursor formula that are used for the experiment'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_peakSpectrum.met_id,
                    data_stage01_isotopomer_peakSpectrum.precursor_formula).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I)).group_by(
                    data_stage01_isotopomer_peakSpectrum.met_id,
                    data_stage01_isotopomer_peakSpectrum.precursor_formula).order_by(
                    data_stage01_isotopomer_peakSpectrum.met_id.asc(),
                    data_stage01_isotopomer_peakSpectrum.precursor_formula).all();
            met_ids_O = [];
            precursor_formulas_O = [];
            if not component_names: exit('bad query result: get_metIDAndPrecursorFormula_experimentIDAndSampleNameAndScanType_peakSpectrum');
            for cn in component_names:
                met_ids_O.append(cn.met_id);
                precursor_formulas_O.append(cn.precursor_formula);
            return met_ids_O, precursor_formulas_O;
        except SQLAlchemyError as e:
            print(e);
    def get_metIDAndPrecursorFormulaAndMass_experimentIDAndSampleNameAndScanType_peakSpectrum(self,experiment_id_I,sample_name_I,scan_type_I):
        '''Querry met_id, precursor formula that are used for the experiment'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_peakSpectrum.met_id,
                    data_stage01_isotopomer_peakSpectrum.precursor_formula,
                    data_stage01_isotopomer_peakSpectrum.precursor_mass).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I)).group_by(
                    data_stage01_isotopomer_peakSpectrum.met_id,
                    data_stage01_isotopomer_peakSpectrum.precursor_formula,
                    data_stage01_isotopomer_peakSpectrum.precursor_mass).order_by(
                    data_stage01_isotopomer_peakSpectrum.met_id.asc(),
                    data_stage01_isotopomer_peakSpectrum.precursor_mass.asc(),
                    data_stage01_isotopomer_peakSpectrum.precursor_formula).all();
            met_ids_O = [];
            precursor_formulas_O = [];
            precursor_mass_O = [];
            if not component_names: exit('bad query result: get_metIDAndPrecursorFormulaAndMass_experimentIDAndSampleNameAndScanType_peakSpectrum');
            for cn in component_names:
                met_ids_O.append(cn.met_id);
                precursor_formulas_O.append(cn.precursor_formula);
                precursor_mass_O.append(cn.precursor_mass);
            return met_ids_O, precursor_formulas_O, precursor_mass_O;
        except SQLAlchemyError as e:
            print(e);
    def get_metID_experimentIDAndTimePointAndSampleNameAbbreviationAndScanTypeAndReplicate_peakSpectrum(self,experiment_id_I,time_point_I,sample_name_abbreviation_I,scan_type_I,sample_replicate_I):
        '''Querry met_ids that are used for the experiment        
        by time-point, sample name abbreviation, scan type, and replicate numbers'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_peakSpectrum.met_id).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_peakSpectrum.time_point.like(time_point_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.replicate_number == sample_replicate_I,
                    data_stage01_isotopomer_peakSpectrum.used_).group_by(
                    data_stage01_isotopomer_peakSpectrum.met_id).order_by(
                    data_stage01_isotopomer_peakSpectrum.met_id.asc()).all();
            met_ids_O = [];
            if not component_names:
                print('no met ids found for experiment_id\ttime_point\tsample_name_abbreviation\tscan_type\tsample_replicate');
                print((experiment_id_I + '\t'+ time_point_I + '\t'+ sample_name_abbreviation_I + '\t'+ scan_type_I + '\t'+ str(sample_replicate_I)));
            else:
                for cn in component_names:
                    met_ids_O.append(cn[0]);
            return met_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_metID_experimentIDAndSampleNameAndScanType_peakSpectrum(self,experiment_id_I,sample_name_I,scan_type_I):
        '''Querry met_ids that are used for the experiment'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_peakSpectrum.met_id).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I)).group_by(
                    data_stage01_isotopomer_peakSpectrum.met_id).order_by(
                    data_stage01_isotopomer_peakSpectrum.met_id.asc()).all();
            met_ids_O = [];
            if not component_names: exit('bad query result: get_metID_experimentIDAndSampleNameAndScanType_peakSpectrum');
            for cn in component_names:
                met_ids_O.append(cn[0]);
            return met_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_precursorFormulaAndMass_experimentIDAndTimePointAndSampleNameAbbreviationAndScanTypeAndReplicateAndMetID_peakSpectrum(self,experiment_id_I,time_point_I,sample_name_abbreviation_I,scan_type_I,sample_replicate_I,met_id_I):
        '''Querry met_ids that are used for the experiment        
        by time-point, sample name abbreviation, scan type, replicate numbers, and met_ids'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_peakSpectrum.precursor_formula,
                    data_stage01_isotopomer_peakSpectrum.precursor_mass).filter(
                    data_stage01_isotopomer_peakSpectrum.met_id.like(met_id_I),
                    data_stage01_isotopomer_peakSpectrum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_peakSpectrum.time_point.like(time_point_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.replicate_number == sample_replicate_I,
                    data_stage01_isotopomer_peakSpectrum.used_).group_by(
                    data_stage01_isotopomer_peakSpectrum.precursor_formula,
                    data_stage01_isotopomer_peakSpectrum.precursor_mass).order_by(
                    data_stage01_isotopomer_peakSpectrum.precursor_mass.asc(),
                    data_stage01_isotopomer_peakSpectrum.precursor_formula).all();
            precursor_formulas_O = [];
            precursor_mass_O = [];
            if not component_names:
                print('no precursor formula nor precursor mass found for experiment_id\ttime_point\tsample_name_abbreviation\tscan_type\tsample_replicate\tmet id');
                print((experiment_id_I + '\t'+ time_point_I + '\t'+ sample_name_abbreviation_I + '\t'+ scan_type_I + '\t'+ str(sample_replicate_I) + '\t'+ met_id_I));
            else:
                for cn in component_names:
                    precursor_formulas_O.append(cn.precursor_formula);
                    precursor_mass_O.append(cn.precursor_mass);
            return precursor_formulas_O, precursor_mass_O;
        except SQLAlchemyError as e:
            print(e);
    def get_precursorFormulaAndMass_experimentIDAndSampleNameAndMetIDAndScanType_peakSpectrum(self,experiment_id_I,sample_name_I,met_id_I,scan_type_I):
        '''Querry precursor formulas and masses that are used for the experiment'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_peakSpectrum.precursor_formula,
                    data_stage01_isotopomer_peakSpectrum.precursor_mass).filter(
                    data_stage01_isotopomer_peakSpectrum.met_id.like(met_id_I),
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I)).group_by(
                    data_stage01_isotopomer_peakSpectrum.precursor_formula,
                    data_stage01_isotopomer_peakSpectrum.precursor_mass).order_by(
                    data_stage01_isotopomer_peakSpectrum.precursor_mass.asc(),
                    data_stage01_isotopomer_peakSpectrum.precursor_formula).all();
            precursor_formulas_O = [];
            precursor_mass_O = [];
            if not component_names: exit('bad query result: get_precursorFormulaAndMass_experimentIDAndSampleNameAndScanType_peakSpectrum');
            for cn in component_names:
                precursor_formulas_O.append(cn.precursor_formula);
                precursor_mass_O.append(cn.precursor_mass);
            return precursor_formulas_O, precursor_mass_O;
        except SQLAlchemyError as e:
            print(e);
    # query scan types for data_stage01_peakSpectrum
    def get_scanType_experimentIDAndTimePointSampleNameAbbreviation_peakSpectrum(self,experiment_id_I,time_point_I,sample_name_abbreviation_I):
        '''Querry scan type that are used for the experiment by time-point and sample name abbreviation'''
        try:
            scantypes = self.session.query(data_stage01_isotopomer_peakSpectrum.scan_type).filter(
                    data_stage01_isotopomer_peakSpectrum.time_point.like(time_point_I),
                    data_stage01_isotopomer_peakSpectrum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.used_).group_by(
                    data_stage01_isotopomer_peakSpectrum.scan_type).order_by(
                    data_stage01_isotopomer_peakSpectrum.scan_type.asc()).all();
            scan_type_O = [];
            if not scantypes:
                print('no scan types found for experiment_id\ttime_point\tsample_name_abbreviation');
                print((experiment_id_I + '\t'+ time_point_I + '\t'+ sample_name_abbreviation_I));
            else:
                for st in scantypes:
                    scan_type_O.append(st[0]);
            return scan_type_O;
        except SQLAlchemyError as e:
            print(e);
    def get_scanType_experimentIDAndSampleName_peakSpectrum(self,experiment_id_I,sample_name_I):
        '''Querry scan type that are used for the experiment'''
        try:
            component_names = self.session.query(data_stage01_isotopomer_peakSpectrum.scan_type).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I)).group_by(
                    data_stage01_isotopomer_peakSpectrum.scan_type).order_by(
                    data_stage01_isotopomer_peakSpectrum.scan_type.asc()).all();
            scan_type_O = [];
            if not component_names: exit('bad query result: get_metIDAndPrecursorFormula_experimentIDAndSampleName_peakSpectrum');
            for cn in component_names:
                scan_type_O.append(cn[0]);
            return scan_type_O;
        except SQLAlchemyError as e:
            print(e);
    # query replicate numbers for data_stage01_peakSpectrum
    def get_replicateNumber_experimentIDAndTimePointAndSampleNameAbbreviationAndScanType_peakSpectrum(self,experiment_id_I,time_point_I,sample_name_abbreviation_I,scan_type_I):
        '''Querry replicate numbers from the experiment
        by time-point, sample name abbreviation and scan type'''
        try:
            replicates = self.session.query(data_stage01_isotopomer_peakSpectrum.replicate_number).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_peakSpectrum.time_point.like(time_point_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.used_).group_by(
                    data_stage01_isotopomer_peakSpectrum.replicate_number).order_by(
                    data_stage01_isotopomer_peakSpectrum.replicate_number.asc()).all();
            sample_replicates_O = [];
            if not replicates: 
                print('no replicates found for experiment_id\ttime_point\tsample_name_abbreviation\tscan_type');
                print((experiment_id_I + '\t'+ time_point_I + '\t'+ sample_name_abbreviation_I + '\t'+ scan_type_I));
            else:
                for r in replicates:
                    sample_replicates_O.append(r[0]);
            return sample_replicates_O;
        except SQLAlchemyError as e:
            print(e);
    # query product formulas
    def get_productFormulas_experimentIDAndTimePointAndSampleNameAbbreviationAndScanTypeAndReplicateAndMetIDAndPrecursorFormula_peakSpectrum(self,experiment_id_I,time_point_I,sample_name_abbreviation_I,scan_type_I,sample_replicate_I,met_id_I,precursor_formula_I):
        '''Querry product formulas that are used for the experiment        
        by time-point, sample name abbreviation, scan type, replicate numbers, met_ids, and precursor formula'''
        try:
            data = self.session.query(data_stage01_isotopomer_peakSpectrum.product_formula).filter(
                    data_stage01_isotopomer_peakSpectrum.precursor_formula.like(precursor_formula_I),
                    data_stage01_isotopomer_peakSpectrum.met_id.like(met_id_I),
                    data_stage01_isotopomer_peakSpectrum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_peakSpectrum.time_point.like(time_point_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.replicate_number == sample_replicate_I,
                    data_stage01_isotopomer_peakSpectrum.used_).group_by(
                    data_stage01_isotopomer_peakSpectrum.product_formula).order_by(
                    data_stage01_isotopomer_peakSpectrum.product_formula.asc()).all();
            product_formulas_O = [];
            if not data:
                print('no product formulas found for experiment_id\ttime_point\tsample_name_abbreviation\tscan_type\tsample_replicate\tmet id\tprecursor formula');
                print((experiment_id_I + '\t'+ time_point_I + '\t'+ sample_name_abbreviation_I + '\t'+ scan_type_I + '\t'+ str(sample_replicate_I) + '\t'+ met_id_I + '\t'+ precursor_formula_I));
            else:
                for d in data:
                    product_formulas_O.append(d.product_formula);
            return product_formulas_O;
        except SQLAlchemyError as e:
            print(e);
    def get_productFormulas_experimentIDAndSampleNameAndMetIDAndPrecursorFormulaAndScanType_peakSpectrum(self,experiment_id_I,sample_name_I,met_id_I,precursor_formula_I,scan_type_I):
        '''Querry peak data for a specific experiment_id, sample_name, met_id, and precursor_formula'''
        try:
            data = self.session.query(data_stage01_isotopomer_peakSpectrum.product_formula).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.met_id.like(met_id_I),
                    data_stage01_isotopomer_peakSpectrum.precursor_formula.like(precursor_formula_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_peakSpectrum.used_).group_by(
                    data_stage01_isotopomer_peakSpectrum.product_formula).order_by(
                    data_stage01_isotopomer_peakSpectrum.product_formula.asc()).all();
            product_formulas_O = [];
            if not data:
                print(('No product formulas found for sample_name: ' + sample_name_I + ', met_id: ' + met_id_I + ', and precursor_formula: ' + precursor_formula_I));
                return product_formulas_O;
            else:
                for d in data:
                    product_formulas_O.append(d.product_formula);
                return product_formulas_O;
        except SQLAlchemyError as e:
            print(e);
    # query normalized intensity from data_stage01_isotopomer_peakSpectrum
    def get_normalizedIntensity_experimentIDAndSampleAbbreviationAndTimePointAndReplicateNumberAndMetIDAndPrecursorFormulaAndMassAndScanType_peakSpectrum(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,replicate_number_I,met_id_I,precursor_formula_I,precursor_mass_I,scan_type_I):
        '''Querry peak data for a specific experiment_id, sample_name, met_id, and scan type'''
        try:
            data = self.session.query(data_stage01_isotopomer_peakSpectrum.intensity_normalized,
                    data_stage01_isotopomer_peakSpectrum.intensity_normalized_units).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_peakSpectrum.time_point.like(time_point_I),
                    data_stage01_isotopomer_peakSpectrum.precursor_formula.like(precursor_formula_I),
                    data_stage01_isotopomer_peakSpectrum.precursor_mass == precursor_mass_I,
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.met_id.like(met_id_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_peakSpectrum.replicate_number == replicate_number_I,
                    data_stage01_isotopomer_peakSpectrum.used_).all();
            intensity_normalized_O = None;
            intensity_normalized_units_O = None;
            if not data:
                print(('No normalized intensities found for sample_name_abbreviation: ' + sample_name_abbreviation_I + ', met_id: ' + met_id_I + ', precursor_formula: ' + precursor_formula_I + ', precursor_mass: ' + str(precursor_mass_I)));
                return intensity_normalized_O;
            else:
                intensity_normalized_O = data[0][0];
                intensity_normalized_units_O = data[0][1];
                return intensity_normalized_O;
        except SQLAlchemyError as e:
            print(e);
    # query data from data_stage01_isotopomer_peakSpectrum
    def get_data_experimentIDAndTimePointAndSampleNameAbbreviationAndScanTypeAndReplicateAndMetIDAndPrecursorFormula_peakSpectrum(self,experiment_id_I,time_point_I,sample_name_abbreviation_I,scan_type_I,sample_replicate_I,met_id_I,precursor_formula_I):
        '''Querry data that are used for the experiment        
        by time-point, sample name abbreviation, scan type, replicate numbers, met_ids, and precursor formula'''

        try:
            data = self.session.query(data_stage01_isotopomer_peakSpectrum.product_formula,
                    data_stage01_isotopomer_peakSpectrum.product_mass,
                    data_stage01_isotopomer_peakSpectrum.intensity_normalized,
                    data_stage01_isotopomer_peakSpectrum.intensity_normalized_units).filter(
                    data_stage01_isotopomer_peakSpectrum.precursor_formula.like(precursor_formula_I),
                    data_stage01_isotopomer_peakSpectrum.met_id.like(met_id_I),
                    data_stage01_isotopomer_peakSpectrum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_peakSpectrum.time_point.like(time_point_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.replicate_number == sample_replicate_I,
                    data_stage01_isotopomer_peakSpectrum.used_).order_by(
                    data_stage01_isotopomer_peakSpectrum.product_formula.asc(),
                    data_stage01_isotopomer_peakSpectrum.product_mass.asc()).all();
            product_formula = '';
            product_formula_old = '';
            data_O = {};
            mass_O = {};
            if not data:
                print(('No normalized intensities found for sample_name: ' + sample_name_I + ', met_id: ' + met_id_I + ', and precursor_formula: ' + precursor_formula_I));
                return data_O;
            else:
                for i,d in enumerate(data):
                    if i==0:
                        product_formula_old = d.product_formula;
                        mass_O[d.product_mass] = d.intensity_normalized;
                    product_formula = d.product_formula;
                    if product_formula != product_formula_old:
                        data_O[product_formula_old] = mass_O;
                        product_formula_old = product_formula
                        mass_O = {};
                        mass_O[d.product_mass] = d.intensity_normalized;
                    elif i == len(data)-1 and product_formula == product_formula_old:
                        mass_O[d.product_mass] = d.intensity_normalized;
                        data_O[product_formula] = mass_O;
                    else: mass_O[d.product_mass] = d.intensity_normalized;
                return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_normalizedIntensity_experimentIDAndSampleNameAndMetIDAndPrecursorFormulaAndScanType_peakSpectrum(self,experiment_id_I,sample_name_I,met_id_I,precursor_formula_I,scan_type_I):
        '''Querry peak data for a specific experiment_id, sample_name, met_id, and precursor_formula'''

        # possible duplicate of get_data_experimentIDAndSampleNameAndMetIDAndPrecursorFormulaAndScanType_peakSpectrum

        try:
            data = self.session.query(data_stage01_isotopomer_peakSpectrum.product_formula,
                    data_stage01_isotopomer_peakSpectrum.product_mass,
                    data_stage01_isotopomer_peakSpectrum.intensity_normalized,
                    data_stage01_isotopomer_peakSpectrum.intensity_normalized_units).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.met_id.like(met_id_I),
                    data_stage01_isotopomer_peakSpectrum.precursor_formula.like(precursor_formula_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_peakSpectrum.used_).order_by(
                    data_stage01_isotopomer_peakSpectrum.product_formula.asc(),
                    data_stage01_isotopomer_peakSpectrum.product_mass.asc()).all();
            product_formula = '';
            product_formula_old = '';
            data_O = {};
            mass_O = {};
            if not data:
                print(('No normalized intensities found for sample_name: ' + sample_name_I + ', met_id: ' + met_id_I + ', and precursor_formula: ' + precursor_formula_I));
                return data_O;
            else:
                for i,d in enumerate(data):
                    if i==0:
                        product_formula_old = d.product_formula;
                        mass_O[d.product_mass] = d.intensity_normalized;
                    product_formula = d.product_formula;
                    if product_formula != product_formula_old:
                        data_O[product_formula_old] = mass_O;
                        product_formula_old = product_formula
                        mass_O = {};
                        mass_O[d.product_mass] = d.intensity_normalized;
                    elif i == len(data)-1 and product_formula == product_formula_old:
                        mass_O[d.product_mass] = d.intensity_normalized;
                        data_O[product_formula] = mass_O;
                    else: mass_O[d.product_mass] = d.intensity_normalized;
                return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_data_experimentIDAndSampleNameAndMetIDAndPrecursorFormulaAndScanType_peakSpectrum(self,experiment_id_I,sample_name_I,met_id_I,precursor_formula_I,scan_type_I):
        '''Querry peak data for a specific experiment_id, sample_name, met_id, and precursor_formula'''
        try:
            data = self.session.query(data_stage01_isotopomer_peakSpectrum.product_formula,
                    data_stage01_isotopomer_peakSpectrum.product_mass,
                    data_stage01_isotopomer_peakSpectrum.intensity_corrected,
                    data_stage01_isotopomer_peakSpectrum.intensity_corrected_units).filter(
                    data_stage01_isotopomer_peakSpectrum.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_peakSpectrum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_peakSpectrum.met_id.like(met_id_I),
                    data_stage01_isotopomer_peakSpectrum.precursor_formula.like(precursor_formula_I),
                    data_stage01_isotopomer_peakSpectrum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_peakSpectrum.used_).order_by(
                    data_stage01_isotopomer_peakSpectrum.product_formula.asc(),
                    data_stage01_isotopomer_peakSpectrum.product_mass.asc()).all();
            product_formula = '';
            product_formula_old = '';
            data_O = {};
            mass_O = {};
            if not data:
                print(('No data found for sample_name: ' + sample_name_I + ', met_id: ' + met_id_I + ', and precursor_formula: ' + precursor_formula_I));
                return data_O;
            else:
                for i,d in enumerate(data):
                    if i==0:
                        product_formula_old = d.product_formula;
                        mass_O[d.product_mass] = d.intensity_corrected;
                    product_formula = d.product_formula;
                    if product_formula != product_formula_old:
                        data_O[product_formula_old] = mass_O;
                        product_formula_old = product_formula
                        mass_O = {};
                        mass_O[d.product_mass] = d.intensity_corrected;
                    elif i == len(data)-1 and product_formula == product_formula_old:
                        mass_O[d.product_mass] = d.intensity_corrected;
                        data_O[product_formula] = mass_O;
                    else: mass_O[d.product_mass] = d.intensity_corrected;
                return data_O;
        except SQLAlchemyError as e:
            print(e);
    # update data for data_stage01_isotopomer_peakSpectrum
    def update_data_stage01_isotopomer_peakSpectrum(self,dataListUpdated_I):
        # update the data_stage01_isotopomer_peakSpectrum
        updates = [];
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage01_isotopomer_peakSpectrum).filter(
                        data_stage01_isotopomer_peakSpectrum.experiment_id.like(d['experiment_id']),
                        data_stage01_isotopomer_peakSpectrum.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                        data_stage01_isotopomer_peakSpectrum.time_point.like(d['time_point']),
                        data_stage01_isotopomer_peakSpectrum.sample_type.like(d['sample_type']),
                        data_stage01_isotopomer_peakSpectrum.replicate_number == d['replicate_number'],
                        data_stage01_isotopomer_peakSpectrum.met_id.like(d['met_id']),
                        data_stage01_isotopomer_peakSpectrum.precursor_formula.like(d['precursor_formula']),
                        data_stage01_isotopomer_peakSpectrum.precursor_mass == d['precursor_mass'],
                        data_stage01_isotopomer_peakSpectrum.product_formula.like(d['product_formula']),
                        data_stage01_isotopomer_peakSpectrum.product_mass == d['product_mass'],
                        data_stage01_isotopomer_peakSpectrum.scan_type.like(d['scan_type'])).update(		
                        {
                        # 'intensity':d['intensity'],
                        #'intensity_units':d['intensity_units'],
                        'intensity_corrected':d['intensity_corrected'],
                        'intensity_corrected_units':d['intensity_corrected_units'],
                        'intensity_normalized':d['intensity_normalized'],
                        'intensity_normalized_units':d['intensity_normalized_units'],
                        'intensity_theoretical':d['intensity_theoretical'],
                        'abs_devFromTheoretical':d['abs_devFromTheoretical']},
                        synchronize_session=False);
                if data_update == 0:
                    print('row not found.')
                    print(d)
                    #print 'row will be added.'
                    #row = data_stage01_isotopomer_peakSpectrum(d['experiment_id'],
                    #    d['sample_name'],
                    #    d['sample_name_abbreviation'],
                    #    d['sample_type'],
                    #    d['time_point'],
                    #    d['replicate_number'],
                    #    d['met_id'],
                    #    d['precursor_formula'],
                    #    d['precursor_mass'],
                    #    d['product_formula'],
                    #    d['product_mass'],
                    #    0.0,
                    #    'cps',
                    #    d['intensity_corrected'],
                    #    d['intensity_corrected_units'],
                    #    d['intensity_normalized'],
                    #    d['intensity_normalized_units'],
                    #    d['intensity_theoretical'],
                    #    d['abs_devFromTheoretical'],
                    #    d['scan_type'],
                    #    True,
                    #    None);
                    #self.session.add(row);
                    #self.session.commit();
                #elif data_update ==1:
                #    print 'good update'
                updates.append(data_update);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();
    def update_validFragments_stage01_isotopomer_peakSpectrum(self,dataListUpdated_I):
        # update the data_stage01_isotopomer_peakSpectrum
        updates = [];
        # set 'used_' = False for all met/fragment pairs for the experiment
        try:
            data_update = self.session.query(data_stage01_isotopomer_peakSpectrum).filter(
                        data_stage01_isotopomer_peakSpectrum.experiment_id.like(dataListUpdated_I[0]['experiment_id'])).update(		
                        {
                        'used_':False},
                        synchronize_session=False);
        except SQLAlchemyError as e:
            print(e);
        self.session.commit();
        # set 'used_' = True for falidated met/fragment pairs for the experiment
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage01_isotopomer_peakSpectrum).filter(
                        data_stage01_isotopomer_peakSpectrum.experiment_id.like(d['experiment_id']),
                        data_stage01_isotopomer_peakSpectrum.met_id.like(d['met_id']),
                        data_stage01_isotopomer_peakSpectrum.product_formula.like(d['product_formula'])).update(		
                        {
                        'used_':True},
                        synchronize_session=False);
                if data_update == 0:
                    print('row not found.')
                    print(d)
                updates.append(data_update);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    # query sample names from data_stage01_isotopomer_normalized
    def get_sampleIDs_experimentID_dataStage01Normalized(self,experiment_id_I):
        '''Querry sample ids that are used from
        the experiment'''
        try:
            sample_ids = self.session.query(data_stage01_isotopomer_normalized.sample_id).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.sample_id).order_by(
                    data_stage01_isotopomer_normalized.sample_id.asc()).all();
            sample_ids_O = [];
            for si in sample_ids: sample_ids_O.append(si.sample_id);
            return sample_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentID_dataStage01Normalized(self,experiment_id_I):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_isotopomer_normalized.sample_name).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.sample_name).order_by(
                    data_stage01_isotopomer_normalized.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNamesAndReplicateNumbersAndSampleTypes_experimentIDAndSampleNameAbbreviationAndMetIDAndTimePointAndDilutionAndScanType_dataStage01Normalized(\
        self,experiment_id_I,sample_name_abbreviation_I,met_id_I,time_point_I,sample_dilution_I, scan_type_I):
        '''Querry sample names that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_isotopomer_normalized.sample_name,
                    data_stage01_isotopomer_normalized.replicate_number,
                    data_stage01_isotopomer_normalized.sample_type).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.met_id.like(met_id_I),
                    data_stage01_isotopomer_normalized.dilution == sample_dilution_I,
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.sample_name,
                    data_stage01_isotopomer_normalized.replicate_number,
                    data_stage01_isotopomer_normalized.sample_type).order_by(
                    data_stage01_isotopomer_normalized.sample_name.asc()).all();
            sample_names_O = [];
            sample_replicates_O = [];
            sample_types_O = [];
            if not sample_names:
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	met_id_I	time_point_I	sample_dilution_I")
                print(experiment_id_I,sample_name_abbreviation_I,met_id_I,time_point_I,sample_dilution_I)
                return sample_names_O,sample_replicates_O,sample_types_O;
            else:
                for sn in sample_names:
                    sample_names_O.append(sn.sample_name);
                    sample_replicates_O.append(sn.replicate_number);
                    sample_types_O.append(sn.sample_type);
                return sample_names_O,sample_replicates_O,sample_types_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNamesAndReplicateNumbersAndSampleTypes_experimentIDAndSampleNameAbbreviationAndMetIDAndTimePointAndScanType_dataStage01Normalized(\
        self,experiment_id_I,sample_name_abbreviation_I,met_id_I,time_point_I, scan_type_I):
        '''Querry sample names that are used from
        the experiment'''
        try:
            sample_names = self.session.query(data_stage01_isotopomer_normalized.sample_name,
                    data_stage01_isotopomer_normalized.replicate_number,
                    data_stage01_isotopomer_normalized.sample_type).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.met_id.like(met_id_I),
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.sample_name,
                    data_stage01_isotopomer_normalized.replicate_number,
                    data_stage01_isotopomer_normalized.sample_type).order_by(
                    data_stage01_isotopomer_normalized.sample_name.asc()).all();
            sample_names_O = [];
            sample_replicates_O = [];
            sample_types_O = [];
            if not sample_names:
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	met_id_I	time_point_I	sample_dilution_I")
                print(experiment_id_I,sample_name_abbreviation_I,met_id_I,time_point_I,sample_dilution_I)
                return sample_names_O,sample_replicates_O,sample_types_O;
            else:
                for sn in sample_names:
                    sample_names_O.append(sn.sample_name);
                    sample_replicates_O.append(sn.replicate_number);
                    sample_types_O.append(sn.sample_type);
                return sample_names_O,sample_replicates_O,sample_types_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameShort_experimentIDAndSampleName_dataStage01Normalized(self,experiment_id_I,sample_name_I):
        '''Querry sample name short that are used from
        the experiment'''
        try:
            sample_name_short = self.session.query(sample_description.sample_name_short).filter(
                    sample.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.sample_name_short).all();
            sample_name_short_O = sample_name_short[0];
            return sample_name_short_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample name abbreviations from data_stage01_isotopomer_normalized
    def get_sampleNameAbbreviations_experimentID_dataStage01Normalized(self,experiment_id_I):
        '''Querry sample names (i.e. unknowns) that are used from
        the experiment'''
        try:
            sample_names = self.session.query(sample_description.sample_name_abbreviation).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_name_abbreviation);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePointAndDilution_dataStage01Normalized(self,experiment_id_I,sample_type_I,time_point_I,dilution_I):
        '''Querry sample name abbreviations that are used from
        the experiment for specific time-points and dilutions'''
        try:
            sample_name_abbreviations = self.session.query(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_normalized.dilution == dilution_I,
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I)).group_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).order_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).all();
            sample_name_abbreviations_O = [];
            for sn in sample_name_abbreviations:
                sample_name_abbreviations_O.append(sn[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePointAndDilutionAndSampleName_dataStage01Normalized(self,experiment_id_I,sample_type_I,time_point_I,dilution_I,sample_name_I):
        '''Querry sample name abbreviations that are used from
        the experiment for specific time-points and dilutions'''
        try:
            sample_name_abbreviations = self.session.query(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_normalized.dilution == dilution_I,
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.sample_name.like(sample_name_I)).group_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).order_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).all();
            sample_name_abbreviations_O = [];
            for sn in sample_name_abbreviations:
                sample_name_abbreviations_O.append(sn[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePointAndComment_dataStage01Normalized(self,experiment_id_I,sample_type_I,time_point_I,comment_I):
        '''Querry sample name abbreviations that are used from
        the experiment for specific time-points'''
        try:
            sample_name_abbreviations = self.session.query(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.comment_.like(comment_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I)).group_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).order_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).all();
            sample_name_abbreviations_O = [];
            for sn in sample_name_abbreviations:
                sample_name_abbreviations_O.append(sn[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePoint_dataStage01Normalized(self,experiment_id_I,sample_type_I,time_point_I):
        '''Querry sample name abbreviations that are used from
        the experiment for specific time-points'''
        try:
            sample_name_abbreviations = self.session.query(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I)).group_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).order_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).all();
            sample_name_abbreviations_O = [];
            for sn in sample_name_abbreviations:
                sample_name_abbreviations_O.append(sn[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePointAndSampleNameAndComment_dataStage01Normalized(self,experiment_id_I,sample_type_I,time_point_I,sample_name_I,comment_I):
        '''Querry sample name abbreviations that are used from
        the experiment for specific time-points'''
        try:
            sample_name_abbreviations = self.session.query(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.comment_.like(comment_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.sample_name.like(sample_name_I)).group_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).order_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).all();
            sample_name_abbreviations_O = [];
            for sn in sample_name_abbreviations:
                sample_name_abbreviations_O.append(sn[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePointAndSampleName_dataStage01Normalized(self,experiment_id_I,sample_type_I,time_point_I,sample_name_I):
        '''Querry sample name abbreviations that are used from
        the experiment for specific time-points'''
        try:
            sample_name_abbreviations = self.session.query(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.sample_name.like(sample_name_I)).group_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).order_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).all();
            sample_name_abbreviations_O = [];
            for sn in sample_name_abbreviations:
                sample_name_abbreviations_O.append(sn[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePointAndSampleNameAbbreviation_dataStage01Normalized(self,experiment_id_I,sample_type_I,time_point_I,sample_name_abbreviation_I,exp_type_I=5):
        '''Querry sample name abbreviations that are used from
        the experiment for specific time-points'''
        try:
            sample_name_abbreviations = self.session.query(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    sample.sample_id.like(sample_description.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.sample_name.like(sample.sample_name)).group_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).order_by(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation).all();
            sample_name_abbreviations_O = [];
            for sn in sample_name_abbreviations:
                sample_name_abbreviations_O.append(sn[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    # Query scan types from data_stage01_normalized
    def get_scanTypes_experimentIDAndTimePointAndDilutionAndSampleAbbreviations_dataStage01Normalized(self,experiment_id_I,time_point_I,dilution_I,sample_name_abbreviations_I):
        '''Querry scan types that are used from the experiment for specific time-points and dilutions and sample name abbreviations'''
        try:
            scan_types = self.session.query(
                    data_stage01_isotopomer_normalized.scan_type).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.dilution == dilution_I,
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviations_I)).group_by(
                    data_stage01_isotopomer_normalized.scan_type).order_by(
                    data_stage01_isotopomer_normalized.scan_type).all();
            scan_types_O = [];
            for st in scan_types:
                scan_types_O.append(st[0]);
            return scan_types_O;
        except SQLAlchemyError as e:
            print(e);
    def get_scanTypes_experimentIDAndTimePointAndSampleAbbreviationsAndComment_dataStage01Normalized(self,experiment_id_I,time_point_I,sample_name_abbreviations_I,comment_I):
        '''Querry scan types that are used from the experiment for specific time-points and sample name abbreviations'''
        try:
            scan_types = self.session.query(
                    data_stage01_isotopomer_normalized.scan_type).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.comment_.like(comment_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviations_I)).group_by(
                    data_stage01_isotopomer_normalized.scan_type).order_by(
                    data_stage01_isotopomer_normalized.scan_type).all();
            scan_types_O = [];
            for st in scan_types:
                scan_types_O.append(st[0]);
            return scan_types_O;
        except SQLAlchemyError as e:
            print(e);
    def get_scanTypes_experimentIDAndTimePointAndSampleAbbreviations_dataStage01Normalized(self,experiment_id_I,time_point_I,sample_name_abbreviations_I):
        '''Querry scan types that are used from the experiment for specific time-points and sample name abbreviations'''
        try:
            scan_types = self.session.query(
                    data_stage01_isotopomer_normalized.scan_type).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviations_I)).group_by(
                    data_stage01_isotopomer_normalized.scan_type).order_by(
                    data_stage01_isotopomer_normalized.scan_type).all();
            scan_types_O = [];
            for st in scan_types:
                scan_types_O.append(st[0]);
            return scan_types_O;
        except SQLAlchemyError as e:
            print(e);
    def get_scanTypes_experimentIDAndTimePointAndSampleAbbreviationsAndSampleType_dataStage01Normalized(self,experiment_id_I,time_point_I,sample_name_abbreviations_I,sample_type_I):
        '''Querry scan types that are used from the experiment for specific time-points and sample name abbreviations'''
        try:
            scan_types = self.session.query(
                    data_stage01_isotopomer_normalized.scan_type).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviations_I)).group_by(
                    data_stage01_isotopomer_normalized.scan_type).order_by(
                    data_stage01_isotopomer_normalized.scan_type).all();
            scan_types_O = [];
            for st in scan_types:
                scan_types_O.append(st[0]);
            return scan_types_O;
        except SQLAlchemyError as e:
            print(e);
    # query met ids from data_stage01_isotopomer_normalized
    def get_metIDs_experimentIDAndSampleAbbreviationAndTimePointAndDilutionAndScanType_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,dilution_I,scan_type_I):
        '''Querry met ids that are used for the experiment, sample abbreviation, time point, dilution, scan type'''
        try:
            met_ids = self.session.query(data_stage01_isotopomer_normalized.met_id).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.dilution == dilution_I,
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.met_id).order_by(
                    data_stage01_isotopomer_normalized.met_id.asc()).all();
            met_ids_O = [];
            if not(met_ids):
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	time_point_I	dilution_I	scan_type_I");
                print(experiment_id_I,sample_name_abbreviation_I,time_point_I,dilution_I,scan_type_I);
            else:
                for cn in met_ids:
                    met_ids_O.append(cn[0]);
                return met_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_metIDs_experimentIDAndSampleAbbreviationAndTimePointAndScanTypeAndComment_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I,comment_I):
        '''Querry met ids that are used for the experiment, sample abbreviation, time point, scan type'''
        try:
            met_ids = self.session.query(data_stage01_isotopomer_normalized.met_id).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.comment_.like(comment_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.met_id).order_by(
                    data_stage01_isotopomer_normalized.met_id.asc()).all();
            met_ids_O = [];
            if not(met_ids):
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	time_point_I	scan_type_I comment_I");
                print(experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I,comment_I);
            else:
                for cn in met_ids:
                    met_ids_O.append(cn[0]);
                return met_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_metIDs_experimentIDAndSampleAbbreviationAndTimePointAndScanType_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I):
        '''Querry met ids that are used for the experiment, sample abbreviation, time point, scan type'''
        try:
            met_ids = self.session.query(data_stage01_isotopomer_normalized.met_id).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.met_id).order_by(
                    data_stage01_isotopomer_normalized.met_id.asc()).all();
            met_ids_O = [];
            if not(met_ids):
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	time_point_I	scan_type_I");
                print(experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I);
            else:
                for cn in met_ids:
                    met_ids_O.append(cn[0]);
                return met_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_metIDs_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndScanType_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I):
        '''Querry met ids that are used for the experiment, sample abbreviation, time point, scan type'''
        try:
            met_ids = self.session.query(data_stage01_isotopomer_normalized.met_id).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.met_id).order_by(
                    data_stage01_isotopomer_normalized.met_id.asc()).all();
            met_ids_O = [];
            if not(met_ids):
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	time_point_I	scan_type_I");
                print(experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I);
            else:
                for cn in met_ids:
                    met_ids_O.append(cn[0]);
                return met_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # Query met ids and other information from data_stage01_isotopomer_normalized
    def get_metIDsAndOther_experimentIDAndSampleAbbreviationAndTimePointAndDilutionAndScanTypeAndMetID_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,dilution_I,scan_type_I,met_id_I):
        '''Querry met ids, fragment formulas, and fragment masses, that are used for the experiment, sample abbreviation, time point, dilution, scan type, and met_ID'''
        try:
            met_ids = self.session.query(data_stage01_isotopomer_normalized.met_id,
                    data_stage01_isotopomer_normalized.fragment_formula,
                    data_stage01_isotopomer_normalized.fragment_mass).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.dilution == dilution_I,
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.met_id.like(met_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.met_id,
                    data_stage01_isotopomer_normalized.fragment_formula,
                    data_stage01_isotopomer_normalized.fragment_mass).order_by(
                    data_stage01_isotopomer_normalized.fragment_mass.asc(),
                    data_stage01_isotopomer_normalized.fragment_formula.desc(),
                    data_stage01_isotopomer_normalized.met_id.asc()).all();
            met_ids_O = [];
            fragment_formulas_O = [];
            fragment_masses_O = [];
            if not(met_ids):
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	time_point_I	dilution_I	scan_type_I	met_id_I");
                print(experiment_id_I,sample_name_abbreviation_I,time_point_I,dilution_I,scan_type_I,met_id_I);
            else:
                for cn in met_ids:
                    met_ids_O.append(cn.met_id);
                    fragment_formulas_O.append(cn.fragment_formula);
                    fragment_masses_O.append(cn.fragment_mass);
                return met_ids_O,fragment_formulas_O,fragment_masses_O;
        except SQLAlchemyError as e:
            print(e);
    def get_metIDsAndOther_experimentIDAndSampleAbbreviationAndTimePointAndDilutionAndScanType_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,dilution_I,scan_type_I):
        '''Querry met ids, fragment formulas, and fragment masses, that are used for the experiment, sample abbreviation, time point, dilution, scan type'''
        try:
            met_ids = self.session.query(data_stage01_isotopomer_normalized.met_id,
                    data_stage01_isotopomer_normalized.fragment_formula,
                    data_stage01_isotopomer_normalized.fragment_mass).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.dilution == dilution_I,
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.met_id,
                    data_stage01_isotopomer_normalized.fragment_formula,
                    data_stage01_isotopomer_normalized.fragment_mass).order_by(
                    data_stage01_isotopomer_normalized.fragment_mass.asc(),
                    data_stage01_isotopomer_normalized.fragment_formula.desc(),
                    data_stage01_isotopomer_normalized.met_id.asc()).all();
            met_ids_O = [];
            fragment_formulas_O = [];
            fragment_masses_O = [];
            if not(met_ids):
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	time_point_I	dilution_I	scan_type_I	met_id_I");
                print(experiment_id_I,sample_name_abbreviation_I,time_point_I,dilution_I,scan_type_I,met_id_I);
            else:
                for cn in met_ids:
                    met_ids_O.append(cn.met_id);
                    fragment_formulas_O.append(cn.fragment_formula);
                    fragment_masses_O.append(cn.fragment_mass);
                return met_ids_O,fragment_formulas_O,fragment_masses_O;
        except SQLAlchemyError as e:
            print(e);
    # Query fragment formulas and masses from data_stage01_isotopomer_normalized
    def get_fragmentFormulasAndMass_experimentIDAndSampleAbbreviationAndTimePointAndScanTypeAndMetID_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I,met_id_I):
        '''Querry fragment formulas and fragment masses, that are used for the experiment, sample abbreviation, time point, scan type, and met_ID'''
        try:
            met_ids = self.session.query(data_stage01_isotopomer_normalized.fragment_formula,
                    data_stage01_isotopomer_normalized.fragment_mass).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.met_id.like(met_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.fragment_formula,
                    data_stage01_isotopomer_normalized.fragment_mass).order_by(
                    data_stage01_isotopomer_normalized.fragment_formula.desc(),
                    data_stage01_isotopomer_normalized.fragment_mass.asc()).all();
            fragment_formulas_O = [];
            fragment_masses_O = [];
            if not(met_ids):
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	time_point_I	scan_type_I	met_id_I");
                print(experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I,met_id_I);
            else:
                for cn in met_ids:
                    fragment_formulas_O.append(cn.fragment_formula);
                    fragment_masses_O.append(cn.fragment_mass);
                return fragment_formulas_O,fragment_masses_O;
        except SQLAlchemyError as e:
            print(e);
    def get_fragmentFormulasAndMass_experimentIDAndSampleAbbreviationAndTimePointAndAndSampleTypeAndScanTypeAndMetID_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I,met_id_I):
        '''Querry fragment formulas and fragment masses, that are used for the experiment, sample abbreviation, time point, scan type, and met_ID'''
        try:
            met_ids = self.session.query(data_stage01_isotopomer_normalized.fragment_formula,
                    data_stage01_isotopomer_normalized.fragment_mass).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.met_id.like(met_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.fragment_formula,
                    data_stage01_isotopomer_normalized.fragment_mass).order_by(
                    data_stage01_isotopomer_normalized.fragment_formula.desc(),
                    data_stage01_isotopomer_normalized.fragment_mass.asc()).all();
            fragment_formulas_O = [];
            fragment_masses_O = [];
            if not(met_ids):
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	time_point_I	scan_type_I	met_id_I");
                print(experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I,met_id_I);
            else:
                for cn in met_ids:
                    fragment_formulas_O.append(cn.fragment_formula);
                    fragment_masses_O.append(cn.fragment_mass);
                return fragment_formulas_O,fragment_masses_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample dilutions from data_stage01_normalized
    def get_sampleDilution_experimentIDAndTimePoint_dataStage01Normalized(self,experiment_id_I,time_point_I):
        '''Querry dilutions that are used from the experiment'''
        try:
            sample_dilutions = self.session.query(data_stage01_isotopomer_normalized.dilution).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I)).group_by(
                    data_stage01_isotopomer_normalized.dilution).order_by(
                    data_stage01_isotopomer_normalized.dilution.asc()).all();
            sample_dilutions_O = [];
            for sd in sample_dilutions: sample_dilutions_O.append(sd.dilution);
            return sample_dilutions_O;
        except SQLAlchemyError as e:
            print(e);
    # query time points from data_stage01_normalized
    def get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry time points that are used from the experiment and sample name abbreviation'''
        try:
            time_points = self.session.query(sample_description.time_point).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True),
                    data_stage01_isotopomer_normalized.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.time_point).order_by(
                    sample_description.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_experimentID_dataStage01Normalized(self,experiment_id_I):
        '''Querry time points that are used from the experiment and sample name'''
        try:
            time_points = self.session.query(data_stage01_isotopomer_normalized.time_point).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.time_point).order_by(
                    data_stage01_isotopomer_normalized.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: 
                if tp.time_point: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_experimentIDAndComment_dataStage01Normalized(self,experiment_id_I,comment_I):
        '''Querry time points that are used from the experiment and sample name'''
        try:
            time_points = self.session.query(data_stage01_isotopomer_normalized.time_point).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.comment_.like(comment_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.time_point).order_by(
                    data_stage01_isotopomer_normalized.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # query replicate numbers from data_stage01_isotopomer_normalized
    def get_replicateNumbers_experimentIDAndSampleAbbreviationAndTimePointAndScanTypeAndMetID_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I,met_id_I):
        '''Querry replicate numbers that are used for the experiment, sample abbreviation, time point, scan type, and met_id'''
        try:
            replicate_numbers = self.session.query(data_stage01_isotopomer_normalized.replicate_number).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.met_id.like(met_id_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.used_.is_(True)).group_by(
                    data_stage01_isotopomer_normalized.replicate_number).order_by(
                    data_stage01_isotopomer_normalized.replicate_number.asc()).all();
            replicate_numbers_O = [];
            if not(replicate_numbers):
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	time_point_I	scan_type_I met_id_I");
                print(experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I,met_id_I);
            else:
                for cn in replicate_numbers:
                    replicate_numbers_O.append(cn[0]);
                return replicate_numbers_O;
        except SQLAlchemyError as e:
            print(e);
    # query normalized intensity from data_stage01_isotopomer_normalized
    def get_normalizedIntensity_experimentIDAndSampleAbbreviationAndTimePointAndReplicateNumberAndMetIDAndFragmentFormulaAndMassAndScanType_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,replicate_number_I,met_id_I,fragment_formula_I,fragment_mass_I,scan_type_I):
        '''Querry peak data for a specific experiment_id, sample_name, met_id, and scan type'''
        try:
            data = self.session.query(data_stage01_isotopomer_normalized.intensity_normalized,
                    data_stage01_isotopomer_normalized.intensity_normalized_units).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.fragment_formula.like(fragment_formula_I),
                    data_stage01_isotopomer_normalized.fragment_mass == fragment_mass_I,
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.met_id.like(met_id_I),
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.replicate_number == replicate_number_I,
                    data_stage01_isotopomer_normalized.used_).all();
            intensity_normalized_O = None;
            intensity_normalized_units_O = None;
            if not data:
                print('No normalized intensities found for the following:')
                print('sample_name_abbreviation\ttime_point\treplicate_number\tmet_id\tfragment_formula\tfragment_mass\tscan_type');
                print((sample_name_abbreviation_I) + '\t' + str(time_point_I) + '\t' + str(replicate_number_I) + '\t' + str(met_id_I) + '\t' + str(fragment_formula_I) + '\t' + str(fragment_mass_I) + '\t' + str(scan_type_I));
                return intensity_normalized_O;
            else:
                intensity_normalized_O = data[0][0];
                intensity_normalized_units_O = data[0][1];
                return intensity_normalized_O;
        except SQLAlchemyError as e:
            print(e);
    def get_normalizedIntensity_experimentIDAndSampleAbbreviationAndTimePointAndMetIDAndFragmentFormulaAndMassAndScanType_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,met_id_I,fragment_formula_I,fragment_mass_I,scan_type_I):
        '''Querry peak data for a specific experiment_id, sample_name, met_id, and scan type'''
        try:
            data = self.session.query(data_stage01_isotopomer_normalized.intensity_normalized,
                    data_stage01_isotopomer_normalized.intensity_normalized_units).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.fragment_formula.like(fragment_formula_I),
                    data_stage01_isotopomer_normalized.fragment_mass == fragment_mass_I,
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.met_id.like(met_id_I),
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.used_).all();
            intensity_normalized_O = [];
            intensity_normalized_units_O = [];
            if not data:
                print('No normalized intensities found for the following:')
                print('sample_name_abbreviation\ttime_point\tmet_id\tfragment_formula\tfragment_mass\tscan_type');
                print((sample_name_abbreviation_I) + '\t' + str(time_point_I) + '\t' + str(met_id_I) + '\t' + str(fragment_formula_I) + '\t' + str(fragment_mass_I) + '\t' + str(scan_type_I));
                return intensity_normalized_O;
            else:
                for d in data:
                    if d.intensity_normalized and not d.intensity_normalized == 0.0: # skip replicates without a value or 0.0
                        intensity_normalized_O.append(d.intensity_normalized);
                        intensity_normalized_units_O.append(d.intensity_normalized_units);
                if intensity_normalized_O: return intensity_normalized_O;
                else: return [0.0];
        except SQLAlchemyError as e:
            print(e);
    def get_normalizedIntensity_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndMetIDAndFragmentFormulaAndMassAndScanType_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,met_id_I,fragment_formula_I,fragment_mass_I,scan_type_I):
        '''Querry peak data for a specific experiment_id, sample_name, met_id, and scan type'''
        try:
            data = self.session.query(data_stage01_isotopomer_normalized.intensity_normalized,
                    data_stage01_isotopomer_normalized.intensity_normalized_units).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.fragment_formula.like(fragment_formula_I),
                    data_stage01_isotopomer_normalized.fragment_mass == fragment_mass_I,
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.met_id.like(met_id_I),
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.used_).all();
            intensity_normalized_O = [];
            intensity_normalized_units_O = [];
            if not data:
                print('No normalized intensities found for the following:')
                print('sample_name_abbreviation\ttime_point\tmet_id\tfragment_formula\tfragment_mass\tscan_type');
                print((sample_name_abbreviation_I) + '\t' + str(time_point_I) + '\t' + str(met_id_I) + '\t' + str(fragment_formula_I) + '\t' + str(fragment_mass_I) + '\t' + str(scan_type_I));
                return intensity_normalized_O;
            else:
                for d in data:
                    if d.intensity_normalized and not d.intensity_normalized == 0.0: # skip replicates without a value or 0.0
                        intensity_normalized_O.append(d.intensity_normalized);
                        intensity_normalized_units_O.append(d.intensity_normalized_units);
                if intensity_normalized_O: return intensity_normalized_O;
                else: return [0.0];
        except SQLAlchemyError as e:
            print(e);
    # query data from data_stage01_isotopomer_normalized
    def get_data_experimentIDAndSampleNameAndMetIDAndAndScanType_normalized(self,experiment_id_I,sample_name_I,met_id_I,scan_type_I):
        '''Querry peak data for a specific experiment_id, sample_name, met_id, and scan type'''
        try:
            data = self.session.query(data_stage01_isotopomer_normalized.fragment_formula,
                    data_stage01_isotopomer_normalized.fragment_mass,
                    data_stage01_isotopomer_normalized.intensity_corrected,
                    data_stage01_isotopomer_normalized.intensity_corrected_units).filter(
                    data_stage01_isotopomer_normalized.sample_name.like(sample_name_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.met_id.like(met_id_I),
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.used_).order_by(
                    data_stage01_isotopomer_normalized.fragment_formula.asc(),
                    data_stage01_isotopomer_normalized.fragment_mass.asc()).all();
            fragment_formula = '';
            fragment_formula_old = '';
            data_O = {};
            if not data:
                print(('No data found for sample_name: ' + sample_name_I + ', met_id: ' + met_id_I));
                return data_O;
            else:
                mass_O = {};
                for i,d in enumerate(data):
                    if i==0:
                        fragment_formula_old = d.fragment_formula;
                        mass_O[d.fragment_mass] = d.intensity_corrected;
                    fragment_formula = d.fragment_formula;
                    if fragment_formula != fragment_formula_old:
                        data_O[fragment_formula_old] = mass_O;
                        fragment_formula_old = fragment_formula
                        mass_O = {};
                    elif i == len(data)-1 and fragment_formula == fragment_formula_old:
                        mass_O[d.fragment_mass] = d.intensity_corrected;
                        data_O[fragment_formula] = mass_O;
                    mass_O[d.fragment_mass] = d.intensity_corrected;
                return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_data_experimentIDAndSampleAbbreviationAndTimePointAndScanTypeAndMetIDAndReplicateNumber_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I,met_id_I,replicate_number_I):
        '''Querry peak data that are used for the experiment, sample abbreviation, time point, scan type, met_id, and replicate number'''
        try:
            data = self.session.query(data_stage01_isotopomer_normalized.dilution,
                    data_stage01_isotopomer_normalized.fragment_formula,
                    data_stage01_isotopomer_normalized.fragment_mass,
                    data_stage01_isotopomer_normalized.intensity_normalized,
                    data_stage01_isotopomer_normalized.intensity_normalized_units,
                    data_stage01_isotopomer_normalized.used_,
                    data_stage01_isotopomer_normalized.comment_).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.met_id.like(met_id_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.replicate_number == replicate_number_I,
                    data_stage01_isotopomer_normalized.used_.is_(True)).order_by(
                    data_stage01_isotopomer_normalized.fragment_formula.asc(),
                    data_stage01_isotopomer_normalized.fragment_mass.asc(),
                    data_stage01_isotopomer_normalized.dilution.asc()).all();
            fragment_formula = '';
            fragment_formula_old = '';
            data_O = {};
            if not data:
                print('No data found');
                return data_O;
            else:
                ## extract out dilutions
                #dilutions = [d.dilution for d in data];
                #dilutions = list(set(dilutions));
                #dilutions.sort();
                #dilutions_dict = dict(zip(dilutions,['low','high']));
                mass_lst = [];
                mass_O = {};
                for i,d in enumerate(data):
                    info = {};
                    if i==0:
                        fragment_formula_old = d.fragment_formula;
                    fragment_formula = d.fragment_formula;
                    if fragment_formula != fragment_formula_old:
                        data_O[fragment_formula_old] = mass_lst;
                        fragment_formula_old = fragment_formula
                        mass_lst = [];
                        info['intensity'] = d.intensity_normalized;
                        info['dilution'] = d.dilution;
                        info['used_'] = d.used_;
                        info['comment_'] = d.comment_;
                        mass_O[d.fragment_mass] = info;
                        mass_lst.append(mass_O);
                        mass_O = {};
                    elif i == len(data)-1 and fragment_formula == fragment_formula_old:
                        info['intensity'] = d.intensity_normalized;
                        info['dilution'] = d.dilution;
                        info['used_'] = d.used_;
                        info['comment_'] = d.comment_;
                        mass_O[d.fragment_mass] = info;
                        mass_lst.append(mass_O);
                        mass_O = {};               
                        data_O[fragment_formula] = mass_lst;
                    else:
                        info['intensity'] = d.intensity_normalized;
                        info['dilution'] = d.dilution;
                        info['used_'] = d.used_;
                        info['comment_'] = d.comment_;
                        mass_O[d.fragment_mass] = info;
                        mass_lst.append(mass_O);
                        mass_O = {};
                return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_dataNormalized_experimentIDAndSampleAbbreviationAndTimePointAndScanTypeAndMetIDAndReplicateNumber_dataStage01Normalized(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I,met_id_I,replicate_number_I):
        '''Querry peak data that are used for the experiment, sample abbreviation, time point, scan type, met_id, and replicate number'''
        try:
            data = self.session.query(data_stage01_isotopomer_normalized.dilution,
                    data_stage01_isotopomer_normalized.fragment_formula,
                    data_stage01_isotopomer_normalized.fragment_mass,
                    data_stage01_isotopomer_normalized.intensity_normalized,
                    data_stage01_isotopomer_normalized.intensity_normalized_units,
                    data_stage01_isotopomer_normalized.used_,
                    data_stage01_isotopomer_normalized.comment_).filter(
                    data_stage01_isotopomer_normalized.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_normalized.met_id.like(met_id_I),
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.time_point.like(time_point_I),
                    data_stage01_isotopomer_normalized.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_normalized.replicate_number == replicate_number_I,
                    data_stage01_isotopomer_normalized.used_.is_(True)).order_by(
                    data_stage01_isotopomer_normalized.fragment_formula.asc(),
                    data_stage01_isotopomer_normalized.fragment_mass.asc(),
                    data_stage01_isotopomer_normalized.dilution.asc()).all();
            fragment_formula = '';
            fragment_formula_old = '';
            data_O = {};
            if not data:
                print('No data found');
                return data_O;
            else:
                mass_O = {};
                for i,d in enumerate(data):
                    if i==0:
                        fragment_formula_old = d.fragment_formula;
                        mass_O[d.fragment_mass] = d.intensity_normalized;
                    fragment_formula = d.fragment_formula;
                    if fragment_formula != fragment_formula_old:
                        data_O[fragment_formula_old] = mass_O;
                        fragment_formula_old = fragment_formula
                        mass_O = {};
                    elif i == len(data)-1 and fragment_formula == fragment_formula_old:
                        mass_O[d.fragment_mass] = d.intensity_normalized;
                        data_O[fragment_formula] = mass_O;
                    mass_O[d.fragment_mass] = d.intensity_normalized;
                return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_experimentID_dataStage01Normalized(self,experiment_id_I):
        '''Query rows for a specific experiment_id'''
        try:
            data = self.session.query(data_stage01_isotopomer_normalized).filter(
                    data_stage01_isotopomer_normalized.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_normalized.used_).order_by(
                    data_stage01_isotopomer_normalized.fragment_formula.asc(),
                    data_stage01_isotopomer_normalized.fragment_mass.asc(),
                    data_stage01_isotopomer_normalized.sample_name.asc()).all();
            data_O = [];
            if not data:
                return data_O;
            else:
                for d in data:
                    data_O.append(d.__repr__dict__());
                return data_O;
        except SQLAlchemyError as e:
            print(e);
    # update data for data_stage01_isotopomer_normalized
    def update_data_stage01_isotopomer_normalized(self,dataListUpdated_I):
        # update the data_stage01_isotopomer_normalized
        updates = [];
        for d in dataListUpdated_I:
            if 'intensity_corrected' in d:
                try:
                    data_update = self.session.query(data_stage01_isotopomer_normalized).filter(
                            data_stage01_isotopomer_normalized.experiment_id.like(d['experiment_id']),
                            data_stage01_isotopomer_normalized.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                            data_stage01_isotopomer_normalized.time_point.like(d['time_point']),
                            data_stage01_isotopomer_normalized.dilution == d['dilution'],
                            data_stage01_isotopomer_normalized.sample_type.like(d['sample_type']),
                            data_stage01_isotopomer_normalized.replicate_number == d['replicate_number'],
                            data_stage01_isotopomer_normalized.met_id.like(d['met_id']),
                            data_stage01_isotopomer_normalized.fragment_formula.like(d['fragment_formula']),
                            data_stage01_isotopomer_normalized.fragment_mass == d['fragment_mass'],
                            data_stage01_isotopomer_normalized.scan_type.like(d['scan_type'])).update(		
                            {
                            # 'intensity':d['intensity'],
                            #'intensity_units':d['intensity_units'],
                            'intensity_corrected':d['intensity_corrected'],
                            'intensity_corrected_units':d['intensity_corrected_units'],
                            'intensity_normalized':d['intensity_normalized'],
                            'intensity_normalized_units':d['intensity_normalized_units'],
                            'intensity_theoretical':d['intensity_theoretical'],
                            'abs_devFromTheoretical':d['abs_devFromTheoretical']},
                            synchronize_session=False);
                    if data_update == 0:
                        print('row not found.')
                        print(d)
                        #print 'row will be added.'
                        #row = data_stage01_isotopomer_normalized();
                        #self.session.add(row);
                        #self.session.commit();
                    #elif data_update ==1:
                    #    print 'good update'
                    updates.append(data_update);
                except SQLAlchemyError as e:
                    print(e);
            elif 'used_' in d:
                try:
                    data_update = self.session.query(data_stage01_isotopomer_normalized).filter(
                            data_stage01_isotopomer_normalized.experiment_id.like(d['experiment_id']),
                            data_stage01_isotopomer_normalized.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                            data_stage01_isotopomer_normalized.time_point.like(d['time_point']),
                            data_stage01_isotopomer_normalized.dilution == d['dilution'],
                            data_stage01_isotopomer_normalized.replicate_number == d['replicate_number'],
                            data_stage01_isotopomer_normalized.met_id.like(d['met_id']),
                            data_stage01_isotopomer_normalized.fragment_formula.like(d['fragment_formula']),
                            data_stage01_isotopomer_normalized.fragment_mass == d['fragment_mass'],
                            data_stage01_isotopomer_normalized.scan_type.like(d['scan_type'])).update(		
                            {
                            # 'intensity':d['intensity'],
                            #'intensity_units':d['intensity_units'],
                            'intensity_normalized':d['intensity_normalized'],
                            'intensity_normalized_units':d['intensity_normalized_units'],
                            'abs_devFromTheoretical':d['abs_devFromTheoretical'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                    if data_update == 0:
                        print('row not found.')
                        print(d)
                    #elif data_update ==1:
                    #    print 'good update'
                    updates.append(data_update);
                except SQLAlchemyError as e:
                    print(e);
        self.session.commit();
    def update_usedAndComment_stage01_isotopomer_normalized(self,dataListUpdated_I):
        # update the data_stage01_isotopomer_normalized used and comment columns from data_stage01_isotopomer_averages
        updates = [];
        for d in dataListUpdated_I:
            if d['used_'] and d['comment_']:
                #update only the comments
                try:
                    data_update = self.session.query(data_stage01_isotopomer_normalized).filter(
                            data_stage01_isotopomer_normalized.experiment_id.like(d['experiment_id']),
                            data_stage01_isotopomer_normalized.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                            data_stage01_isotopomer_normalized.time_point.like(d['time_point']),
                            data_stage01_isotopomer_normalized.sample_type.like(d['sample_type']),
                            data_stage01_isotopomer_normalized.met_id.like(d['met_id']),
                            data_stage01_isotopomer_normalized.fragment_formula.like(d['fragment_formula']),
                            data_stage01_isotopomer_normalized.fragment_mass == d['fragment_mass'],
                            data_stage01_isotopomer_normalized.scan_type.like(d['scan_type'])).update(		
                            {
                            'comment_':d['comment_']},
                            synchronize_session=False);
                    if data_update == 0:
                        print('row not found.')
                        print(d)
                        #print 'row will be added.'
                        #row = data_stage01_isotopomer_normalized();
                        #self.session.add(row);
                        #self.session.commit();
                    #elif data_update ==1:
                    #    print 'good update'
                    updates.append(data_update);
                except SQLAlchemyError as e:
                    print(e);
            if not d['used_']:
                # update both used_ and comment_
                try:
                    data_update = self.session.query(data_stage01_isotopomer_normalized).filter(
                            data_stage01_isotopomer_normalized.experiment_id.like(d['experiment_id']),
                            data_stage01_isotopomer_normalized.sample_name_abbreviation.like(d['sample_name_abbreviation']),
                            data_stage01_isotopomer_normalized.time_point.like(d['time_point']),
                            data_stage01_isotopomer_normalized.sample_type.like(d['sample_type']),
                            data_stage01_isotopomer_normalized.met_id.like(d['met_id']),
                            data_stage01_isotopomer_normalized.fragment_formula.like(d['fragment_formula']),
                            data_stage01_isotopomer_normalized.fragment_mass == d['fragment_mass'],
                            data_stage01_isotopomer_normalized.scan_type.like(d['scan_type'])).update(		
                            {
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                    if data_update == 0:
                        print('row not found.')
                        print(d)
                        #print 'row will be added.'
                        #row = data_stage01_isotopomer_normalized();
                        #self.session.add(row);
                        #self.session.commit();
                    #elif data_update ==1:
                    #    print 'good update'
                    updates.append(data_update);
                except SQLAlchemyError as e:
                    print(e);
        self.session.commit();

    ## Query data from data_stage01_isotopomer_averages:
    # query normalized intensity from data_stage01_isotopomer_averages
    def get_normalizedIntensity_experimentIDAndSampleAbbreviationAndTimePointAndMetIDAndFragmentFormulaAndMassAndScanType_dataStage01Averages(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,met_id_I,fragment_formula_I,fragment_mass_I,scan_type_I):
        '''Querry peak data for a specific experiment_id, sample_name, met_id, and scan type'''
        try:
            data = self.session.query(data_stage01_isotopomer_averages.intensity_normalized_average,
                    data_stage01_isotopomer_averages.intensity_normalized_cv,
                    data_stage01_isotopomer_averages.intensity_normalized_units).filter(
                    data_stage01_isotopomer_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averages.time_point.like(time_point_I),
                    data_stage01_isotopomer_averages.fragment_formula.like(fragment_formula_I),
                    data_stage01_isotopomer_averages.fragment_mass == fragment_mass_I,
                    data_stage01_isotopomer_averages.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averages.met_id.like(met_id_I),
                    data_stage01_isotopomer_averages.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averages.used_).all();
            intensity_normalized_average_O = None;
            intensity_normalized_cv_O = None;
            intensity_normalized_units_O = None;
            if not data:
                print('No normalized intensities found for the following:')
                print('sample_name_abbreviation\ttime_point\tmet_id\tfragment_formula\tfragment_mass\tscan_type');
                print((sample_name_abbreviation_I) + '\t' + str(time_point_I) + '\t' + str(met_id_I) + '\t' + str(fragment_formula_I) + '\t' + str(fragment_mass_I) + '\t' + str(scan_type_I));
                return intensity_normalized_average_O,intensity_normalized_cv_O;
            else:
                intensity_normalized_average_O = data[0][0];
                intensity_normalized_cv_O = data[0][1];
                intensity_normalized_units_O = data[0][2];
                return intensity_normalized_average_O,intensity_normalized_cv_O;
        except SQLAlchemyError as e:
            print(e);
    # query time points from data_stage01_isotopomer_averages:
    def get_timePoint_experimentID_dataStage01Averages(self,experiment_id_I):
        '''Querry time points that are used from the experiment and sample name'''
        try:
            time_points = self.session.query(data_stage01_isotopomer_averages.time_point).filter(
                    data_stage01_isotopomer_averages.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averages.used_.is_(True)).group_by(
                    data_stage01_isotopomer_averages.time_point).order_by(
                    data_stage01_isotopomer_averages.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample name abbreviations from data_stage01_isotopomer_averages:
    def get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePoint_dataStage01Averages(self,experiment_id_I,sample_type_I,time_point_I):
        '''Querry sample name abbreviations that are used from
        the experiment for specific time-points'''
        try:
            sample_name_abbreviations = self.session.query(
                    data_stage01_isotopomer_averages.sample_name_abbreviation).filter(
                    data_stage01_isotopomer_averages.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averages.used_.is_(True),
                    data_stage01_isotopomer_averages.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averages.time_point.like(time_point_I)).group_by(
                    data_stage01_isotopomer_averages.sample_name_abbreviation).order_by(
                    data_stage01_isotopomer_averages.sample_name_abbreviation).all();
            sample_name_abbreviations_O = [];
            for sn in sample_name_abbreviations:
                sample_name_abbreviations_O.append(sn[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    # query scan types from data_stage01_isotopomer_averages
    def get_scanTypes_experimentIDAndTimePointAndSampleAbbreviationsAndSampleType_dataStage01Averages(self,experiment_id_I,time_point_I,sample_name_abbreviations_I,sample_type_I):
        '''Querry scan types that are used from the experiment for specific time-points and sample name abbreviations'''
        try:
            scan_types = self.session.query(
                    data_stage01_isotopomer_averages.scan_type).filter(
                    data_stage01_isotopomer_averages.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averages.used_.is_(True),
                    data_stage01_isotopomer_averages.time_point.like(time_point_I),
                    data_stage01_isotopomer_averages.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averages.sample_name_abbreviation.like(sample_name_abbreviations_I)).group_by(
                    data_stage01_isotopomer_averages.scan_type).order_by(
                    data_stage01_isotopomer_averages.scan_type).all();
            scan_types_O = [];
            for st in scan_types:
                scan_types_O.append(st[0]);
            return scan_types_O;
        except SQLAlchemyError as e:
            print(e);
    # query met_ids  from data_stage01_isotopomer_averages
    def get_metIDs_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndScanType_dataStage01Averages(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I):
        '''Querry met ids that are used for the experiment, sample abbreviation, time point, scan type'''
        try:
            met_ids = self.session.query(data_stage01_isotopomer_averages.met_id).filter(
                    data_stage01_isotopomer_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averages.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averages.time_point.like(time_point_I),
                    data_stage01_isotopomer_averages.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averages.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averages.used_.is_(True)).group_by(
                    data_stage01_isotopomer_averages.met_id).order_by(
                    data_stage01_isotopomer_averages.met_id.asc()).all();
            met_ids_O = [];
            if not(met_ids):
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	time_point_I	scan_type_I");
                print(experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I);
            else:
                for cn in met_ids:
                    met_ids_O.append(cn[0]);
                return met_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # query normalized intensity from data_stage01_isotopomer_averages
    def get_dataProductFragment_experimentIDAndTimePointSampleAbbreviationAndSampleTypeAndScanTypeAndMetID_dataStage01Averages(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I, met_id_I):
        '''Querry peak data for a specific experiment_id, sample_name_abbreviation'''
        try:
            data = self.session.query(data_stage01_isotopomer_averages.fragment_formula,
                    data_stage01_isotopomer_averages.fragment_mass,
                    MS_components.product_fragment,
                    data_stage01_isotopomer_averages.intensity_normalized_average,
                    data_stage01_isotopomer_averages.intensity_normalized_cv,
                    data_stage01_isotopomer_averages.intensity_theoretical,
                    data_stage01_isotopomer_averages.abs_devFromTheoretical,
                    data_stage01_isotopomer_spectrumAccuracy.spectrum_accuracy,
                    data_stage01_isotopomer_averages.scan_type).filter(
                    data_stage01_isotopomer_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averages.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averages.time_point.like(time_point_I),
                    data_stage01_isotopomer_averages.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averages.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averages.met_id.like(met_id_I),
                    data_stage01_isotopomer_averages.fragment_formula.like(MS_components.product_formula),
                    data_stage01_isotopomer_averages.met_id.like(MS_components.met_id),
                    MS_components.ms_methodtype.like('tuning'),
                    data_stage01_isotopomer_averages.used_,
                    data_stage01_isotopomer_spectrumAccuracy.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_spectrumAccuracy.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_spectrumAccuracy.time_point.like(time_point_I),
                    data_stage01_isotopomer_spectrumAccuracy.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_spectrumAccuracy.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_spectrumAccuracy.met_id.like(met_id_I),
                    data_stage01_isotopomer_spectrumAccuracy.used_.is_(True),
                    data_stage01_isotopomer_spectrumAccuracy.fragment_formula.like(MS_components.product_formula),
                    data_stage01_isotopomer_spectrumAccuracy.met_id.like(MS_components.met_id)).group_by(
                    data_stage01_isotopomer_averages.fragment_formula,
                    data_stage01_isotopomer_averages.fragment_mass,
                    MS_components.product_fragment,
                    data_stage01_isotopomer_averages.intensity_normalized_average,
                    data_stage01_isotopomer_averages.intensity_normalized_cv,
                    data_stage01_isotopomer_averages.intensity_theoretical,
                    data_stage01_isotopomer_averages.abs_devFromTheoretical,
                    data_stage01_isotopomer_spectrumAccuracy.spectrum_accuracy,
                    data_stage01_isotopomer_averages.scan_type).order_by(
                    data_stage01_isotopomer_averages.fragment_formula.desc(),
                    data_stage01_isotopomer_averages.fragment_mass.asc()).all();
            data_O = [];
            if not data:
                print('No normalized intensities found for the following:')
                print('sample_name_abbreviation: ' + sample_name_abbreviation_I);
                return data_O;
            else:
                # algorithm will break there is no data for a0 mass and there are jumps in the a values (i.e. a0 to a2);
                fragment_formula = '';
                fragment_formula_old = '';
                data_cnt = len(data)-1;
                i = 0;
                while i <= data_cnt:
                    fragment_formula_old = data[i].fragment_formula;
                    row_key = [];
                    row_theoretical = [];
                    row_measured = [];
                    row_measured_cv = [];
                    row_measured_dif = [];
                    row_spectrum_accuracy = [];
                    row = [];
                    for a in range(50):
                        if i <= data_cnt:
                            fragment_formula = data[i].fragment_formula;
                            if fragment_formula == fragment_formula_old:
                                if a == 0:
                                    # add key columns
                                    row_key.append(sample_name_abbreviation_I);
                                    row_key.append(time_point_I);
                                    row_key.append(met_id_I);
                                    row_key.append(data[i].fragment_formula);
                                    row_key.append(str(data[i].product_fragment));
                                    row_key.append(data[i].scan_type);
                                    row_spectrum_accuracy.append(data[i].spectrum_accuracy);
                                    mass0 = data[i].fragment_mass
                                massi = data[i].fragment_mass;
                                massDif = massi-mass0;
                                # add a+0... information
                                if data[i].intensity_theoretical: theoretical = numpy.round(data[i].intensity_theoretical,3);
                                else: theoretical = data[i].intensity_theoretical;
                                row_theoretical.append(theoretical)
                                if data[i].intensity_normalized_average: measured = numpy.round(data[i].intensity_normalized_average,3);
                                else: measured = data[i].intensity_normalized_average;
                                row_measured.append(measured)
                                if data[i].intensity_normalized_cv: cv = numpy.round(data[i].intensity_normalized_cv,3);
                                else: cv = data[i].intensity_normalized_cv;
                                row_measured_cv.append(cv);
                                if data[i].abs_devFromTheoretical: dif = numpy.round(data[i].abs_devFromTheoretical,3)
                                else: dif = data[i].abs_devFromTheoretical;
                                row_measured_dif.append(dif)
                                i += 1;
                            else:
                                row_theoretical.append(None);
                                row_measured.append(None);
                                row_measured_cv.append(None);
                                row_measured_dif.append(None);
                        else:
                            row_theoretical.append(None);
                            row_measured.append(None);
                            row_measured_cv.append(None);
                            row_measured_dif.append(None);
                    row.extend(row_key);
                    row.extend(row_theoretical);
                    row.extend(row_measured);
                    row.extend(row_measured_cv);
                    row.extend(row_measured_dif);
                    row.extend(row_spectrum_accuracy);
                    data_O.append(row);
                return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_dataPrecursorFragment_experimentIDAndTimePointSampleAbbreviationAndSampleTypeAndScanTypeAndMetID_dataStage01Averages(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I, met_id_I):
        '''Querry peak data for a specific experiment_id, sample_name_abbreviation'''
        try:
            data = self.session.query(data_stage01_isotopomer_averages.fragment_formula,
                    data_stage01_isotopomer_averages.fragment_mass,
                    MS_components.precursor_fragment,
                    data_stage01_isotopomer_averages.intensity_normalized_average,
                    data_stage01_isotopomer_averages.intensity_normalized_cv,
                    data_stage01_isotopomer_averages.intensity_theoretical,
                    data_stage01_isotopomer_averages.abs_devFromTheoretical,
                    data_stage01_isotopomer_spectrumAccuracy.spectrum_accuracy,
                    data_stage01_isotopomer_averages.scan_type).filter(
                    data_stage01_isotopomer_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averages.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averages.time_point.like(time_point_I),
                    data_stage01_isotopomer_averages.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averages.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averages.met_id.like(met_id_I),
                    data_stage01_isotopomer_averages.fragment_formula.like(MS_components.precursor_formula),
                    data_stage01_isotopomer_averages.met_id.like(MS_components.met_id),
                    MS_components.ms_methodtype.like('tuning'),
                    data_stage01_isotopomer_averages.used_,
                    data_stage01_isotopomer_spectrumAccuracy.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_spectrumAccuracy.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_spectrumAccuracy.time_point.like(time_point_I),
                    data_stage01_isotopomer_spectrumAccuracy.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_spectrumAccuracy.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_spectrumAccuracy.met_id.like(met_id_I),
                    data_stage01_isotopomer_spectrumAccuracy.used_.is_(True),
                    data_stage01_isotopomer_spectrumAccuracy.fragment_formula.like(MS_components.precursor_formula),
                    data_stage01_isotopomer_spectrumAccuracy.met_id.like(MS_components.met_id)).group_by(
                    data_stage01_isotopomer_averages.fragment_formula,
                    data_stage01_isotopomer_averages.fragment_mass,
                    MS_components.precursor_fragment,
                    data_stage01_isotopomer_averages.intensity_normalized_average,
                    data_stage01_isotopomer_averages.intensity_normalized_cv,
                    data_stage01_isotopomer_averages.intensity_theoretical,
                    data_stage01_isotopomer_averages.abs_devFromTheoretical,
                    data_stage01_isotopomer_spectrumAccuracy.spectrum_accuracy,
                    data_stage01_isotopomer_averages.scan_type).order_by(
                    data_stage01_isotopomer_averages.fragment_formula.desc(),
                    data_stage01_isotopomer_averages.fragment_mass.asc()).all();
            data_O = [];
            if not data:
                print('No normalized intensities found for the following:')
                print('sample_name_abbreviation: ' + sample_name_abbreviation_I);
                return data_O;
            else:
                # algorithm will break there is no data for a0 mass and there are jumps in the a values (i.e. a0 to a2);
                fragment_formula = '';
                fragment_formula_old = '';
                data_cnt = len(data)-1;
                i = 0;
                while i <= data_cnt:
                    fragment_formula_old = data[i].fragment_formula;
                    row_key = [];
                    row_theoretical = [];
                    row_measured = [];
                    row_measured_cv = [];
                    row_measured_dif = [];
                    row_spectrum_accuracy = [];
                    row = [];
                    for a in range(50):
                        if i <= data_cnt:
                            fragment_formula = data[i].fragment_formula;
                            if fragment_formula == fragment_formula_old:
                                if a == 0:
                                    # add key columns
                                    row_key.append(sample_name_abbreviation_I);
                                    row_key.append(time_point_I);
                                    row_key.append(met_id_I);
                                    row_key.append(data[i].fragment_formula);
                                    row_key.append(str(data[i].precursor_fragment));
                                    row_key.append(data[i].scan_type);
                                    row_spectrum_accuracy.append(data[i].spectrum_accuracy);
                                    mass0 = data[i].fragment_mass
                                massi = data[i].fragment_mass;
                                massDif = massi-mass0;
                                # add a+0... information
                                if data[i].intensity_theoretical: theoretical = numpy.round(data[i].intensity_theoretical,3);
                                else: theoretical = data[i].intensity_theoretical;
                                row_theoretical.append(theoretical)
                                if data[i].intensity_normalized_average: measured = numpy.round(data[i].intensity_normalized_average,3);
                                else: measured = data[i].intensity_normalized_average;
                                row_measured.append(measured)
                                if data[i].intensity_normalized_cv: cv = numpy.round(data[i].intensity_normalized_cv,3);
                                else: cv = data[i].intensity_normalized_cv;
                                row_measured_cv.append(cv);
                                if data[i].abs_devFromTheoretical: dif = numpy.round(data[i].abs_devFromTheoretical,3)
                                else: dif = data[i].abs_devFromTheoretical;
                                row_measured_dif.append(dif)
                                i += 1;
                            else:
                                row_theoretical.append(None);
                                row_measured.append(None);
                                row_measured_cv.append(None);
                                row_measured_dif.append(None);
                        else:
                            row_theoretical.append(None);
                            row_measured.append(None);
                            row_measured_cv.append(None);
                            row_measured_dif.append(None);
                    row.extend(row_key);
                    row.extend(row_theoretical);
                    row.extend(row_measured);
                    row.extend(row_measured_cv);
                    row.extend(row_measured_dif);
                    row.extend(row_spectrum_accuracy);
                    data_O.append(row);
                return data_O;
        except SQLAlchemyError as e:
            print(e);
    # query used and comment from data_stage01_isotopomer_averages
    def get_row_experimentID_dataStage01Averages(self,experiment_id_I):
        '''Querry row information (used and comment) from data_stage01_isotopomer_averages'''
        try:
            data = self.session.query(data_stage01_isotopomer_averages.experiment_id,
                    data_stage01_isotopomer_averages.sample_name_abbreviation,
                    data_stage01_isotopomer_averages.sample_type,
                    data_stage01_isotopomer_averages.time_point,
                    data_stage01_isotopomer_averages.met_id,
                    data_stage01_isotopomer_averages.fragment_formula,
                    data_stage01_isotopomer_averages.fragment_mass,
                    data_stage01_isotopomer_averages.scan_type,
                    data_stage01_isotopomer_averages.used_,
                    data_stage01_isotopomer_averages.comment_).filter(
                    data_stage01_isotopomer_averages.experiment_id.like(experiment_id_I)).all();
            data_O = [];
            if not data:
                print(('No row information found for experiment_id: ' + experiment_id_I));
                return data_O;
            else:
                for d in data:
                    data_tmp = {};
                    data_tmp['experiment_id']=d.experiment_id;
                    data_tmp['sample_name_abbreviation']=d.sample_name_abbreviation;
                    data_tmp['sample_type']=d.sample_type;
                    data_tmp['time_point']=d.time_point;
                    data_tmp['met_id']=d.met_id;
                    data_tmp['fragment_formula']=d.fragment_formula;
                    data_tmp['fragment_mass']=d.fragment_mass;
                    data_tmp['scan_type']=d.scan_type;
                    data_tmp['used_']=d.used_;
                    data_tmp['comment_']=d.comment_;
                    data_O.append(data_tmp);
                return data_O;
        except SQLAlchemyError as e:
            print(e);

    ## Query from data_stage01_isotopomer_averagesNormSum:
    # query time points from data_stage01_isotopomer_averagesNormSum:
    def get_timePoint_experimentID_dataStage01AveragesNormSum(self,experiment_id_I):
        '''Querry time points that are used from the experiment'''
        try:
            time_points = self.session.query(data_stage01_isotopomer_averagesNormSum.time_point).filter(
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True)).group_by(
                    data_stage01_isotopomer_averagesNormSum.time_point).order_by(
                    data_stage01_isotopomer_averagesNormSum.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01AveragesNormSum(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry time points that are used from the experiment and sample name abbreviation'''
        try:
            time_points = self.session.query(data_stage01_isotopomer_averagesNormSum.time_point).filter(
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True)).group_by(
                    data_stage01_isotopomer_averagesNormSum.time_point).order_by(
                    data_stage01_isotopomer_averagesNormSum.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample name abbreviations from data_stage01_isotopomer_averagesNormSum:
    def get_sampleNameAbbreviations_experimentIDAndSampleType_dataStage01AveragesNormSum(self,experiment_id_I,sample_type_I):
        '''Querry sample name abbreviations that are used from
        the experiment'''
        try:
            sample_name_abbreviations = self.session.query(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation).filter(
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I)).group_by(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation).order_by(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation).all();
            sample_name_abbreviations_O = [];
            for sn in sample_name_abbreviations:
                sample_name_abbreviations_O.append(sn[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_experimentIDAndSampleTypeAndTimePoint_dataStage01AveragesNormSum(self,experiment_id_I,sample_type_I,time_point_I):
        '''Querry sample name abbreviations that are used from
        the experiment for specific time-points'''
        try:
            sample_name_abbreviations = self.session.query(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation).filter(
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I)).group_by(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation).order_by(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation).all();
            sample_name_abbreviations_O = [];
            for sn in sample_name_abbreviations:
                sample_name_abbreviations_O.append(sn[0]);
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);
    # query scan types from data_stage01_isotopomer_averagesNormSum
    def get_scanTypes_experimentIDAndTimePointAndSampleAbbreviationsAndSampleType_dataStage01AveragesNormSum(self,experiment_id_I,time_point_I,sample_name_abbreviations_I,sample_type_I):
        '''Querry scan types that are used from the experiment for specific time-points and sample name abbreviations'''
        try:
            scan_types = self.session.query(
                    data_stage01_isotopomer_averagesNormSum.scan_type).filter(
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviations_I)).group_by(
                    data_stage01_isotopomer_averagesNormSum.scan_type).order_by(
                    data_stage01_isotopomer_averagesNormSum.scan_type).all();
            scan_types_O = [];
            for st in scan_types:
                scan_types_O.append(st[0]);
            return scan_types_O;
        except SQLAlchemyError as e:
            print(e);
    # query met_ids  from data_stage01_isotopomer_averagesNormSum
    def get_metIDs_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndScanType_dataStage01AveragesNormSum(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I):
        '''Querry met ids that are used for the experiment, sample abbreviation, time point, scan type'''
        try:
            met_ids = self.session.query(data_stage01_isotopomer_averagesNormSum.met_id).filter(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True)).group_by(
                    data_stage01_isotopomer_averagesNormSum.met_id).order_by(
                    data_stage01_isotopomer_averagesNormSum.met_id.asc()).all();
            met_ids_O = [];
            if not(met_ids):
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	time_point_I	scan_type_I");
                print(experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I);
            else:
                for cn in met_ids:
                    met_ids_O.append(cn[0]);
                return met_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # query fragment formulas  from data_stage01_isotopomer_averagesNormSum
    def get_fragmentFormula_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndScanTypeAndMetID_dataStage01AveragesNormSum(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I,met_id_I):
        '''Querry fragments that are used for the experiment, sample abbreviation, time point, scan type, met id'''
        try:
            fragments = self.session.query(data_stage01_isotopomer_averagesNormSum.fragment_formula).filter(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averagesNormSum.met_id.like(met_id_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True)).group_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_formula).order_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.asc()).all();
            fragments_O = [];
            if not(fragments):
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	time_point_I	scan_type_I met_id_I");
                print(experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I,met_id_I);
            else:
                for cn in fragments:
                    fragments_O.append(cn[0]);
                return fragments_O;
        except SQLAlchemyError as e:
            print(e);
    # query spectrum from data_stage01_isotopomer_averagesNormSum
    def get_spectrum_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndScanTypeAndMetIDAndFragmentFormula_dataStage01AveragesNormSum(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I,met_id_I,fragment_formula_I):
        '''Querry fragments that are used for the experiment, sample abbreviation, time point, scan type, met id'''
        try:
            fragments = self.session.query(data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv).filter(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averagesNormSum.met_id.like(met_id_I),
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.like(fragment_formula_I),
                    data_stage01_isotopomer_averagesNormSum.used_.is_(True)).group_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv).order_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_mass.asc()).all();
            fragment_mass_O = [];
            intensity_normalized_average_O = [];
            intensity_normalized_cv_O = [];
            if not(fragments):
                print("no results found")
                print("experiment_id_I	sample_name_abbreviation_I	time_point_I	scan_type_I met_id_I    fragment_forula_I");
                print(experiment_id_I,sample_name_abbreviation_I,time_point_I,scan_type_I,met_id_I,fragment_forula_I);
            else:
                for cn in fragments:
                    fragment_mass_O.append(cn[0]);
                    intensity_normalized_average_O.append(cn[1]);
                    intensity_normalized_cv_O.append(cn[2]);
                return intensity_normalized_average_O,intensity_normalized_cv_O,fragment_mass_O;
        except SQLAlchemyError as e:
            print(e);
    # query normalized intensity from data_stage01_isotopomer_averagesNormSum
    def get_dataProductFragment_experimentIDAndTimePointSampleAbbreviationAndSampleTypeAndScanTypeAndMetID_dataStage01AveragesNormSum(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I, met_id_I):
        '''Querry peak data for a specific experiment_id, sample_name_abbreviation'''
        try:
            data = self.session.query(data_stage01_isotopomer_averagesNormSum.fragment_formula,
                    data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    MS_components.product_fragment,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv,
                    data_stage01_isotopomer_averagesNormSum.intensity_theoretical,
                    data_stage01_isotopomer_averagesNormSum.abs_devFromTheoretical,
                    data_stage01_isotopomer_spectrumAccuracyNormSum.spectrum_accuracy,
                    data_stage01_isotopomer_averagesNormSum.scan_type).filter(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averagesNormSum.met_id.like(met_id_I),
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.like(MS_components.product_formula),
                    data_stage01_isotopomer_averagesNormSum.met_id.like(MS_components.met_id),
                    MS_components.ms_methodtype.like('tuning'),
                    data_stage01_isotopomer_averagesNormSum.used_,
                    data_stage01_isotopomer_spectrumAccuracyNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.met_id.like(met_id_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.used_.is_(True),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.fragment_formula.like(MS_components.product_formula),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.met_id.like(MS_components.met_id)).group_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_formula,
                    data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    MS_components.product_fragment,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv,
                    data_stage01_isotopomer_averagesNormSum.intensity_theoretical,
                    data_stage01_isotopomer_averagesNormSum.abs_devFromTheoretical,
                    data_stage01_isotopomer_spectrumAccuracyNormSum.spectrum_accuracy,
                    data_stage01_isotopomer_averagesNormSum.scan_type).order_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.desc(),
                    data_stage01_isotopomer_averagesNormSum.fragment_mass.asc()).all();
            data_O = [];
            if not data:
                print('No normalized intensities found for the following:')
                print('sample_name_abbreviation: ' + sample_name_abbreviation_I);
                return data_O;
            else:
                # algorithm will break there is no data for a0 mass and there are jumps in the a values (i.e. a0 to a2);
                fragment_formula = '';
                fragment_formula_old = '';
                data_cnt = len(data)-1;
                i = 0;
                while i <= data_cnt:
                    fragment_formula_old = data[i].fragment_formula;
                    row_key = [];
                    row_theoretical = [];
                    row_measured = [];
                    row_measured_cv = [];
                    row_measured_dif = [];
                    row_spectrum_accuracy = [];
                    row = [];
                    for a in range(50):
                        if i <= data_cnt:
                            fragment_formula = data[i].fragment_formula;
                            if fragment_formula == fragment_formula_old:
                                if a == 0:
                                    # add key columns
                                    row_key.append(sample_name_abbreviation_I);
                                    row_key.append(time_point_I);
                                    row_key.append(met_id_I);
                                    row_key.append(data[i].fragment_formula);
                                    row_key.append(str(data[i].product_fragment));
                                    row_key.append(data[i].scan_type);
                                    row_spectrum_accuracy.append(data[i].spectrum_accuracy);
                                    mass0 = data[i].fragment_mass
                                massi = data[i].fragment_mass;
                                massDif = massi-mass0;
                                # add a+0... information
                                if data[i].intensity_theoretical: theoretical = numpy.round(data[i].intensity_theoretical,3);
                                else: theoretical = data[i].intensity_theoretical;
                                row_theoretical.append(theoretical)
                                if data[i].intensity_normalized_average: measured = numpy.round(data[i].intensity_normalized_average,3);
                                else: measured = data[i].intensity_normalized_average;
                                row_measured.append(measured)
                                if data[i].intensity_normalized_cv: cv = numpy.round(data[i].intensity_normalized_cv,3);
                                else: cv = data[i].intensity_normalized_cv;
                                row_measured_cv.append(cv);
                                if data[i].abs_devFromTheoretical: dif = numpy.round(data[i].abs_devFromTheoretical,3)
                                else: dif = data[i].abs_devFromTheoretical;
                                row_measured_dif.append(dif)
                                i += 1;
                            else:
                                row_theoretical.append(None);
                                row_measured.append(None);
                                row_measured_cv.append(None);
                                row_measured_dif.append(None);
                        else:
                            row_theoretical.append(None);
                            row_measured.append(None);
                            row_measured_cv.append(None);
                            row_measured_dif.append(None);
                    row.extend(row_key);
                    row.extend(row_theoretical);
                    row.extend(row_measured);
                    row.extend(row_measured_cv);
                    row.extend(row_measured_dif);
                    row.extend(row_spectrum_accuracy);
                    data_O.append(row);
                return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_dataPrecursorFragment_experimentIDAndTimePointSampleAbbreviationAndSampleTypeAndScanTypeAndMetID_dataStage01AveragesNormSum(self,experiment_id_I,sample_name_abbreviation_I,time_point_I,sample_type_I,scan_type_I, met_id_I):
        '''Querry peak data for a specific experiment_id, sample_name_abbreviation'''
        try:
            data = self.session.query(data_stage01_isotopomer_averagesNormSum.fragment_formula,
                    data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    MS_components.precursor_fragment,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv,
                    data_stage01_isotopomer_averagesNormSum.intensity_theoretical,
                    data_stage01_isotopomer_averagesNormSum.abs_devFromTheoretical,
                    data_stage01_isotopomer_spectrumAccuracyNormSum.spectrum_accuracy,
                    data_stage01_isotopomer_averagesNormSum.scan_type).filter(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_averagesNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_averagesNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_averagesNormSum.met_id.like(met_id_I),
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.like(MS_components.precursor_formula),
                    data_stage01_isotopomer_averagesNormSum.met_id.like(MS_components.met_id),
                    MS_components.ms_methodtype.like('tuning'),
                    data_stage01_isotopomer_averagesNormSum.used_,
                    data_stage01_isotopomer_spectrumAccuracyNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.time_point.like(time_point_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.sample_type.like(sample_type_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.scan_type.like(scan_type_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.met_id.like(met_id_I),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.used_.is_(True),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.fragment_formula.like(MS_components.precursor_formula),
                    data_stage01_isotopomer_spectrumAccuracyNormSum.met_id.like(MS_components.met_id)).group_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_formula,
                    data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    MS_components.precursor_fragment,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv,
                    data_stage01_isotopomer_averagesNormSum.intensity_theoretical,
                    data_stage01_isotopomer_averagesNormSum.abs_devFromTheoretical,
                    data_stage01_isotopomer_spectrumAccuracyNormSum.spectrum_accuracy,
                    data_stage01_isotopomer_averagesNormSum.scan_type).order_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.desc(),
                    data_stage01_isotopomer_averagesNormSum.fragment_mass.asc()).all();
            data_O = [];
            if not data:
                print('No normalized intensities found for the following:')
                print('sample_name_abbreviation: ' + sample_name_abbreviation_I);
                return data_O;
            else:
                # algorithm will break there is no data for a0 mass and there are jumps in the a values (i.e. a0 to a2);
                fragment_formula = '';
                fragment_formula_old = '';
                data_cnt = len(data)-1;
                i = 0;
                while i <= data_cnt:
                    fragment_formula_old = data[i].fragment_formula;
                    row_key = [];
                    row_theoretical = [];
                    row_measured = [];
                    row_measured_cv = [];
                    row_measured_dif = [];
                    row_spectrum_accuracy = [];
                    row = [];
                    for a in range(50):
                        if i <= data_cnt:
                            fragment_formula = data[i].fragment_formula;
                            if fragment_formula == fragment_formula_old:
                                if a == 0:
                                    # add key columns
                                    row_key.append(sample_name_abbreviation_I);
                                    row_key.append(time_point_I);
                                    row_key.append(met_id_I);
                                    row_key.append(data[i].fragment_formula);
                                    row_key.append(str(data[i].precursor_fragment));
                                    row_key.append(data[i].scan_type);
                                    row_spectrum_accuracy.append(data[i].spectrum_accuracy);
                                    mass0 = data[i].fragment_mass
                                massi = data[i].fragment_mass;
                                massDif = massi-mass0;
                                # add a+0... information
                                if data[i].intensity_theoretical: theoretical = numpy.round(data[i].intensity_theoretical,3);
                                else: theoretical = data[i].intensity_theoretical;
                                row_theoretical.append(theoretical)
                                if data[i].intensity_normalized_average: measured = numpy.round(data[i].intensity_normalized_average,3);
                                else: measured = data[i].intensity_normalized_average;
                                row_measured.append(measured)
                                if data[i].intensity_normalized_cv: cv = numpy.round(data[i].intensity_normalized_cv,3);
                                else: cv = data[i].intensity_normalized_cv;
                                row_measured_cv.append(cv);
                                if data[i].abs_devFromTheoretical: dif = numpy.round(data[i].abs_devFromTheoretical,3)
                                else: dif = data[i].abs_devFromTheoretical;
                                row_measured_dif.append(dif)
                                i += 1;
                            else:
                                row_theoretical.append(None);
                                row_measured.append(None);
                                row_measured_cv.append(None);
                                row_measured_dif.append(None);
                        else:
                            row_theoretical.append(None);
                            row_measured.append(None);
                            row_measured_cv.append(None);
                            row_measured_dif.append(None);
                    row.extend(row_key);
                    row.extend(row_theoretical);
                    row.extend(row_measured);
                    row.extend(row_measured_cv);
                    row.extend(row_measured_dif);
                    row.extend(row_spectrum_accuracy);
                    data_O.append(row);
                return data_O;
        except SQLAlchemyError as e:
            print(e);
    # query row from data_stage01_isotopomer_averagesNormSum
    def get_dataProductFragment_experimentIDAndSampleAbbreviation_dataStage01AveragesNormSum(self,experiment_id_I,sample_name_abbreviation_I):
        '''Querry peak data for a specific experiment_id, sample_name_abbreviation'''
        try:
            data = self.session.query(data_stage01_isotopomer_averagesNormSum.fragment_formula,
                    data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv,
                    data_stage01_isotopomer_averagesNormSum.intensity_theoretical,
                    data_stage01_isotopomer_averagesNormSum.scan_type,
                    data_stage01_isotopomer_averagesNormSum.experiment_id,
                    data_stage01_isotopomer_averagesNormSum.time_point,
                    data_stage01_isotopomer_averagesNormSum.sample_type,
                    data_stage01_isotopomer_averagesNormSum.met_id,
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation,
                    MS_components.product_fragment).filter(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_isotopomer_averagesNormSum.experiment_id.like(experiment_id_I),
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.like(MS_components.product_formula),
                    data_stage01_isotopomer_averagesNormSum.met_id.like(MS_components.met_id),
                    MS_components.ms_methodtype.like('tuning'),
                    data_stage01_isotopomer_averagesNormSum.used_).group_by(
                    data_stage01_isotopomer_averagesNormSum.fragment_formula,
                    data_stage01_isotopomer_averagesNormSum.fragment_mass,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_average,
                    data_stage01_isotopomer_averagesNormSum.intensity_normalized_cv,
                    data_stage01_isotopomer_averagesNormSum.intensity_theoretical,
                    data_stage01_isotopomer_averagesNormSum.scan_type,
                    data_stage01_isotopomer_averagesNormSum.experiment_id,
                    data_stage01_isotopomer_averagesNormSum.time_point,
                    data_stage01_isotopomer_averagesNormSum.sample_type,
                    data_stage01_isotopomer_averagesNormSum.met_id,
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation,
                    MS_components.product_fragment).order_by(
                    data_stage01_isotopomer_averagesNormSum.sample_name_abbreviation.asc(),
                    data_stage01_isotopomer_averagesNormSum.sample_type.asc(),
                    data_stage01_isotopomer_averagesNormSum.met_id.asc(),
                    data_stage01_isotopomer_averagesNormSum.fragment_formula.desc(),
                    data_stage01_isotopomer_averagesNormSum.fragment_mass.asc()).all();
            data_O = [];
            if not data:
                print('No normalized intensities found for the following:')
                print('sample_name_abbreviation: ' + sample_name_abbreviation_I);
                return data_O;
            else:
                for d in data:
                    #TODO:
                    data_O.append(d);
                return data_O;
        except SQLAlchemyError as e:
            print(e);