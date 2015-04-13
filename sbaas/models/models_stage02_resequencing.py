# ORMs
from models_base import *
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
        return {'experiment_id':self.experiment_id,
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
        return {'experiment_id':self.experiment_id,
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
    #map_reduce_criteria = Column(postgresql.JSON); #todo: add?
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('experiment_id','sample_name','sample_name_abbreviation','analysis_type','analysis_id'),
            )

    def __init__(self,analysis_id_I,
                 experiment_id_I,
            sample_name_I,
            sample_name_abbreviation_I,
            analysis_type_I,
            used__I,
            comment__I):
        self.analysis_id=analysis_id_I
        self.experiment_id=experiment_id_I
        self.sample_name=sample_name_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.analysis_type=analysis_type_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'analysis_id':self.analysis_id,
            'experiment_id':self.experiment_id,
            'sample_name':self.sample_name,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'analysis_type':self.analysis_type,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())