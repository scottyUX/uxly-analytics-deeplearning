import pandas as pd
import json
import os

from data_handler.query_handlers.chain_query_controller \
    import ChainQueryController
from data_handler.query_handlers.chain_query_controller \
    import ChainQueryController
from utils.path_provider import PathProvider
from utils.custom_keys import CustomKeys as ck
from data_handler.models.base_models.query_parameters import *


class ChainQueryControllerTest():

    def __init__(self):
        paths_json_path = os.getenv(ck.PATHS_JSON_PATH)
        prefix_path = os.getenv(ck.PREFIX_PATH)
        self.__path_provider = PathProvider(paths_json_path, prefix_path)
        self.__controller = ChainQueryController(
            self.__path_provider.get_api_keys_path(),
        )
        self.__claimers = pd.read_csv(self.__path_provider[ck.CLAIMERS_PATH])
        with open(self.__path_provider.get_table_file_path(), 'r') as file:
            self.__tables = json.loads(file.read())
        print(self.__tables)

    def __test_query_wallet_token_transfers_with_contracts(self):
        address = self.__claimers.iloc[36][ck.WALLET_ADDRESS]
        prms1 = TokenTransfersQueryParameters(
            address=address, 
            chain='base',
            cached_first=False,
            from_date='2012-12-01T00:00:00Z',
            to_date='2024-06-01T00:00:00Z',
            )
        history, _ = self.__controller.get_wallet_token_transfer_history(prms1)
        print()
        print(history.get_transaction_count())
        prms2 = TokenTransfersQueryParameters(
            address=address, 
            chain='base',
            cached_first=False,
            from_date='2012-12-01T00:00:00Z',
            to_date='2024-06-01T00:00:00Z',
            contract_addresses=['0x9f07f8a82cb1af1466252e505b7b7ddee103bc91'],
            )
        history, _ = self.__controller.get_wallet_token_transfer_history(prms2)
        print()
        print(history.get_transaction_count())
        return

    def __test_query_wallet_token_transfers(self):
        contract_addresses=['0x4ed4e862860bed51a9570b96d89af5e1b0efefed']
        addresses = self.__claimers[ck.WALLET_ADDRESS].to_list()[:8]
        for address in addresses:
            params = TokenTransfersQueryParameters(
                address=address, 
                chain='base',
                cached_first=True,
                from_date='2024-01-01T00:00:00Z',
                contract_addresses=contract_addresses,
                )
            history, _ = self.__controller.get_wallet_token_transfer_history(
                params,
            )
            print(history.get_transaction_count())

    def run_tests(self):
        self.__test_query_wallet_token_transfers_with_contracts()
        self.__test_query_wallet_token_transfers()