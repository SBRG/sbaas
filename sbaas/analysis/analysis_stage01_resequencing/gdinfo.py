#breseq_evidenceTypes
#script
import gdparse

gd = gdparse.GDParser(file_handle= open(r'C:\Users\dmccloskey-sbrg\Desktop\reseq_data\Evo04pgiEvo01EP\Evo04pgiEvo01EP\output.gd', 'rb'))

def find_uniqueEvidenceKeys():
    #what are all of the different evidence keys?
    mutation_ids = [];
    mutation_ids = gd.data['mutation'].keys()
    parent_ids = [];
    for mid in mutation_ids:
        parents = [];
        parents = gd.data['mutation'][mid]['parent_ids'];
        parent_ids.extend(parents);
    evidence_fields = [];
    for pid in parent_ids:
        evidence = [];
        evidence = gd.data['evidence'][pid].keys()
        evidence_fields.extend(evidence)
    evidence_fields_unique = [];
    evidence_fields_unique = list(set(evidence_fields))
    #evidence_fields_unique
    #['key', 'side_1_read_count', 'log10_qual_likelihood_position_model', 'left_inside_cov', 'max_min_left', 'left_outside_cov', 'polymorphism_quality', 'side_2_seq_id', 'coverage_minus', 'new_junction_coverage', 'new_cov', 'side_2_strand', 'side_1_position', 'ks_quality_p_value', 'frequency', 'max_min_left_plus', 'side_2_annotate_key', 'start_range', 'alignment_overlap', 'quality', 'bias_e_value', 'end_range', 'side_2_overlap', 'flanking_left', 'continuation_right', 'max_left', 'neg_log10_pos_hash_p_value', 'seq_id', 'total_non_overlap_reads', 'coverage_plus', 'side_1_strand', 'overlap', 'quality_position_model', 'fisher_strand_p_value', 'ref_base', 'max_left_plus', 'max_left_minus', 'side_2_redundant', 'type', 'start', 'max_right_minus', 'new_base', 'genotype_quality', 'side_1_redundant', 'right_inside_cov', 'max_min_left_minus', 'new_junction_read_count', 'max_pos_hash_score', 'new_junction_frequency', 'side_1_coverage', 'log10_base_likelihood', 'max_right_plus', 'pos_hash_score', 'end', 'right_outside_cov', 'continuation_left', 'side_1_overlap', 'bias_p_value', 'max_min_right', 'flanking_right', 'max_right', 'ref_cov', 'side_2_coverage', 'side_1_seq_id', 'side_2_position', 'insert_position', 'log10_strand_likelihood_position_model', 'max_min_right_plus', 'side_2_read_count', 'position', 'max_min_right_minus', 'tot_cov', 'side_1_annotate_key']

