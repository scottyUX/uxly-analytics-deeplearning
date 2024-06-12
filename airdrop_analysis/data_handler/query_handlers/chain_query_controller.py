

from data_handler.query_handlers.moralis_query_handler \
    import MoralisQueryHandler
from data_handler.query_handlers.dynomodb_query_handler \
    import DynamoDBQueryHandler
from data_handler.models.base_models.query_parameters import *
from data_handler.models.base_models.wallet import Wallet
from data_handler.models.base_models.wallet import WalletStats
from data_handler.models.base_models.transaction_history \
    import TransactionHistory


class ChainQueryController():
    def __init__(self, api_keys_path: str, access_key_path: str):
        self.__moralis_handler = MoralisQueryHandler(api_keys_path)
        self.__dynamodb_handler = DynamoDBQueryHandler(access_key_path)

    def get_wallet_stats(self, params: StatsQueryParameters) -> WalletStats:
        stats = None
        if params.cached_first:
            stats = self.__dynamodb_handler.get_wallet_stats(params)
        if stats is not None:
            return stats
        response = self.__moralis_handler.query_wallet_stats(params)
        stats = WalletStats.from_moralis_dict(
            params.address, params.chain, response,
        )
        self.__dynamodb_handler.put_wallet_stats(params.table_name, stats)
        return stats

    def get_wallet_transaction_history(
            self,
            params: TransactionsQueryParameters,
        ) -> TransactionHistory:
        history = None
        if params.cached_first:
            history = self.__dynamodb_handler.get_wallet_transactions(params)
        if history is not None:
            return history
        tnxs, cursor = self.__moralis_handler.query_wallet_transactions(params)
        d = params.to_dict()
        d[ck.TRANSACTIONS] = tnxs 
        d[ck.CURSOR] = cursor
        history = TransactionHistory.from_dict(d)
        self.__dynamodb_handler.put_wallet_transactions(
            params.table_name, 
            history,
        )
        return history

    def get_wallet(self, params: WalletQueryParameters) -> Wallet:
        stats = self.get_wallet_stats(params.to_stats_query())
        history = self.get_wallet_transaction_history(params)
        return Wallet(stats, history)
