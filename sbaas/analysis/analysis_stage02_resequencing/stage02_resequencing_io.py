from analysis.analysis_base import *
from analysis.analysis_stage01_resequencing.stage01_resequencing_io import stage01_resequencing_io
from stage02_resequencing_query import stage02_resequencing_query
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import json

class stage02_resequencing_io(stage01_resequencing_io):
    '''class for resequencing analysis'''
    def __init__(self):
        self.session = Session();
        self.stage02_resequencing_query = stage02_resequencing_query();
        self.calculate = base_calculate();
    
    def import_dataStage02ResequencingMapResequencingPhysiology_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02ResequencingMapResequencingPhysiology(data.data);
        data.clear_data();

    def add_dataStage02ResequencingMapResequencingPhysiology(self, data_I):
        '''add rows of data_stage02_resequencing_mapResequencingPhysiology'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_resequencing_mapResequencingPhysiology(
                        d['experiment_id'],
                        d['sample_name'],
                        d['mutation_frequency'],
                        d['mutation_type'],
                        d['mutation_position'],
                        d['mutation_data'],
                        d['mutation_annotations'],
                        d['mutation_genes'],
                        d['mutation_locations'],
                        d['mutation_links'],
                        d['sample_name_abbreviation'],
                        d['met_id'],
                        d['rate_average'],
                        d['rate_var'],
                        d['rate_lb'],
                        d['rate_ub'],
                        d['rate_units'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage02ResequencingMapResequencingPhysiology_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02ResequencingMapResequencingPhysiology(data.data);
        data.clear_data();

    def update_dataStage02ResequencingMapResequencingPhysiology(self,data_I):
        '''update rows of data_stage02_resequencing_mapResequencingPhysiology'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_resequencing_mapResequencingPhysiology).filter(
                           data_stage02_resequencing_mapResequencingPhysiology.id==d['id']).update(
                            {'experiment_id':d['experiment_id'],
                                'sample_name':d['sample_name'],
                                'mutation_frequency':d['mutation_frequency'],
                                'mutation_type':d['mutation_type'],
                                'mutation_position':d['mutation_position'],
                                'mutation_data':d['mutation_data'],
                                'mutation_annotations':d['mutation_annotations'],
                                'mutation_genes':d['mutation_genes'],
                                'mutation_locations':d['mutation_locations'],
                                'mutation_links':d['mutation_links'],
                                'sample_name_abbreviation':d['sample_name_abbreviation'],
                                'met_id':d['met_id'],
                                'rate_average':d['rate_average'],
                                'rate_var':d['rate_var'],
                                'rate_lb':d['rate_lb'],
                                'rate_ub':d['rate_ub'],
                                'rate_units':d['rate_units'],
                                'used_':d['used_'],
                                'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage02ResequencingReduceResequencingPhysiology_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02ResequencingReduceResequencingPhysiology(data.data);
        data.clear_data();

    def add_dataStage02ResequencingReduceResequencingPhysiology(self, data_I):
        '''add rows of data_stage02_resequencing_reduceResequencingPhysiology'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_resequencing_reduceResequencingPhysiology(
                        d['experiment_id'],
                        d['group_name'],
                        d['sample_names'],
                        d['sample_name_abbreviations'],
                        d['resequencing_reduce_id'],
                        d['physiology_reduce_id'],
                        d['reduce_count'],
                        d['mutation_frequencies'],
                        d['mutation_types'],
                        d['mutation_positions'],
                        d['met_ids'],
                        d['rate_averages'],
                        d['rate_vars'],
                        d['rate_lbs'],
                        d['rate_ubs'],
                        d['rate_units'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage02ResequencingReduceResequencingPhysiology_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02ResequencingReduceResequencingPhysiology(data.data);
        data.clear_data();

    def update_dataStage02ResequencingReduceResequencingPhysiology(self,data_I):
        '''update rows of data_stage02_resequencing_reduceResequencingPhysiology'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_resequencing_reduceResequencingPhysiology).filter(
                           data_stage02_resequencing_reduceResequencingPhysiology.id==d['id']).update(
                            {'experiment_id':d['experiment_id'],
                                'group_name':d['group_name'],
                                'sample_names':d['sample_names'],
                                'sample_name_abbreviations':d['sample_name_abbreviations'],
                                'resequencing_reduce_id':d['resequencing_reduce_id'],
                                'physiology_reduce_id':d['physiology_reduce_id'],
                                'reduce_count':d['reduce_count'],
                                'mutation_frequencies':d['mutation_frequencies'],
                                'mutation_types':d['mutation_types'],
                                'mutation_positions':d['mutation_positions'],
                                'met_ids':d['met_ids'],
                                'rate_averages':d['rate_averages'],
                                'rate_vars':d['rate_vars'],
                                'rate_lbs':d['rate_lbs'],
                                'rate_ubs':d['rate_ubs'],
                                'rate_units':d['rate_units'],
                                'used_':d['used_'],
                                'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def export_dataStage02ResequencingLineage_d3_v1(self, experiment_id,group_names_I=[],
                                                 json_var_name='data',
                                                 filename=['visualization/data/','/resequencing-physiology/heatmap/','.js']):
        '''Export data for viewing using d3'''
        #Input:
        #   experiment_id
        #   lineage_names = list of lineage_names to export
        #Output:
        #   
        
        # get group_names
        if group_names_I:
            group_names = group_names_I;
        else:
            group_names = [];
            group_names = self.stage02_resequencing_query.get_groupNames_experimentID_dataStage02ResequencingReduceResequencingPhysiology(experiment_id);
        for gn in group_names:
            # get data for the group
            group_data = [];
            group_data = self.stage02_resequencing_query.get_row_experimentIDAndGroupName_dataStage02ResequencingReduceResequencingPhysiology(experiment_id,gn);
            # find unique mutation_reduce_ids
            mutation_ids = [x['resequencing_reduce_id'] for x in group_data];
            mutation_ids_unique = list(set(mutation_ids));
            mutation_ids_unique.sort();
            physiology_reduce_ids = [x['physiology_reduce_id'] for x in group_data];
            physiology_reduce_unique = list(set(physiology_reduce_ids));
            physiology_reduce_unique.sort();
            # generate the frequency matrix data structure (mutation x intermediate)
            json_O = {};
            data_O = [];
            options_O = {};
            options_O['row_axis_label'] = 'physiology_id';
            options_O['col_axis_label'] = 'resequencing_id';
            options_O['value_label'] = 'count';
            options_O['domain'] = '2';
            labels_O = {};
            labels_O['row_labels']=[];
            labels_O['col_labels']=[];
            labels_O['hcrow']=[];
            labels_O['hccol']=[];
            labels_O['lineage']=[];
            labels_O['maxval']=None;
            labels_O['minval']=None;
            col_cnt = 0;
            # order 2: groups each lineage by mutation (intermediate x mutation)
            for physiology_reduce_id_cnt,physiology_id in enumerate(physiology_reduce_unique): #all lineages for intermediate j / mutation i
                labels_O['row_labels'].append(physiology_id); # corresponding label from hierarchical clustering (in this case, arbitrary)
                labels_O['hcrow'].append(col_cnt+1); # ordering from hierarchical clustering (in this case, arbitrary)
                for mutation_id_cnt,mutation_id in enumerate(mutation_ids_unique): #all mutations i for intermediate j
                    if physiology_reduce_id_cnt==0: # record only once
                        labels_O['col_labels'].append(mutation_id); # corresponding label from hierarchical clustering (in this case, arbitrary)
                        labels_O['lineage'].append(physiology_id);
                        labels_O['hccol'].append(mutation_id_cnt+1); # ordering from hierarchical clustering (in this case, arbitrary)
                    data_tmp = {};
                    data_tmp['col'] = mutation_id_cnt+1;
                    data_tmp['row'] = col_cnt+1;
                    data_tmp['value'] = 0.0;
                    for row in group_data:
                        if row['physiology_reduce_id'] == physiology_id and row['resequencing_reduce_id'] == mutation_id:
                            data_tmp['value'] = row['reduce_count'];
                    data_O.append(data_tmp);
                col_cnt+=1;
            labels_O['maxval']=max([x['value'] for x in data_O]);
            labels_O['minval']=min([x['value'] for x in data_O]);
            json_O['heatmap_data']=data_O;
            json_O.update(labels_O);
            json_O['options'] = options_O;
            # dump the data to a json file
            json_str = 'var ' + json_var_name + ' = ' + json.dumps(json_O);
            filename_str = filename[0] + experiment_id + filename[1] + gn + filename[2]
            with open(filename_str,'w') as file:
                file.write(json_str);

    def export_dataStage02ResequencingLineage_d3(self, experiment_id,group_names_I=[],
                                                 json_var_name='data',
                                                 filename=['visualization/data/','/resequencing-physiology/heatmap/','.js']):
        '''Export data for viewing using d3'''
        #Input:
        #   experiment_id
        #   lineage_names = list of lineage_names to export
        #Output:
        #   
        
        # get group_names
        if group_names_I:
            group_names = group_names_I;
        else:
            group_names = [];
            group_names = self.stage02_resequencing_query.get_groupNames_experimentID_dataStage02ResequencingReduceResequencingPhysiology(experiment_id);
        for gn in group_names:
            # get data for the group
            group_data = [];
            group_data = self.stage02_resequencing_query.get_row_experimentIDAndGroupName_dataStage02ResequencingReduceResequencingPhysiology(experiment_id,gn);
            # find unique mutation_reduce_ids
            mutation_ids = [x['resequencing_reduce_id'] for x in group_data];
            mutation_ids_unique = list(set(mutation_ids));
            mutation_ids_unique.sort();
            physiology_reduce_ids = [x['physiology_reduce_id'] for x in group_data];
            physiology_reduce_unique = list(set(physiology_reduce_ids));
            physiology_reduce_unique.sort();
            # generate the frequency matrix data structure (mutation x intermediate)
            data_O = numpy.zeros((len(physiology_reduce_unique),len(mutation_ids_unique)));
            labels_O = {};
            labels_O['lineage']=[];
            col_cnt = 0;
            # order 2: groups each lineage by mutation (intermediate x mutation)
            for physiology_reduce_id_cnt,physiology_id in enumerate(physiology_reduce_unique): #all lineages for intermediate j / mutation i
                labels_O['lineage'].append(physiology_id);
                for mutation_id_cnt,mutation_id in enumerate(mutation_ids_unique): #all mutations i for intermediate j
                    data_tmp = {};
                    for row in group_data:
                        if row['physiology_reduce_id'] == physiology_id and row['resequencing_reduce_id'] == mutation_id:
                            data_O[physiology_reduce_id_cnt,mutation_id_cnt] = row['reduce_count'];
                col_cnt+=1;
            # generate the clustering for the heatmap
            json_O = {};
            json_O = self.calculate.heatmap(data_O,physiology_reduce_unique,mutation_ids_unique);
            options_O = {};
            options_O['row_axis_label'] = 'physiology_id';
            options_O['col_axis_label'] = 'resequencing_id';
            options_O['value_label'] = 'count';
            options_O['domain'] = '2';
            json_O.update(labels_O);
            json_O['options'] = options_O;
            # dump the data to a json file
            json_str = 'var ' + json_var_name + ' = ' + json.dumps(json_O);
            filename_str = filename[0] + experiment_id + filename[1] + gn + filename[2]
            with open(filename_str,'w') as file:
                file.write(json_str);