def find_uniqueEvidenceKeysByEvidenceType():
    #what are the different evidence keys by evidence type?
    mutation_ids = [];
    mutation_ids = gd.data['mutation'].keys()
    parent_ids = [];
    for mid in mutation_ids:
        parents = [];
        parents = gd.data['mutation'][mid]['parent_ids'];
        parent_ids.extend(parents);
    RA_evidence_fields=[]
    MC_evidence_fields=[]
    JC_evidence_fields=[]
    UN_evidence_fields=[]
    for pid in parent_ids:
        evidence = [];
        if gd.data['evidence'][pid]['type'] == 'RA': 
            evidence = gd.data['evidence'][pid].keys()
            RA_evidence_fields.extend(evidence)
        elif gd.data['evidence'][pid]['type'] == 'MC': 
            evidence = gd.data['evidence'][pid].keys()
            MC_evidence_fields.extend(evidence)
        elif gd.data['evidence'][pid]['type'] == 'JC': 
            evidence = gd.data['evidence'][pid].keys()
            JC_evidence_fields.extend(evidence)
        elif gd.data['evidence'][pid]['type'] == 'UN': 
            evidence = gd.data['evidence'][pid].keys()
            UN_evidence_fields.extend(evidence)
    RA_evidence_fields_unique = [];
    RA_evidence_fields_unique = list(set(RA_evidence_fields))
    MC_evidence_fields_unique = [];
    MC_evidence_fields_unique = list(set(MC_evidence_fields))
    JC_evidence_fields_unique = [];
    JC_evidence_fields_unique = list(set(JC_evidence_fields))
    UN_evidence_fields_unique = [];
    UN_evidence_fields_unique = list(set(UN_evidence_fields))

    #RA_evidence_fields_unique
    #['bias_p_value', 'new_base', 'genotype_quality', 'ref_base', 'polymorphism_quality', 'seq_id', 'insert_position', 'log10_qual_likelihood_position_model', 'quality_position_model', 'fisher_strand_p_value', 'ks_quality_p_value', 'frequency', 'ref_cov', 'log10_base_likelihood', 'type', 'position', 'tot_cov', 'quality', 'bias_e_value', 'new_cov', 'log10_strand_likelihood_position_model']
    #MC_evidence_fields_unique
    #['end_range', 'end', 'left_outside_cov', 'seq_id', 'right_inside_cov', 'right_outside_cov', 'start', 'start_range', 'left_inside_cov', 'type']
    #JC_evidence_fields_unique
    #['key', 'side_1_read_count', 'max_min_left', 'side_2_seq_id', 'coverage_minus', 'new_junction_coverage', 'side_2_strand', 'frequency', 'max_min_left_plus', 'side_2_annotate_key', 'alignment_overlap', 'max_left_plus', 'flanking_left', 'continuation_right', 'max_left', 'max_min_right_plus', 'total_non_overlap_reads', 'coverage_plus', 'side_1_strand', 'overlap', 'side_2_overlap', 'neg_log10_pos_hash_p_value', 'max_left_minus', 'side_2_redundant', 'side_2_coverage', 'max_right_minus', 'max_min_left_minus', 'new_junction_read_count', 'max_pos_hash_score', 'new_junction_frequency', 'max_right_plus', 'pos_hash_score', 'continuation_left', 'side_1_overlap', 'max_min_right', 'flanking_right', 'max_right', 'type', 'side_1_seq_id', 'side_2_position', 'side_1_position', 'side_1_coverage', 'side_2_read_count', 'max_min_right_minus', 'side_1_redundant', 'side_1_annotate_key']
    #UN_evidence_fields_unique
    #['seq_id', 'start', 'end']

