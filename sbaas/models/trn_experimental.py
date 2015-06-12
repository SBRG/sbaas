#trnlib/orm/experimental.py

"""Module to implement ORM for the experimental portion of the OME database"""

from trnlib.orm.base import *

from sqlalchemy.orm import relationship
from sqlalchemy import Table, MetaData, create_engine, Column, Integer, \
    String, Float, ForeignKey, select
from sqlalchemy.ext.hybrid import hybrid_property

import simplejson as json


class ExpandedEnvironments:
    """
    Make carbon_source, nitrogen_source etc. queryable if the object
    is related to a condition
    """
    @hybrid_property
    def carbon_source(self):
        return self.environment.carbon_source
    @carbon_source.expression
    def carbon_source(cls):
        return select([Environment.carbon_source]).\
            where(Environment.id == cls.environment_id).label("carbon_source")
    @hybrid_property
    def nitrogen_source(self):
        return self.environment.nitrogen_source
    @nitrogen_source.expression
    def nitrogen_source(cls):
        return select([Environment.nitrogen_source]).\
            where(Environment.id == cls.environment_id).label("nitrogen_source")
    @hybrid_property
    def eacceptor(self):
        return self.environment.eacceptor
    @eacceptor.expression
    def eacceptor(cls):
        return select([Environment.eacceptor]).\
            where(Environment.id == cls.environment_id).label("eacceptor")


class Strain(Base):
    __table__ = make_table("strains")
    ##knockouts = relationship("Gene", secondary=_knockouts)
    ##tags = relationship("Gene", secondary=GeneTag.__table__)
    def __repr__(self):
        return "Strain: %s" % (self.name)
    
    def __repr__dict__(self):
        return {"name":self.name,"wid":self.id,"values":{}}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

         
class Dataset(Base):
    __table__ = make_table('datasets')
    #citations = _create_citation_relation(__table__)
    def __repr__(self):
        return "Dataset %s (#%d)" % (self.name, self.id)
    
    def __repr__dict__(self):
        return {"name":self.name,"wid":self.id,"values":{"lab":self.lab,"institution":self.institution}}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())


class EnvironmentTypes(Base):
    __table__ = make_table("environment_types")
    def __repr__(self):
        return "EnvironmentType (#%d):  %s" % \
            (self.id, self.name)


class Environment(Base):
    __table__ = make_table("environments")
    environment_type = relationship(EnvironmentTypes)
    
    __mapper_args__ = {
        'polymorphic_identity': 'environments',
        'polymorphic_on': __table__.c.env_type_id}
    
    def __repr__(self):
        return "Environment: type:%s, name:%s" % \
            (self.environment_type.name, self.name)
    
    def __repr__dict__(self):
        return {"name":self.name,"wid":self.id, "type":self.environment_type.name, "values":{}}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())    

    
class InSilicoEnvironment(Environment):
    __table__ = make_table("in_silico_environments")
    
    __mapper_args__ = { 'polymorphic_identity': 2 }
    
    def __repr__dict(self):
        environment = Environment.__repr__dict__(self)
        environment['values'] = {}
        return environment

        
class InVivoEnvironment(Environment):
    __table__ = make_table("in_vivo_environments")
    
    __mapper_args__ = { 'polymorphic_identity': 1 }    
    
    def __repr__(self):
        return "Environment: C:%s, N:%s, e:%s" % \
            (self.carbon_source, self.nitrogen_source, self.electron_acceptor)
                
    def __repr__dict__(self):
        environment = Environment.__repr__dict__(self)
        environment['values'] = {"carbon_source":self.carbon_source,\
                                 "nitrogen_source":self.nitrogen_source,\
                                 "electron_acceptor":self.electron_acceptor,
                                 "temperature":self.temperature}
        return environment


class Protocol(Base):
    __table__ = make_table("protocols")
    def __repr__(self):
        return "Protocol (#%d, %s):  %s" % \
            (self.id, self.name, self.location)


class ExperimentTypes(Base):
    __table__ = make_table("experiment_types")
    def __repr__(self):
        return "ExperimentType (#%d):  %s" % \
            (self.id, self.name)
              

