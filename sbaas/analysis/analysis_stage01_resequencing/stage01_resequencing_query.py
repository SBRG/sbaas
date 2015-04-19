from analysis.analysis_base import *
import json

class stage01_resequencing_query(base_analysis):
    # query sample names from data_stage01_resequencing_metadata
    def get_sampleNames_experimentID_dataStage01ResequencingMetadata(self,experiment_id_I,exp_type_I=8):
        '''Query samples names from resequencing metadata'''
        try:
            sample_names = self.session.query(data_stage01_resequencing_metadata.experiment_id,
                    data_stage01_resequencing_metadata.sample_name).filter(
                    data_stage01_resequencing_metadata.experiment_id.like(experiment_id_I),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(data_stage01_resequencing_metadata.sample_name)).order_by(
                    data_stage01_resequencing_metadata.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: 
                sample_names_O.append(sn.sample_name);
            return sample_names_O
        except SQLAlchemyError as e:
            print(e);

    # query data from data_stage01_resequencing_mutations
    def get_mutations_experimentIDAndSampleName_dataStage01ResequencingMutations(self,experiment_id_I,sample_name_I,
              frequency_criteria=0.1):
        '''Query mutation data
        NOTES:
        1. JSON is not a standard type across databases, therefore the key/values of the JSON
            object will be filtered post-query'''
        #1 filter sample_names that do not meet the frequency criteria
        try:
            data = self.session.query(data_stage01_resequencing_mutations).filter(
                    data_stage01_resequencing_mutations.experiment_id.like(experiment_id_I),
                    data_stage01_resequencing_mutations.sample_name.like(sample_name_I)).all();
            data_O = [];
            for d in data: 
                data_dict = {};
                data_dict['experiment_id'] = d.experiment_id;
                data_dict['sample_name'] = d.sample_name;
                data_dict['mutation_id'] = d.mutation_id;
                data_dict['parent_ids'] = d.parent_ids;
                data_dict['mutation_data'] = d.mutation_data;
                #data_dict['mutation_data'] = json.loads(d.mutation_data);
                data_O.append(data_dict);
            # filter:
            data_filtered = [];
            for d in data_O:
                if d['mutation_data'].has_key('frequency') and d['mutation_data']['frequency'] >= frequency_criteria:
                    data_filtered.append(d);
                #note: frequency is only provided for population resequences
                elif not d['mutation_data'].has_key('frequency'):
                    data_filtered.append(d);
            return data_filtered;
        except SQLAlchemyError as e:
            print(e);
            
    # query data from data_stage01_resequencing_evidence
    def get_evidence_experimentIDAndSampleNameAndParentID_dataStage01ResequencingEvidence(self,experiment_id_I,sample_name_I,parent_id_I,
              p_value_criteria=0.01,quality_criteria=6.0,frequency_criteria=0.1):
        '''Query evidence data
        NOTES:
        1. JSON is not a standard type across databases, therefore the key/values of the JSON
            object will be filtered post-query'''
        #2 filter sample_names by evidence-specific criteria
        try:
            data = self.session.query(data_stage01_resequencing_evidence).filter(
                    data_stage01_resequencing_evidence.experiment_id.like(experiment_id_I),
                    data_stage01_resequencing_evidence.sample_name.like(sample_name_I),
                    data_stage01_resequencing_evidence.parent_id == parent_id_I).all();
            data_O = [];
            for d in data: 
                data_dict = {};
                data_dict['experiment_id'] = d.experiment_id;
                data_dict['sample_name'] = d.sample_name;
                data_dict['parent_id'] = d.parent_id;
                data_dict['evidence_data'] = d.evidence_data;
                #data_dict['evidence_data'] = json.loads(d.evidence_data);
                data_O.append(data_dict);
            # filter:
            data_filtered = [];
            data_filtered_dict = {};
            for d in data_O:
                if d['evidence_data']['type'] == 'RA':
                    #population only
                    if d['evidence_data'].has_key('quality') and \
                        d['evidence_data'].has_key('bias_p_value') and \
                        d['evidence_data'].has_key('fisher_strand_p_value') and \
                        d['evidence_data'].has_key('frequency') and \
                        d['evidence_data']['frequency'] >= frequency_criteria and \
                        d['evidence_data']['quality'] >= quality_criteria and \
                        d['evidence_data']['bias_p_value'] <= p_value_criteria and \
                        d['evidence_data']['fisher_strand_p_value'] <= p_value_criteria:
                        data_filtered_dict = d;
                        data_filtered.append(d);
                    #population and isolate
                    elif d['evidence_data'].has_key('quality') and \
                        d['evidence_data'].has_key('frequency') and \
                        d['evidence_data']['frequency'] >= frequency_criteria and \
                        d['evidence_data']['quality'] >= quality_criteria:
                        data_filtered_dict = d;
                        data_filtered.append(d);
                elif d['evidence_data']['type'] == 'JC':
                    data_filtered_dict = d;
                    data_filtered.append(d);
                elif d['evidence_data']['type'] == 'MC':
                    data_filtered_dict = d;
                    data_filtered.append(d);
                elif d['evidence_data']['type'] == 'UN':
                    data_filtered_dict = d;
                    data_filtered.append(d);
                else:
                    print 'mutation evidence of type ' + d['evidence_data']['type'] +\
                        ' has not yet been included in the filter criteria';
            return data_filtered_dict;
        except SQLAlchemyError as e:
            print(e);
            
    # query data from data_stage01_resequencing_mutationsFiltered
    def get_sampleNames_experimentID_dataStage01ResequencingMutationsFiltered(self,experiment_id_I):
        '''Query mutation data'''
        try:
            data = self.session.query(data_stage01_resequencing_mutationsFiltered.sample_name).filter(
                    data_stage01_resequencing_mutationsFiltered.experiment_id.like(experiment_id_I)).group_by(
                    data_stage01_resequencing_mutationsFiltered.sample_name).order_by(
                    data_stage01_resequencing_mutationsFiltered.sample_name.asc()).all();
            sample_names_O = [];
            for d in data: 
                sample_names_O.append(d.sample_name);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query data from data_stage01_resequencing_mutationsFiltered
    def get_mutations_experimentIDAndSampleName_dataStage01ResequencingMutationsFiltered(self,experiment_id_I,sample_name_I):
        '''Query mutation data'''
        try:
            data = self.session.query(data_stage01_resequencing_mutationsFiltered.experiment_id,
                    data_stage01_resequencing_mutationsFiltered.sample_name,
                    data_stage01_resequencing_mutationsFiltered.mutation_id,
                    data_stage01_resequencing_mutationsFiltered.parent_ids,
                    data_stage01_resequencing_mutationsFiltered.mutation_data).filter(
                    data_stage01_resequencing_mutationsFiltered.experiment_id.like(experiment_id_I),
                    data_stage01_resequencing_mutationsFiltered.sample_name.like(sample_name_I)).all();
            data_O = [];
            for d in data: 
                data_dict = {};
                data_dict['experiment_id'] = d.experiment_id;
                data_dict['sample_name'] = d.sample_name;
                data_dict['mutation_id'] = d.mutation_id;
                data_dict['parent_ids'] = d.parent_ids;
                data_dict['mutation_data'] = d.mutation_data;
                #data_dict['mutation_data'] = json.loads(d.mutation_data);
                data_O.append(data_dict);
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    # query gene names from biologicalMaterial_geneReferences
    def get_orderedLocusName_biologicalmaterialIDAndGeneName_biologicalMaterialGeneReferences(self,biologicalmaterial_id_I,gene_name_I):
        '''Query ordered locus name from gene name'''
        try:
            data = self.session.query(biologicalMaterial_geneReferences.biologicalmaterial_id,
                    biologicalMaterial_geneReferences.gene_name,
                    biologicalMaterial_geneReferences.ordered_locus_name).filter(
                    biologicalMaterial_geneReferences.biologicalmaterial_id.like(biologicalmaterial_id_I),
                    biologicalMaterial_geneReferences.gene_name.like(gene_name_I)).all();
            data_O = [];
            for d in data: 
                data_dict = {};
                data_dict['ordered_locus_name'] = d.ordered_locus_name;
                data_O.append(data_dict);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_ecogeneAccessionNumber_biologicalmaterialIDAndGeneName_biologicalMaterialGeneReferences(self,biologicalmaterial_id_I,gene_name_I):
        '''Query ecogene accession number from gene name'''
        try:
            data = self.session.query(biologicalMaterial_geneReferences.biologicalmaterial_id,
                    biologicalMaterial_geneReferences.gene_name,
                    biologicalMaterial_geneReferences.ecogene_accession_number).filter(
                    biologicalMaterial_geneReferences.biologicalmaterial_id.like(biologicalmaterial_id_I),
                    biologicalMaterial_geneReferences.gene_name.like(gene_name_I)).all();
            data_O = [];
            for d in data: 
                data_dict = {};
                data_dict['ecogene_accession_number'] = d.ecogene_accession_number;
                data_O.append(data_dict);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_geneName_biologicalmaterialIDAndOrderedLocusName_biologicalMaterialGeneReferences(self,biologicalmaterial_id_I,ordered_locus_name_I):
        '''Query gene name from ordered locus name'''
        try:
            data = self.session.query(biologicalMaterial_geneReferences.biologicalmaterial_id,
                    biologicalMaterial_geneReferences.gene_name,
                    biologicalMaterial_geneReferences.ordered_locus_name).filter(
                    biologicalMaterial_geneReferences.biologicalmaterial_id.like(biologicalmaterial_id_I),
                    biologicalMaterial_geneReferences.ordered_locus_name.like(ordered_locus_name_I)).all();
            data_O = [];
            for d in data: 
                data_dict = {};
                data_dict['ordered_locus_name'] = d.ordered_locus_name;
                data_O.append(data_dict);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_ecogeneAccessionNumber_biologicalmaterialIDAndOrderedLocusName_biologicalMaterialGeneReferences(self,biologicalmaterial_id_I,ordered_locus_name_I):
        '''Query ecogene accession number from ordered locus name name'''
        try:
            data = self.session.query(biologicalMaterial_geneReferences.biologicalmaterial_id,
                    biologicalMaterial_geneReferences.ordered_locus_name,
                    biologicalMaterial_geneReferences.ecogene_accession_number).filter(
                    biologicalMaterial_geneReferences.biologicalmaterial_id.like(biologicalmaterial_id_I),
                    biologicalMaterial_geneReferences.ordered_locus_name.like(ordered_locus_name_I)).all();
            data_O = [];
            for d in data: 
                data_dict = {};
                data_dict['ecogene_accession_number'] = d.ecogene_accession_number;
                data_O.append(data_dict);
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    # query sample names from data_stage01_resequencing_lineage
    def get_sampleNames_experimentID_dataStage01ResequencingLineage(self,experiment_id_I):
        '''Query samples names from resequencing lineage'''
        try:
            sample_names = self.session.query(data_stage01_resequencing_lineage.experiment_id,
                    data_stage01_resequencing_lineage.sample_name).filter(
                    data_stage01_resequencing_lineage.experiment_id.like(experiment_id_I)).group_by(data_stage01_resequencing_lineage.experiment_id,
                    data_stage01_resequencing_lineage.sample_name).order_by(
                    data_stage01_resequencing_lineage.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: 
                sample_names_O.append(sn.sample_name);
            return sample_names_O
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNames_experimentIDAndLineageName_dataStage01ResequencingLineage(self,experiment_id_I,lineage_name_I):
        '''Query samples names from resequencing lineage'''
        try:
            data = self.session.query(data_stage01_resequencing_lineage.experiment_id,
                    data_stage01_resequencing_lineage.sample_name).filter(
                    data_stage01_resequencing_lineage.experiment_id.like(experiment_id_I),
                    data_stage01_resequencing_lineage.lineage_name.like(lineage_name_I)).group_by(
                    data_stage01_resequencing_lineage.experiment_id,
                    data_stage01_resequencing_lineage.sample_name).order_by(
                    data_stage01_resequencing_lineage.lineage_name.asc()).all();
            data_O = [];
            for d in data: 
                #data_tmp = {};
                #data_tmp['sample_name']=d.sample_name;
                #data_O.append(data_tmp);
                data_O.append(d.sample_name);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    # Query intermediates from data_stage01_resequencing_lineage
    def get_intermediates_experimentIDAndLineageName_dataStage01ResequencingLineage(self,experiment_id_I,lineage_name_I):
        '''Query intermediates from resequencing lineage'''
        try:
            data = self.session.query(data_stage01_resequencing_lineage.experiment_id,
                    data_stage01_resequencing_lineage.intermediate).filter(
                    data_stage01_resequencing_lineage.experiment_id.like(experiment_id_I),
                    data_stage01_resequencing_lineage.lineage_name.like(lineage_name_I)).group_by(
                    data_stage01_resequencing_lineage.experiment_id,
                    data_stage01_resequencing_lineage.intermediate).order_by(
                    data_stage01_resequencing_lineage.intermediate.asc()).all();
            data_O = [];
            for d in data: 
                #data_tmp = {};
                #data_tmp['intermediate']=d.intermediate;
                #data_O.append(data_tmp);
                data_O.append(d.intermediate);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    # query mutation information from data_stage01_resequencing_lineage
    def get_mutationData_experimentIDAndLineageName_dataStage01ResequencingLineage(self,experiment_id_I,lineage_name_I):
        '''Query mutation information from resequencing lineage'''
        try:
            data = self.session.query(data_stage01_resequencing_lineage.mutation_type,
                    data_stage01_resequencing_lineage.mutation_position,
                    data_stage01_resequencing_lineage.mutation_genes,
                    data_stage01_resequencing_lineage.mutation_locations).filter(
                    data_stage01_resequencing_lineage.experiment_id.like(experiment_id_I),
                    data_stage01_resequencing_lineage.lineage_name.like(lineage_name_I)).group_by(
                    data_stage01_resequencing_lineage.mutation_type,
                    data_stage01_resequencing_lineage.mutation_position,
                    data_stage01_resequencing_lineage.mutation_genes,
                    data_stage01_resequencing_lineage.mutation_locations).order_by(
                    data_stage01_resequencing_lineage.mutation_type.asc(),
                    data_stage01_resequencing_lineage.mutation_position.asc(),
                    data_stage01_resequencing_lineage.mutation_genes.asc(),
                    data_stage01_resequencing_lineage.mutation_locations.asc()).all();
            data_O = [];
            for d in data: 
                #data_tmp = {};
                #data_tmp['mutation_type']=d.mutation_type;
                #data_tmp['mutation_position']=d.mutation_position;
                #data_tmp['mutation_genes']=d.mutation_genes;
                #data_tmp['mutation_locations']=d.mutation_locations;
                #data_O.append(data_tmp);
                data_tmp_str = '';
                mutation_genes_str = '';
                for gene in d.mutation_genes:
                    mutation_genes_str = mutation_genes_str + gene + '-/-'
                mutation_genes_str = mutation_genes_str[:-3];
                #mutation_locations_str = '';
                #for location in d.mutation_locations:
                #    mutation_locations_str = mutation_locations_str + location + '&'
                #mutation_locations_str = mutation_locations_str[:-1];
                data_tmp_str = d.mutation_type+'_'+mutation_genes_str+'_'+str(d.mutation_position)
                data_O.append(data_tmp_str);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    # query row from data_stage01_resequencing_lineage
    def get_row_experimentIDAndSampleName_dataStage01ResequencingLineage(self,experiment_id_I,sample_name_I):
        '''Query samples names from resequencing lineage'''
        try:
            data = self.session.query(data_stage01_resequencing_lineage).filter(
                    data_stage01_resequencing_lineage.experiment_id.like(experiment_id_I),
                    data_stage01_resequencing_lineage.sample_name.like(sample_name_I)).all();
            data_O = [];
            for d in data: 
                data_tmp = {};
                data_tmp['id']=d.id;
                data_tmp['experiment_id']=d.experiment_id;
                data_tmp['lineage_name']=d.lineage_name;
                data_tmp['sample_name']=d.sample_name;
                data_tmp['intermediate']=d.intermediate;
                data_tmp['mutation_frequency']=d.mutation_frequency;
                data_tmp['mutation_type']=d.mutation_type;
                data_tmp['mutation_position']=d.mutation_position;
                data_tmp['mutation_data']=d.mutation_data;
                data_tmp['mutation_annotations']=d.mutation_annotations;
                data_tmp['mutation_genes']=d.mutation_genes;
                data_tmp['mutation_locations']=d.mutation_locations;
                data_tmp['mutation_links']=d.mutation_links;
                data_tmp['comment_']=d.comment_;
                data_O.append(data_tmp);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_row_experimentIDAndLineageName_dataStage01ResequencingLineage(self,experiment_id_I,lineage_name_I):
        '''Query samples names from resequencing lineage'''
        try:
            data = self.session.query(data_stage01_resequencing_lineage).filter(
                    data_stage01_resequencing_lineage.experiment_id.like(experiment_id_I),
                    data_stage01_resequencing_lineage.lineage_name.like(lineage_name_I)).all();
            data_O = [];
            for d in data: 
                data_tmp = {};
                data_tmp['id']=d.id;
                data_tmp['experiment_id']=d.experiment_id;
                data_tmp['lineage_name']=d.lineage_name;
                data_tmp['sample_name']=d.sample_name;
                data_tmp['intermediate']=d.intermediate;
                data_tmp['mutation_frequency']=d.mutation_frequency;
                data_tmp['mutation_type']=d.mutation_type;
                data_tmp['mutation_position']=d.mutation_position;
                data_tmp['mutation_data']=d.mutation_data;
                data_tmp['mutation_annotations']=d.mutation_annotations;
                data_tmp['mutation_genes']=d.mutation_genes;
                data_tmp['mutation_locations']=d.mutation_locations;
                data_tmp['mutation_links']=d.mutation_links;
                data_tmp['comment_']=d.comment_;
                data_tmp_str = '';
                mutation_genes_str = '';
                for gene in d.mutation_genes:
                    mutation_genes_str = mutation_genes_str + gene + '-/-'
                mutation_genes_str = mutation_genes_str[:-3];
                #mutation_locations_str = '';
                #for location in d.mutation_locations:
                #    mutation_locations_str = mutation_locations_str + location + '&'
                #mutation_locations_str = mutation_locations_str[:-1];
                data_tmp_str = d.mutation_type+'_'+mutation_genes_str+'_'+str(d.mutation_position)
                data_tmp['mutation_id'] = data_tmp_str;
                data_O.append(data_tmp);
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    # query sample names from data_stage01_resequencing_endpoints
    def get_sampleNames_experimentID_dataStage01ResequencingEndpoints(self,experiment_id_I):
        '''Query samples names from resequencing endpoints'''
        try:
            sample_names = self.session.query(data_stage01_resequencing_endpoints.experiment_id,
                    data_stage01_resequencing_endpoints.sample_name).filter(
                    data_stage01_resequencing_endpoints.experiment_id.like(experiment_id_I)).group_by(data_stage01_resequencing_endpoints.experiment_id,
                    data_stage01_resequencing_endpoints.sample_name).order_by(
                    data_stage01_resequencing_endpoints.sample_name.asc()).all();
            sample_names_O = [];
            for sn in sample_names: 
                sample_names_O.append(sn.sample_name);
            return sample_names_O
        except SQLAlchemyError as e:
            print(e);
    # query row from data_stage01_resequencing_endpoints
    def get_row_experimentIDAndSampleName_dataStage01ResequencingEndpoints(self,experiment_id_I,sample_name_I):
        '''Query samples names from resequencing endpoints'''
        try:
            data = self.session.query(data_stage01_resequencing_endpoints).filter(
                    data_stage01_resequencing_endpoints.experiment_id.like(experiment_id_I),
                    data_stage01_resequencing_endpoints.sample_name.like(sample_name_I)).all();
            data_O = [];
            for d in data: 
                data_tmp = {};
                data_tmp['id']=d.id;
                data_tmp['experiment_id']=d.experiment_id;
                data_tmp['analysis_id']=d.analysis_id;
                data_tmp['sample_name']=d.sample_name;
                data_tmp['mutation_frequency']=d.mutation_frequency;
                data_tmp['mutation_type']=d.mutation_type;
                data_tmp['mutation_position']=d.mutation_position;
                data_tmp['mutation_data']=d.mutation_data;
                data_tmp['isUnique']=d.isUnique;
                data_tmp['mutation_annotations']=d.mutation_annotations;
                data_tmp['mutation_genes']=d.mutation_genes;
                data_tmp['mutation_locations']=d.mutation_locations;
                data_tmp['mutation_links']=d.mutation_links;
                data_tmp['comment_']=d.comment_;
                data_O.append(data_tmp);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
   
    # query data from data_stage01_resequencing_mutationsAnnotated
    def get_mutations_experimentIDAndSampleName_dataStage01ResequencingMutationsAnnotated(self,experiment_id_I,sample_name_I):
        '''Query mutation data'''
        try:
            data = self.session.query(data_stage01_resequencing_mutationsAnnotated).filter(
                    data_stage01_resequencing_mutationsAnnotated.experiment_id.like(experiment_id_I),
                    data_stage01_resequencing_mutationsAnnotated.sample_name.like(sample_name_I)).all();
            data_O = [];
            for d in data: 
                data_dict = {'experiment_id':d.experiment_id,
                            'sample_name':d.sample_name,
                            'mutation_frequency':d.mutation_frequency,
                            'mutation_type':d.mutation_type,
                            'mutation_position':d.mutation_position,
                            'mutation_data':d.mutation_data,
                            'mutation_annotations':d.mutation_annotations,
                            'mutation_genes':d.mutation_genes,
                            'mutation_locations':d.mutation_locations,
                            'mutation_links':d.mutation_links,
                            'used_':d.used_,
                            'comment_':d.comment_};
                data_O.append(data_dict);
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    # query data from data_stage01_resequencing_analysis
    def get_analysis_analysisID_dataStage01ResequencingAnalysis(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage01_resequencing_analysis).filter(
                    data_stage01_resequencing_analysis.analysis_id.like(analysis_id_I),
                    data_stage01_resequencing_analysis.used_.is_(True)).all();
            analysis_id_O = []
            experiment_id_O = []
            lineage_name_O = []
            sample_name_O = []
            analysis_type_O = []
            analysis_O = {};
            if data: 
                for d in data:
                    analysis_id_O.append(d.analysis_id);
                    experiment_id_O.append(d.experiment_id);
                    lineage_name_O.append(d.lineage_name);
                    sample_name_O.append(d.sample_name);
                    analysis_type_O.append(d.analysis_type);
                analysis_id_O = list(set(analysis_id_O))
                experiment_id_O = list(set(experiment_id_O))
                lineage_name_O = list(set(lineage_name_O))
                sample_name_O = list(set(sample_name_O))
                analysis_type_O = list(set(analysis_type_O))
                analysis_O={
                        'analysis_id':analysis_id_O,
                        'experiment_id':experiment_id_O,
                        'lineage_name':lineage_name_O,
                        'sample_name':sample_name_O,
                        'analysis_type':analysis_type_O};
                
            return analysis_O;
        except SQLAlchemyError as e:
            print(e);
    def get_experimentIDAndLineageName_analysisID_dataStage01ResequencingAnalysis(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage01_resequencing_analysis.experiment_id,
                    data_stage01_resequencing_analysis.lineage_name).filter(
                    data_stage01_resequencing_analysis.analysis_id.like(analysis_id_I),
                    data_stage01_resequencing_analysis.used_.is_(True)).group_by(
                    data_stage01_resequencing_analysis.experiment_id,
                    data_stage01_resequencing_analysis.lineage_name).order_by(
                    data_stage01_resequencing_analysis.experiment_id.asc(),
                    data_stage01_resequencing_analysis.lineage_name.asc()).all();
            experiment_id_O = []
            lineage_name_O = []
            if data: 
                for d in data:
                    experiment_id_O.append(d.experiment_id);
                    lineage_name_O.append(d.lineage_name);                
            return  experiment_id_O,lineage_name_O;
        except SQLAlchemyError as e:
            print(e);
    def get_experimentIDAndSampleName_analysisID_dataStage01ResequencingAnalysis(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage01_resequencing_analysis.experiment_id,
                    data_stage01_resequencing_analysis.sample_name).filter(
                    data_stage01_resequencing_analysis.analysis_id.like(analysis_id_I),
                    data_stage01_resequencing_analysis.used_.is_(True)).group_by(
                    data_stage01_resequencing_analysis.experiment_id,
                    data_stage01_resequencing_analysis.sample_name).order_by(
                    data_stage01_resequencing_analysis.experiment_id.asc(),
                    data_stage01_resequencing_analysis.sample_name.asc()).all();
            experiment_id_O = []
            sample_name_O = []
            if data: 
                for d in data:
                    experiment_id_O.append(d.experiment_id);
                    sample_name_O.append(d.sample_name);                
            return  experiment_id_O,sample_name_O;
        except SQLAlchemyError as e:
            print(e);
    def get_experimentIDAndSampleNameAndTimePoint_analysisID_dataStage01ResequencingAnalysis(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage01_resequencing_analysis.experiment_id,
                    data_stage01_resequencing_analysis.sample_name,
                    data_stage01_resequencing_analysis.time_point).filter(
                    data_stage01_resequencing_analysis.analysis_id.like(analysis_id_I),
                    data_stage01_resequencing_analysis.used_.is_(True)).group_by(
                    data_stage01_resequencing_analysis.experiment_id,
                    data_stage01_resequencing_analysis.sample_name,
                    data_stage01_resequencing_analysis.time_point).order_by(
                    data_stage01_resequencing_analysis.experiment_id.asc(),
                    data_stage01_resequencing_analysis.sample_name.asc(),
                    data_stage01_resequencing_analysis.time_point.asc()).all();
            experiment_id_O = []
            sample_name_O = []
            time_point_O = []
            if data: 
                for d in data:
                    experiment_id_O.append(d.experiment_id);
                    sample_name_O.append(d.sample_name);    
                    time_point_O.append(d.time_point);              
            return  experiment_id_O,sample_name_O,time_point_O;
        except SQLAlchemyError as e:
            print(e);

    # query data from data_stage01_resequencing_heatmap
    def get_rows_analysisID_dataStage01ResequencingHeatmap(self,analysis_id_I):
        '''Query rows from data_stage01_resequencing_heatmap'''
        try:
            data = self.session.query(data_stage01_resequencing_heatmap).filter(
                    data_stage01_resequencing_heatmap.analysis_id.like(analysis_id_I),
                    data_stage01_resequencing_heatmap.used_).all();
            data_O = [];
            for d in data: 
                data_dict = {'analysis_id':d.analysis_id,
                    'col_index':d.col_index,
                    'row_index':d.row_index,
                    'value':d.value,
                    'col_leaves':d.col_leaves,
                    'row_leaves':d.row_leaves,
                    'col_label':d.col_label,
                    'row_label':d.row_label,
                    'col_pdist_metric':d.col_pdist_metric,
                    'row_pdist_metric':d.row_pdist_metric,
                    'col_linkage_method':d.col_linkage_method,
                    'row_linkage_method':d.row_linkage_method,
                    'value_units':d.value_units,
                    'used_':d.used_,
                    'comment_':d.comment_};
                data_O.append(data_dict);
            return data_O;
        except SQLAlchemyError as e:
            print(e);