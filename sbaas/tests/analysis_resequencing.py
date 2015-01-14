from analysis import *

def strain_lineages():
    strain_lineages_O = {"evo04tpiAevo01":{0:"140401_0_OxicEvo04tpiAEcoliGlcM9_Broth-1",1:"140702_1_OxicEvo04tpiAEvo01J01EcoliGlcM9_Broth-1",2:"140702_3_OxicEvo04tpiAEvo01J03EcoliGlcM9_Broth-1",3:"140807_11_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1"},
                        "evo04tpiAevo02":{0:"140401_0_OxicEvo04tpiAEcoliGlcM9_Broth-1",1:"140702_1_OxicEvo04tpiAEvo02J01EcoliGlcM9_Broth-1",2:"140702_3_OxicEvo04tpiAEvo02J03EcoliGlcM9_Broth-1",3:"140807_11_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1"},
                        "evo04tpiAevo03":{0:"140401_0_OxicEvo04tpiAEcoliGlcM9_Broth-1",1:"140702_1_OxicEvo04tpiAEvo03J01EcoliGlcM9_Broth-1",2:"140702_3_OxicEvo04tpiAEvo03J03EcoliGlcM9_Broth-1",3:"140807_11_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1"},
                        "evo04tpiAevo04":{0:"140401_0_OxicEvo04tpiAEcoliGlcM9_Broth-1",1:"140702_1_OxicEvo04tpiAEvo04J01EcoliGlcM9_Broth-1",2:"140702_3_OxicEvo04tpiAEvo04J03EcoliGlcM9_Broth-1",3:"140807_11_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1"},
                        };
    return strain_lineages_O;
def initial_final_pairs():
    initial_final_O = [
                    "140401_0_OxicEvo04tpiAEcoliGlcM9_Broth-1","140807_11_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1",
                    "140401_0_OxicEvo04tpiAEcoliGlcM9_Broth-1","140807_11_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1",
                    "140401_0_OxicEvo04tpiAEcoliGlcM9_Broth-1","140807_11_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1",
                    "140401_0_OxicEvo04tpiAEcoliGlcM9_Broth-1","140807_11_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1"];
    return initial_final_O;
def initial_final():
    initial_final_O = [
                    "140401_0_OxicEvo04tpiAEcoliGlcM9_Broth-1","140807_11_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1",
                    "140807_11_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1",
                    "140807_11_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1",
                    "140807_11_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1"];
    return initial_final_O;
def reduce_groupNames():
    reduce_group_names_O = {"evo04tpiAevoEP":["140807_11_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1",
                                        "140807_11_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1",
                                        "140807_11_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1",
                                        "140807_11_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1"]};
    return reduce_group_names_O;

def data_stage00():
    
    '''data import'''
    execute00 = stage00_execute();
    execute00.execute_makeExperimentFromSampleFile('data\\tests\\analysis_resequencing\\140823_Resequencing_ALEsKOs01_sampleFile01.csv',0,[]);

def data_stage01():

    execute01 = stage01_resequencing_execute();
    #execute01.drop_dataStage01();
    execute01.initialize_dataStage01();

    '''data import'''
    io = stage01_resequencing_io();
    # import resequencing data from breseq
    iobase = base_importData();
    iobase.read_csv('data\\tests\\analysis_resequencing\\140823_Resequencing_ALEsKOs01_fileList01.csv');
    fileList = iobase.data;
    # read in each data file
    for file in fileList:
        print 'importing resequencing data for sample ' + file['sample_name']
        io.import_resequencingData_add(file['filename'],file['experiment_id'],file['sample_name']);
    iobase.clear_data();

    '''data analysis'''
    execute01.reset_dataStage01_filtered('ALEsKOs01');
    execute01.execute_filterMutations_population('ALEsKOs01');
    execute01.reset_dataStage01_lineage('ALEsKOs01')
    execute01.execute_analyzeLineage_population('ALEsKOs01',
                                         strain_lineages());
    execute01.execute_annotateMutations_lineage('ALEsKOs01');
    execute01.reset_dataStage01_endpoints('ALEsKOs01')
    execute01.execute_analyzeEndpointReplicates_population('ALEsKOs01',
                                         {"evo04tpiA":["140807_11_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1","140807_11_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1",
                                                     "140807_11_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1","140807_11_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1"],
                                        });
    execute01.execute_annotateMutations_endpoints('ALEsKOs01');
    execute01.execute_annotateFilteredMutations('ALEsKOs01');

    '''data export'''
    mutation_id_base = ['MOB_insA-/-uspC_1977510',
                        'SNP_ylbE_547694',
                        'SNP_yifN_3957957',
                        'DEL_corA_3999668',
                        'MOB_tdk_1292255',
                        'SNP_rpoB_4182566',
                        'INS__4294403',
                        'DEL_pyrE-/-rph_3813882',
                        'SNP_wcaA_2130811']
    io.export_dataStage01ResequencingLineage_d3('ALEsKOs01',
                                                ['evo04tpiAevo01','evo04tpiAevo02','evo04tpiAevo03','evo04tpiAevo04'],
                                                filename='visualization\\data\\ALEsKOs01\\resequencing\\heatmap\\tpiA.js',
                                                mutation_id_exclusion_list = mutation_id_base);

    io.export_dataStage01ResequencingMutationsAnnotated_d3('ALEsKOs01',
                                         strain_lineages(),
                                                mutation_id_exclusion_list = ['insA-/-uspC_MOB_1977510',
                        'ylbE_SNP_547694',
                        'yifN_SNP_3957957',
                        'corA_DEL_3999668',
                        'tdk_MOB_1292255',
                        'rpoB_SNP_4182566',
                        '_INS_4294403',
                        'pyrE-/-rph_DEL_3813882',
                        'wcaA_SNP_2130811']);

def data_stage02():
    '''Note: Requires analysis_physiology'''

    ex02 = stage02_resequencing_execute();
    #ex02.drop_dataStage02();
    ex02.initialize_dataStage02();

    '''data import'''
    io02 = stage02_resequencing_io();

    '''data analysis'''
    ex02.reset_dataStage02('ALEsKOs01');
    ex02.execute_mapResequencingPhysiology_population('ALEsKOs01',sample_names_I=initial_final())
    ex02.reset_dataStage02_reduceResequencingPhysiology('ALEsKOs01')
    ex02.execute_reduceResequencingPhysiology_population('ALEsKOs01',reduce_groupNames())

    io02.export_dataStage02ResequencingLineage_d3('ALEsKOs01');

def run_all_tests():
    print 'testing data_stage00_resequencing...'
    data_stage00();
    print 'testing data_stage01_resequencing...'
    data_stage01();
    print 'testing data_stage02_resequencing...'
    data_stage02();