class Experiments(Base):
    __table__ = make_table("experiments")
    strain = relationship(Strain)
    dataset = relationship(Dataset)
    environment = relationship(Environment)
    experiment_type = relationship(ExperimentTypes)
    
    __mapper_args__ = {
        'polymorphic_identity': 'experiments',
        'polymorphic_on': __table__.c.exp_type_id}
    
    def __repr__(self):
        return "ExperimentSet (#%d):  %s" % \
            (self.id, self.dataset)
    
    def __repr__dict__(self):
        experiment = {"name":self.name,"id":self.id, "type":self.experiment_type.name, "values":{}}
        
        experiment['values']['strain'] = self.strain.__repr__dict__()
        experiment['values']['dataset'] = self.dataset.__repr__dict__()
        experiment['values']['environment'] = self.environment.__repr__dict__()
        
        return experiment
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())


class ArrayExperiments(Experiments):
    __table__ = make_table("array_experiments")
    
    __mapper_args__ = { 'polymorphic_identity': 1 }
    
    def __repr__(self):
        return "ArrayExperiment (#%d, %s):  %s  %s" % \
            (self.id, self.name, self.platform, self.replicate)
    
    def __repr__dict__(self):
        experiment = Experiments.__repr__dict__(self)
                                         
        experiment['values']['platform'] = {"name":self.platform,"values":{}}
        experiment['values']['replicate'] = {"name":self.replicate,"values":{}}
                                                            
        return experiment
    

class RNASeqExperiment(Experiments):
    __table__ = make_table("rna_seq_experiments")
    
    __mapper_args__ = { 'polymorphic_identity': 2 }
    
    def __repr__(self):
        return "RNASeqExperiment (#%d, %s):  %s" % \
            (self.id, self.name, self.replicate)

    def __repr__dict__(self):
        experiment = Experiments.__repr__dict__(self)
                                         
        experiment['values']['sequencing_type'] = {"name":self.sequencing_type,"values":{}}
        experiment['values']['machine_id'] = {"name":self.machine_id,"values":{}}
        experiment['values']['replicate'] = {"name":self.replicate,"values":{}}               
        
        return experiment
    
    
class ChIPExperiment(Experiments):
    __table__ = make_table("chip_experiments")
    
    __mapper_args__ = { 'polymorphic_identity': 3 }
    
    def __repr__(self):
        return "ChIPExperiment (#%d, %s): %s %s %s" % \
            (self.id, self.name, self.protocol_type, self.target, self.replicate)

    def __repr__dict__(self):
        experiment = Experiments.__repr__dict__(self)
                                         
        experiment['values']['antibody'] = {"name":self.antibody,"values":{}}
        experiment['values']['protocol_type'] = {"name":self.protocol_type,"values":{}}
        experiment['values']['target'] = {"name":self.target,"values":{}} 
        experiment['values']['replicate'] = {"name":self.replicate,"values":{}}               
        
        return experiment
    

def _load_data(collection,data):    
    collection.insert(data)
    
    
def load_genome_data(file_path,experiment_id):
    genome_data = bigg_data.genome_data
    if file_path[-3:] == 'gff':
        entries = []
        for cntr,line in enumerate(open(file_path,'r').readlines()):
            if line[0] == '#': continue
            data = line.rstrip('\n').split('\t')
            
            entries.append({
                "leftpos": int(data[3]),
                "rightpos": int(data[4]),
                "value": float(data[5]),
                "strand": data[6],
                "experiment_id": experiment_id})
            
            if cntr%10000 == 0:
                genome_data.insert(entries)
                entries = []
            
   
def query_genome_data(experiment_ids,leftpos,rightpos,strand,value=0):
    genome_data = bigg_data.genome_data
    return genome_data.find({"$and": 
                            [{"leftpos" : {"$gte": leftpos}}, 
                             {"rightpos": {"$lte": rightpos}}, 
                             {"strand": {"$in" : strand }},
                             {"experiment_id": {"$in" : experiment_ids}}
                         ]})
    
    
def query_reaction_data():
    return
    
def query_metabolite_data():
    return
            
if __name__ == "__main__":
    print('word')
    session = Session()    