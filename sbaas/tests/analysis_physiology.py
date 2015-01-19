from analysis import *

def data_stage00():
    
    '''acqusition method import'''
    execute00 = stage00_execute();
    execute00.execute_makeExperimentFromSampleFile('data/tests/analysis_physiology/140905_Physiology_ALEsKOs01_sampleFile01.csv',0,[]);
    execute00.execute_makeExperimentFromSampleFile('data/tests/analysis_physiology/140905_Quantification_ALEsKOs01_biomass01.csv',0,[]);

def data_stage01():

    execute01 = stage01_physiology_execute();
    execute01.initialize_dataStage01();

    '''data import'''
    io = stage01_physiology_io();
    io.import_dataStage01PhysiologyData_add('data/tests/analysis_physiology/140905_Physiology_ALEsKOs01_samples01.csv');
    io.import_dataStage01PhysiologyData_update('data/tests/analysis_physiology/140905_Physiology_ALEsKOs01_update01.csv');
    io.import_dataStage01PhysiologyData_add('data/tests/analysis_physiology/140905_Quantification_ALEsKOs01_biomass01.csv');

    '''data analysis'''
    #functions to return sample names
    #physiology samples to calculate the growth rates
    def sample_names_short_calculateGrowthRates_QPR():
        return [
                'OxicEvo04tpiAEcoliGlc_Broth-1',
                'OxicEvo04tpiAEcoliGlc_Broth-2',
                'OxicEvo04tpiAEcoliGlc_Broth-3',
                'OxicEvo04tpiAEvo01EPEcoliGlc_Broth-1',
                'OxicEvo04tpiAEvo01EPEcoliGlc_Broth-2',
                'OxicEvo04tpiAEvo01EPEcoliGlc_Broth-3',
                'OxicEvo04tpiAEvo02EPEcoliGlc_Broth-1',
                'OxicEvo04tpiAEvo02EPEcoliGlc_Broth-2',
                'OxicEvo04tpiAEvo02EPEcoliGlc_Broth-3',
                'OxicEvo04tpiAEvo03EPEcoliGlc_Broth-1',
                'OxicEvo04tpiAEvo03EPEcoliGlc_Broth-2',
                'OxicEvo04tpiAEvo03EPEcoliGlc_Broth-3',
                'OxicEvo04tpiAEvo04EPEcoliGlc_Broth-1',
                'OxicEvo04tpiAEvo04EPEcoliGlc_Broth-2',
                'OxicEvo04tpiAEvo04EPEcoliGlc_Broth-3'
                ];
    def sample_names_abbreviation_calculateRatesAverages_QPR():
        return [
                'OxicEvo04tpiAEcoliGlc',
                'OxicEvo04tpiAEvo01EPEcoliGlc',
                'OxicEvo04tpiAEvo02EPEcoliGlc',
                'OxicEvo04tpiAEvo02EPEcoliGlc',
                'OxicEvo04tpiAEvo04EPEcoliGlc'];
    #physiology samples used to calculate the uptake and secretion rates
    def sample_names_interpolateBiomassFromReplicates_P():
        return [
            '140721_1_OxicEvo04tpiAEcoliGlcM9_Broth-1',
            '140721_2_OxicEvo04tpiAEcoliGlcM9_Broth-1',
            '140721_3_OxicEvo04tpiAEcoliGlcM9_Broth-1',
            '140721_4_OxicEvo04tpiAEcoliGlcM9_Broth-1',
            '140721_5_OxicEvo04tpiAEcoliGlcM9_Broth-1',
            '140721_1_OxicEvo04tpiAEcoliGlcM9_Broth-2',
            '140721_2_OxicEvo04tpiAEcoliGlcM9_Broth-2',
            '140721_3_OxicEvo04tpiAEcoliGlcM9_Broth-2',
            '140721_4_OxicEvo04tpiAEcoliGlcM9_Broth-2',
            '140721_5_OxicEvo04tpiAEcoliGlcM9_Broth-2',
            '140721_1_OxicEvo04tpiAEcoliGlcM9_Broth-3',
            '140721_2_OxicEvo04tpiAEcoliGlcM9_Broth-3',
            '140721_3_OxicEvo04tpiAEcoliGlcM9_Broth-3',
            '140721_4_OxicEvo04tpiAEcoliGlcM9_Broth-3',
            '140721_5_OxicEvo04tpiAEcoliGlcM9_Broth-3',
            '140807_1_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1',
            '140807_2_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1',
            '140807_3_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1',
            '140807_4_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1',
            '140807_5_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1',
            '140807_6_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1',
            '140807_1_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-2',
            '140807_2_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-2',
            '140807_3_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-2',
            '140807_4_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-2',
            '140807_5_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-2',
            '140807_6_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-2',
            '140807_1_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-3',
            '140807_2_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-3',
            '140807_3_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-3',
            '140807_4_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-3',
            '140807_5_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-3',
            '140807_6_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-3',
            '140807_1_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1',
            '140807_2_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1',
            '140807_3_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1',
            '140807_4_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1',
            '140807_5_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1',
            '140807_6_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1',
            '140807_1_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-2',
            '140807_2_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-2',
            '140807_3_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-2',
            '140807_4_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-2',
            '140807_5_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-2',
            '140807_6_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-2',
            '140807_1_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-3',
            '140807_2_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-3',
            '140807_3_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-3',
            '140807_4_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-3',
            '140807_5_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-3',
            '140807_6_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-3',
            '140811_1_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1',
            '140811_2_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1',
            '140811_3_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1',
            '140811_4_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1',
            '140811_5_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1',
            '140811_6_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1',
            '140811_1_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-2',
            '140811_2_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-2',
            '140811_3_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-2',
            '140811_4_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-2',
            '140811_5_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-2',
            '140811_6_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-2',
            '140811_1_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-3',
            '140811_2_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-3',
            '140811_3_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-3',
            '140811_4_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-3',
            '140811_5_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-3',
            '140811_6_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-3',
            '140811_1_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1',
            '140811_2_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1',
            '140811_3_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1',
            '140811_4_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1',
            '140811_5_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1',
            '140811_6_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1',
            '140811_1_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-2',
            '140811_2_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-2',
            '140811_3_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-2',
            '140811_4_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-2',
            '140811_5_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-2',
            '140811_6_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-2',
            '140811_1_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-3',
            '140811_2_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-3',
            '140811_3_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-3',
            '140811_4_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-3',
            '140811_5_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-3',
            '140811_6_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-3'];
    def sample_names_updatePhysiologicalParametersFromOD600_P():
        return [
            '140721_1_OxicEvo04tpiAEcoliGlcM9_Broth-1',
            '140721_2_OxicEvo04tpiAEcoliGlcM9_Broth-1',
            '140721_3_OxicEvo04tpiAEcoliGlcM9_Broth-1',
            '140721_4_OxicEvo04tpiAEcoliGlcM9_Broth-1',
            '140721_5_OxicEvo04tpiAEcoliGlcM9_Broth-1',
            '140721_1_OxicEvo04tpiAEcoliGlcM9_Broth-2',
            '140721_2_OxicEvo04tpiAEcoliGlcM9_Broth-2',
            '140721_3_OxicEvo04tpiAEcoliGlcM9_Broth-2',
            '140721_4_OxicEvo04tpiAEcoliGlcM9_Broth-2',
            '140721_5_OxicEvo04tpiAEcoliGlcM9_Broth-2',
            '140721_1_OxicEvo04tpiAEcoliGlcM9_Broth-3',
            '140721_2_OxicEvo04tpiAEcoliGlcM9_Broth-3',
            '140721_3_OxicEvo04tpiAEcoliGlcM9_Broth-3',
            '140721_4_OxicEvo04tpiAEcoliGlcM9_Broth-3',
            '140721_5_OxicEvo04tpiAEcoliGlcM9_Broth-3',
            '140807_1_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1',
            '140807_2_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1',
            '140807_3_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1',
            '140807_4_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1',
            '140807_5_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1',
            '140807_6_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-1',
            '140807_1_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-2',
            '140807_2_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-2',
            '140807_3_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-2',
            '140807_4_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-2',
            '140807_5_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-2',
            '140807_6_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-2',
            '140807_1_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-3',
            '140807_2_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-3',
            '140807_3_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-3',
            '140807_4_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-3',
            '140807_5_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-3',
            '140807_6_OxicEvo04tpiAEvo01EPEcoliGlcM9_Broth-3',
            '140807_1_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1',
            '140807_2_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1',
            '140807_3_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1',
            '140807_4_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1',
            '140807_5_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1',
            '140807_6_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-1',
            '140807_1_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-2',
            '140807_2_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-2',
            '140807_3_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-2',
            '140807_4_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-2',
            '140807_5_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-2',
            '140807_6_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-2',
            '140807_1_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-3',
            '140807_2_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-3',
            '140807_3_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-3',
            '140807_4_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-3',
            '140807_5_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-3',
            '140807_6_OxicEvo04tpiAEvo02EPEcoliGlcM9_Broth-3',
            '140811_1_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1',
            '140811_2_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1',
            '140811_3_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1',
            '140811_4_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1',
            '140811_5_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1',
            '140811_6_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-1',
            '140811_1_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-2',
            '140811_2_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-2',
            '140811_3_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-2',
            '140811_4_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-2',
            '140811_5_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-2',
            '140811_6_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-2',
            '140811_1_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-3',
            '140811_2_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-3',
            '140811_3_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-3',
            '140811_4_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-3',
            '140811_5_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-3',
            '140811_6_OxicEvo04tpiAEvo03EPEcoliGlcM9_Broth-3',
            '140811_1_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1',
            '140811_2_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1',
            '140811_3_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1',
            '140811_4_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1',
            '140811_5_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1',
            '140811_6_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-1',
            '140811_1_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-2',
            '140811_2_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-2',
            '140811_3_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-2',
            '140811_4_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-2',
            '140811_5_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-2',
            '140811_6_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-2',
            '140811_1_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-3',
            '140811_2_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-3',
            '140811_3_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-3',
            '140811_4_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-3',
            '140811_5_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-3',
            '140811_6_OxicEvo04tpiAEvo04EPEcoliGlcM9_Broth-3'];
    def sample_names_short_calculateUptakeAndSecretionRates_P():
        return [
                "OxicEvo04tpiAEcoliGlc_Broth-1",
                "OxicEvo04tpiAEcoliGlc_Broth-2",
                "OxicEvo04tpiAEcoliGlc_Broth-3",
                "OxicEvo04tpiAEvo01EPEcoliGlc_Broth-1",
                "OxicEvo04tpiAEvo01EPEcoliGlc_Broth-2",
                "OxicEvo04tpiAEvo01EPEcoliGlc_Broth-3",
                "OxicEvo04tpiAEvo02EPEcoliGlc_Broth-1",
                "OxicEvo04tpiAEvo02EPEcoliGlc_Broth-2",
                "OxicEvo04tpiAEvo02EPEcoliGlc_Broth-3",
                "OxicEvo04tpiAEvo02EPEcoliGlc_Broth-1",
                "OxicEvo04tpiAEvo02EPEcoliGlc_Broth-2",
                "OxicEvo04tpiAEvo02EPEcoliGlc_Broth-3",
                "OxicEvo04tpiAEvo04EPEcoliGlc_Broth-1",
                "OxicEvo04tpiAEvo04EPEcoliGlc_Broth-2",
                "OxicEvo04tpiAEvo04EPEcoliGlc_Broth-3"];
    def sample_names_abbreviation_exportRatesAverages_P():
        return [
                'OxicEvo04tpiAEcoliGlc',
                'OxicEvo04tpiAEvo01EPEcoliGlc',
                'OxicEvo04tpiAEvo02EPEcoliGlc',
                'OxicEvo04tpiAEvo02EPEcoliGlc',
                'OxicEvo04tpiAEvo04EPEcoliGlc'];
    
    #Physiology starting and endpoint growth rates
    execute01.execute_calculateGrowthRates('ALEsKOs01',sample_names_short_calculateGrowthRates_QPR());
    execute01.execute_interpolateBiomassFromReplicates('ALEsKOs01',sample_names_interpolateBiomassFromReplicates_P());
    execute01.execute_updatePhysiologicalParametersFromOD600('ALEsKOs01',sample_names_updatePhysiologicalParametersFromOD600_P());
    execute01.execute_calculateUptakeAndSecretionRates('ALEsKOs01',sample_names_short_calculateUptakeAndSecretionRates_P());
    execute01.execute_calculateRatesAverages('ALEsKOs01',sample_names_abbreviation_calculateRatesAverages_QPR());

    '''data export'''
    io.export_dataStage01PhysiologyRatesAverages_d3('ALEsKOs01',
                                                    sample_name_abbreviations_I=['OxicEvo04tpiAEcoliGlc',
                                                    'OxicEvo04tpiAEvo01EPEcoliGlc',
                                                    'OxicEvo04tpiAEvo02EPEcoliGlc',
                                                    'OxicEvo04tpiAEvo02EPEcoliGlc',
                                                    'OxicEvo04tpiAEvo04EPEcoliGlc'],
                                                    #met_ids_exclude_I=['glc-D'],
                                                    json_var_name='data',
                                                 #filename='visualization/data/ALEsKOs01/physiology/barchart/tpiA.csv');
                                                 filename='visualization/data/ALEsKOs01/physiology/barchart/tpiA.js');

