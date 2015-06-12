from analysis.analysis_base import *
from .stage01_ale_query import *
from .stage01_ale_io import *

class stage01_ale_execute():
    '''class for ale analysis'''
    def __init__(self, session_I=None):
        if session_I: self.session = session_I;
        else: self.session = Session();
        self.stage01_ale_query = stage01_ale_query(self.session);
        self.calculate = base_calculate();

    #analyses:
    def execute_findJumps(self,experiment_id_I,sample_name_abbreviations_I=[],fit_func_I='lowess'):
        '''Find jumps in ALE after smoothing trajectories
        TODO: make jump_finder algorithm'''

        #query sample_name abbreviations
        if sample_name_abbreviations_I:
            sample_name_abbreviations = sample_name_abbreviations_I;
        else:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.stage01_ale_query.get_sampleNameAbbreviations_experimentID_dataStage01AleTrajectories(experiment_id_I);
        for sna in sample_name_abbreviations:
            #query growth rates and times
            growth_rates = [];
            growth_rates = self.stage01_ale_query.get_rows_experimentIDAndSampleNameAbbreviation_dataStage01AleTrajectories(experiment_id_I,sna)
            #smooth growth rates
            x,y=[],[];
            for k in growth_rates:
                x.append(k['ale_time'])
                y.append(k['rate'])
            x_fit,y_fit=[],[];
            x_fit,y_fit=self.calculate.fit_trajectories(x,y,fit_func_I);
            #identify jumps
            jump_start,jump_stop=[],[];
            #jump_start,jump_stop=self.find_jumps(x_fit,y_fit);
            for i,start in enumerate(jump_starts):
                #add rows to the data base
                row = [];
                row = data_stage01_ale_jumps(experiment_id_I, sna,
                        #TODO: jump_start[i],jump_stop[i],
                        True, None);
                self.session.add(row);
        self.session.commit();
    #internal:
    def find_jumps(self,x_fit_I,y_fit_I):
        '''Determine jumps based on changes in the growth trajectory
        TODO:'''
        return;
    #table initializations:
    def drop_dataStage01(self):
        try:
            data_stage01_ale_trajectories.__table__.drop(engine,True);
            data_stage01_ale_jumps.__table__.drop(engine,True);
            data_stage01_ale_analysis.__table__.drop(engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage01(self,experiment_id_I = None):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage01_ale_trajectories).filter(data_stage01_ale_trajectories.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_ale_jumps).filter(data_stage01_ale_jumps.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage01_ale_trajectories).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_ale_jumps).delete(synchronize_session=False);
                reset = self.session.query(data_stage01_ale_analysis).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_dataStage01(self):
        try:
            data_stage01_ale_trajectories.__table__.create(engine,True);
            data_stage01_ale_jumps.__table__.create(engine,True);
            data_stage01_ale_analysis.__table__.create(engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage01Analysis(self,analysis_id_I=None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage01_ale_analysis).filter(data_stage01_ale_analysis.analysis_id.like(analysis_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage01_ale_analysis).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
