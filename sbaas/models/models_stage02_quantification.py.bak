# models_stage02_quantification
# i.e. statistics

# ORMs
from models_base import *
from sqlalchemy.orm import relationship

# ORM classes
class data_stage02_quantification_glogNormalized(Base):
    __tablename__ = 'data_stage02_quantification_glogNormalized'
    id = Column(Integer, Sequence('data_stage02_quantification_glogNormalized_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_short = Column(String(100))
    time_point = Column(String(10))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    calculated_concentration = Column(Float)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('experiment_id','sample_name_short','time_point','component_name'),
                      UniqueConstraint('analysis_id','experiment_id','sample_name_short','time_point','component_name','calculated_concentration_units'),
            )

    def __init__(self, 
                 analysis_id_I,
                 experiment_id_I, sample_name_short_I, time_point_I,
                 component_group_name_I, component_name_I, calculated_concentration_I,calculated_concentration_units_I,
                 used_I,comment_I):
        self.analysis_id = analysis_id_I;
        self.experiment_id = experiment_id_I;
        self.sample_name_short = sample_name_short_I;
        self.time_point = time_point_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.calculated_concentration = calculated_concentration_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
            "analysis_id":self.analysis_id,
            "experiment_id":self.experiment_id,
                "sample_name_short":self.sample_name_short,
                "time_point":self.time_point,
                "component_group_name":self.component_group_name,
                "component_name":self.component_name,
                "calculated_concentration":self.calculated_concentration,
                "calculated_concentration_units":self.calculated_concentration_units,
                "used_":self.used_,
                'comments_I':self.comments_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_anova(Base):
    #anova (more than 2 samples), independent t-test (2 samples)
    __tablename__ = 'data_stage02_quantification_anova'
    id = Column(Integer, Sequence('data_stage02_quantification_anova_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    sample_name_abbreviation = Column(postgresql.ARRAY(String(100)))
    #time_point = Column(String(10))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    test_stat = Column(Float)
    test_description = Column(String(50));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('experiment_id','sample_name_abbreviation','time_point','component_name'),
                      UniqueConstraint('analysis_id','sample_name_abbreviation','component_name','calculated_concentration_units'),
            )

    def __init__(self, 
                 analysis_id_I,
                 #experiment_id_I, 
                 sample_name_abbreviation_I, 
                 #time_point_I, 
                 component_group_name_I, component_name_I,
                 test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I, 
                 calculated_concentration_units_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        #self.time_point = time_point_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self): 
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'test_stat':self.test_stat,
            'test_description':self.test_description,
            'pvalue':self.pvalue,
            'pvalue_corrected':self.pvalue_corrected,
            'pvalue_corrected_description':self.pvalue_corrected_description,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_pairWiseTest(Base):
    #pairedttest
    __tablename__ = 'data_stage02_quantification_pairWiseTest'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseTest_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    sample_name_abbreviation_1 = Column(String(100))
    sample_name_abbreviation_2 = Column(String(100))
    #time_point_1 = Column(String(10))
    #time_point_2 = Column(String(10))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    test_stat = Column(Float)
    test_description = Column(String(50));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    mean = Column(Float)
    ci_lb = Column(Float)
    ci_ub = Column(Float)
    ci_level = Column(Float)
    fold_change = Column(Float)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('experiment_id','sample_name_abbreviation_1','time_point_1','sample_name_abbreviation_2','time_point_2','component_name'),
                      UniqueConstraint('analysis_id','sample_name_abbreviation_1','sample_name_abbreviation_2','component_name','calculated_concentration_units','test_description'),
            )

    def __init__(self,
                 analysis_id_I,
                 #experiment_id_I,
                 sample_name_abbreviation_1_I, sample_name_abbreviation_2_I,
                 #time_point_1_I, time_point_2_I,
                 component_group_name_I, component_name_I,
                 mean_I, test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 ci_lb_I, ci_ub_I, ci_level_I,
                 fold_change_I, calculated_concentration_units_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation_1 = sample_name_abbreviation_1_I;
        self.sample_name_abbreviation_2 = sample_name_abbreviation_2_I;
        #self.time_point_1 = time_point_1_I;
        #self.time_point_2 = time_point_2_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.mean=mean_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.ci_lb=ci_lb_I;
        self.ci_ub=ci_ub_I;
        self.ci_level=ci_level_I;
        self.fold_change=fold_change_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_abbreviation_1':self.sample_name_abbreviation_1,
            'sample_name_abbreviation_2':self.sample_name_abbreviation_2,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'test_stat':self.test_stat,
            'test_description':self.test_description,
            'pvalue':self.pvalue,
            'pvalue_corrected':self.pvalue_corrected,
            'pvalue_corrected_description':self.pvalue_corrected_description,
            'mean':self.mean,
            'ci_lb':self.ci_lb,
            'ci_ub':self.ci_ub,
            'ci_level':self.ci_level,
            'fold_change':self.fold_change,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_pca_scores(Base):
    __tablename__ = 'data_stage02_quantification_pca_scores'
    id = Column(Integer, Sequence('data_stage02_quantification_pca_scores_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    sample_name_short = Column(String(100))
    #time_point = Column(String(10))
    score = Column(Float);
    axis = Column(Integer);
    var_proportion = Column(Float);
    var_cumulative = Column(Float);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('analysis_id','experiment_id','sample_name_short','axis','calculated_concentration_units'),
                      UniqueConstraint('analysis_id','sample_name_short','axis','calculated_concentration_units'),
            )

    def __init__(self, 
                 analysis_id_I,
                 #experiment_id_I,
                 sample_name_short_I, 
                 #time_point_I,
                 score_I, axis_I,
                 var_proportion_I, var_cumulative_I,
                 calculated_concentration_units_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        self.sample_name_short = sample_name_short_I;
        #self.time_point = time_point_I;
        self.score=score_I
        self.axis=axis_I
        self.var_proportion=var_proportion_I
        self.var_cumulative=var_cumulative_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_short':self.sample_name_short,
            'score':self.score,
            'axis':self.axis,
            'var_proportion':self.var_proportion,
            'var_cumulative':self.var_cumulative,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_pca_loadings(Base):
    __tablename__ = 'data_stage02_quantification_pca_loadings'
    id = Column(Integer, Sequence('data_stage02_quantification_pca_loadings_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    #time_point = Column(String(10))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    loadings = Column(Float);
    axis = Column(Integer)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      #UniqueConstraint('analysis_id','experiment_id','component_name','axis','calculated_concentration_units'),
                      UniqueConstraint('analysis_id','component_name','axis','calculated_concentration_units'),
            )

    def __init__(self, 
                 analysis_id_I,
                 #experiment_id_I,
                 #time_point_I,
                 component_group_name_I, component_name_I,
                 loadings_I, axis_I, calculated_concentration_units_I, 
                 used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        #self.time_point = time_point_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.loadings=loadings_I
        self.axis=axis_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'loadings':self.loadings,
            'axis':self.axis,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_dendrogram(Base):
    __tablename__ = 'data_stage02_quantification_dendrogram'
    id = Column(Integer, Sequence('data_stage02_quantification_dendrogram_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    leaves = Column(postgresql.ARRAY(Float))
    icoord = Column(postgresql.JSON)
    dcoord = Column(postgresql.JSON)
    ivl = Column(postgresql.ARRAY(String(100)))
    colors = Column(postgresql.ARRAY(String(25)))
    pdist_metric = Column(String(100))
    linkage_method = Column(String(100))
    value_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','ivl','pdist_metric','linkage_method','value_units'),
            )

    def __init__(self,analysis_id_I,
                leaves_I,
                icoord_I,
                dcoord_I,
                ivl_I,
                colors_I,
                pdist_metric_I,
                linkage_method_I,
                value_units_I,
                used__I,
                comment__I):
        self.analysis_id=analysis_id_I
        self.leaves=leaves_I
        self.icoord=icoord_I
        self.dcoord=dcoord_I
        self.ivl=ivl_I
        self.colors=colors_I
        self.pdist_metric=pdist_metric_I
        self.linkage_method=linkage_method_I
        self.value_units = value_units_I;
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
            'leaves':self.leaves,
            'icoord':self.icoord,
            'dcoord':self.dcoord,
            'ivl':self.ivl,
            'colors':self.ivl,
            'pdist_metric':self.pdist_metric,
            'linkage_method':self.linkage_method,
            'value_units':self.value_units,
            'used_':self.used_,
            'comment_':self.comment_};
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__());

class data_stage02_quantification_heatmap(Base):
    __tablename__ = 'data_stage02_quantification_heatmap'
    id = Column(Integer, Sequence('data_stage02_quantification_heatmap_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    col_index = Column(Integer)
    row_index = Column(Integer)
    value = Column(Float)
    col_leaves = Column(Integer)
    row_leaves = Column(Integer)
    col_label = Column(String(100))
    row_label = Column(String(100))
    col_pdist_metric = Column(String(100))
    row_pdist_metric = Column(String(100))
    col_linkage_method = Column(String(100))
    row_linkage_method = Column(String(100))
    value_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('experiment_id','sample_name_short','time_point','component_name'),
                      UniqueConstraint('analysis_id','col_label','row_label','col_pdist_metric','row_pdist_metric','col_linkage_method','row_linkage_method','value_units'),
            )

    def __init__(self,analysis_id_I,
                col_index_I,
                row_index_I,
                value_I,
                col_leaves_I,
                row_leaves_I,
                col_label_I,
                row_label_I,
                col_pdist_metric_I,
                row_pdist_metric_I,
                col_linkage_method_I,
                row_linkage_method_I,
                value_units_I,
                used__I,
                comment__I):
        self.analysis_id=analysis_id_I
        self.col_index=col_index_I
        self.row_index=row_index_I
        self.value=value_I
        self.col_leaves=col_leaves_I
        self.row_leaves=row_leaves_I
        self.col_label=col_label_I
        self.row_label=row_label_I
        self.col_pdist_metric=col_pdist_metric_I
        self.row_pdist_metric=row_pdist_metric_I
        self.col_linkage_method=col_linkage_method_I
        self.row_linkage_method=row_linkage_method_I
        self.value_units = value_units_I;
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self): 
        return {'id':self.id,
                'analysis_id':self.analysis_id,
            'col_index':self.col_index,
            'row_index':self.row_index,
            'value':self.value,
            'col_leaves':self.col_leaves,
            'row_leaves':self.row_leaves,
            'col_label':self.col_label,
            'row_label':self.row_label,
            'col_pdist_metric':self.col_pdist_metric,
            'row_pdist_metric':self.row_pdist_metric,
            'col_linkage_method':self.col_linkage_method,
            'row_linkage_method':self.row_linkage_method,
            'value_units':self.value_units,
            'used_':self.used_,
            'comment_':self.comment_};
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__());

class data_stage02_quantification_svm(Base):
    #TODO
    __tablename__ = 'data_stage02_quantification_svm'
    id = Column(Integer, Sequence('data_stage02_quantification_svm_id_seq'), primary_key=True)
    #analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_short = Column(String(100))
    time_point = Column(String(10))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    #...
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('experiment_id','sample_name_short','component_name'),
                      #UniqueConstraint('analysis_id','experiment_id','sample_name_short','component_name',''),
            )

    def __init__(self, 
                 #analysis_id_I,
                 experiment_id_I, sample_name_I, sample_name_abbreviation_I,
                 time_point_I, dilution_I, replicate_number_I, met_id_I, used_I, comment_I):
        #self.analysis_id = analysis_id_I;
        self.experiment_id = experiment_id_I;
        self.sample_name = sample_name_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.dilution = dilution_I;
        self.replicate_number = replicate_number_I;
        self.met_id = met_id_I;
        #...
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self): # not complete!
        return {'id':self.id,
            #"analysis_id":self.analysis_id,
            'experiment_id_I':self.experiment_id,
                'sample_name_I':self.sample_name,
                'sample_name_abbreviation_I':self.sample_name_abbreviation,
                'time_point_I':self.time_point,
                'dilution_I':self.dilution,
                'replicate_number_I':self.replicate_number,
                'met_id_I':self.met_id,
                #...
                'used_I':self.used_,
                'comments_I':self.comments_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_descriptiveStats(Base):
    __tablename__ = 'data_stage02_quantification_descriptiveStats'
    id = Column(Integer, Sequence('data_stage02_quantification_descriptiveStats_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    test_stat = Column(Float)
    test_description = Column(String(50));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    mean = Column(Float)
    var = Column(Float)
    cv = Column(Float)
    n = Column(Float)
    ci_lb = Column(Float)
    ci_ub = Column(Float)
    ci_level = Column(Float)
    min = Column(Float)
    max = Column(Float)
    median = Column(Float)
    iq_1 = Column(Float)
    iq_3 = Column(Float)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('experiment_id','sample_name_abbreviation','component_name','time_point'),
                      UniqueConstraint('analysis_id','experiment_id','sample_name_abbreviation','component_name','time_point','calculated_concentration_units'),
            )

    def __init__(self, 
                 analysis_id_I,
                 experiment_id_I, sample_name_abbreviation_I, 
                 time_point_I, component_group_name_I, component_name_I,
                 mean_I, var_I, cv_I, n_I, test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 ci_lb_I, ci_ub_I, ci_level_I,
                 min_I,max_I,median_I,iq_1_I,iq_3_I,
                 calculated_concentration_units_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.mean=mean_I;
        self.var=var_I;
        self.cv=cv_I;
        self.n=n_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.ci_lb=ci_lb_I;
        self.ci_ub=ci_ub_I;
        self.ci_level=ci_level_I;
        self.min=min_I;
        self.max=max_I;
        self.median=median_I;
        self.iq_1=iq_1_I;
        self.iq_3=iq_3_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self): 
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'component_group_name':self.component_group_name,
                'component_name':self.component_name,
                'test_stat':self.test_stat,
                'test_description':self.test_description,
                'pvalue':self.pvalue,
                'pvalue_corrected':self.pvalue_corrected,
                'pvalue_corrected_description':self.pvalue_corrected_description,
                'mean':self.mean,
                'var':self.var,
                'cv':self.cv,
                'n':self.n,
                'ci_lb':self.ci_lb,
                'ci_ub':self.ci_ub,
                'ci_level':self.ci_level,
                'min':self.min,
                'max':self.max,
                'median':self.median,
                'iq_1':self.iq_1,
                'iq_3':self.iq_3,
                'calculated_concentration_units':self.calculated_concentration_units,
                'used_':self.used_,
                'comment_':self.comment_
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_data(Base):
    __tablename__ = 'data_stage02_quantification_data'
    id = Column(Integer, Sequence('data_stage02_quantification_data_id_seq'), primary_key=True)
    experiment_id = Column(String(50), primary_key=True)
    sample_name_short = Column(String(100), primary_key=True)
    time_point = Column(String(10), primary_key=True)
    component_group_name = Column(String(100))
    component_name = Column(String(500), primary_key=True)
    calculated_concentration = Column(Float)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    def __init__(self, experiment_id_I, sample_name_short_I, time_point_I,
                 component_group_name_I, component_name_I, calculated_concentration_I,calculated_concentration_units_I,
                 used_I,comment_I):
        self.experiment_id = experiment_id_I;
        self.sample_name_short = sample_name_short_I;
        self.time_point = time_point_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.calculated_concentration = calculated_concentration_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
                "experiment_id":self.experiment_id,
                "sample_name_short":self.sample_name_short,
                "time_point":self.time_point,
                "component_group_name":self.component_group_name,
                "component_name":self.component_name,
                "calculated_concentration":self.calculated_concentration,
                "calculated_concentration_units":self.calculated_concentration_units,
                "used_":self.used_,
                'comments_I':self.comments_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_analysis(Base):
    __tablename__ = 'data_stage02_quantification_analysis'
    id = Column(Integer, Sequence('data_stage02_quantification_analysis_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_short = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    analysis_type = Column(String(100)); # time-course (i.e., multiple time points), paired (i.e., control compared to multiple replicates), group (i.e., single grouping of samples).
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('experiment_id','sample_name_short','sample_name_abbreviation','time_point','analysis_type','analysis_id'),
            )

    def __init__(self,analysis_id_I,
                 experiment_id_I,
            sample_name_short_I,
            sample_name_abbreviation_I,
            time_point_I,
            analysis_type_I,
            used__I,
            comment__I):
        self.analysis_id=analysis_id_I
        self.experiment_id=experiment_id_I
        self.sample_name_short=sample_name_short_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        self.analysis_type=analysis_type_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
            'experiment_id':self.experiment_id,
            'sample_name_short':self.sample_name_short,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'time_point':self.time_point,
            'analysis_type':self.analysis_type,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())