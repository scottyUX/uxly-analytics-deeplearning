from typing import TYPE_CHECKING, Dict, List, Optional
from pydantic import BaseModel

if TYPE_CHECKING:
    from data_handler.models.graph_models.edge import Edge 


class Node(BaseModel):
    id: str
    hirerarchy: int
    __incoming_edges: Dict[str, 'Edge'] = {}
    __outgoing_edges: Dict[str, 'Edge'] = {}

    @property
    def incoming_edges(self):
        return list(self.__incoming_edges.values())
    
    @property
    def outgoing_edges(self):
        return list(self.__outgoing_edges.values())


    @property
    def edges(self):
        return self.incoming_edges + self.outgoing_edges

    @property
    def parents(self):
        return [e.source for e in self.incoming_edges]
    
    @property
    def children(self):
        return [e.destination for e in self.outgoing_edges]

    def add_incoming_edge(self, edge: 'Edge'):
        if edge.id in self.__incoming_edges:
            return False
        self.__incoming_edges[edge.id] = edge
        return True

    def add_outgoing_edge(self, edge: 'Edge'):
        if edge.id in self.__outgoing_edges:
            return False
        self.__outgoing_edges[edge.id] = edge
        return True

    def add_edge(self, edge: 'Edge'):
        if edge.destination == self:
            return self.add_incoming_edge(edge)
        elif edge.source == self:
            return self.add_outgoing_edge(edge)
        else:
            return False
            
    def add_edges(self, edges: List['Edge']):
        for edge in edges:
            self.add_edge(edge)

    def add_incoming_edges(self, edges: List['Edge']):
        for edge in edges:
            self.add_incoming_edge(edge)

    def add_outgoing_edges(self, edges: List['Edge']):
        for edge in edges:
            self.add_outgoing_edge(edge)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.id == other
        if isinstance(other, Node):
            return self.id == other.id
        raise ValueError(f'Cannot compare Node to {type(other)}')

    def to_dict(self):
        return self.model_dump() 