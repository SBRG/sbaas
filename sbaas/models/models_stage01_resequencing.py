# ORMs
from models_base import *
from sqlalchemy.orm import relationship

# ORM classes
class data_stage01_resequencing_metadata(Base):
    
    __tablename__ = 'data_stage01_resequencing_metadata'
    id = Column(Integer, Sequence('data_stage01_resequencing_metadata_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name = Column(String(100), unique=True)
    genome_diff = Column(Float)
    refseq = Column(String(500))
    readseq = Column(postgresql.ARRAY(String(500)))
    author = Column(String(100))

    def __init__(self, experiment_id_I,
            sample_name_I,
            genome_diff_I,
            refseq_I,
            readseq_I,
            author_I):
        self.experiment_id=experiment_id_I
        self.sample_name=sample_name_I
        self.genome_diff=genome_diff_I
        self.refseq=refseq_I
        self.readseq=readseq_I
        self.author=author_I

    def __repr__dict__(self):
        return {'id':self.id,
                'experiment_id':self.experiment_id,
                'sample_name':self.sample_name,
                'genome_diff':self.genome_diff,
                'refseq':self.refseq,
                'readseq':self.readseq,
                'author':self.author
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
    
class data_stage01_resequencing_mutations(Base):
    
    __tablename__ = 'data_stage01_resequencing_mutations'
    id = Column(Integer, Sequence('data_stage01_resequencing_mutations_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name = Column(String(100))
    mutation_id = Column(Integer)
    parent_ids = Column(postgresql.ARRAY(Integer))
    mutation_data = Column(postgresql.JSON)

    __table_args__ = (
            UniqueConstraint('experiment_id','sample_name','mutation_id'),
            )

    def __init__(self, experiment_id_I,
                sample_name_I,
                mutation_id_I,
                parent_ids_I,
                mutation_data_I):
        self.experiment_id=experiment_id_I
        self.sample_name=sample_name_I
        self.mutation_id=mutation_id_I
        self.parent_ids=parent_ids_I
        self.mutation_data=mutation_data_I

    def __repr__dict__(self):
        return {'experiment_id_I':self.experiment_id,
                'sample_name_I':self.sample_name,
                #TODO
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage01_resequencing_evidence(Base):
    
    __tablename__ = 'data_stage01_resequencing_evidence'
    id = Column(Integer, Sequence('data_stage01_resequencing_evidence_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name = Column(String(100))
    parent_id = Column(Integer)
    evidence_data = Column(postgresql.JSON)

    __table_args__ = (
            UniqueConstraint('experiment_id','sample_name','parent_id'),
            )

    def __init__(self, experiment_id_I,
            sample_name_I,
            parent_id_I,
            evidence_data_I):
        self.experiment_id=experiment_id_I
        self.sample_name=sample_name_I
        self.parent_id=parent_id_I
        self.evidence_data=evidence_data_I

    def __repr__dict__(self):
        return {'experiment_id_I':self.experiment_id,
                'sample_name_I':self.sample_name,
                #TODO
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage01_resequencing_validation(Base):
    
    __tablename__ = 'data_stage01_resequencing_validation'
    id = Column(Integer, Sequence('data_stage01_resequencing_validation_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name = Column(String(100))
    validation_id = Column(Integer)
    validation_data = Column(postgresql.JSON)

    __table_args__ = (
            UniqueConstraint('experiment_id','sample_name','validation_id'),
            )

    def __init__(self, experiment_id_I,
            sample_name_I,
            validation_id_I,
            validation_data_I):
        self.experiment_id=experiment_id_I
        self.sample_name=sample_name_I
        self.validation_id=validation_id_I
        self.validation_data=validation_data_I

    def __repr__dict__(self):
        return {'experiment_id_I':self.experiment_id,
                'sample_name_I':self.sample_name,
                #TODO
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
    
class data_stage01_resequencing_mutationsFiltered(Base):
    
    __tablename__ = 'data_stage01_resequencing_mutationsFiltered'
    id = Column(Integer, Sequence('data_stage01_resequencing_mutationsFiltered_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    sample_name = Column(String(100))
    mutation_id = Column(Integer)
    parent_ids = Column(postgresql.ARRAY(Integer))
    mutation_data = Column(postgresql.JSON)

    __table_args__ = (
            UniqueConstraint('experiment_id','sample_name','mutation_id'),
            )

    def __init__(self, experiment_id_I,
                sample_name_I,
                mutation_id_I,
                parent_ids_I,
                mutation_data_I):
        self.experiment_id=experiment_id_I
        self.sample_name=sample_name_I
        self.mutation_id=mutation_id_I
        self.parent_ids=parent_ids_I
        self.mutation_data=mutation_data_I

    def __repr__dict__(self):
        return {'experiment_id_I':self.experiment_id,
                'sample_name_I':self.sample_name,
                #TODO
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
    
class data_stage01_resequencing_lineage(Base):
    #TODO: rename to _timecourse
    __tablename__ = 'data_stage01_resequencing_lineage'
    id = Column(Integer, Sequence('data_stage01_resequencing_lineage_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    lineage_name = Column(String(500)) #lineage_name
    sample_name = Column(String(100))
    intermediate = Column(Integer)
    mutation_frequency = Column(Float)
    mutation_type = Column(String(3))
    mutation_position = Column(Integer)
    mutation_data = Column(postgresql.JSON)
    mutation_annotations = Column(postgresql.ARRAY(String(500)))
    mutation_genes = Column(postgresql.ARRAY(String(25)))
    mutation_locations = Column(postgresql.ARRAY(String(100)))
    mutation_links = Column(postgresql.ARRAY(String(500)))
    comment_ = Column(Text)

    __table_args__ = (UniqueConstraint('lineage_name','experiment_id','sample_name','intermediate'),
            )

    def __init__(self, 
                experiment_id_I,
                lineage_name_I,
                sample_name_I,
                intermediate_I,
                mutation_frequency_I,
                mutation_type_I,
                mutation_position_I,
                mutation_data_I,
                mutation_annotations_I,
                mutation_genes_I,
                mutation_locations_I,
                mutation_links_I,
                comment__I):
        self.experiment_id=experiment_id_I
        self.lineage_name=lineage_name_I
        self.sample_name=sample_name_I
        self.intermediate=intermediate_I
        self.mutation_frequency=mutation_frequency_I
        self.mutation_type=mutation_type_I
        self.mutation_position=mutation_position_I
        self.mutation_data=mutation_data_I
        self.mutation_annotations=mutation_annotations_I
        self.mutation_genes=mutation_genes_I
        self.mutation_locations=mutation_locations_I
        self.mutation_links=mutation_links_I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'experiment_id':self.experiment_id,
                'lineage_name':self.lineage_name,
                'sample_name':self.sample_name,
                'intermediate':self.intermediate,
                'mutation_frequency':self.mutation_frequency,
                'mutation_type':self.mutation_type,
                'mutation_position':self.mutation_position,
                'mutation_data':self.mutation_data,
                'mutation_annotations':self.mutation_annotations,
                'mutation_genes':self.mutation_genes,
                'mutation_locations':self.mutation_locations,
                'mutation_links':self.mutation_links,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
    
class data_stage01_resequencing_endpoints(Base):
    #TODO: rename to _group
    __tablename__ = 'data_stage01_resequencing_endpoints'
    id = Column(Integer, Sequence('data_stage01_resequencing_endpoints_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    analysis_id = Column(String(500))
    sample_name = Column(String(100))
    mutation_frequency = Column(Float)
    mutation_type = Column(String(3))
    mutation_position = Column(Integer)
    mutation_data = Column(postgresql.JSON)
    isUnique = Column(Boolean)
    mutation_annotations = Column(postgresql.ARRAY(String(500)))
    mutation_genes = Column(postgresql.ARRAY(String(25)))
    mutation_locations = Column(postgresql.ARRAY(String(100)))
    mutation_links = Column(postgresql.ARRAY(String(500)))
    comment_ = Column(Text)

    __table_args__ = (UniqueConstraint('analysis_id','experiment_id','sample_name'),
            )

    def __init__(self, experiment_id_I,
                analysis_id_I,
                sample_name_I,
                mutation_frequency_I,
                mutation_type_I,
                mutation_position_I,
                mutation_data_I,
                isUnique_I,
                mutation_annotations_I,
                mutation_genes_I,
                mutation_locations_I,
                mutation_links_I,
                comment__I):
        self.experiment_id=experiment_id_I
        self.analysis_id=analysis_id_I
        self.sample_name=sample_name_I
        self.mutation_frequency=mutation_frequency_I
        self.mutation_type=mutation_type_I
        self.mutation_position=mutation_position_I
        self.mutation_data=mutation_data_I
        self.isUnique=isUnique_I
        self.mutation_annotations=mutation_annotations_I
        self.mutation_genes=mutation_genes_I
        self.mutation_locations=mutation_locations_I
        self.mutation_links=mutation_links_I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'experiment_id':self.experiment_id,
                'analysis_id':self.analysis_id,
                'sample_name':self.sample_name,
                'mutation_frequency':self.mutation_frequency,
                'mutation_type':self.mutation_type,
                'mutation_position':self.mutation_position,
                'mutation_data':self.mutation_data,
                'isUnique':self.isUnique,
                'mutation_annotations':self.mutation_annotations,
                'mutation_genes':self.mutation_genes,
                'mutation_locations':self.mutation_locations,
                'mutation_links':self.mutation_links,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage01_resequencing_mutationsAnnotated(Base):
    __tablename__ = 'data_stage01_resequencing_mutationsAnnotated'
    id = Column(Integer, Sequence('data_stage01_resequencing_mutationsAnnotated_id_seq'), primary_key=True)
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
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage01_resequencing_analysis(Base):
    __tablename__ = 'data_stage01_resequencing_analysis'
    id = Column(Integer, Sequence('data_stage01_resequencing_analysis_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    lineage_name = Column(String(500)) # equivalent to sample_name_abbreviation
    sample_name = Column(String(500)) # equivalent to sample_name_abbreviation
    time_point = Column(String(10)) # converted to intermediate in lineage analysis
    analysis_type = Column(String(100)); # time-course (i.e., multiple time points), paired (i.e., control compared to multiple replicates), group (i.e., single grouping of samples).
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('experiment_id','lineage_name','sample_name','time_point','analysis_type','analysis_id'),
            )

    def __init__(self,analysis_id_I,
                 experiment_id_I,
            lineage_name_I,
            sample_name_I,
            time_point_I,
            analysis_type_I,
            used__I,
            comment__I):
        self.analysis_id=analysis_id_I
        self.experiment_id=experiment_id_I
        self.lineage_name=lineage_name_I
        self.sample_name=sample_name_I
        self.time_point=time_point_I
        self.analysis_type=analysis_type_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
            'experiment_id':self.experiment_id,
            'lineage_name':self.lineage_name,
            'sample_name':self.sample_name,
            'time_point':self.time_point,
            'analysis_type':self.analysis_type,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage01_resequencing_dendrogram(Base):
    __tablename__ = 'data_stage01_resequencing_dendrogram'
    id = Column(Integer, Sequence('data_stage01_resequencing_dendrogram_id_seq'), primary_key=True)
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

class data_stage01_resequencing_heatmap(Base):
    __tablename__ = 'data_stage01_resequencing_heatmap'
    id = Column(Integer, Sequence('data_stage01_resequencing_heatmap_id_seq'), primary_key=True)
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