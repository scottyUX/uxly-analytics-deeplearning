from pydantic import BaseModel
from typing import Optional

from data_handler.models.graph_models.node import Node
from data_handler.models.graph_models.graph import Graph


class GraphAnalyzer(BaseModel):
    graph: Optional[Graph] = None

    def get_hierarchy_groups(self):
        hierarchy_groups = {}
        for node in self.graph.nodes.values():
            if node.hierarchy not in hierarchy_groups:
                hierarchy_groups[node.hierarchy] = set()
                hierarchy_groups[node.hierarchy].add(node.id)
            else:
                hierarchy_groups[node.hierarchy].add(node.id)
        return dict(sorted(hierarchy_groups.items(), key=lambda x: x[0]))

    def get_hierarchy_analysis(self):
        groups = self.get_hierarchy_groups()
        counts = {g: len(groups[g]) for g in groups}
        return counts

    def analyze(self, graph: Graph):
        self.graph = graph
        return {
            'nodes': len(self.graph.nodes),
            'edges': len(self.graph.edges),
            'hierarchy_analysis': self.get_hierarchy_analysis()
        }