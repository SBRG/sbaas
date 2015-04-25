from models_base import *
from sqlalchemy.orm import relationship

# ORM classes
class data_stage01_ale_trajectories(Base):
    __tablename__ = 'data_stage01_ale_trajectories'
    id = Column(Integer, Sequence('data_stage01_ale_trajectories_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100))
    ale_time=Column(Float,nullable=False);
    ale_time_units=Column(String(50))
    rate = Column(Float)
    rate_units = Column(String(50))
    used_ = Column(Boolean)
    comment_ = Column(Text);

    def __init__(self,
            experiment_id_I,
            sample_name_abbreviation_I,
            ale_time_I,
            ale_time_units_I,
            rate_I,
            rate_units_I,
            used__I,
            comment__I):
        self.experiment_id=experiment_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.ale_time=ale_time_I
        self.ale_time_units=ale_time_units_I
        self.rate=rate_I
        self.rate_units=rate_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'ale_time':self.ale_time,
                'ale_time_units':self.ale_time_units,
                'rate':self.rate,
                'rate_units':self.rate_units,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage01_ale_jumps(Base):
    __tablename__ = 'data_stage01_ale_jumps'
    id = Column(Integer, Sequence('data_stage01_ale_jumps_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100))
    jump_region_start = Column(Float)
    jump_region_stop = Column(Float)
    used_ = Column(Boolean)
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,
            sample_name_abbreviation_I,
            ale_time_I,
            ale_time_units_I,
            rate_fitted_I,
            rate_fitted_units_I,
            jump_region_I,
            used__I,
            comment__I):
        self.experiment_id=experiment_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.ale_time=ale_time_I
        self.ale_time_units=ale_time_units_I
        self.rate_fitted=rate_fitted_I
        self.rate_fitted_units=rate_fitted_units_I
        self.jump_region=jump_region_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'ale_time':self.ale_time,
                'ale_time_units':self.ale_time_units,
                'rate_fitted':self.rate_fitted,
                'rate_fitted_units':self.rate_fitted_units,
                'jump_region':self.jump_region,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage01_ale_analysis(Base):
    __tablename__ = 'data_stage01_ale_analysis'
    id = Column(Integer, Sequence('data_stage01_ale_analysis_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    analysis_type = Column(String(100)); # time-course (i.e., multiple time points), paired (i.e., control compared to multiple replicates), group (i.e., single grouping of samples).
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('experiment_id','sample_name_abbreviation','analysis_type','analysis_id'),
            )

    def __init__(self,analysis_id_I,
                 experiment_id_I,
            sample_name_abbreviation_I,
            analysis_type_I,
            used__I,
            comment__I):
        self.analysis_id=analysis_id_I
        self.experiment_id=experiment_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.analysis_type=analysis_type_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
            'experiment_id':self.experiment_id,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'analysis_type':self.analysis_type,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())