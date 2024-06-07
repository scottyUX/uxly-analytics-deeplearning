
import pandas as pd
import json

from data_handler.query_handlers.chain_query_controller \
    import ChainQueryController
from data_handler.query_handlers.chain_query_controller \
    import ChainQueryController
from utils.path_provider import PathProvider
from utils.custom_keys import CustomKeys as ck
from data_handler.models.base_models.query_parameters import *


class ChainQueryControllerTest():

    def __init__(self, paths_json_path: str, prefix_path: str):
        self.__path_provider = PathProvider(paths_json_path, prefix_path)
        self.__controller = ChainQueryController(
            self.__path_provider.get_api_keys_path(),
            self.__path_provider.get_aws_access_key_path(),
        )
        self.__claimers = pd.read_csv(self.__path_provider[ck.CLAIMERS_PATH])
        with open(self.__path_provider.get_table_file_path(), 'r') as file:
            self.__tables = json.loads(file.read())
        print(self.__tables)

    def __test_query_wallet_stats(self):
        address = self.__claimers.iloc[0][ck.WALLET_ADDRESS]
        stats_table = self.__tables[ck.AIRDROPS][ck.DEGEN][0][ck.STATS_TABLE]
        params = StatsQueryParameters(address, stats_table)
        stats = self.__controller.get_wallet_stats(params)
        print(stats.to_dict())

    def __test_query_wallet_transactions(self):
        address = self.__claimers.iloc[0][ck.WALLET_ADDRESS]

        table = self.__tables[ck.AIRDROPS][ck.DEGEN][0][ck.TRANSACTIONS_TABLE]
        params = TransactionsQueryParameters(address, table)
        history = self.__controller.get_wallet_transaction_history(params)
        print(history.to_dict())

    def __test_query_wallet(self):
        address = self.__claimers.iloc[0][ck.WALLET_ADDRESS]
        stats_table = self.__tables[ck.AIRDROPS][ck.DEGEN][0][ck.STATS_TABLE]
        t_tble = self.__tables[ck.AIRDROPS][ck.DEGEN][0][ck.TRANSACTIONS_TABLE]
        params = WalletQueryParameters(address, stats_table, t_tble)
        wallet = self.__controller.get_wallet(params)
        print(wallet.to_dict())

    def run_tests(self):
        self.__test_query_wallet_stats()
        self.__test_query_wallet_transactions()
        self.__test_query_wallet()