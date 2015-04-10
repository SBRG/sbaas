from analysis.analysis_base import *
from analysis.analysis_stage01_resequencing.stage01_resequencing_query import stage01_resequencing_query
from analysis.analysis_stage01_physiology.stage01_physiology_query import stage01_physiology_query
import json

class stage02_resequencing_query(stage01_resequencing_query,stage01_physiology_query):
    # query sample_name_abbreviation from sample_description
    def get_sampleNameAbbreviation_experimentIDAndSampleID_sampleDescription(self,experiment_id_I,sample_id_I):
        '''Query description by sample id from sample_description'''
        try:
            data = self.session.query(sample_description.sample_name_abbreviation).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.sample_name_abbreviation).all();
            sample_name_abbreviation_O = None;
            if len(data)>2:
                print 'more than 1 sample name abbreviation found!'
            if data: 
                sample_name_abbreviation_O=data[0].sample_name_abbreviation;
            return sample_name_abbreviation_O;
        except SQLAlchemyError as e:
            print(e);
            
    # query sample names from data_stage02_resequencing_mapResequencingPhysiology
    def get_sampleNames_experimentID_dataStage02ResequencingMapResequencingPhysiology(self,experiment_id_I):
        '''Query samples names from resequencing lineage'''
        try:
            sample_names = self.session.query(data_stage02_resequencing_mapResequencingPhysiology.experiment_id,
                    data_stage02_resequencing_mapResequencingPhysiology.sample_name).filter(
                    data_stage02_resequencing_mapResequencingPhysiology.experiment_id.like(experiment_id_I)).group_by(data_stage02_resequencing_mapResequencingPhysiology.experiment_id,
                    data_stage02_resequencing_mapResequencingPhysiology.sample_name).order_by(
                    data_stage02_resequencing_mapResequencingPhysiology.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: 
                sample_names_O.append(sn.sample_name);
            return sample_names_O
        except SQLAlchemyError as e:
            print(e);
    # query row from data_stage02_resequencing_mapResequencingPhysiology
    def get_row_experimentIDAndSampleName_dataStage02ResequencingMapResequencingPhysiology(self,experiment_id_I,sample_name_I):
        '''Query samples names from resequencing lineage'''
        try:
            data = self.session.query(data_stage02_resequencing_mapResequencingPhysiology).filter(
                    data_stage02_resequencing_mapResequencingPhysiology.experiment_id.like(experiment_id_I),
                    data_stage02_resequencing_mapResequencingPhysiology.sample_name.like(sample_name_I)).all();
            data_O = [];
            for d in data: 
                data_tmp = {'experiment_id':d.experiment_id,
                'sample_name':d.sample_name,
                'mutation_frequency':d.mutation_frequency,
                'mutation_type':d.mutation_type,
                'mutation_position':d.mutation_position,
                'mutation_data':d.mutation_data,
                'mutation_annotations':d.mutation_annotations,
                'mutation_genes':d.mutation_genes,
                'mutation_locations':d.mutation_locations,
                'mutation_links':d.mutation_links,
                'sample_name_abbreviation':d.sample_name_abbreviation,
                'met_id':d.met_id,
                'rate_average':d.rate_average,
                'rate_var':d.rate_var,
                'rate_lb':d.rate_lb,
                'rate_ub':d.rate_ub,
                'rate_units':d.rate_units,
                'used_':d.used_,
                'comment_':d.comment_};
                data_O.append(data_tmp);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    
    # query group names from data_stage02_resequencing_reduceResequencingPhysiology
    def get_groupNames_experimentID_dataStage02ResequencingReduceResequencingPhysiology(self,experiment_id_I):
        '''Query group names from data_stage02_resequencing_reduceResequencingPhysiology'''
        try:
            group_names = self.session.query(data_stage02_resequencing_reduceResequencingPhysiology.experiment_id,
                    data_stage02_resequencing_reduceResequencingPhysiology.group_name).filter(
                    data_stage02_resequencing_reduceResequencingPhysiology.experiment_id.like(experiment_id_I)).group_by(data_stage02_resequencing_reduceResequencingPhysiology.experiment_id,
                    data_stage02_resequencing_reduceResequencingPhysiology.group_name).order_by(
                    data_stage02_resequencing_reduceResequencingPhysiology.group_name.asc()).all();
            group_names_O = [];
            for sn in group_names: 
                group_names_O.append(sn.group_name);
            return group_names_O
        except SQLAlchemyError as e:
            print(e);
    # query row from data_stage02_resequencing_reduceResequencingPhysiology
    def get_row_experimentIDAndGroupName_dataStage02ResequencingReduceResequencingPhysiology(self,experiment_id_I,group_name_I):
        '''Query row'''
        try:
            data = self.session.query(data_stage02_resequencing_reduceResequencingPhysiology).filter(
                    data_stage02_resequencing_reduceResequencingPhysiology.experiment_id.like(experiment_id_I),
                    data_stage02_resequencing_reduceResequencingPhysiology.group_name.like(group_name_I)).all();
            data_O = [];
            for d in data: 
                data_tmp = {'experiment_id':d.experiment_id,
                    'group_name':d.group_name,
                    'sample_names':d.sample_names,
                    'sample_name_abbreviations':d.sample_name_abbreviations,
                    'resequencing_reduce_id':d.resequencing_reduce_id,
                    'physiology_reduce_id':d.physiology_reduce_id,
                    'reduce_count':d.reduce_count,
                    'mutation_frequencies':d.mutation_frequencies,
                    'mutation_types':d.mutation_types,
                    'mutation_positions':d.mutation_positions,
                    'met_ids':d.met_ids,
                    'rate_averages':d.rate_averages,
                    'rate_vars':d.rate_vars,
                    'rate_lbs':d.rate_lbs,
                    'rate_ubs':d.rate_ubs,
                    'rate_units':d.rate_units,
                    'used_':d.used_,
                    'comment_':d.comment_};
                data_O.append(data_tmp);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
