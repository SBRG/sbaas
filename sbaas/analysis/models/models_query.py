from sbaas.analysis.analysis_base import *

class models_query(base_analysis):
    # query data from models_eschermaps
    def get_rows_eschermapID_modelsEschermaps(self,eschermap_id_I):
        '''Query rows that are used from the eschermaps'''
        try:
            data = self.session.query(models_eschermaps).filter(
                    models_eschermaps.eschermaps_id.like(eschermap_id_I),
                    models_eschermaps.used_.is_(True)).order_by(
                    models_eschermaps.eschermap_id.asc()).all();
            data_O = [];
            if data: 
                for d in data:
                    data_O.append({
                        'model_id':d.model_id,
                        'eschermap_id':d.eschermap_id,
                        'eschermap_json':d.eschermap_json,
                        'used_':d.used_,
                        'comment_':d.comment_
                    });
            return  data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_modelID_modelsEschermaps(self,model_id_I):
        '''Query rows that are used from the eschermaps'''
        try:
            data = self.session.query(models_eschermaps).filter(
                    models_eschermaps.model_id.like(model_id_I),
                    models_eschermaps.used_.is_(True)).order_by(
                    models_eschermaps.eschermap_id.asc()).all();
            data_O = [];
            if data: 
                for d in data:
                    data_O.append({
                        'model_id':d.model_id,
                        'eschermap_id':d.eschermap_id,
                        'eschermap_json':d.eschermap_json,
                        'used_':d.used_,
                        'comment_':d.comment_
                    });
            return  data_O;
        except SQLAlchemyError as e:
            print(e);
