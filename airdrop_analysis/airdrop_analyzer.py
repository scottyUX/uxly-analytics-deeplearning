import pandas as pd

from data_handler.graph_builder import GraphBuilder
from data_handler.graph_visualizer import GraphVisualizer
from data_handler.models.base_models.query_parameters import \
    GraphQueryParameters
from utils.path_provider import PathProvider
from utils.custom_keys import CustomKeys as ck


class AirdropAnalyzer:
    def __init__(self, airdrop_data):
        self.__path_provider = PathProvider(paths_json_path, prefix_path)
        self.__builder = GraphBuilder(
            self.__path_provider.get_api_keys_path(),
            self.__path_provider.get_dex_addresses_path()
        )
        self.__claimers = pd.read_csv(self.__path_provider[ck.CLAIMERS_PATH])

        self.airdrop_data = airdrop_data
        self.stats = {
            RESULT: {},
            NFTS: {},
            NFT_COUNT: 0,
            COLLECTIONS: {},
            COLLECTION_COUNT: 0,
            TRANSACTIONS: {},
            TRANSACTION_COUNT: