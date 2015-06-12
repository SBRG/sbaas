from analysis.analysis_base import *
from visualization_query import *
from visualization_io import *

class visualization_execute():
    '''class for ale analysis'''
    def __init__(self, session_I=None):
        if session_I: self.session = session_I;
        else: self.session = Session();
        self.visualization_query = visualization_query(self.session);

    #analyses:
    def execute_getVisualizationProjects(self):
        '''queries of _analysis tables'''
        #TODO:
        query_cmd = """SELECT analysis_id
              FROM data_stage01_ale_analysis
              GROUP BY analysis_id
              ORDER BY analysis_id ASC;

            SELECT analysis_id
              FROM data_stage01_resequencing_analysis
              GROUP BY analysis_id
              ORDER BY analysis_id ASC;

            SELECT analysis_id
              FROM data_stage02_resequencing_analysis
              GROUP BY analysis_id
              ORDER BY analysis_id ASC;

            SELECT analysis_id
              FROM data_stage01_physiology_analysis
              GROUP BY analysis_id
              ORDER BY analysis_id ASC;"""
    #table initializations:
    def drop_visualization(self):
        try:
            visualization_project.__table__.drop(engine,True);
            visualization_project_description.__table__.drop(engine,True);
            #visualization_project_status.__table__.drop(engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_visualization(self,project_id_I = None):
        try:
            if project_id_I:
                reset = self.session.query(visualization_project).filter(visualization_project.project_id.like(project_id_I)).delete(synchronize_session=False);
                reset = self.session.query(visualization_project_description).filter(visualization_project_description.project_id.like(project_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(visualization_project).delete(synchronize_session=False);
                reset = self.session.query(visualization_project_description).delete(synchronize_session=False);
                #reset = self.session.query(visualization_project_status).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_visualization(self):
        try:
            visualization_project.__table__.create(engine,True);
            visualization_project_description.__table__.create(engine,True);
            #visualization_project_status.__table__.create(engine,True);
        except SQLAlchemyError as e:
            print(e);
