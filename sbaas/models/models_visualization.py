# ORMs
from .models_base import *
from sqlalchemy.orm import relationship

# ORM classes
class visualization_project(Base):
    __tablename__ = 'visualization_project'
    id = Column(Integer, Sequence('visualization_project_id_seq'), primary_key=True)
    project_id = Column(String(100))
    pipeline_id = Column(String(100))
    analysis_id = Column(String(500))
    data_export_id = Column(String(100))
    container_export_id = Column(String(100))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('project_id','analysis_id','data_export_id','container_export_id','pipeline_id'),
            )

    def __init__(self, project_id_I, pipeline_id_I, analysis_id_I, data_export_id_I,container_export_id_I,used_I,comment_I):
        self.project_id = project_id_I;
        self.pipeline_id = pipeline_id_I;
        self.analysis_id = analysis_id_I;
        self.data_export_id = data_export_id_I;
        self.container_export_id = container_export_id_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
            'project_id':self.project_id,
            'pipeline_id':self.pipeline_id,
                'analysis_id':self.analysis_id,
                'data_export_id':self.data_export_id,
                'container_export_id':self.container_export_id,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class visualization_project_description(Base):
    __tablename__ = 'visualization_project_description'
    id = Column(Integer, Sequence('visualization_project_description_id_seq'), primary_key=True)
    project_id = Column(String(100))
    project_section = Column(String(250));
    project_heading = Column(String(250));
    project_paragraph = Column(Text);
    project_media = Column(Text);
    project_href = Column(Text);
    project_tileorder = Column(Text);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('project_id','project_section','project_heading','project_tileorder'),
            )

    def __init__(self, project_id_I, project_section_I, project_heading_I,
                 project_paragraph_I,project_media_I,project_href_I,project_tileorder_I,
                 used_I,comment_I):
        self.project_id = project_id_I;
        self.project_section = project_section_I;
        self.project_heading = project_heading_I;
        self.project_paragraph = project_paragraph_I;
        self.project_media = project_media_I;
        self.project_href = project_href_I;
        self.project_tileorder = project_tileorder_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
            'project_id':self.project_id,
                'project_section':self.project_section,
                'project_heading':self.project_heading,
                'project_paragraph':self.project_paragraph,
                'project_media':self.project_media,
                'project_href':self.project_href,
                'project_tileorder':self.project_tileorder,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class visualization_project_status(Base):
    __tablename__ = 'visualization_project_status'
    id = Column(Integer, Sequence('visualization_project_status_id_seq'), primary_key=True)
    project_id = Column(String(100))
    pipeline_id = Column(String(100));
    pipeline_progress = Column(Float);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('project_id','pipeline_id'),
            )

    def __init__(self, project_id_I, pipeline_id_I,pipeline_progress_I,used_I,comment_I):
        self.project_id = project_id_I;
        self.pipeline_id = pipeline_id_I;
        self.pipeline_progress = pipeline_progress_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
            'project_id':self.project_id,
                'pipeline_id':self.pipeline_id,
                'pipeline_progress':self.pipeline_progress,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class visualization_user(Base):
    __tablename__ = 'visualization_user'
    id = Column(Integer, Sequence('visualization_user_id_seq'), primary_key=True)
    project_ids = Column(postgresql.ARRAY(String(100)));
    user_name = Column(String(100));
    user_password = Column(String(100));
    user_role = Column(String(100));
    user_host = Column(String(100));
    user_database = Column(String(100));
    user_schema = Column(String(100));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('user_name'),
            )

    def __init__(self,project_ids_I,
                    user_name_I,
                    user_password_I,
                    user_role_I,
                    user_host_I,
                    user_database_I,
                    user_schema_I,
                    used__I,
                    comment__I):
        self.project_ids=project_ids_I
        self.user_name=user_name_I
        self.user_password=user_password_I
        self.user_role=user_role_I
        self.user_host=user_host_I
        self.user_database=user_database_I
        self.user_schema=user_schema_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'project_ids':self.project_ids,
                'user_name':self.user_name,
                'user_password':self.user_password,
                'user_role':self.user_role,
                'user_host':self.user_host,
                'user_database':self.user_database,
                'user_schema':self.user_schema,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

