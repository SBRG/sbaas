from analysis.analysis_base import *
from analysis.analysis_stage01_resequencing.stage01_resequencing_io import stage01_resequencing_io
from .stage02_resequencing_query import stage02_resequencing_query
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import json

class stage02_resequencing_io(stage01_resequencing_io):
    '''class for resequencing analysis'''
    def __init__(self,session_I=None):
        if session_I: self.session = session_I;
        else: self.session = Session();
        self.stage02_resequencing_query = stage02_resequencing_query(self.session);
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

    def export_dataStage02ResequencingLineage_d3(self, experiment_id,group_names_I=[],
                                                 json_var_name='data',
                                                 filename=['visualization/data/','/resequencing-physiology/heatmap/','.js']):
        '''Export data for viewing using d3'''
        #Input:
        #   experiment_id
        #   analysis_ids = list of analysis_ids to export
        #Output:
        #   

        #TODO: drive from analysis
        
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

    def import_dataStage02ResequencingAnalysis_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02ResequencingAnalysis(data.data);
        data.clear_data();

    def add_dataStage02ResequencingAnalysis(self, data_I):
        '''add rows of data_stage02_resequencing_analysis'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_resequencing_analysis(
                        d['analysis_id'],
                        d['experiment_id'],
                        d['sample_name'],
                        d['sample_name_abbreviation'],
                        d['analysis_type'],
                        d['reduce_criteria_1'],
                        d['reduce_criteria_2'],
                        d['used_'],
                        d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage02ResequencingAnalysis_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02ResequencingAnalysisy(data.data);
        data.clear_data();

    def update_dataStage02ResequencingAnalysis(self,data_I):
        '''update rows of data_stage02_resequencing_analysis'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_resequencing_analysis).filter(
                           data_stage02_resequencing_analysis.id==d['id']).update(
                            {'analysis_id':d['analysis_id'],
                            'experiment_id':d['experiment_id'],
                            'sample_name':d['sample_name'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'analysis_type':d['analysis_type'],
                            'reduce_criteria_1':d['reduce_criteria_1'],
                            'reduce_criteria_2':d['reduce_criteria_2'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def export_dataStage02ResequencingHeatmap_js(self,analysis_id_I,data_dir_I="tmp"):
        """export heatmap to js file"""

        #get the heatmap data for the analysis
        data_O = self.stage02_resequencing_query.get_rows_analysisID_dataStage02ResequencingHeatmap(analysis_id_I);
        # dump chart parameters to a js files
        data1_keys = [
            #'analysis_id',
                      'row_label','col_label','row_index','col_index','row_leaves','col_leaves',
                'col_pdist_metric','row_pdist_metric','col_linkage_method','row_linkage_method',
                'value_units']
        data1_nestkeys = ['analysis_id'];
        data1_keymap = {'xdata':'row_leaves','ydata':'col_leaves','zdata':'value',
                'rowslabel':'row_label','columnslabel':'col_label',
                'rowsindex':'row_index','columnsindex':'col_index',
                'rowsleaves':'row_leaves','columnsleaves':'col_leaves'};
        # make the data object
        dataobject_O = [{"data":data_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys}];
        # make the tile parameter objects
        svgparameters_O = {"svgtype":'heatmap2d_01',"svgkeymap":[data1_keymap],
                            'svgid':'svg1',
                             'svgcellsize':18,'svgmargin':{ 'top': 200, 'right': 50, 'bottom': 100, 'left': 200 },
                            'svgcolorscale':'quantile',
                            'svgcolorcategory':'heatmap10',
                            'svgcolordomain':'min,max',
                            'svgcolordatalabel':'value',
                            'svgdatalisttileid':'tile1'};
        svgtileparameters_O = {'tileheader':'heatmap','tiletype':'svg','tileid':"tile2",'rowid':"row2",'colid':"col2",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"};
        svgtileparameters_O.update(svgparameters_O);
        formtileparameters_O = {'tileheader':'filter menu','tiletype':'html','tileid':"tile1",'rowid':"row1",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"
            
            };
        formparameters_O = {'htmlid':'datalist1','htmltype':'datalist_01','datalist': [{'value':'hclust','text':'by cluster'},
                            {'value':'probecontrast','text':'by row and column'},
                            {'value':'probe','text':'by row'},
                            {'value':'contrast','text':'by column'},
                            {'value':'custom','text':'by value'}]}
        formtileparameters_O.update(formparameters_O);
        tile2datamap_O = {"tile1":[0],"tile2":[0]};
        parametersobject_O = [ formtileparameters_O,svgtileparameters_O];

        data_str = 'var ' + 'data' + ' = ' + json.dumps(dataobject_O) + ';';
        parameters_str = 'var ' + 'parameters' + ' = ' + json.dumps(parametersobject_O) + ';';
        tile2datamap_str = 'var ' + 'tile2datamap' + ' = ' + json.dumps(tile2datamap_O) + ';';
        if data_dir_I=='tmp':
            filename_str = settings.visualization_data + '/tmp/ddt_data.js'
        elif data_dir_I=='project':
            filename_str = settings.visualization_data + '/project/' + analysis_id_I + '_data_stage02_resequencing_heatmap' + '.js'
        elif data_dir_I=='data_json':
            data_json_O = data_str + '\n' + parameters_str + '\n' + tile2datamap_str;
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(data_str);
            file.write(parameters_str);
            file.write(tile2datamap_str);
