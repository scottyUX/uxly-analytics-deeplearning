from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data_handler.models.graph_models.node import Node


class Edge(BaseModel):
    source: 'Node'
    destination: 'Node'
    edge_type: str
    edge_value: float
    edge_timestamp: str

    @property
    def id(self):
        return f'{self.source.id} -> {self.destination.id}'

    def to_dict(self):
        return self.model_dump()