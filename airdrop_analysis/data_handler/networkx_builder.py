import community as community_louvain
from pyvis.network import Network
import matplotlib.pyplot as plt
import networkx as nx

from data_handler.models.graph_models.graph import Graph


class NetworkXBuilder:
    def __init__(self):
        self.__color_map = {
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

    def colorize_graph_by_partition(
            self,
            graph: Graph,
            partition: dict,
        ) -> nx.Graph:
        # Normalize partition values for color mapping
        partition_values = list(partition.values())
        max_partition = max(partition_values)
        min_partition = min(partition_values)
        norm = plt.Normalize(min_partition, max_partition)
        for node in graph.nodes:
            graph.nodes[node]['group'] = partition[node]
            graph.nodes[node]['color'] = \
                plt.cm.rainbow(norm(partition[node]))
        return graph

    def __build(self, nx_graph: nx.Graph, graph: Graph):
        for node in graph.nodes.values():
            nx_graph.add_node(
                node.label, 
                hirerarchy=node.hierarchy,
                color=self.__color_map[node.hierarchy],
            )
        for edge in graph.edges.values():
            nx_graph.add_edge(
                edge.source.label, 
                edge.destination.label, 
            )
        return nx_graph

    def get_undirected_nx_graph(self, graph: Graph) -> nx.Graph:
        return self.__build(nx.Graph(), graph)

    def get_louvain_partition_from_nx(self, graph: nx.Graph) -> dict:
        return community_louvain.best_partition(graph)

    def get_louvain_partition(self, graph: Graph) -> tuple[dict, nx.Graph]:
        nx_graph = self.get_undirected_nx_graph(graph)
        partition = self.get_louvain_partition_from_nx(nx_graph)
        return partition, nx_graph

    def get_undirected_nx_graph_with_partition(
            self, 
            graph: Graph,
            colorize: bool = True,
        ) -> nx.Graph:
        partition, nx_graph = self.get_louvain_partition(graph)
        if colorize:
            nx_graph = self.colorize_graph_by_partition(nx_graph, partition)
        return nx_graph
  
    def get_directed_nx_graph(self, graph: Graph) -> nx.Graph:
        return self.__build(nx.DiGraph(), graph)

    def visualize_with_plt(self, graph: nx.Graph):
        plt.figure(figsize=(12, 12))
        colors = [node[1]['color'] for node in graph.nodes(data=True)]
        nx.draw(
            self.G, 
            with_labels=True, 
            node_size=3000,
            node_color=colors, 
            edge_color='black', 
            arrows=True,
        )
        plt.show()

    def visualize_with_pyvis(
            self, 
            graph: nx.Graph,
            html_file_path: str, 
            show: bool = False,
        ) -> str:
        net = Network(height='1000px', width='100%', directed=True)
        net.from_nx(graph)
        print()
        if show:
            net.show(html_file_path, notebook=False)
            return ''
        return net.generate_html(html_file_path)