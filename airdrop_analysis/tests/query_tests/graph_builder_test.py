import pandas as pd
import os

from data_handler.graph_builder import GraphBuilder
from data_handler.graph_visualizer import GraphVisualizer
from data_handler.models.base_models.query_parameters import \
    GraphQueryParameters
from utils.path_provider import PathProvider
from utils.custom_keys import CustomKeys as ck


class GraphBuilderTest():

    def __init__(self):
        paths_json_path = os.getenv(ck.PATHS_JSON_PATH)
        prefix_path = os.getenv(ck.PREFIX_PATH)
        self.__path_provider = PathProvider(paths_json_path, prefix_path)
        self.__builder = GraphBuilder(
            self.__path_provider.get_api_keys_path(),
            self.__path_provider.get_dex_addresses_path()
        )
        self.__claimers = pd.read_csv(self.__path_provider[ck.CLAIMERS_PATH])

    def __test_building_graph_with_limit_one(self, n: int = 1):
        addresses = self.__claimers.iloc[:n][ck.WALLET_ADDRESS]
        contract_addresses = ['0x4ed4e862860bed51a9570b96d89af5e1b0efefed']
        param1 = GraphQueryParameters(
            center_addresses=addresses.to_list(),
            chain='base',
            contract_addresses=contract_addresses,
            from_date='2012-12-01T00:00:00Z',
            to_date='2024-06-01T00:00:00Z',
            parent_depth=2,
            child_depth=2,
            edge_limit=3,
            edge_order='DESC',
            )
        g = self.__builder.build_graph(param1)
        g.remove_indirect_nodes()
        file_path = self.__path_provider.get_graph_html_path('test_graph')
        GraphVisualizer(g).visualize_with_pyvis(file_path)

    def run_tests(self):
        self.__test_building_graph_with_limit_one()