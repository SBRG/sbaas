from analysis import *

def data_stage00():
    
    '''acqusition method import'''
    method_io = stage00_io();

def data_stage01():
    
    execute01 = stage01_ale_execute();
    execute01.initialize_dataStage01();

    '''exeriment data imports'''
    data_io = stage01_ale_io();
    data_io.import_dataStage01AleTrajectories_matlab('ALEsKOs01',
          'data/tests/analysis_ale/ALEsKOs_trajectories.mat');

    '''data analysis'''
    #execute01.execute_findJumps('ALEsKOs01');

    '''experiment data exports'''
    
    data_io.export_dataStage01AleTrajectories_d3('ALEsKOs01',
                        sample_name_abbreviations_I=['OxicEvo04tpiAEvo01EcoliGlc',
                                                'OxicEvo04tpiAEvo02EcoliGlc',
                                                'OxicEvo04tpiAEvo03EcoliGlc',
                                                'OxicEvo04tpiAEvo04EcoliGlc'],
                        fit_func_I='lowess',
                        json_var_name='data',
                        filename='visualization/data/ALEsKOs01/ale/scatterlineplot/tpiA.js');

def run_all_tests():
    print('testing data_stage00_ale...')
    data_stage00();
    print('testing data_stage01_ale...')
    data_stage01();
    