def find_uniqueEvidenceKeysAndKeyValueTypeByEvidenceType():
    #what are the different evidence keys and key data types by evidence type?
    mutation_ids = [];
    mutation_ids = gd.data['mutation'].keys()
    parent_ids = [];
    for mid in mutation_ids:
        parents = [];
        parents = gd.data['mutation'][mid]['parent_ids'];
        parent_ids.extend(parents);
    RA_evidence_fields=[]
    MC_evidence_fields=[]
    JC_evidence_fields=[]
    UN_evidence_fields=[]
    for pid in parent_ids:
        evidence = [];
        if gd.data['evidence'][pid]['type'] == 'RA':
            for k,v in gd.data['evidence'][pid].iteritems():
                evidence.append((k,type(v)))
            RA_evidence_fields.extend(evidence)
        elif gd.data['evidence'][pid]['type'] == 'MC': 
            for k,v in gd.data['evidence'][pid].iteritems():
                evidence.append((k,type(v)))
            MC_evidence_fields.extend(evidence)
        elif gd.data['evidence'][pid]['type'] == 'JC': 
            for k,v in gd.data['evidence'][pid].iteritems():
                evidence.append((k,type(v)))
            JC_evidence_fields.extend(evidence)
        elif gd.data['evidence'][pid]['type'] == 'UN': 
            for k,v in gd.data['evidence'][pid].iteritems():
                evidence.append((k,type(v)))
            UN_evidence_fields.extend(evidence)
    RA_evidence_fields_unique = [];
    RA_evidence_fields_unique = list(set(RA_evidence_fields))
    MC_evidence_fields_unique = [];
    MC_evidence_fields_unique = list(set(MC_evidence_fields))
    JC_evidence_fields_unique = [];
    JC_evidence_fields_unique = list(set(JC_evidence_fields))
    UN_evidence_fields_unique = [];
    UN_evidence_fields_unique = list(set(UN_evidence_fields))

    #RA_evidence_fields_unique
    #[('position', <type 'int'>), ('log10_base_likelihood', <type 'float'>), ('bias_e_value', <type 'int'>), ('frequency', <type 'int'>), ('frequency', <type 'float'>), ('ref_base', <type 'str'>), ('seq_id', <type 'str'>), ('quality', <type 'float'>), ('genotype_quality', <type 'float'>), ('bias_p_value', <type 'float'>), ('log10_strand_likelihood_position_model', <type 'float'>), ('ks_quality_p_value', <type 'int'>), ('fisher_strand_p_value', <type 'int'>), ('log10_qual_likelihood_position_model', <type 'float'>), ('quality_position_model', <type 'float'>), ('new_cov', <type 'str'>), ('type', <type 'str'>), ('tot_cov', <type 'str'>), ('insert_position', <type 'int'>), ('polymorphism_quality', <type 'float'>), ('new_base', <type 'str'>), ('ref_cov', <type 'str'>), ('fisher_strand_p_value', <type 'float'>), ('ks_quality_p_value', <type 'float'>), ('bias_p_value', <type 'int'>)]
    #MC_evidence_fields_unique
    #[('left_inside_cov', <type 'int'>), ('end', <type 'int'>), ('type', <type 'str'>), ('left_outside_cov', <type 'int'>), ('start_range', <type 'int'>), ('start', <type 'int'>), ('seq_id', <type 'str'>), ('right_inside_cov', <type 'int'>), ('end_range', <type 'int'>), ('right_outside_cov', <type 'int'>)]
    #JC_evidence_fields_unique
    #[('side_1_seq_id', <type 'str'>), ('frequency', <type 'float'>), ('neg_log10_pos_hash_p_value', <type 'str'>), ('side_1_redundant', <type 'int'>), ('coverage_plus', <type 'int'>), ('new_junction_frequency', <type 'float'>), ('side_2_coverage', <type 'str'>), ('max_right', <type 'int'>), ('side_1_overlap', <type 'int'>), ('side_2_read_count', <type 'int'>), ('max_left', <type 'int'>), ('max_left_plus', <type 'int'>), ('side_1_position', <type 'int'>), ('side_2_overlap', <type 'int'>), ('total_non_overlap_reads', <type 'int'>), ('new_junction_read_count', <type 'int'>), ('flanking_right', <type 'int'>), ('side_2_coverage', <type 'float'>), ('max_min_left_minus', <type 'int'>), ('side_2_redundant', <type 'int'>), ('side_2_seq_id', <type 'str'>), ('max_left_minus', <type 'int'>), ('max_right_minus', <type 'int'>), ('pos_hash_score', <type 'int'>), ('type', <type 'str'>), ('side_1_coverage', <type 'float'>), ('alignment_overlap', <type 'int'>), ('max_min_left_plus', <type 'int'>), ('max_min_right_plus', <type 'int'>), ('side_1_coverage', <type 'str'>), ('side_1_read_count', <type 'int'>), ('max_min_right', <type 'int'>), ('max_min_left', <type 'int'>), ('overlap', <type 'int'>), ('continuation_right', <type 'int'>), ('side_2_read_count', <type 'str'>), ('new_junction_coverage', <type 'float'>), ('side_2_strand', <type 'int'>), ('max_pos_hash_score', <type 'int'>), ('max_min_right_minus', <type 'int'>), ('side_2_position', <type 'int'>), ('coverage_minus', <type 'int'>), ('side_1_strand', <type 'int'>), ('max_right_plus', <type 'int'>), ('flanking_left', <type 'int'>), ('side_1_annotate_key', <type 'str'>), ('key', <type 'str'>), ('side_1_read_count', <type 'str'>), ('continuation_left', <type 'int'>), ('side_2_annotate_key', <type 'str'>)]
    #UN_evidence_fields_unique
    #[('seq_id',<type 'str'>), ('start',<type 'int'>), ('end',<type 'int'>)]

