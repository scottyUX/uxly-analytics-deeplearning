
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
        params = StatsQueryParameters(address=address, table_name=stats_table)
        stats = self.__controller.get_wallet_stats(params)
        print(stats.to_dict())

    def __test_query_wallet_transactions(self):
        address = self.__claimers.iloc[467][ck.WALLET_ADDRESS]

        table = self.__tables[ck.AIRDROPS][ck.DEGEN][0][ck.TRANSACTIONS_TABLE]
        params = TransactionsQueryParameters(address=address, table_name=table)
        history = self.__controller.get_wallet_transaction_history(params)
        print(history.get_transaction_count())

    def __test_query_wallet_transactions_with_dates(self):
        address = self.__claimers.iloc[0][ck.WALLET_ADDRESS]
        table = self.__tables[ck.AIRDROPS][ck.DEGEN][0][ck.TRANSACTIONS_TABLE]
        params1 = TransactionsQueryParameters(
            address=address, 
            table_name=table,
            cached_first=False,
            from_date='2023-12-01T00:00:00Z',
            to_date='2024-01-09T00:00:00Z',
            )
        history = self.__controller.get_wallet_transaction_history(params1)
        print()
        print(history.get_transaction_count())
        params2 = TransactionsQueryParameters(
            address=address, 
            table_name=table,
            cached_first=False,
            from_date='2014-12-01T00:00:00Z',
            to_date='2024-01-09T00:00:00Z',
            )
        history = self.__controller.get_wallet_transaction_history(params2)
        print()
        print(history.get_transaction_count())

    def __test_query_wallet_transactions_with_contracts(self):
        address = self.__claimers.iloc[36][ck.WALLET_ADDRESS]
        table = self.__tables[ck.AIRDROPS][ck.DEGEN][0][ck.TRANSACTIONS_TABLE]
        params1 = TokenTransfersQueryParameters(
            address=address, 
            table_name=table,
            cached_first=False,
            from_date='2012-12-01T00:00:00Z',
            to_date='2024-06-01T00:00:00Z',
            )
        history = self.__controller.get_wallet_token_transfer_history(params1)
        print()
        print(history.get_transaction_count())
        params2 = TokenTransfersQueryParameters(
            address=address, 
            table_name=table,
            cached_first=False,
            from_date='2012-12-01T00:00:00Z',
            to_date='2024-06-01T00:00:00Z',
            contract_addresses=['0x9f07f8a82cb1af1466252e505b7b7ddee103bc91'],
            )
        history = self.__controller.get_wallet_token_transfer_history(params2)
        print()
        print(history.get_transaction_count())
        return

    def __test_query_wallet_token_transfers(self):
        contract_addresses=['0x4ed4e862860bed51a9570b96d89af5e1b0efefed']
        addresses = self.__claimers[ck.WALLET_ADDRESS].to_list()[:40]
        table = self.__tables[ck.AIRDROPS][ck.DEGEN][0][ck.TRANSACTIONS_TABLE]
        for address in addresses:
            params = TokenTransfersQueryParameters(
                address=address, 
                chain='base',
                table_name=table,
                cached_first=False,
                contract_addresses=contract_addresses,
                )
            history = self.__controller.get_wallet_token_transfer_history(params)
            print(history.get_transaction_count())

    def run_tests(self):
        # self.__test_query_wallet_stats()
        # self.__test_query_wallet_transactions()
        # self.__test_query_wallet_transactions_with_dates()
        # self.__test_query_wallet_transactions_with_contracts()
        self.__test_query_wallet_token_transfers()