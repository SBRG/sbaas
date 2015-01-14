'''resequencing class'''

from analysis.analysis_base import *
from analysis.analysis_stage01_resequencing.stage01_resequencing_execute import *
from stage02_resequencing_query import *
from stage02_resequencing_io import *

class stage02_resequencing_execute(stage01_resequencing_execute):
    '''class for resequencing analysis'''
    def __init__(self):
        self.session = Session();
        self.stage02_resequencing_query = stage02_resequencing_query();
        self.calculate = base_calculate();
    #table initializations:
    def drop_dataStage02(self):
        try:
            data_stage02_resequencing_mapResequencingPhysiology.__table__.drop(engine,True);
            data_stage02_resequencing_reduceResequencingPhysiology.__table__.drop(engine,True);
            #data_stage01_resequencing_metadata.__table__.drop(engine,True);
            #data_stage01_resequencing_validation.__table__.drop(engine,True);
            #data_stage02_resequencing_reduceResequencingPhysiologyFiltered.__table__.drop(engine,True);
            #data_stage01_resequencing_lineage.__table__.drop(engine,True);
            #data_stage01_resequencing_endpoints.__table__.drop(engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02(self,experiment_id_I = None):
        try:
            if experiment_id_I:
                #reset = self.session.query(data_stage01_resequencing_metadata).filter(data_stage01_resequencing_metadata.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_resequencing_reduceResequencingPhysiology).filter(data_stage02_resequencing_reduceResequencingPhysiology.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_resequencing_mapResequencingPhysiology).filter(data_stage02_resequencing_mapResequencingPhysiology.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                #reset = self.session.query(data_stage01_resequencing_validation).filter(data_stage01_resequencing_validation.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                #reset = self.session.query(data_stage02_resequencing_reduceResequencingPhysiologyFiltered).filter(data_stage02_resequencing_reduceResequencingPhysiologyFiltered.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                #reset = self.session.query(data_stage01_resequencing_lineage).filter(data_stage01_resequencing_lineage.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                #reset = self.session.query(data_stage01_resequencing_endpoints).filter(data_stage01_resequencing_endpoints.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
            else:
                #reset = self.session.query(data_stage01_resequencing_metadata).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_resequencing_reduceResequencingPhysiology).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_resequencing_mapResequencingPhysiology).delete(synchronize_session=False);
                #reset = self.session.query(data_stage01_resequencing_validation).delete(synchronize_session=False);
                #reset = self.session.query(data_stage02_resequencing_reduceResequencingPhysiologyFiltered).delete(synchronize_session=False);
                #reset = self.session.query(data_stage01_resequencing_lineage).delete(synchronize_session=False);
                #reset = self.session.query(data_stage01_resequencing_endpoints).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_dataStage02(self):
        try:
            #data_stage01_resequencing_metadata.__table__.create(engine,True);
            data_stage02_resequencing_reduceResequencingPhysiology.__table__.create(engine,True);
            data_stage02_resequencing_mapResequencingPhysiology.__table__.create(engine,True);
            #data_stage01_resequencing_validation.__table__.create(engine,True);
            #data_stage02_resequencing_reduceResequencingPhysiologyFiltered.__table__.create(engine,True);
            #data_stage01_resequencing_lineage.__table__.create(engine,True);
            #data_stage01_resequencing_endpoints.__table__.create(engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_reduceResequencingPhysiology(self,experiment_id_I = None):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage02_resequencing_reduceResequencingPhysiology).filter(data_stage02_resequencing_reduceResequencingPhysiology.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_resequencing_reduceResequencingPhysiology).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    #analysis:
    def execute_mapResequencingPhysiology_population(self,experiment_id,sample_names_I=[],met_ids_include_I=[]):
        '''Map the mutations found in the resequencing data with the phenotype found in the physiology data'''
        #Input:
        #   experiment_id = id for the experiment
        print 'Executing mapResequencingPysiology_population...'
        genotype_phenotype_O = [];
        # query sample names
        if sample_names_I:
            sample_names = sample_names_I;
        else:
            sample_names = [];
            sample_names = self.stage02_resequencing_query.get_sampleNames_experimentID_dataStage01ResequencingMutationsAnnotated(experiment_id);
        for sn in sample_names:
            print 'analyzing sample_name ' + sn;
            # query mutation data:
            mutations = [];
            mutations = self.stage02_resequencing_query.get_mutations_experimentIDAndSampleName_dataStage01ResequencingMutationsAnnotated(experiment_id,sn);
            mutation_data_O = [];
            for end_cnt,mutation in enumerate(mutations):
                print 'analyzing mutations'
                data_tmp = {};
                data_tmp['mutation_genes'] = mutation['mutation_genes']
                data_tmp['mutation_locations'] = mutation['mutation_locations']
                data_tmp['mutation_annotations'] = mutation['mutation_annotations']
                data_tmp['mutation_links'] = mutation['mutation_links']
                data_tmp['experiment_id'] = mutation['experiment_id'];
                data_tmp['sample_name'] = mutation['sample_name'];
                data_tmp['mutation_frequency'] = mutation['mutation_frequency']
                data_tmp['mutation_position'] = mutation['mutation_position']
                data_tmp['mutation_type'] = mutation['mutation_type']
                data_tmp['mutation_data'] = mutation['mutation_data'];
                mutation_data_O.append(data_tmp);
            # query sample_name_abbreviation:
            sna = None;
            sna = self.stage02_resequencing_query.get_sampleNameAbbreviation_experimentIDAndSampleID_sampleDescription(experiment_id,sn);
            # query met_ids from physiological data
            if met_ids_include_I:
                met_ids = met_ids_include_I;
            else:
                met_ids = [];
                met_ids = self.stage02_resequencing_query.get_metIDs_experimentID_dataStage01PhysiologyRatesAverages(experiment_id,sna);
            phenotype_data_O = [];
            for met in met_ids: 
                print 'analyzing met_id ' + met;
                # query rate data
                slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var = None,None,None,None,None,None,None;
                slope_average, intercept_average, \
                    rate_average, rate_lb, rate_ub, \
                    rate_units, rate_var = self.stage02_resequencing_query.get_rateData_experimentIDAndSampleNameAbbreviationAndMetID_dataStage01PhysiologyRatesAverages(experiment_id,sna,met);
                phenotype_data_O.append({'sample_name_abbreviation':sna,
                            'met_id':met,
                            'rate_average':rate_average,
                            'rate_lb':rate_lb,
                            'rate_ub':rate_ub,
                            'rate_units':rate_units,
                            'rate_var':rate_var});
            # construct the initial genotype/phenotype matrix
            print 'constructing the initial genotype/phenotype matrix';
            for mutation in mutation_data_O:
                for phenotype in phenotype_data_O:
                    tmp = {};
                    tmp.update(mutation);
                    tmp.update(phenotype);
                    genotype_phenotype_O.append(tmp);
                    # add data to the database
                    row = [];
                    row = data_stage02_resequencing_mapResequencingPhysiology(tmp['experiment_id'],
                            tmp['sample_name'],
                            tmp['mutation_frequency'],
                            tmp['mutation_type'],
                            tmp['mutation_position'],
                            tmp['mutation_data'],
                            tmp['mutation_annotations'],
                            tmp['mutation_genes'],
                            tmp['mutation_locations'],
                            tmp['mutation_links'],
                            tmp['sample_name_abbreviation'],
                            tmp['met_id'],
                            tmp['rate_average'],
                            tmp['rate_var'],
                            tmp['rate_lb'],
                            tmp['rate_ub'],
                            tmp['rate_units'],
                            True,
                            None);
                    self.session.add(row);
        self.session.commit();
    def execute_reduceResequencingPhysiology_population(self,experiment_id,group_names,phenotype_reduce_criteria=None,genotype_reduce_critiera=None):
        '''reduce the mutations found in the resequencing data with the phenotype found in the physiology data'''
        #Input:
        #   experiment_id = id for the experiment
        #   group_names = {group_name:[sample_name],}
        #   phenotype_reduce_criteria = {'met_id':{rate_range:['none','low','medium','high']};
        #   phenotype_reduce_criteria = default: {'ac':{rate_range:['none','low','high']}},
        #                                         'lac-L':{rate_range:['none','low','high']}},
        #                                         'succ':{rate_range:['none','low','high']}},
        #                                         'glc-D':{rate_range:['low','medium','high']}},
        #                                         'biomass':{rate_range:['low','medium','high']}}};
        #   genotype_reduce_critiera = {'mutation_frequency': Boolean,'mutation_position': Boolean, 'mutation_type': Boolean,'mutation_genes': Boolean,'mutation_locations': Boolean}
        #   genotype_reduce_critiera = default1: {'mutation_frequency': False,'mutation_position': True, 'mutation_type': True,'mutation_genes': False,'mutation_locations': False}
        #   genotype_reduce_critiera = default2: {'mutation_frequency': False,'mutation_position': False, 'mutation_type': True,'mutation_genes': True,'mutation_locations': False}
        #Output:
        #   mutation_frequencies = [float]
        #   sample_names = [string]
        #   sample_count = int;
        #   reduce_criteria = string

        print 'Executing reduceResequencingPhysiology...'
        data_O = [];
        for gn,sample_names in group_names.iteritems():
            print 'Reducing group_name ' + gn;
            group_data = [];
            # get all data for the group
            for sn in sample_names:
                # get data
                data = [];
                data = self.stage02_resequencing_query.get_row_experimentIDAndSampleName_dataStage02ResequencingMapResequencingPhysiology(experiment_id,sn);
                group_data.extend(data);
            # list out the unique mutations
            mutation_ids = [];
            for gd in group_data:
                mutation_genes_str = '';
                for gene in gd['mutation_genes']:
                    mutation_genes_str = mutation_genes_str + gene + '-/-'
                mutation_genes_str = mutation_genes_str[:-3];
                mutation_ids.append(mutation_genes_str + '_' + gd['mutation_type'] + '_' + str(gd['mutation_position']));
            mutation_ids_unique = list(set(mutation_ids));
            # assign a unique resequencing_id
            for i,gd in enumerate(group_data):
                # assign a resequencing_id
                mutation_genes_str = '';
                for gene in gd['mutation_genes']:
                    mutation_genes_str = mutation_genes_str + gene + '-/-'
                mutation_genes_str = mutation_genes_str[:-3];
                mutation_genes_str += '_' + gd['mutation_type'] + '_' + str(gd['mutation_position']);
                group_data[i].update({'resequencing_id':mutation_genes_str});
            # list out the unique met_ids
            met_ids = [x['met_id'] for x in group_data];
            met_ids_unique = list(set(met_ids));
            # find the max and min for each metabolite
            mets = {};
            group_data_add = [];
            for met_id in met_ids_unique:
                mets[met_id] = {'lb':[],'ub':[],'ave':[],'var':[]};
                for sn in sample_names:
                    met_id_absent = True;
                    for gd in group_data:
                        if met_id == gd['met_id'] and sn == gd['sample_name']:
                            mets[met_id]['ave'].append(gd['rate_average']);
                            mets[met_id]['lb'].append(gd['rate_lb']);
                            mets[met_id]['ub'].append(gd['rate_ub']);
                            mets[met_id]['var'].append(gd['rate_var']);
                            met_id_absent = False;
                            break;
                    if met_id_absent:
                        for mutation_id in mutation_ids_unique:
                            for gd in group_data:
                                if mutation_id == gd['resequencing_id'] and sn == gd['sample_name']:
                                    group_data_add.append({'experiment_id':gd['experiment_id'],
                                    'sample_name':sn,
                                    'mutation_frequency':gd['mutation_frequency'],
                                    'mutation_type':gd['mutation_type'],
                                    'mutation_position':gd['mutation_position'],
                                    'mutation_data':gd['mutation_data'],
                                    'mutation_annotations':gd['mutation_annotations'],
                                    'mutation_genes':gd['mutation_genes'],
                                    'mutation_locations':gd['mutation_locations'],
                                    'mutation_links':gd['mutation_links'],
                                    'sample_name_abbreviation':gd['sample_name_abbreviation'],
                                    'met_id':met_id,
                                    'rate_average':0.0,
                                    'rate_var':0.0,
                                    'rate_lb':0.0,
                                    'rate_ub':0.0,
                                    'rate_units':None,
                                    'used_':False,
                                    'comment_':'spaceholder',
                                    'resequencing_id':gd['resequencing_id']});
                                    break;
            group_data.extend(group_data_add);
            mets_max = {};
            for k,v in mets.iteritems():
                mets_max[k]=0.0;
                mets_max[k] = max(v['ave']);
            # assign a category to each sample
            physiology_reduce_ids = [];
            for met_id in met_ids_unique:
                for level in ['none','low','medium','high']:
                    pid = met_id + '_' + level;
                    physiology_reduce_ids.append(pid);
            physiology_reduce_unique = list(set(physiology_reduce_ids));
            for i,gd in enumerate(group_data):
                # assign a physiology_id
                if gd['rate_average'] == 0.0:
                    pid = gd['met_id']+'_'+'none'
                    group_data[i].update({'physiology_id':pid});
                    #physiology_reduce_ids.append(pid);
                elif gd['rate_average']/mets_max[gd['met_id']] < 1.0/3.0:
                    pid = gd['met_id']+'_'+'low'
                    group_data[i].update({'physiology_id':pid});
                    #physiology_reduce_ids.append(pid);
                elif gd['rate_average']/mets_max[gd['met_id']] >= 1.0/3.0 and gd['rate_average']/mets_max[gd['met_id']] < 2.0/3.0:
                    pid = gd['met_id']+'_'+'medium'
                    group_data[i].update({'physiology_id':pid});
                    #physiology_reduce_ids.append(pid);
                elif gd['rate_average']/mets_max[gd['met_id']] >= 2.0/3.0:
                    pid = gd['met_id']+'_'+'high'
                    group_data[i].update({'physiology_id':pid});
                    #physiology_reduce_ids.append(pid);
            # reduce
            for mutation_id in mutation_ids_unique:
                for physiology_id in physiology_reduce_unique:
                    data_O_tmp = {};
                    data_O_tmp['experiment_id'] = experiment_id;
                    data_O_tmp['group_name'] = gn;
                    data_O_tmp['sample_names'] = [];
                    data_O_tmp['sample_name_abbreviations'] = [];
                    data_O_tmp['resequencing_reduce_id'] = mutation_id;
                    data_O_tmp['physiology_reduce_id'] = physiology_id;
                    data_O_tmp['reduce_count'] = 0;
                    data_O_tmp['mutation_frequencies'] = [];
                    data_O_tmp['mutation_types'] = [];
                    data_O_tmp['mutation_positions'] = [];
                    data_O_tmp['met_ids'] = [];
                    data_O_tmp['rate_averages'] = [];
                    data_O_tmp['rate_vars'] = [];
                    data_O_tmp['rate_lbs'] = [];
                    data_O_tmp['rate_ubs'] = [];
                    data_O_tmp['rate_units'] = [];
                    for gd in group_data:
                        if gd.has_key('resequencing_id') and gd.has_key('physiology_id') and\
                            gd['resequencing_id'] == mutation_id and gd['physiology_id'] == physiology_id:
                            data_O_tmp['sample_names'].append(gd['sample_name']);
                            data_O_tmp['sample_name_abbreviations'].append(gd['sample_name_abbreviation']);
                            data_O_tmp['mutation_frequencies'].append(gd['mutation_frequency']);
                            data_O_tmp['mutation_types'].append(gd['mutation_type']);
                            data_O_tmp['mutation_positions'].append(gd['mutation_position']);
                            data_O_tmp['met_ids'].append(gd['met_id']);
                            data_O_tmp['rate_averages'].append(gd['rate_average']);
                            data_O_tmp['rate_vars'].append(gd['rate_var']);
                            data_O_tmp['rate_lbs'].append(gd['rate_lb']);
                            data_O_tmp['rate_ubs'].append(gd['rate_ub']);
                            data_O_tmp['rate_units'].append(gd['rate_units']);
                            data_O_tmp['reduce_count'] += 1;
                    data_O.append(data_O_tmp);
        for d in data_O:
            if d['reduce_count'] != 0:
                # add data to the database:
                row = [];
                row = data_stage02_resequencing_reduceResequencingPhysiology(
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
                        True,None);
                self.session.add(row);
        self.session.commit();
    #analysis TODO:    
    def execute_correlateResequencingPysiology_population(self,experiment_id,phenotype_reduce_criteria,genotype_reduce_critiera):
        '''Correlate the mutations found in the resequencing data with the phenotype found in the physiology data'''
        #Input:
        #   experiment_id = id for the experiment
        return
    
    def execute_quantifyResequencingPysiology_population(self,experiment_id,phenotype_reduce_criteria,genotype_reduce_critiera):
        '''Quantify the change in phenotype found in the physiology data over that of a base strain due to a change in frequency of mutation'''
        #Input:
        #   experiment_id = id for the experiment
        #   group_names = {group_name:{'initial':strain_name,'final':strain_name},}
        #Output:
        #   met_id
        #   mutation_...
        #   change = change in rate / change in mutation frequency
        return
