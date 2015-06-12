from analysis.analysis_base import *
from models_query import models_query

class models_io(base_analysis):

    def __init__(self, session_I=None):
        if session_I: self.session = session_I;
        else: self.session = Session();
        self.models_query = models_query(self.session);

    def import_modelsEschermaps_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_modelsEschermaps(data.data);
        data.clear_data();

    def add_modelsEschermaps(self, data_I):
        '''add rows of models_eschermaps'''
        if data_I:
            for d in data_I:
                try:
                    data_add = models_eschermaps(
                                    d['used_'],
                                    d['comment_']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def import_modelsEschermaps_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_modelsEschermaps(data.data);
        data.clear_data();

    def update_modelsEschermaps(self,data_I):
        '''update rows of models_eschermaps'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(models_eschermaps).filter(
                            models_eschermaps.id == d['id']).update(
                            {
                            'used_':d['used_'],
                            'comment_':d['comment_']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
