from models_base import *
from sqlalchemy.orm import relationship

# ORM classes
class data_stage01_physiology_data(Base):
    __tablename__ = 'data_stage01_physiology_data'
    id = Column(Integer, Sequence('data_stage01_physiology_data_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_id=Column(String(500), nullable=False, primary_key=True);
    #sample_name_short = Column(String(100), primary_key=True)
    #time_point = Column(String(10))
    #sample_date = Column(DateTime, primary_key=True)
    met_id = Column(String(100), primary_key=True)
    data_raw = Column(Float)
    data_corrected = Column(Float)
    data_units = Column(String(100))
    data_reference = Column(String(500), primary_key=True)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I,sample_id_I,
                 #sample_name_short_I,time_point_I,sample_date_I,
                 met_id_I,data_raw_I,data_corrected_I,
                 data_units_I,data_reference_I,used__I,comment__I,):
        self.experiment_id=experiment_id_I
        self.sample_id=sample_id_I
        #self.time_point=time_point_I
        #self.sample_date=sample_date_I
        self.met_id=met_id_I
        self.data_raw=data_raw_I
        self.data_corrected=data_corrected_I
        self.data_units=data_units_I
        self.data_reference=data_reference_I
        self.used_=used__I
        self.comment_=comment__I

class data_stage01_physiology_rates(Base):
    __tablename__ = 'data_stage01_physiology_rates'
    id = Column(Integer, Sequence('data_stage01_physiology_rates_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_short = Column(String(100), primary_key=True)
    met_id = Column(String(100), primary_key=True)
    slope = Column(Float)
    intercept = Column(Float)
    r2 = Column(Float)
    rate = Column(Float)
    rate_units = Column(String(20))
    p_value = Column(Float)
    std_err = Column(Float)
    used_ = Column(Boolean)
    comment_ = Column(Text);

    def __init__(self, experiment_id_I, sample_name_short_I,
                 met_id_I, slope_I, intercept_I,
                 r2_I, rate_I, rate_units_I,
                 p_value_I, std_err_I,
                 used__I, comment__I):
        self.experiment_id = experiment_id_I;
        self.sample_name_short = sample_name_short_I;
        self.slope = slope_I;
        self.intercept = intercept_I;
        self.met_id=met_id_I
        self.r2 = r2_I;
        self.rate = rate_I;
        self.rate_units = rate_units_I;
        self.p_value = p_value_I;
        self.std_err = std_err_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

class data_stage01_physiology_ratesAverages(Base):
    __tablename__ = 'data_stage01_physiology_ratesAverages'
    id = Column(Integer, Sequence('data_stage01_physiology_ratesAverages_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100))
    met_id = Column(String(100), primary_key=True)
    n = Column(Integer)
    slope_average = Column(Float)
    intercept_average = Column(Float)
    rate_average = Column(Float)
    rate_var = Column(Float)
    rate_lb = Column(Float)
    rate_ub = Column(Float)
    rate_units = Column(String(50))
    used_ = Column(Boolean)
    comment_ = Column(Text);

    def __init__(self, experiment_id_I, sample_name_abbreviation_I,
                 met_id_I, n_I, slope_average_I, intercept_average_I, rate_average_I, rate_var_I,
                 rate_lb_I, rate_ub_I, rate_units_I, used__I, comment__I):
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.met_id=met_id_I;
        self.n = n_I;
        self.slope_average = slope_average_I;
        self.intercept_average = intercept_average_I;
        self.rate_average = rate_average_I;
        self.rate_var = rate_var_I;
        self.rate_lb = rate_lb_I;
        self.rate_ub = rate_ub_I;
        self.rate_units = rate_units_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

class data_stage01_physiology_analysis(Base):
    __tablename__ = 'data_stage01_physiology_analysis'
    id = Column(Integer, Sequence('data_stage01_physiology_analysis_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_short = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    analysis_type = Column(String(100)); # time-course (i.e., multiple time points), paired (i.e., control compared to multiple replicates), group (i.e., single grouping of samples).
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('experiment_id','sample_name_short','sample_name_abbreviation','analysis_type','analysis_id'),
            )

    def __init__(self,analysis_id_I,
                 experiment_id_I,
            sample_name_short_I,
            sample_name_abbreviation_I,
            analysis_type_I,
            used__I,
            comment__I):
        self.analysis_id=analysis_id_I
        self.experiment_id=experiment_id_I
        self.sample_name_short=sample_name_short_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.analysis_type=analysis_type_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'analysis_id':self.analysis_id,
            'experiment_id':self.experiment_id,
            'sample_name_short':self.sample_name_short,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'analysis_type':self.analysis_type,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())