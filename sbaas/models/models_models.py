from models_base import *
from sqlalchemy.orm import relationship
import datetime

class models_eschermaps(Base):
    __tablename__ = 'models_eschermaps'
    id = Column(Integer, Sequence('models_eschermaps_id_seq'), primary_key=True)
    model_id = Column(String(50))
    eschermap_id = Column(String(50))
    eschermap_json = Column(postgresql.JSON)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('model_id','eschermap_id'),
            )

    def __init__(self,model_id_I,eschermap_id_I,
            eschermap_json_I,
            used__I,
            comment__I):
        self.model_id=model_id_I
        self.eschermap_id=eschermap_id_I
        self.eschermap_json=eschermap_json_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'model_id':self.model_id,
                'eschermap_id':self.eschermap_id,
                'eschermap_json':self.eschermap_json,
                'used_':self.used_,
                'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())