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
        return {'experiment_id_I':self.experiment_id,
                'sample_name_I':self.sample_name,
                #TODO
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
    __tablename__ = 'data_stage01_resequencing_lineage'
    id = Column(Integer, Sequence('data_stage01_resequencing_lineage_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    lineage_name = Column(String(100))
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

    def __init__(self, experiment_id_I,
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
        return {'experiment_id':self.experiment_id,
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
    __tablename__ = 'data_stage01_resequencing_endpoints'
    id = Column(Integer, Sequence('data_stage01_resequencing_endpoints_id_seq'), primary_key=True)
    experiment_id = Column(String(50))
    endpoint_name = Column(String(100))
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

    def __init__(self, experiment_id_I,
                endpoint_name_I,
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
        self.endpoint_name=endpoint_name_I
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
        return {'experiment_id':self.experiment_id,
                'endpoint_name':self.endpoint_name,
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
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())