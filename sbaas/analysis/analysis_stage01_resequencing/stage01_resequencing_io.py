from analysis.analysis_base import *
from stage01_resequencing_query import stage01_resequencing_query
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from analysis.analysis_stage01_resequencing import gdparse
import json

class stage01_resequencing_io(base_analysis):
    '''class for resequencing analysis'''
    def __init__(self):
        self.session = Session();
        self.stage01_resequencing_query = stage01_resequencing_query();
        self.calculate = base_calculate();
    
    def import_resequencingData_add(self, filename, experiment_id, sample_name):
        '''table adds'''
        gd = gdparse.GDParser(file_handle=open(filename, 'rb'))
        # extract out ids
        mutation_ids = [];
        mutation_ids = gd.data['mutation'].keys()
        parent_ids = [];
        for mid in mutation_ids:
            parents = [];
            parents = gd.data['mutation'][mid]['parent_ids'];
            parent_ids.extend(parents);
        # split into seperate data structures based on the destined table add
        metadata = [];
        mutation_data = [];
        evidence_data = [];
        validation_data = [];
        if gd.metadata:
            metadata.append({'experiment_id':experiment_id,
                                 'sample_name':sample_name,
                                 'genome_diff':gd.metadata['GENOME_DIFF'],
                                 'refseq':gd.metadata['REFSEQ'],
                                 'readseq':gd.metadata['READSEQ'],
                                 'author':gd.metadata['AUTHOR']});
        if gd.data['mutation']:
            for mid in mutation_ids:
                mutation_data.append({'experiment_id':experiment_id,
                                 'sample_name':sample_name,
                                 'mutation_id':mid,
                                 'parent_ids':gd.data['mutation'][mid]['parent_ids'],
                                 'mutation_data':gd.data['mutation'][mid]});
                                 #'mutation_data':json.dumps(gd.data['mutation'][mid])});
        if gd.data['evidence']:
            for pid in parent_ids:
                evidence_data.append({'experiment_id':experiment_id,
                                 'sample_name':sample_name,
                                 'parent_id':pid,
                                 'evidence_data':gd.data['evidence'][pid]});
                                 #'evidence_data':json.dumps(gd.data['evidence'][pid])});
        if gd.data['validation']:
            for mid in mutation_ids:
                validation_data.append({'experiment_id':experiment_id,
                                 'sample_name':sample_name,
                                 'validation_id':mid,
                                 'validation_data':gd.data['validation'][mid]});
                                 #'validation_data':json.dumps(gd.data['validation'][mid])});
        # add data to the database:
        self.add_dataStage01ResequencingMetadata(metadata);
        self.add_dataStage01ResequencingMutations(mutation_data);
        self.add_dataStage01ResequencingEvidence(evidence_data);
        self.add_dataStage01ResequencingValidation(validation_data);

    def add_dataStage01ResequencingMutations(self, data_I):
        '''add rows of data_stage01_resequencing_mutations'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage01_resequencing_mutations(d['experiment_id'],
                                    d['sample_name'],
                                    d['mutation_id'],
                                    d['parent_ids'],
                                    d['mutation_data']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_dataStage01ResequencingMetadata(self, data_I):
        '''add rows of data_stage01_resequencing_metadata'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage01_resequencing_metadata(d['experiment_id'],
                            d['sample_name'],
                            d['genome_diff'],
                            d['refseq'],
                            d['readseq'],
                            d['author']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_dataStage01ResequencingEvidence(self, data_I):
        '''add rows of data_stage01_resequencing_evidence'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage01_resequencing_evidence(d['experiment_id'],
                        d['sample_name'],
                        d['parent_id'],
                        d['evidence_data']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_dataStage01ResequencingValidation(self, data_I):
        '''add rows of data_stage01_resequencing_validation'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage01_resequencing_validation(d['experiment_id'],
                        d['sample_name'],
                        d['validation_id'],
                        d['validation_data']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage01ResequencingLineage_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage01ResequencingLineage(data.data);
        data.clear_data();

    def add_dataStage01ResequencingLineage(self, data_I):
        '''add rows of data_stage01_resequencing_lineage'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage01_resequencing_lineage(d['experiment_id'],
                                d['analysis_id'],
                                d['sample_name'],
                                d['intermediate'],
                                d['mutation_frequency'],
                                d['mutation_type'],
                                d['mutation_position'],
                                d['mutation_data'],
                                d['mutation_annotations'],
                                d['mutation_genes'],
                                d['mutation_locations'],
                                d['mutation_links'],
                                d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage01ResequencingLineage_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01ResequencingLineage(data.data);
        data.clear_data();

    def update_dataStage01ResequencingLineage(self,data_I):
        '''update rows of data_stage01_resequencing_lineage'''
        if data_I:
            for d in data_I:
                try:
                    #if d['mutation_genes']:
                    #    d['mutation_genes']=d['mutation_genes'].split();
                    #if d['mutation_location']:
                    #    d['mutation_location']=d['mutation_location'].split();
                    data_update = self.session.query(data_stage01_resequencing_lineage).filter(
                           data_stage01_resequencing_lineage.id==d['id']).update(
                            {'experiment_id':d['experiment_id'],
                                'analysis_id':d['analysis_id'],
                                'sample_name':d['sample_name'],
                                'intermediate':d['intermediate'],
                                'mutation_frequency':d['mutation_frequency'],
                                'mutation_type':d['mutation_type'],
                                'mutation_position':d['mutation_position'],
                                'mutation_data':d['mutation_data'],
                                'mutation_annotations':d['mutation_annotations'],
                                'mutation_genes':d['mutation_genes'],
                                'mutation_locations':d['mutation_locations'],
                                'mutation_links':d['mutation_links'],
                                'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage01ResequencingEndpoints_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage01ResequencingEndpoints(data.data);
        data.clear_data();

    def add_dataStage01ResequencingEndpoints(self, data_I):
        '''add rows of data_stage01_resequencing_endpoints'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage01_resequencing_endpoints(d['experiment_id'],
                            d['analysis_id'],
                            d['sample_name'],
                            d['mutation_frequency'],
                            d['mutation_type'],
                            d['mutation_position'],
                            d['mutation_data'],
                            d['isUnique'],
                            d['mutation_annotations'],
                            d['mutation_genes'],
                            d['mutation_locations'],
                            d['mutation_links'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage01ResequencingEndpoints_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01ResequencingEndpoints(data.data);
        data.clear_data();

    def update_dataStage01ResequencingEndpoints(self,data_I):
        '''update rows of data_stage01_resequencing_endpoints'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage01_resequencing_endpoints).filter(
                           data_stage01_resequencing_endpoints.id==d['id']).update(
                            {'experiment_id':d['experiment_id'],
                            'analysis_id':d['analysis_id'],
                            'sample_name':d['sample_name'],
                            'mutation_frequency':d['mutation_frequency'],
                            'mutation_type':d['mutation_type'],
                            'mutation_position':d['mutation_position'],
                            'mutation_data':d['mutation_data'],
                            'isUnique':d['isUnique'],
                            'mutation_annotations':d['mutation_annotations'],
                            'mutation_genes':d['mutation_genes'],
                            'mutation_locations':d['mutation_locations'],
                            'mutation_links':d['mutation_links'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def export_dataStage01ResequencingLineage_d3(self, experiment_id, analysis_ids,
                                                 filename='visualization/data/ALEsKOs01/resequencing/heatmap/data.js',
                                                 json_var_name='data',
                                                 mutation_id_exclusion_list = []):
        '''Export data for viewing using d3'''
        #Input:
        #   experiment_id
        #   analysis_ids = list of analysis_ids to export
        #Output:
        #   
        
        intermediates_lineage = [];
        mutation_data_lineage_all = [];
        rows_lineage = [];
        n_lineages = len(analysis_ids)
        cnt_sample_names = 0;
        for analysis_id in analysis_ids:
            ## get ALL sample names by experiment_id and lineage name
            #sample_names = [];
            #sample_names = self.stage01_resequencing_query.get_sampleNames_experimentIDAndLineageName_dataStage01ResequencingLineage(experiment_id,analysis_id);
            # get ALL intermediates by experiment_id and lineage name
            intermediates = [];
            intermediates = self.stage01_resequencing_query.get_intermediates_experimentIDAndLineageName_dataStage01ResequencingLineage(experiment_id,analysis_id);
            intermediates_lineage.append(intermediates);
            cnt_sample_names += len(intermediates)
            # get ALL mutation data by experiment_id and lineage name
            mutation_data = [];
            mutation_data = self.stage01_resequencing_query.get_mutationData_experimentIDAndLineageName_dataStage01ResequencingLineage(experiment_id,analysis_id);
            mutation_data_lineage_all.extend(mutation_data);
            # get ALL mutation frequencies by experiment_id and lineage name
            rows = [];
            rows = self.stage01_resequencing_query.get_row_experimentIDAndLineageName_dataStage01ResequencingLineage(experiment_id,analysis_id)
            rows_lineage.extend(rows);
        mutation_data_lineage_unique = list(set(mutation_data_lineage_all));
        mutation_data_lineage = [x for x in mutation_data_lineage_unique if not x in mutation_id_exclusion_list];
        min_inter = min(intermediates_lineage)
        max_inter = max(intermediates_lineage);
        # generate the frequency matrix data structure (mutation x intermediate)
        data_O = numpy.zeros((cnt_sample_names,len(mutation_data_lineage)));
        labels_O = {};
        labels_O['lineage']=[];
        col_cnt = 0;
        # order 2: groups each lineage by mutation (intermediate x mutation)
        for analysis_id_cnt,analysis_id in enumerate(analysis_ids): #all lineages for intermediate j / mutation i
            for intermediate_cnt,intermediate in enumerate(intermediates_lineage[analysis_id_cnt]):
                if intermediate_cnt == min(intermediates_lineage[analysis_id_cnt]):
                    labels_O['lineage'].append(analysis_id+": "+"start"); # corresponding label from hierarchical clustering (in this case, arbitrary)
                elif intermediate_cnt == max(intermediates_lineage[analysis_id_cnt]):
                    labels_O['lineage'].append(analysis_id+": "+"end"); # corresponding label from hierarchical clustering (in this case, arbitrary)
                else:
                    labels_O['lineage'].append(analysis_id+": "+str(intermediate)); # corresponding label from hierarchical clustering (in this case, arbitrary)
                for mutation_cnt,mutation in enumerate(mutation_data_lineage): #all mutations i for intermediate j
                    for row in rows_lineage:
                        if row['mutation_id'] == mutation and row['intermediate'] == intermediate and row['analysis_id'] == analysis_id:
                            data_O[col_cnt,mutation_cnt] = row['mutation_frequency'];
                            print col_cnt,mutation_cnt
                col_cnt+=1;
        # generate the clustering for the heatmap
        json_O = {};
        json_O = self.calculate.heatmap(data_O,labels_O['lineage'],mutation_data_lineage);
        options_O = {};
        options_O['row_axis_label'] = 'lineage_id';
        options_O['col_axis_label'] = 'mutation_id';
        options_O['value_label'] = 'population frequency';
        options_O['domain'] = '2';
        json_O.update(labels_O);
        json_O['options'] = options_O;
        # dump the data to a json file
        json_str = 'var ' + json_var_name + ' = ' + json.dumps(json_O);
        with open(filename,'w') as file:
            file.write(json_str);

    def export_dataStage01ResequencingMutationsAnnotated_d3(self,experiment_id,strain_lineage,mutation_id_exclusion_list=[],frequency_threshold=0.1):
        '''Plot the mutation frequency accross the strain lineage for all filtered mutations'''
        
        print 'Executing plotMutationFrequency_population...'
        for analysis_id,strain in strain_lineage.iteritems():
            print 'analyzing lineage ' + analysis_id;
            intermediates = strain.keys();
            intermediates.sort();
            mutation_data_O = [];
            mutation_ids = [];
            for intermediate in intermediates:
                print 'analyzing intermediate ' + str(intermediate);
                # query mutation data:
                mutations = [];
                mutations = self.stage01_resequencing_query.get_mutations_experimentIDAndSampleName_dataStage01ResequencingMutationsAnnotated(experiment_id,strain[intermediate]);
                for end_cnt,mutation in enumerate(mutations):
                    print 'analyzing mutations'
                    if mutation['mutation_position'] > 4000000: #ignore positions great than 4000000
                        continue;
                    if mutation['mutation_frequency']<frequency_threshold:
                        continue;
                    # mutation id
                    mutation_genes_str = '';
                    for gene in mutation['mutation_genes']:
                        mutation_genes_str = mutation_genes_str + gene + '-/-'
                    mutation_genes_str = mutation_genes_str[:-3];
                    mutation_id = mutation_genes_str + '_' + mutation['mutation_type'] + '_' + str(mutation['mutation_position'])
                    tmp = {};
                    tmp.update(mutation);
                    tmp.update({'mutation_id':mutation_id});
                    mutation_data_O.append(tmp);
                    mutation_ids.append(mutation_id);
            mutation_ids_screened = [x for x in mutation_ids if x not in mutation_id_exclusion_list];
            mutation_ids_unique = list(set(mutation_ids_screened));
            data_O = [];
            data_fitted_O = [];
            for intermediate in intermediates:
                for mutation_id in mutation_ids_unique:
                    tmp = {};
                    tmp_fitted = {};
                    tmp['samples']=mutation_id
                    tmp['x_data']=intermediate
                    tmp['y_data']=0.0;
                    tmp_fitted['samples']=mutation_id
                    tmp_fitted['x_data_fitted']=intermediate
                    tmp_fitted['y_data_fitted']=0.0;
                    for mutation in mutation_data_O:
                        if strain[intermediate] == mutation['sample_name'] and mutation_id == mutation['mutation_id']:
                            tmp['y_data']=mutation['mutation_frequency'];
                            tmp_fitted['y_data_fitted']=mutation['mutation_frequency'];
                            break;
                    data_O.append(tmp);
                    data_fitted_O.append(tmp_fitted);
            #Update js variable
            options_O = {};
            options_O['x_axis'] = [];
            options_O['y_axis'] = [];
            options_O['x_axis_label'] = 'lineage';
            options_O['y_axis_label'] = 'frequency';
            options_O['feature_name'] = 'mutation';
            options_O['fit_function'] = 'linear';
            json_O = {};
            json_O['data'] = data_O;
            json_O['data_fitted'] = data_fitted_O;
            json_O['options'] = options_O;
            # dump the data to a json file
            json_str = 'var ' + 'data' + ' = ' + json.dumps(json_O);
            filename_str = 'visualization/data/' + experiment_id + '/resequencing/scatterlineplot/' + analysis_id + '.js'
            with open(filename_str,'w') as file:
                file.write(json_str);

    def import_dataStage01ResequencingAnalysis_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage01ResequencingAnalysis(data.data);
        data.clear_data();

    def add_dataStage01ResequencingAnalysis(self, data_I):
        '''add rows of data_stage01_resequencing_analysis'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage01_resequencing_analysis(d['analysis_id'],
                            d['experiment_id'],
                            d['sample_name'],
                            d['time_point'],
                            d['analysis_type'],
                            d['used_'],
                            d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_dataStage01ResequencingAnalysis_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage01ResequencingAnalysis(data.data);
        data.clear_data();

    def update_dataStage01ResequencingAnalysis(self,data_I):
        '''update rows of data_stage01_resequencing_lineage'''
        if data_I:
            for d in data_I:
                try:
                    #if d['mutation_genes']:
                    #    d['mutation_genes']=d['mutation_genes'].split();
                    #if d['mutation_location']:
                    #    d['mutation_location']=d['mutation_location'].split();
                    data_update = self.session.query(data_stage01_resequencing_analysis).filter(
                           data_stage01_resequencing_analysis.id==d['id']).update(
                            {'analysis_id':d['analysis_id'],
                            'experiment_id':d['experiment_id'],
                            'sample_name':d['sample_name'],
                            'time_point':d['time_point'],
                            'analysis_type':d['analysis_type'],
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
