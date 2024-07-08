from pydantic import BaseModel
from typing import Dict, List, Union

from data_handler.models.graph_models.node import Node
from data_handler.models.graph_models.edge import Edge


class Graph(BaseModel):
    __nodes: Dict[str, Node] = {}
    __edges: Dict[str, Edge] = {}

    @property
    def nodes(self):
        return self.__nodes
    
    @property
    def edges(self):
        return self.__edges

    def add_edge(self, edge: Edge) -> bool:
        if edge.id in self.__edges:
            return False
        self.__edges[edge.id] = edge
        self.add_node(edge.source)
        self.add_node(edge.destination)
        return True

    def add_edges(self, edges: List[Edge]):
        for edge in edges:
            self.add_edge(edge)

    def add_node(self, node: Node) -> bool:
        if node.id in self.__nodes:
            return False
        self.__nodes[node.id] = node
        self.add_edges(node.incoming_edges)
        self.add_edges(node.outgoing_edges)
        return True
    
    def add_nodes(self, nodes: List[Node]):
        for node in nodes:
            self.add_node(node)

    def __contains__(self, node: Union[Node, str]) -> bool:
        if isinstance(node, str):
            return node in self.__nodes
        else:
            return node.id in self.__nodes       
