import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network

from data_handler.models.graph_models.graph import Graph


class GraphVisualizer:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.color_map = {
            -5: 'blue',
            -4: 'green',
            -3: 'yellow',
            -2: 'orange',
            -1: 'red',
            0: 'purple',
            1: 'pink',
            2: 'brown',
            3: 'black',
            4: 'grey',
            5: 'cyan',
        }
        self.G = nx.DiGraph()
        for node in self.graph.nodes.values():
            self.G.add_node(
                node.label, 
                hirerarchy=node.hirerarchy,
                color=self.color_map[node.hirerarchy],
            )
        for edge in self.graph.edges.values():
            self.G.add_edge(
                edge.source.label, 
                edge.destination.label, 
            )

    def visualize_with_plt(self):
        plt.figure(figsize=(12, 12))
        nx.draw(
            self.G, 
            with_labels=True, 
            node_size=3000,
            node_color=[node[1]['color'] for node in  self.G.nodes(data=True)], 
            edge_color='black', 
            arrows=True,
        )
        plt.show()

    def visualize_with_pyvis(
            self, 
            html_file_path: str, 
            show: bool = False,
        ) -> str:
        net = Network(
            height='1000px', 
            width='100%', 
            directed=True, 
        )
        net.from_nx(self.G)
        print()
        if show:
            net.show(html_file_path, notebook=False)
        return net.generate_html(html_file_path)