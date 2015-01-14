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
# TODO:
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