def find_uniqueEvidenceKeysAndKeyValueType():
    #what are all unique evidences keys and evidences key data types?
    mutation_ids = [];
    mutation_ids = gd.data['mutation'].keys()
    parent_ids = [];
    for mid in mutation_ids:
        parents = [];
        parents = gd.data['mutation'][mid]['parent_ids'];
        parent_ids.extend(parents);
    RA_evidence_fields=[]
    MC_evidence_fields=[]
    JC_evidence_fields=[]
    UN_evidence_fields=[]
    for pid in parent_ids:
        evidence = [];
        if gd.data['evidence'][pid]['type'] == 'RA':
            for k,v in gd.data['evidence'][pid].iteritems():
                evidence.append((k,type(v)))
            RA_evidence_fields.extend(evidence)
        elif gd.data['evidence'][pid]['type'] == 'MC': 
            for k,v in gd.data['evidence'][pid].iteritems():
                evidence.append((k,type(v)))
            MC_evidence_fields.extend(evidence)
        elif gd.data['evidence'][pid]['type'] == 'JC': 
            for k,v in gd.data['evidence'][pid].iteritems():
                evidence.append((k,type(v)))
            JC_evidence_fields.extend(evidence)
        elif gd.data['evidence'][pid]['type'] == 'UN': 
            for k,v in gd.data['evidence'][pid].iteritems():
                evidence.append((k,type(v)))
            UN_evidence_fields.extend(evidence)
    RA_evidence_fields_unique = [];
    RA_evidence_fields_unique = list(set(RA_evidence_fields))
    MC_evidence_fields_unique = [];
    MC_evidence_fields_unique = list(set(MC_evidence_fields))
    JC_evidence_fields_unique = [];
    JC_evidence_fields_unique = list(set(JC_evidence_fields))
    UN_evidence_fields_unique = [];
    UN_evidence_fields_unique = list(set(UN_evidence_fields))
    evidence_fields = [];
    evidence_fields = []
    evidence_fields = RA_evidence_fields_unique+MC_evidence_fields_unique+JC_evidence_fields_unique+UN_evidence_fields_unique;
    evidence_fields_unique = [];
    evidence_fields_unique = list(set(evidence_fields))

    #evidence_fields_unique
    #[('left_inside_cov', <type 'int'>), ('position', <type 'int'>), ('side_1_seq_id', <type 'str'>), ('log10_base_likelihood', <type 'float'>), ('bias_e_value', <type 'int'>), ('frequency', <type 'int'>), ('start', <type 'int'>), ('frequency', <type 'float'>), ('ref_base', <type 'str'>), ('bias_p_value', <type 'float'>), ('right_inside_cov', <type 'int'>), ('max_right_minus', <type 'int'>), ('seq_id', <type 'str'>), ('new_junction_frequency', <type 'float'>), ('coverage_plus', <type 'int'>), ('quality', <type 'float'>), ('genotype_quality', <type 'float'>), ('side_2_overlap', <type 'int'>), ('log10_qual_likelihood_position_model', <type 'float'>), ('max_right', <type 'int'>), ('side_1_overlap', <type 'int'>), ('log10_strand_likelihood_position_model', <type 'float'>), ('side_2_strand', <type 'int'>), ('max_left', <type 'int'>), ('coverage_minus', <type 'int'>), ('max_left_plus', <type 'int'>), ('ks_quality_p_value', <type 'int'>), ('continuation_right', <type 'int'>), ('fisher_strand_p_value', <type 'int'>), ('right_outside_cov', <type 'int'>), ('max_right_plus', <type 'int'>), ('new_junction_read_count', <type 'int'>), ('flanking_right', <type 'int'>), ('side_2_coverage', <type 'float'>), ('end_range', <type 'int'>), ('quality_position_model', <type 'float'>), ('fisher_strand_p_value', <type 'float'>), ('max_left_minus', <type 'int'>), ('side_1_redundant', <type 'int'>), ('pos_hash_score', <type 'int'>), ('type', <type 'str'>), ('left_outside_cov', <type 'int'>), ('side_2_read_count', <type 'str'>), ('neg_log10_pos_hash_p_value', <type 'str'>), ('alignment_overlap', <type 'int'>), ('max_min_left_plus', <type 'int'>), ('max_min_left_minus', <type 'int'>), ('side_1_strand', <type 'int'>), ('side_1_coverage', <type 'float'>), ('side_1_coverage', <type 'str'>), ('side_1_read_count', <type 'str'>), ('tot_cov', <type 'str'>), ('side_1_read_count', <type 'int'>), ('insert_position', <type 'int'>), ('side_2_read_count', <type 'int'>), ('max_min_left', <type 'int'>), ('overlap', <type 'int'>), ('end', <type 'int'>), ('start_range', <type 'int'>), ('new_junction_coverage', <type 'float'>), ('polymorphism_quality', <type 'float'>), ('max_min_right_plus', <type 'int'>), ('max_pos_hash_score', <type 'int'>), ('max_min_right_minus', <type 'int'>), ('new_base', <type 'str'>), ('ref_cov', <type 'str'>), ('total_non_overlap_reads', <type 'int'>), ('side_2_coverage', <type 'str'>), ('side_2_position', <type 'int'>), ('side_2_redundant', <type 'int'>), ('continuation_left', <type 'int'>), ('new_cov', <type 'str'>), ('side_1_position', <type 'int'>), ('flanking_left', <type 'int'>), ('ks_quality_p_value', <type 'float'>), ('side_2_seq_id', <type 'str'>), ('key', <type 'str'>), ('bias_p_value', <type 'int'>), ('side_1_annotate_key', <type 'str'>), ('max_min_right', <type 'int'>), ('side_2_annotate_key', <type 'str'>)]

