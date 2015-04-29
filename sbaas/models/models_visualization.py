# ORMs
from models_base import *
from sqlalchemy.orm import relationship

# ORM classes
class visualization_project(Base):
    __tablename__ = 'visualization_project'
    id = Column(Integer, Sequence('visualization_project_id_seq'), primary_key=True)
    project_id = Column(String(100))
    analysis_id = Column(String(500))
    data_export_id = Column(String(100))
    container_export_id = Column(String(100))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('project_id','analysis_id','data_export_id','container_export_id'),
            )

    def __init__(self, project_id_I, analysis_id_I, data_export_id_I,container_export_id_I,used_I,comment_I):
        self.project_id = project_id_I;
        self.analysis_id = analysis_id_I;
        self.data_export_id = data_export_id_I;
        self.container_export_id = container_export_id_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
            'project_id':self.project_id,
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
    project_description = Column(Text);
    project_svg = Column(Text);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('project_id'),
            )

    def __init__(self, project_id_I, project_description_I,project_svg_I,used_I,comment_I):
        self.project_id = project_id_I;
        self.project_description = project_description_I;
        self.project_svg = project_svg_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
            'project_id':self.project_id,
                'project_description':self.project_description,
                'project_svg':self.project_svg,
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