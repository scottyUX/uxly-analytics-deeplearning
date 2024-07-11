import os

from data_handler.claimers_list_provider import ClaimerListProvider
from data_handler.graph_builder import GraphBuilder
from data_handler.graph_visualizer import GraphVisualizer
from data_handler.models.base_models.query_parameters import AirdropParameters
from utils.path_provider import PathProvider


class AirdropAnalyzer:
    def __init__(self):
        self.__path_provider = PathProvider()
        self.__builder = GraphBuilder(
            self.__path_provider.get_api_keys_path(),
            self.__path_provider.get_dex_addresses_path()
        )
        self.__list_provider = ClaimerListProvider()

    def get_airdrop_graph(self, param: AirdropParameters):
        param.chain = self.__list_provider.get_token_chain(param.token)
        param.contract_addresses = \
            self.__list_provider.get_token_contract_addresses(param.token)
        param.center_addresses = self.__list_provider.get_claimers_list(
                param.token, param.airdrop, param.season,
        )
        if param.claimer_limit > 0:
            param.center_addresses = \
                param.center_addresses[:param.claimer_limit]
        g = self.__builder.build_graph(param)
        g.remove_indirect_nodes()
        file_path = self.__path_provider.get_graph_html_path('test_graph')
        GraphVisualizer(g).visualize_with_pyvis(file_path)
        return g