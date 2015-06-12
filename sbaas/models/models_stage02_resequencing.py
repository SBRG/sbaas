# ORMs
from .models_base import *
from sqlalchemy.orm import relationship

# ORM classes
class data_stage02_resequencing_mapResequencingPhysiology(Base):
    __tablename__ = 'data_stage02_resequencing_mapResequencingPhysiology'
    id = Column(Integer, Sequence('data_stage02_resequencing_mapResequencingPhysiology_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name = Column(String(100))
    mutation_frequency = Column(Float)
    mutation_type = Column(String(3))
    mutation_position = Column(Integer)
    mutation_data = Column(postgresql.JSON)
    mutation_annotations = Column(postgresql.ARRAY(String(500)))
    mutation_genes = Column(postgresql.ARRAY(String(25)))
    mutation_locations = Column(postgresql.ARRAY(String(100)))
    mutation_links = Column(postgresql.ARRAY(String(500)))
    sample_name_abbreviation = Column(String(100))
    met_id = Column(String(100))
    rate_average = Column(Float)
    rate_var = Column(Float)
    rate_lb = Column(Float)
    rate_ub = Column(Float)
    rate_units = Column(String(50))
    used_ = Column(Boolean)
    comment_ = Column(Text)

    def __init__(self, experiment_id_I,
                sample_name_I,
                mutation_frequency_I,
                mutation_type_I,
                mutation_position_I,
                mutation_data_I,
                mutation_annotations_I,
                mutation_genes_I,
                mutation_locations_I,
                mutation_links_I,
                sample_name_abbreviation_I,
                met_id_I,
                rate_average_I,
                rate_var_I,
                rate_lb_I,
                rate_ub_I,
                rate_units_I,
                used__I,
                comment__I):
        self.experiment_id=experiment_id_I
        self.sample_name=sample_name_I
        self.mutation_frequency=mutation_frequency_I
        self.mutation_type=mutation_type_I
        self.mutation_position=mutation_position_I
        self.mutation_data=mutation_data_I
        self.mutation_annotations=mutation_annotations_I
        self.mutation_genes=mutation_genes_I
        self.mutation_locations=mutation_locations_I
        self.mutation_links=mutation_links_I
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.met_id=met_id_I
        self.rate_average = rate_average_I;
        self.rate_var = rate_var_I;
        self.rate_lb = rate_lb_I;
        self.rate_ub = rate_ub_I;
        self.rate_units = rate_units_I;
        self.used_ = used__I;
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'experiment_id':self.experiment_id,
                'sample_name':self.sample_name,
                'mutation_frequency':self.mutation_frequency,
                'mutation_type':self.mutation_type,
                'mutation_position':self.mutation_position,
                'mutation_data':self.mutation_data,
                'mutation_annotations':self.mutation_annotations,
                'mutation_genes':self.mutation_genes,
                'mutation_locations':self.mutation_locations,
                'mutation_links':self.mutation_links,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'met_id':self.met_id,
                'rate_average':self.rate_average,
                'rate_var':self.rate_var,
                'rate_lb':self.rate_lb,
                'rate_ub':self.rate_ub,
                'rate_units':self.rate_units,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
 
class data_stage02_resequencing_reduceResequencingPhysiology(Base):
    __tablename__ = 'data_stage02_resequencing_reduceResequencingPhysiology'
    id = Column(Integer, Sequence('data_stage02_resequencing_reduceResequencingPhysiology_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    group_name = Column(String(100))
    sample_names = Column(postgresql.ARRAY(String(100)))
    sample_name_abbreviations = Column(postgresql.ARRAY(String(100)))
    resequencing_reduce_id = Column(String);
    physiology_reduce_id = Column(String);
    reduce_count = Column(Integer);
    mutation_frequencies = Column(postgresql.ARRAY(Float))
    mutation_types = Column(postgresql.ARRAY(String(3)))
    mutation_positions = Column(postgresql.ARRAY(Integer))
    met_ids = Column(postgresql.ARRAY(String(100)))
    rate_averages = Column(postgresql.ARRAY(Float))
    rate_vars = Column(postgresql.ARRAY(Float))
    rate_lbs = Column(postgresql.ARRAY(Float))
    rate_ubs = Column(postgresql.ARRAY(Float))
    rate_units = Column(postgresql.ARRAY(String(50)))
    used_ = Column(Boolean)
    comment_ = Column(Text)

    __table_args__ = (
            UniqueConstraint('experiment_id','group_name','sample_names','sample_name_abbreviations','resequencing_reduce_id','physiology_reduce_id'),
            )

    def __init__(self,
                experiment_id_I,
                group_name_I,
                sample_names_I,
                sample_name_abbreviations_I,
                resequencing_reduce_id_I,
                physiology_reduce_id_I,
                reduce_count_I,
                mutation_frequencies_I,
                mutation_types_I,
                mutation_positions_I,
                met_ids_I,
                rate_averages_I,
                rate_vars_I,
                rate_lbs_I,
                rate_ubs_I,
                rate_units_I,
                used__I,
                comment__I):
        self.experiment_id=experiment_id_I
        self.group_name=group_name_I
        self.sample_names=sample_names_I
        self.sample_name_abbreviations=sample_name_abbreviations_I
        self.resequencing_reduce_id=resequencing_reduce_id_I
        self.physiology_reduce_id=physiology_reduce_id_I
        self.reduce_count=reduce_count_I
        self.mutation_frequencies=mutation_frequencies_I
        self.mutation_types=mutation_types_I
        self.mutation_positions=mutation_positions_I
        self.met_ids=met_ids_I
        self.rate_averages=rate_averages_I
        self.rate_vars=rate_vars_I
        self.rate_lbs=rate_lbs_I
        self.rate_ubs=rate_ubs_I
        self.rate_units=rate_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'experiment_id':self.experiment_id,
            'group_name':self.group_name,
            'sample_names':self.sample_names,
            'sample_name_abbreviations':self.sample_name_abbreviations,
            'resequencing_reduce_id':self.resequencing_reduce_id,
            'physiology_reduce_id':self.physiology_reduce_id,
            'reduce_count':self.reduce_count,
            'mutation_frequencies':self.mutation_frequencies,
            'mutation_types':self.mutation_types,
            'mutation_positions':self.mutation_positions,
            'met_ids':self.met_ids,
            'rate_averages':self.rate_averages,
            'rate_vars':self.rate_vars,
            'rate_lbs':self.rate_lbs,
            'rate_ubs':self.rate_ubs,
            'rate_units':self.rate_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_resequencing_analysis(Base):
    __tablename__ = 'data_stage02_resequencing_analysis'
    id = Column(Integer, Sequence('data_stage02_resequencing_analysis_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50)) # resequencing->phenomics
    sample_name = Column(String(500))
    sample_name_abbreviation = Column(String(100)) # resequencing->phenomics
    analysis_type = Column(String(100)); # time-course (i.e., multiple time points), paired (i.e., control compared to multiple replicates), group (i.e., single grouping of samples).
    reduce_criteria_1 = Column(String(500));
    reduce_criteria_2 = Column(String(500));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('experiment_id','sample_name','sample_name_abbreviation','analysis_type','analysis_id','reduce_criteria_1','reduce_criteria_2'),
            )

    def __init__(self,analysis_id_I,
                 experiment_id_I,
            sample_name_I,
            sample_name_abbreviation_I,
            analysis_type_I,
            reduce_criteria_1_I,
            reduce_criteria_2_I,
            used__I,
            comment__I):
        self.analysis_id=analysis_id_I
        self.experiment_id=experiment_id_I
        self.sample_name=sample_name_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.analysis_type=analysis_type_I
        self.reduce_criteria_1=reduce_criteria_1_I
        self.reduce_criteria_2=reduce_criteria_2_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
            'experiment_id':self.experiment_id,
            'sample_name':self.sample_name,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'analysis_type':self.analysis_type,
            'reduce_criteria_1':self.reduce_criteria_1,
            'reduce_criteria_2':self.reduce_criteria_2,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_resequencing_dendrogram(Base):
    __tablename__ = 'data_stage02_resequencing_dendrogram'
    id = Column(Integer, Sequence('data_stage02_resequencing_dendrogram_id_seq'), primary_key=True)
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

class data_stage02_resequencing_heatmap(Base):
    __tablename__ = 'data_stage02_resequencing_heatmap'
    id = Column(Integer, Sequence('data_stage02_resequencing_heatmap_id_seq'), primary_key=True)
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
 
class data_stage02_resequencing_reduce(Base):
    __tablename__ = 'data_stage02_resequencing_reduce'
    id = Column(Integer, Sequence('data_stage02_resequencing_reduce_id_seq'), primary_key=True)
    analysis_id = Column(String(100))
    sample_name_abbreviations = Column(postgresql.ARRAY(String(100)))
    reduce_id_1 = Column(String);
    reduce_id_2 = Column(String);
    reduce_count = Column(Integer);
    reduce_criteria_1 = Column(String(500));
    reduce_criteria_2 = Column(String(500));
    used_ = Column(Boolean)
    comment_ = Column(Text)

    __table_args__ = (
            UniqueConstraint('analysis_id','sample_name_abbreviations','reduce_id_1','reduce_id_2','reduce_criteria_1','reduce_criteria_2'),
            )

    def __init__(self,
                analysis_id_I,
                sample_name_abbreviations_I,
                reduce_id_1_I,
                reduce_id_2_I,
                reduce_count_I,
            reduce_criteria_1_I,
            reduce_criteria_2_I,
                used__I,
                comment__I):
        self.analysis_id=analysis_id_I
        self.sample_name_abbreviations=sample_name_abbreviations_I
        self.reduce_id_1=reduce_id_1_I
        self.reduce_id_2=reduce_id_2_I
        self.reduce_count=reduce_count_I
        self.reduce_criteria_1=reduce_criteria_1_I
        self.reduce_criteria_2=reduce_criteria_2_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_abbreviations':self.sample_name_abbreviations,
            'reduce_id_1':self.reduce_id_1,
            'reduce_id_2':self.reduce_id_2,
            'reduce_count':self.reduce_count,
            'reduce_criteria_1':self.reduce_criteria_1,
            'reduce_criteria_2':self.reduce_criteria_2,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())