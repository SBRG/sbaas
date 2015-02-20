from models_base import *
from sqlalchemy.orm import relationship

# ORM classes
class data_stage01_quantification_LLOQAndULOQ(Base):
    __tablename__ = 'data_stage01_quantification_LLOQAndULOQ'
    id = Column(Integer, Sequence('data_stage01_quantification_lloqanduloq_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name = Column(String(100), primary_key=True)
    component_group_name = Column(String(100))
    component_name = Column(String(500), primary_key=True)
    calculated_concentration = Column(Float)
    calculated_concentration_units = Column(String(20))
    correlation = Column(Float)
    lloq = Column(Float);
    uloq = Column(Float);
    points = Column(Float);
    used_ = Column(Boolean);

    def __init__(self, experiment_id_I, sample_name_I, component_group_name_I, component_name_I,
                    calculated_concentration_I, calculated_concentration_units_I,
                    correlation_I, lloq_I, uloq_I, points_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name = sample_name_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.calculated_concentration = calculated_concentration_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.correlation = correlation_I;
        self.lloq = lloq_I;
        self.uloq = uloq_I;
        self.points = points_I;
        self.used_ = used_I;
class data_stage01_quantification_dilutions(Base):
    __tablename__ = 'data_stage01_quantification_dilutions'
    id = Column(Integer, Sequence('data_stage01_quantification_dilutions_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_id = Column(String(100), primary_key=True)
    component_group_name = Column(String(100))
    component_name = Column(String(500), primary_key=True)
    n_replicates = Column(Integer)
    calculated_concentration_average = Column(Float)
    calculated_concentration_cv = Column(Float)
    calculated_concentration_units = Column(String(20))

    def __init__(self, experiment_id_I, sample_id_I, component_group_name_I, component_name_I, n_replicates_I,
                    calculated_concentration_average_I, calculated_concentration_cv_I, calculated_concentration_units_I):
        self.experiment_id = experiment_id_I;
        self.sample_id = sample_id_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.n_replicates = n_replicates_I;
        self.calculated_concentration_average = calculated_concentration_average_I;
        self.calculated_concentration_cv = calculated_concentration_cv_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
class data_stage01_quantification_QCs(Base):
    __tablename__ = 'data_stage01_quantification_QCs'
    id = Column(Integer, Sequence('data_stage01_quantification_qcs_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    sample_dilution = Column(Float, primary_key=True);
    component_group_name = Column(String(100))
    component_name = Column(String(500), primary_key=True)
    n_replicates = Column(Integer)
    calculated_concentration_average = Column(Float)
    calculated_concentration_CV = Column(Float)
    calculated_concentration_units = Column(String(20))

    def __init__(self, experiment_id_I, sample_name_abbreviation_I, sample_dilution_I, component_group_name_I, component_name_I, n_replicates_I,
                    calculated_concentration_average_I, calculated_concentration_CV_I, calculated_concentration_units_I):
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.sample_dilution = sample_dilution_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.n_replicates = n_replicates_I;
        self.calculated_concentration_average = calculated_concentration_average_I;
        self.calculated_concentration_CV = calculated_concentration_CV_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
class data_stage01_quantification_normalized(Base):
    __tablename__ = 'data_stage01_quantification_normalized'
    id = Column(Integer, Sequence('data_stage01_quantification_normalized_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name = Column(String(100))
    sample_id = Column(String(100))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    calculated_concentration = Column(Float)
    calculated_concentration_units = Column(String(20))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I, sample_name_I, sample_id_I, component_group_name_I, component_name_I,
                    calculated_concentration_I, calculated_concentration_units_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name = sample_name_I;
        self.sample_id = sample_id_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.calculated_concentration = calculated_concentration_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;

    def __repr__dict__(self):
        return {
            'experiment_id':self.experiment_id,
            'sample_name':self.sample_name,
            'sample_id':self.sample_id,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'calculated_concentration':self.calculated_concentration,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage01_quantification_replicates(Base):
    __tablename__ = 'data_stage01_quantification_replicates'
    id = Column(Integer, Sequence('data_stage01_quantification_replicates_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_short = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    component_group_name = Column(String(100))
    component_name = Column(String(500), primary_key=True)
    calculated_concentration = Column(Float)
    calculated_concentration_units = Column(String(20))
    used_ = Column(Boolean);

    def __init__(self, experiment_id_I, sample_name_short_I, time_point_I, component_group_name_I, component_name_I,
                    calculated_concentration_I,calculated_concentration_units_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name_short = sample_name_short_I;
        self.time_point = time_point_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.calculated_concentration = calculated_concentration_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;

    def __repr__dict__(self):
        return {"experiment_id":self.experiment_id,
                "sample_name_short":self.sample_name_short,
                "time_point":self.time_point,
                "component_group_name":self.component_group_name,
                "component_name":self.component_name,
                "calculated_concentration":self.calculated_concentration,
                "calculated_concentration_units":self.calculated_concentration_units,
                "used_":self.used_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage01_quantification_replicatesMI(Base):
    __tablename__ = 'data_stage01_quantification_replicatesmi'
    id = Column(Integer, Sequence('data_stage01_quantification_replicatesmi_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_short = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    component_group_name = Column(String(100))
    component_name = Column(String(500), primary_key=True)
    calculated_concentration = Column(Float)
    calculated_concentration_units = Column(String(20))
    used_ = Column(Boolean);

    def __init__(self, experiment_id_I, sample_name_short_I, time_point_I, component_group_name_I, component_name_I,
                    calculated_concentration_I,calculated_concentration_units_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name_short = sample_name_short_I;
        self.time_point = time_point_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.calculated_concentration = calculated_concentration_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;

    def __repr__dict__(self):
        return {"experiment_id":self.experiment_id,
                "sample_name_short":self.sample_name_short,
                "time_point":self.time_point,
                "component_group_name":self.component_group_name,
                "component_name":self.component_name,
                "calculated_concentration":self.calculated_concentration,
                "calculated_concentration_units":self.calculated_concentration_units,
                "used_":self.used_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage01_quantification_averages(Base):
    __tablename__ = 'data_stage01_quantification_averages'
    id = Column(Integer, Sequence('data_stage01_quantification_averages_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    component_group_name = Column(String(100))
    component_name = Column(String(500), primary_key=True)
    n_replicates_broth = Column(Integer)
    calculated_concentration_broth_average = Column(Float)
    calculated_concentration_broth_cv = Column(Float)
    n_replicates_filtrate = Column(Integer)
    calculated_concentration_filtrate_average = Column(Float)
    calculated_concentration_filtrate_cv = Column(Float)
    n_replicates = Column(Integer)
    calculated_concentration_average = Column(Float)
    calculated_concentration_cv = Column(Float)
    calculated_concentration_units = Column(String(20))
    extracellular_percent = Column(Float)
    used_ = Column(Boolean);

    def __init__(self, experiment_id_I, sample_name_abbreviation_I, time_point_I, component_group_name_I, component_name_I,
                    n_replicates_broth_I, calculated_concentration_broth_average_I, calculated_concentration_broth_cv_I,
                    n_replicates_filtrate_I, calculated_concentration_filtrate_average_I, calculated_concentration_filtrate_cv_I,
                    n_replicates_I, calculated_concentration_average_I, calculated_concentration_cv_I,
                    calculated_concentration_units_I, extracellular_percent_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.n_replicates_broth = n_replicates_broth_I;
        self.calculated_concentration_broth_average = calculated_concentration_broth_average_I;
        self.calculated_concentration_broth_cv = calculated_concentration_broth_cv_I;
        self.n_replicates_filtrate = n_replicates_filtrate_I;
        self.calculated_concentration_filtrate_average = calculated_concentration_filtrate_average_I;
        self.calculated_concentration_filtrate_cv = calculated_concentration_filtrate_cv_I;
        self.n_replicates = n_replicates_I;
        self.calculated_concentration_average = calculated_concentration_average_I;
        self.calculated_concentration_cv = calculated_concentration_cv_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.extracellular_percent = extracellular_percent_I;
        self.used_ = used_I;
class data_stage01_quantification_averagesMI(Base):
    __tablename__ = 'data_stage01_quantification_averagesmi'
    id = Column(Integer, Sequence('data_stage01_quantification_averagesmi_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    component_group_name = Column(String(100))
    component_name = Column(String(500), primary_key=True)
    n_replicates = Column(Integer)
    calculated_concentration_average = Column(Float)
    calculated_concentration_cv = Column(Float)
    calculated_concentration_units = Column(String(20))
    used_ = Column(Boolean);

    def __init__(self, experiment_id_I, sample_name_abbreviation_I, time_point_I, component_group_name_I, component_name_I,
                    n_replicates_I, calculated_concentration_average_I, calculated_concentration_cv_I,
                    calculated_concentration_units_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.n_replicates = n_replicates_I;
        self.calculated_concentration_average = calculated_concentration_average_I;
        self.calculated_concentration_cv = calculated_concentration_cv_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;

    def __repr__dict__(self):
        return {"experiment_id":self.experiment_id,
                "sample_name_abbreviation":self.sample_name_abbreviation,
                "time_point":self.time_point,
                "component_group_name":self.component_group_name,
                "component_name":self.component_name,
                "calculated_concentration_average":self.calculated_concentration_average,
                "calculated_concentration_cv":self.calculated_concentration_cv,
                "calculated_concentration_units":self.calculated_concentration_units,
                "used_":self.used_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage01_quantification_averagesMIgeo(Base):
    __tablename__ = 'data_stage01_quantification_averagesmigeo'
    id = Column(Integer, Sequence('data_stage01_quantification_averagesmigeo_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    component_group_name = Column(String(100))
    component_name = Column(String(500), primary_key=True)
    n_replicates = Column(Integer)
    calculated_concentration_average = Column(Float)
    calculated_concentration_var = Column(Float)
    calculated_concentration_lb = Column(Float)
    calculated_concentration_ub = Column(Float)
    calculated_concentration_units = Column(String(20))
    used_ = Column(Boolean);

    def __init__(self, experiment_id_I, sample_name_abbreviation_I, time_point_I, component_group_name_I, component_name_I,
                    n_replicates_I, calculated_concentration_average_I, calculated_concentration_var_I,
                    calculated_concentration_lb_I, calculated_concentration_ub_I,
                    calculated_concentration_units_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.n_replicates = n_replicates_I;
        self.calculated_concentration_average = calculated_concentration_average_I;
        self.calculated_concentration_var = calculated_concentration_var_I;
        self.calculated_concentration_lb = calculated_concentration_lb_I;
        self.calculated_concentration_ub = calculated_concentration_ub_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;

    def __repr__dict__(self):
        return {"experiment_id":self.experiment_id,
                "sample_name_abbreviation":self.sample_name_abbreviation,
                "time_point":self.time_point,
                "component_group_name":self.component_group_name,
                "component_name":self.component_name,
                "n_replicates":self.n_replicates,
                "calculated_concentration_average":self.calculated_concentration_average,
                "calculated_concentration_var":self.calculated_concentration_cv,
                "calculated_concentration_lb":self.calculated_concentration_lb,
                "calculated_concentration_ub":self.calculated_concentration_ub,
                "calculated_concentration_units":self.calculated_concentration_units,
                "used_":self.used_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage01_quantification_physiologicalRatios_replicates(Base):
    __tablename__ = 'data_stage01_quantification_physiologicalRatios_replicates'
    id = Column(Integer, Sequence('data_stage01_quantification_physiologicalRatios_replicates_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_short = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    physiologicalratio_id = Column(String(50), primary_key=True)
    physiologicalratio_name = Column(String(100))
    physiologicalratio_value = Column(Float)
    physiologicalratio_description = Column(String(500))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I,
                sample_name_short_I,
                time_point_I,
                physiologicalratio_id_I,
                physiologicalratio_name_I,
                physiologicalratio_value_I,
                physiologicalratio_description_I,
                used__I,
                comment__I):
        self.experiment_id=experiment_id_I
        self.sample_name_short=sample_name_short_I
        self.time_point=time_point_I
        self.physiologicalratio_id=physiologicalratio_id_I
        self.physiologicalratio_name=physiologicalratio_name_I
        self.physiologicalratio_value=physiologicalratio_value_I
        self.physiologicalratio_description=physiologicalratio_description_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__(self):
        return "data_stage01_quantification_physiologicalRatios_replicates: %s, %s, %s" % (self.experiment_id,
                                                                            self.sample_name_short,
                                                                            self.physiologicalratio_id)

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
            'sample_name_short':self.sample_name_short,
            'time_point':self.time_point,
            'physiologicalratio_id':self.physiologicalratio_id,
            'physiologicalratio_name':self.physiologicalratio_name,
            'physiologicalratio_value':self.physiologicalratio_value,
            'physiologicalratio_description':self.physiologicalratio_description,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage01_quantification_physiologicalRatios_averages(Base):
    __tablename__ = 'data_stage01_quantification_physiologicalRatios_averages'
    id = Column(Integer, Sequence('data_stage01_quantification_physiologicalRatios_averages_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    physiologicalratio_id = Column(String(50), primary_key=True)
    physiologicalratio_name = Column(String(100))
    physiologicalratio_value_ave = Column(Float)
    physiologicalratio_value_cv = Column(Float)
    physiologicalratio_value_lb = Column(Float)
    physiologicalratio_value_ub = Column(Float)
    physiologicalratio_description = Column(String(500))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,experiment_id_I,
                sample_name_abbreviation_I,
                time_point_I,
                physiologicalratio_id_I,
                physiologicalratio_name_I,
                physiologicalratio_value_ave_I,
                physiologicalratio_value_cv_I,
                physiologicalratio_value_lb_I,
                physiologicalratio_value_ub_I,
                physiologicalratio_description_I,
                used__I,
                comment__I):
        self.experiment_id=experiment_id_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        self.physiologicalratio_id=physiologicalratio_id_I
        self.physiologicalratio_name=physiologicalratio_name_I
        self.physiologicalratio_value_ave=physiologicalratio_value_ave_I
        self.physiologicalratio_value_cv=physiologicalratio_value_cv_I
        self.physiologicalratio_value_lb=physiologicalratio_value_lb_I
        self.physiologicalratio_value_ub=physiologicalratio_value_ub_I
        self.physiologicalratio_description=physiologicalratio_description_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__(self):
        return "data_stage01_quantification_physiologicalRatios_averages: %s, %s, %s" % (self.experiment_id,
                                                                            self.sample_name_abbreviation,
                                                                            self.physiologicalratio_id)

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
            'time_point':self.time_point,
                'physiologicalratio_id':self.physiologicalratio_id,
                'physiologicalratio_name':self.physiologicalratio_name,
                'physiologicalratio_value_ave':self.physiologicalratio_value_ave,
                'physiologicalratio_value_cv':self.physiologicalratio_value_cv,
                'physiologicalratio_value_lb':self.physiologicalratio_value_lb,
                'physiologicalratio_value_ub':self.physiologicalratio_value_ub,
                'physiologicalratio_description':self.physiologicalratio_description,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage01_quantification_peakInformation(Base):
    __tablename__ = 'data_stage01_quantification_peakInformation'
    id = Column(Integer, Sequence('data_stage01_quantification_peakInformation_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    peakInfo_parameter = Column(String(50))
    peakInfo_ave = Column(Float)
    peakInfo_cv = Column(Float)
    peakInfo_lb = Column(Float)
    peakInfo_ub = Column(Float)
    peakInfo_units = Column(String(50))
    sample_names = Column(postgresql.ARRAY(String(100)))
    sample_types = Column(postgresql.ARRAY(String(100)))
    acqusition_date_and_times = Column(postgresql.ARRAY(DateTime))
    peakInfo_data = Column(postgresql.ARRAY(Float))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,
                 experiment_id_I,
                component_group_name_I,
                component_name_I,
                peakInfo_parameter_I,
                peakInfo_ave_I,
                peakInfo_cv_I,
                peakInfo_lb_I,
                peakInfo_ub_I,
                peakInfo_units_I,
                sample_names_I,
                sample_types_I,
                acqusition_date_and_times_I,
                peakInfo_data_I,
                used__I,
                comment__I):
        self.experiment_id=experiment_id_I
        self.component_group_name=component_group_name_I
        self.component_name=component_name_I
        self.peakInfo_parameter=peakInfo_parameter_I
        self.peakInfo_ave=peakInfo_ave_I
        self.peakInfo_cv=peakInfo_cv_I
        self.peakInfo_lb=peakInfo_lb_I
        self.peakInfo_ub=peakInfo_ub_I
        self.peakInfo_units=peakInfo_units_I
        self.sample_names=sample_names_I
        self.sample_types=sample_types_I
        self.acqusition_date_and_times=acqusition_date_and_times_I
        self.peakInfo_data=peakInfo_data_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'peakInfo_parameter':self.peakInfo_parameter,
            'peakInfo_ave':self.peakInfo_ave,
            'peakInfo_cv':self.peakInfo_cv,
            'peakInfo_lb':self.peakInfo_lb,
            'peakInfo_ub':self.peakInfo_ub,
            'peakInfo_units':self.peakInfo_units,
            'sample_names':self.sample_names,
            'sample_types':self.sample_types,
            'acqusition_date_and_times':self.acqusition_date_and_times,
            'peakInfo_data':self.peakInfo_data,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage01_quantification_peakResolution(Base):
    __tablename__ = 'data_stage01_quantification_peakResolution'
    id = Column(Integer, Sequence('data_stage01_quantification_peakResolution_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    component_group_name_pair = Column(postgresql.ARRAY(String(100)))
    component_name_pair = Column(postgresql.ARRAY(String(500)))
    peakInfo_parameter = Column(String(50))
    peakInfo_ave = Column(Float)
    peakInfo_cv = Column(Float)
    peakInfo_lb = Column(Float)
    peakInfo_ub = Column(Float)
    peakInfo_units = Column(String(50))
    sample_names = Column(postgresql.ARRAY(String(100)))
    sample_types = Column(postgresql.ARRAY(String(100)))
    acqusition_date_and_times = Column(postgresql.ARRAY(DateTime))
    peakInfo_data = Column(postgresql.ARRAY(Float))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self,
                 experiment_id_I,
                component_group_name_pair_I,
                component_name_pair_I,
                peakInfo_parameter_I,
                peakInfo_ave_I,
                peakInfo_cv_I,
                peakInfo_lb_I,
                peakInfo_ub_I,
                peakInfo_units_I,
                sample_names_I,
                sample_types_I,
                acqusition_date_and_times_I,
                peakInfo_data_I,
                used__I,
                comment__I):
        self.experiment_id=experiment_id_I
        self.component_group_name_pair=component_group_name_pair_I
        self.component_name_pair=component_name_pair_I
        self.peakInfo_parameter=peakInfo_parameter_I
        self.peakInfo_ave=peakInfo_ave_I
        self.peakInfo_cv=peakInfo_cv_I
        self.peakInfo_lb=peakInfo_lb_I
        self.peakInfo_ub=peakInfo_ub_I
        self.peakInfo_units=peakInfo_units_I
        self.sample_names=sample_names_I
        self.sample_types=sample_types_I
        self.acqusition_date_and_times=acqusition_date_and_times_I
        self.peakInfo_data=peakInfo_data_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'experiment_id':self.experiment_id,
            'component_group_name_pair':self.component_group_name_pair,
            'component_name_pair':self.component_name_pair,
            'peakInfo_parameter':self.peakInfo_parameter,
            'peakInfo_ave':self.peakInfo_ave,
            'peakInfo_cv':self.peakInfo_cv,
            'peakInfo_lb':self.peakInfo_lb,
            'peakInfo_ub':self.peakInfo_ub,
            'peakInfo_units':self.peakInfo_units,
            'sample_names':self.sample_names,
            'sample_types':self.sample_types,
            'acqusition_date_and_times':self.acqusition_date_and_times,
            'peakInfo_data':self.peakInfo_data,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
# views:
class data_stage01_quantification_checkLLOQAndULOQ(Base):
    __tablename__ = 'data_stage01_quantification_checkLLOQAndULOQ'
    experiment_id = Column(String(50), primary_key=True)
    sample_name = Column(String(100), primary_key=True)
    component_group_name = Column(String(100))
    component_name = Column(String(500), primary_key=True)
    calculated_concentration = Column(Float)
    calculated_concentration_units = Column(String(20))
    correlation = Column(Float)
    lloq = Column(Float);
    uloq = Column(Float);
    points = Column(Float);
    used_ = Column(Boolean);

    def __init__(self, experiment_id_I, sample_name_I, component_group_name_I, component_name_I,
                    calculated_concentration_I, calculated_concentration_units_I,
                    correlation_I, lloq_I, uloq_I, points_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name = sample_name_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.calculated_concentration = calculated_concentration_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.correlation = correlation_I;
        self.lloq = lloq_I;
        self.uloq = uloq_I;
        self.points = points_I;
        self.used_ = used_I;
class data_stage01_quantification_checkISMatch(Base):
    __tablename__ = 'data_stage01_quantification_checkISMatch'
    experiment_id = Column(String(50), primary_key=True)
    sample_name = Column(String(100), primary_key=True)
    component_name = Column(String(500), primary_key=True)
    IS_name_samples = Column(String(500))
    IS_name_calibrators = Column(String(500))

    def __init__(self, experiment_id_I, sample_name_I, component_name_I,
                    IS_name_samples_I, IS_name_calibrators_I):
        self.experiment_id = experiment_id_I;
        self.sample_name = sample_name_I;
        self.component_name = component_name_I;
        self.IS_name_samples = IS_name_samples_I;
        self.IS_name_calibrators = IS_name_calibrators_I;
class data_stage01_quantification_checkCV_QCs(Base):
    __tablename__ = 'data_stage01_quantification_checkCV_QCs'
    experiment_id = Column(String(50), primary_key=True)
    sample_Name_Abbreviation = Column(String(100), primary_key=True)
    sample_dilution = Column(Float, primary_key=True);
    component_group_name = Column(String(100))
    component_name = Column(String(500), primary_key=True)
    n_replicates = Column(Integer)
    calculated_concentration_average = Column(Float)
    calculated_concentration_cv = Column(Float)
    calculated_concentration_units = Column(String(20))

    def __init__(self, experiment_id_I, sample_Name_Abbreviation_I, sample_dilution_I, component_group_name_I, component_name_I, n_replicates_I,
                    calculated_concentration_average_I, calculated_concentration_cv_I,
                    calculated_concentration_units_I):
        self.experiment_id = experiment_id_I;
        self.sample_Name_Abbreviation = sample_Name_Abbreviation_I;
        self.sample_dilution = sample_dilution_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.n_replicates = n_replicates_I;
        self.calculated_concentration_average = calculated_concentration_average_I;
        self.calculated_concentration_cv = calculated_concentration_cv_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
class data_stage01_quantification_checkCV_dilutions(Base):
    __tablename__ = 'data_stage01_quantification_checkCV_dilutions'
    experiment_id = Column(String(50), primary_key=True)
    sample_id = Column(String(100), primary_key=True)
    component_group_name = Column(String(100))
    component_name = Column(String(500), primary_key=True)
    n_replicates = Column(Integer)
    calculated_concentration_average = Column(Float)
    calculated_concentration_cv = Column(Float)
    calculated_concentration_units = Column(String(20))

    def __init__(self, experiment_id_I, sample_id_I, component_group_name_I, component_name_I, n_replicates_I,
                    calculated_concentration_average_I, calculated_concentration_cv_I,
                    calculated_concentration_units_I):
        self.experiment_id = experiment_id_I;
        self.sample_id = sample_id_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.n_replicates = n_replicates_I;
        self.calculated_concentration_average = calculated_concentration_average_I;
        self.calculated_concentration_cv = calculated_concentration_cv_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
class data_stage01_quantification_checkCVAndExtracellular_averages(Base):
    __tablename__ = 'data_stage01_quantification_checkCVAndExtracellular_averages'
    experiment_id = Column(String(50), primary_key=True)
    sample_name_abbreviation = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    component_group_name = Column(String(100))
    component_name = Column(String(500), primary_key=True)
    n_replicates_broth = Column(Integer)
    calculated_concentration_broth_average = Column(Float)
    calculated_concentration_broth_cv = Column(Float)
    n_replicates_filtrate = Column(Integer)
    calculated_concentration_filtrate_average = Column(Float)
    calculated_concentration_filtrate_cv = Column(Float)
    n_replicates = Column(Integer)
    calculated_concentration_average = Column(Float)
    calculated_concentration_cv = Column(Float)
    calculated_concentration_units = Column(String(20))
    extracellular_percent = Column(Float)
    used_ = Column(Boolean);

    def __init__(self, experiment_id_I, sample_name_abbreviation_I, component_group_name_I, time_point_I, component_name_I,
                    n_replicates_broth_I, calculated_concentration_broth_average_I, calculated_concentration_broth_cv_I,
                    n_replicates_filtrate_I, calculated_concentration_filtrate_average_I, calculated_concentration_filtrate_cv_I,
                    n_replicates_I, calculated_concentration_average_I, calculated_concentration_cv_I,
                    calculated_concentration_units_I, extracellular_percent_I, used_I):
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.component_group_name = component_group_name_I;
        self.time_point = time_point_I;
        self.component_name = component_name_I;
        self.n_replicates_broth = n_replicates_broth_I;
        self.calculated_concentration_broth_average = calculated_concentration_broth_average_I;
        self.calculated_concentration_broth_cv = calculated_concentration_broth_cv_I;
        self.n_replicates_filtrate = n_replicates_filtrate_I;
        self.calculated_concentration_filtrate_average = calculated_concentration_filtrate_average_I;
        self.calculated_concentration_filtrate_cv = calculated_concentration_filtrate_cv_I;
        self.n_replicates = n_replicates_I;
        self.calculated_concentration_average = calculated_concentration_average_I;
        self.calculated_concentration_cv = calculated_concentration_cv_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.extracellular_percent = extracellular_percent_I;
        self.used_ = used_I;

class data_stage01_quantification_MQResultsTable(Base):
    #__table__ = make_table('data_stage01_quantification_mqresultstable')
    __tablename__ = 'data_stage01_quantification_mqresultstable'
    index_=Column(Integer);
    sample_index=Column(Integer);
    original_filename=Column(Text);
    sample_name=Column(String(100),nullable=False, primary_key=True);
    sample_id=Column(String(500));
    sample_comment=Column(Text);
    sample_type=Column(String(20));
    acquisition_date_and_time=Column(DateTime,nullable=False, primary_key=True);
    rack_number=Column(Integer);
    plate_number=Column(Integer);
    vial_number=Column(Integer);
    dilution_factor=Column(Float);
    injection_volume=Column(Float);
    operator_name=Column(String(100));
    acq_method_name=Column(String(100));
    is_=Column(Boolean);
    component_name=Column(String(500),nullable=False, primary_key=True);
    component_index=Column(Integer);
    component_comment=Column(Text);
    is_comment=Column(Text);
    mass_info=Column(String(100));
    is_mass=Column(String(100));
    is_name=Column(String(500));
    component_group_name=Column(String(100));
    conc_units=Column(String(20));
    failed_query=Column(Boolean);
    is_failed_query=Column(Boolean);
    peak_comment=Column(Text);
    is_peak_comment=Column(Text);
    actual_concentration=Column(Float);
    is_actual_concentration=Column(Float);
    concentration_ratio=Column(Float);
    expected_rt=Column(Float);
    is_expected_rt=Column(Float);
    integration_type=Column(String(100));
    is_integration_type=Column(String(100));
    area=Column(Float);
    is_area=Column(Float);
    corrected_area=Column(Float);
    is_corrected_area=Column(Float);
    area_ratio=Column(Float);
    height=Column(Float);
    is_height=Column(Float);
    corrected_height=Column(Float);
    is_corrected_height=Column(Float);
    height_ratio=Column(Float);
    area_2_height=Column(Float);
    is_area_2_height=Column(Float);
    corrected_area2height=Column(Float);
    is_corrected_area2height=Column(Float);
    region_height=Column(Float);
    is_region_height=Column(Float);
    quality=Column(Float);
    is_quality=Column(Float);
    retention_time=Column(Float);
    is_retention_time=Column(Float);
    start_time=Column(Float);
    is_start_time=Column(Float);
    end_time=Column(Float);
    is_end_time=Column(Float);
    total_width=Column(Float);
    is_total_width=Column(Float);
    width_at_50=Column(Float);
    is_width_at_50=Column(Float);
    signal_2_noise=Column(Float);
    is_signal_2_noise=Column(Float);
    baseline_delta_2_height=Column(Float);
    is_baseline_delta_2_height=Column(Float);
    modified_=Column(Boolean);
    relative_rt=Column(Float);
    used_=Column(Boolean);
    calculated_concentration=Column(Float);
    accuracy_=Column(Float);
    comment_=Column(Text);
    use_calculated_concentration=Column(Boolean,default=True);

    #__table_args__ = (
    #        UniqueConstraint('component_name','sample_name','acquisition_date_and_time'),
    #        )

    def __init__(self,index__I,sample_index_I,original_filename_I,
                 sample_name_I,sample_id_I,sample_comment_I,sample_type_I,
                 acquisition_date_and_time_I,rack_number_I,plate_number_I,
                 vial_number_I,dilution_factor_I,injection_volume_I,
                 operator_name_I,acq_method_name_I,is__I,component_name_I,
                 component_index_I,component_comment_I,is_comment_I,
                 mass_info_I,is_mass_I,is_name_I,component_group_name_I,
                 conc_units_I,failed_query_I,is_failed_query_I,peak_comment_I,
                 is_peak_comment_I,actual_concentration_I,is_actual_concentration_I,
                 concentration_ratio_I,expected_rt_I,is_expected_rt_I,
                 integration_type_I,is_integration_type_I,area_I,is_area_I,
                 corrected_area_I,is_corrected_area_I,area_ratio_I,height_I,
                 is_height_I,corrected_height_I,is_corrected_height_I,
                 height_ratio_I,area_2_height_I,is_area_2_height_I,
                 corrected_area2height_I,is_corrected_area2height_I,
                 region_height_I,is_region_height_I,quality_I,is_quality_I,
                 retention_time_I,is_retention_time_I,start_time_I,
                 is_start_time_I,end_time_I,is_end_time_I,total_width_I,
                 is_total_width_I,width_at_50_I,is_width_at_50_I,
                 signal_2_noise_I,is_signal_2_noise_I,baseline_delta_2_height_I,
                 is_baseline_delta_2_height_I,modified__I,relative_rt_I,used__I,
                 calculated_concentration_I,accuracy__I,comment__I,use_calculated_concentration_I):
        self.index_=index__I;
        self.sample_index=sample_index_I;
        self.original_filename=original_filename_I;
        self.sample_name=sample_name_I;
        self.sample_id=sample_id_I;
        self.sample_comment=sample_comment_I;
        self.sample_type=sample_type_I;
        self.acquisition_date_and_time=acquisition_date_and_time_I;
        self.rack_number=rack_number_I;
        self.plate_number=plate_number_I;
        self.vial_number=vial_number_I;
        self.dilution_factor=dilution_factor_I;
        self.injection_volume=injection_volume_I;
        self.operator_name=operator_name_I;
        self.acq_method_name=acq_method_name_I;
        self.is_=is__I;
        self.component_name=component_name_I;
        self.component_index=component_index_I;
        self.component_comment=component_comment_I;
        self.is_comment=is_comment_I;
        self.mass_info=mass_info_I;
        self.is_mass=is_mass_I;
        self.is_name=is_name_I;
        self.component_group_name=component_group_name_I;
        self.conc_units=conc_units_I;
        self.failed_query=failed_query_I;
        self.is_failed_query=is_failed_query_I;
        self.peak_comment=peak_comment_I;
        self.is_peak_comment=is_peak_comment_I;
        self.actual_concentration=actual_concentration_I;
        self.is_actual_concentration=is_actual_concentration_I;
        self.concentration_ratio=concentration_ratio_I;
        self.expected_rt=expected_rt_I;
        self.is_expected_rt=is_expected_rt_I;
        self.integration_type=integration_type_I;
        self.is_integration_type=is_integration_type_I;
        self.area=area_I;
        self.is_area=is_area_I;
        self.corrected_area=corrected_area_I;
        self.is_corrected_area=is_corrected_area_I;
        self.area_ratio=area_ratio_I;
        self.height=height_I;
        self.is_height=is_height_I;
        self.corrected_height=corrected_height_I;
        self.is_corrected_height=is_corrected_height_I;
        self.height_ratio=height_ratio_I;
        self.area_2_height=area_2_height_I;
        self.is_area_2_height=is_area_2_height_I;
        self.corrected_area2height=corrected_area2height_I;
        self.is_corrected_area2height=is_corrected_area2height_I;
        self.region_height=region_height_I;
        self.is_region_height=is_region_height_I;
        self.quality=quality_I;
        self.is_quality=is_quality_I;
        self.retention_time=retention_time_I;
        self.is_retention_time=is_retention_time_I;
        self.start_time=start_time_I;
        self.is_start_time=is_start_time_I;
        self.end_time=end_time_I;
        self.is_end_time=is_end_time_I;
        self.total_width=total_width_I;
        self.is_total_width=is_total_width_I;
        self.width_at_50=width_at_50_I;
        self.is_width_at_50=is_width_at_50_I;
        self.signal_2_noise=signal_2_noise_I;
        self.is_signal_2_noise=is_signal_2_noise_I;
        self.baseline_delta_2_height=baseline_delta_2_height_I;
        self.is_baseline_delta_2_height=is_baseline_delta_2_height_I;
        self.modified_=modified__I;
        self.relative_rt=relative_rt_I;
        self.used_=used__I;
        self.calculated_concentration=calculated_concentration_I;
        self.accuracy_=accuracy__I;
        self.comment_=comment__I;
        self.use_calculated_concentration=use_calculated_concentration_I;

    #TODO:
    #define relations

    #define representation
    def __repr__(self):
        return "data_stage01_quantification_MQResultsTable %s" % (self.acquisition_date_and_time, self.sample_name,self.component_name)