def data_stage02():
    ex02 = stage02_physiology_execute();
    ex02.initialize_dataStage02();

    '''data import'''
    qio02 = stage02_physiology_io();
    qio02.import_dataStage02PhysiologySimulation_add('data/tests/analysis_physiology/141020_data_stage02_physiology_simulation.csv');
    qio02.import_dataStage02PhysiologyModel_sbml('iJO1366','10/11/2011 0:00','data/models/iJO1366.xml')

    ex02.load_models('ALEsKOs01');
    ex02.execute_makeMeasuredFluxes('ALEsKOs01',
                                {'glc-D':{'model_id':'iJO1366','rxn_id':'EX_glc_LPAREN_e_RPAREN_'},
                                'ac':{'model_id':'iJO1366','rxn_id':'EX_ac_LPAREN_e_RPAREN_'},
                                'succ':{'model_id':'iJO1366','rxn_id':'EX_succ_LPAREN_e_RPAREN_'},
                                'lac-L':{'model_id':'iJO1366','rxn_id':'EX_lac_DASH_L_LPAREN_e_RPAREN_'},
                                'biomass':{'model_id':'iJO1366','rxn_id':'Ec_biomass_iJO1366_WT_53p95M'}});
    ex02.execute_addMeasuredFluxes('ALEsKOs01',ko_list={'iJO1366':{
                                                    'OxicEvo04tpiAEcoliGlc':['TPI'],
                                                    'OxicEvo04tpiAEvo01EPEcoliGlc':['TPI'],
                                                    'OxicEvo04tpiAEvo02EPEcoliGlc':['TPI'],
                                                    'OxicEvo04tpiAEvo03EPEcoliGlc':['TPI'],
                                                    'OxicEvo04tpiAEvo04EPEcoliGlc':['TPI']
                                                    }});
    ex02.execute_sampling('ALEsKOs01');
    ex02.execute_analyzeSamplingPoints('ALEsKOs01');

    '''data export'''
    qio02.export_samplingAnalysis_escher('ALEsKOs01',
                                         model_ids_dict_I=ex02.models);
    
def run_all_tests():
    print 'testing data_stage00_physiology...'
    data_stage00();
    print 'testing data_stage01_physiology...'
    data_stage01();
    #print 'testing data_stage02_physiology...'
    #data_stage02();