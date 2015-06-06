from analysis.analysis_base import *

class visualization_query(base_analysis):
    # query data from visualization_project
    def get_project_projectID_visualizationProject(self,project_id_I):
        '''Query rows that are used from the project'''
        try:
            data = self.session.query(visualization_project).filter(
                    visualization_project.project_id.like(project_id_I),
                    visualization_project.used_.is_(True)).order_by(
                    visualization_project.pipeline_id.asc(),
                    visualization_project.data_export_id.asc()).all();
            project_id_O = []
            pipeline_id_O = []
            analysis_id_O = []
            data_export_id_O = []
            container_export_id_O = []
            project_O = {};
            if data: 
                for d in data:
                    project_id_O.append(d.project_id);
                    pipeline_id_O.append(d.pipeline_id);
                    analysis_id_O.append(d.analysis_id);
                    data_export_id_O.append(d.data_export_id);
                    container_export_id_O.append(d.container_export_id);
                project_id_O = list(set(project_id_O))
                pipeline_id_O = list(set(pipeline_id_O))
                analysis_id_O = list(set(analysis_id_O))
                data_export_id_O = list(set(data_export_id_O))
                container_export_id_O = list(set(container_export_id_O))
                project_O={
                        'project_id':project_id_O,
                        'pipeline_id':pipeline_id_O,
                        'analysis_id':analysis_id_O,
                        'data_export_id':data_export_id_O,
                        'container_export_id':container_export_id_O};
                
            return project_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_projectID_visualizationProject(self,project_id_I):
        '''Query rows that are used from the project'''
        try:
            data = self.session.query(visualization_project).filter(
                    visualization_project.project_id.like(project_id_I),
                    visualization_project.used_.is_(True)).order_by(
                    visualization_project.data_export_id.asc(),
                    visualization_project.analysis_id.asc(),
                    visualization_project.container_export_id.asc()).all();
            data_O = [];
            if data: 
                for d in data:
                    data_O.append({'project_id':d.project_id,
                        'pipeline_id':d.pipeline_id,
                        'analysis_id':d.analysis_id,
                        'data_export_id':d.data_export_id,
                        'container_export_id':d.container_export_id
                    });
            return  data_O;
        except SQLAlchemyError as e:
            print(e);

    # query data from visualization_project_description
    def get_rows_projectID_visualizationProjectDescription(self,project_id_I):
        '''Query rows that are used from the project'''
        try:
            data = self.session.query(visualization_project_description).filter(
                    visualization_project_description.project_id.like(project_id_I),
                    visualization_project_description.used_.is_(True)).order_by(
                    visualization_project_description.project_tileorder.asc()).all();
            data_O = [];
            if data: 
                for d in data:
                    data_O.append({'project_id':d.project_id,
                    'project_section':d.project_section,
                    'project_heading':d.project_heading,
                    'project_paragraph':d.project_paragraph,
                    'project_media':d.project_media,
                    'project_href':d.project_href,
                    'project_tileorder':d.project_tileorder,
                    'used_':d.used_,
                    'comment_':d.comment_
                    });
            return  data_O;
        except SQLAlchemyError as e:
            print(e);