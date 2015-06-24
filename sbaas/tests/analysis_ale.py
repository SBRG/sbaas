from sbaas.analysis.analysis_stage00 import stage00_io
from sbaas.analysis.analysis_stage01_ale import stage01_ale_execute, stage01_ale_io
from sbaas.analysis.analysis_base.base_importData import base_importData
from sbaas.models import *

def data_stage00(session):
    
    '''acqusition method import'''
    method_io = stage00_io(session);

def data_stage01(session):
    
    execute01 = stage01_ale_execute(session);
    execute01.initialize_dataStage01();

    '''exeriment data imports'''
    data_io = stage01_ale_io(session);
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
    session = Session();
    print('testing data_stage00_ale...')
    data_stage00(session);
    print('testing data_stage01_ale...')
    data_stage01(session);
    