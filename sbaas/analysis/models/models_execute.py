from sbaas.analysis.analysis_base import *
from .models_query import *
from .models_io import *

class models_execute(base_analysis):
    '''class for analysis models'''
    def __init__(self, session_I=None):
        if session_I: self.session = session_I;
        else: self.session = Session();
        self.models_query = models_query(self.session);

    #analyses:
    #table initializations:
    def drop_models(self):
        try:
            models_eschermaps.__table__.drop(engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_models(self,eschermap_id_I = None):
        try:
            if eschermaps_id_I:
                reset = self.session.query(models_eschermaps).filter(models_eschermaps.eschermap_id.like(eschermap_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(models_eschermaps).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_models(self):
        try:
            models_eschermaps.__table__.create(engine,True);
        except SQLAlchemyError as e:
            print(e);
