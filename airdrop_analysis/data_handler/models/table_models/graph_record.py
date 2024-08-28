from peewee import CharField, DateTimeField, IntegerField, FloatField
import json
from datetime import datetime

from data_handler.models.table_models.base_model import BaseModel
from utils.custom_keys import CustomKeys as ck

class Graph_Record(BaseModel):
    user_id = CharField()
    time_stamp = DateTimeField()
    graph = CharField()
    
    def create_from(user_id : str , graph : dict):
        return Graph_Record.create(
            user_id = user_id,
            time_stamp = datetime.now().strftime(ck.DATETIME_FORMAT_FOR_QUERIED_TRANSFERS),
            graph = json.dumps(graph)
        )
    
    def to_dict(data):
        return {
            "user_id": data.user_id,
            "time_stamp": str(data.time_stamp),
            "graph": json.loads(data.graph)
        }