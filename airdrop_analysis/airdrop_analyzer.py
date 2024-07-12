from typing import Optional

from data_handler.claimer_list_provider import ClaimerListProvider
from data_handler.graph_builder import GraphBuilder
from data_handler.graph_visualizer import GraphVisualizer
from data_handler.models.base_models.query_parameters import \
    GraphQueryParameters, ClaimersGraphParameters
from data_handler.models.graph_models.graph import Graph
from utils.path_provider import PathProvider


class AirdropAnalyzer:
    def __init__(self):
        self.__path_provider = PathProvider()
        self.__builder = GraphBuilder(
            self.__path_provider.get_api_keys_path(),
            self.__path_provider.get_dex_addresses_path()
        )
        self.__list_provider = ClaimerListProvider()

    def get_graph_html(self, g: Graph, clean: Optional[bool] = True) -> str:
        if clean:
            g.remove_indirect_nodes()
        file_path = self.__path_provider.get_graph_html_path('test_graph')
        html = GraphVisualizer(g).visualize_with_pyvis(file_path, show=False)
        return html

    def get_claimers_graph(self, param: ClaimersGraphParameters) -> str:
        param = self.__list_provider.adjust_params_for_claimer_list(param)
        g = self.__builder.build_graph(param)
        return self.get_graph_html(g)

    def get_distribution_graph(self, param: GraphQueryParameters) -> str:
        g = self.__builder.build_graph_from_distributor(param)
        return self.get_graph_html(g)
