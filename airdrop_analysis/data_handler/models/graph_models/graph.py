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
            if (self.__nodes[node.id].edges) == node.edges:
                self.add_edges(node.incoming_edges)
                self.add_edges(node.outgoing_edges)
                return True
            return False
        self.__nodes[node.id] = node
        self.add_edges(node.incoming_edges)
        self.add_edges(node.outgoing_edges)
        return True
    
    def add_nodes(self, nodes: List[Node]):
        for node in nodes:
            self.add_node(node)

    def delete_edge(self, edge: Union[Edge, str]) -> bool:
        if isinstance(edge, str):
            edge_id = edge
        else:
            edge_id = edge.id
        if edge_id not in self.__edges:
            return False
        edge = self.__edges.pop(edge_id)
        edge.source.delete_edge(edge)
        edge.destination.delete_edge(edge)
        return True

    def delete_node(self, node: Union[Node, str]) -> bool:
        if isinstance(node, str):
            node_id = node
        else:
            node_id = node.id
        if node_id not in self.__nodes:
            return False
        node = self.__nodes.pop(node_id)
        for edge in node.incoming_edges + node.outgoing_edges:
            self.delete_edge(edge)
        return True

    def clear_children_from_rootless_parents(self):
        nodes_to_delete = []
        for node in self.__nodes.values():
            if node.hirerarchy > 0 and not node.incoming_edges:
                nodes_to_delete.append(node)
        for node in nodes_to_delete:
            self.delete_node(node)
        return

    def clear_parents_from_leaf_children(self):
        nodes_to_delete = []
        for node in self.__nodes.values():
            if node.hirerarchy < 0 and not node.outgoing_edges:
                nodes_to_delete.append(node)
        for node in nodes_to_delete:
            self.delete_node(node)
        return

    def remove_indirect_nodes(self):
        self.clear_children_from_rootless_parents()
        self.clear_parents_from_leaf_children()

    def __contains__(self, node: Union[Node, str]) -> bool:
        if isinstance(node, str):
            return node in self.__nodes
        else:
            return node.id in self.__nodes       