def find_uniqueMutationKeysAndKeyValueTypeByMutationType():
    #what are the different mutation keys and key data types by mutation type?
    mutation_ids = [];
    mutation_ids = gd.data['mutation'].keys()
    SNP_mutation_fields=[]
    SUB_mutation_fields=[]
    DEL_mutation_fields=[]
    INS_mutation_fields=[]
    MOB_mutation_fields=[]
    AMP_mutation_fields=[]
    CON_mutation_fields=[]
    INV_mutation_fields=[]
    for mid in mutation_ids:
        mutation = [];
        if gd.data['mutation'][mid]['type'] == 'SNP':
            for k,v in gd.data['mutation'][mid].iteritems():
                mutation.append((k,type(v)))
            SNP_mutation_fields.extend(mutation)
        elif gd.data['mutation'][mid]['type'] == 'SUB': 
            for k,v in gd.data['mutation'][pid].iteritems():
                mutation.append((k,type(v)))
            SUB_mutation_fields.extend(mutation)
        elif gd.data['mutation'][mid]['type'] == 'DEL': 
            for k,v in gd.data['mutation'][mid].iteritems():
                mutation.append((k,type(v)))
            DEL_mutation_fields.extend(mutation)
        elif gd.data['mutation'][mid]['type'] == 'INS': 
            for k,v in gd.data['mutation'][mid].iteritems():
                mutation.append((k,type(v)))
            INS_mutation_fields.extend(mutation)
        elif gd.data['mutation'][mid]['type'] == 'MOB': 
            for k,v in gd.data['mutation'][mid].iteritems():
                mutation.append((k,type(v)))
            MOB_mutation_fields.extend(mutation)
        elif gd.data['mutation'][mid]['type'] == 'AMP': 
            for k,v in gd.data['mutation'][mid].iteritems():
                mutation.append((k,type(v)))
            AMP_mutation_fields.extend(mutation)
        elif gd.data['mutation'][mid]['type'] == 'INV': 
            for k,v in gd.data['mutation'][mid].iteritems():
                mutation.append((k,type(v)))
            INV_mutation_fields.extend(mutation)
    SNP_mutation_fields_unique = [];
    SNP_mutation_fields_unique = list(set(SNP_mutation_fields))
    SUB_mutation_fields_unique = [];
    SUB_mutation_fields_unique = list(set(SUB_mutation_fields))
    DEL_mutation_fields_unique = [];
    DEL_mutation_fields_unique = list(set(DEL_mutation_fields))
    INS_mutation_fields_unique = [];
    INS_mutation_fields_unique = list(set(INS_mutation_fields))
    MOB_mutation_fields_unique = [];
    MOB_mutation_fields_unique = list(set(MOB_mutation_fields))
    AMP_mutation_fields_unique = [];
    AMP_mutation_fields_unique = list(set(AMP_mutation_fields))
    CON_mutation_fields_unique = [];
    CON_mutation_fields_unique = list(set(CON_mutation_fields))
    INV_mutation_fields_unique = [];
    INV_mutation_fields_unique = list(set(INV_mutation_fields))

    return SNP_mutation_fields_unique,SUB_mutation_fields_unique,DEL_mutation_fields_unique,\
        INS_mutation_fields_unique,MOB_mutation_fields_unique,AMP_mutation_fields_unique,\
        CON_mutation_fields_unique,INV_mutation_fields_unique