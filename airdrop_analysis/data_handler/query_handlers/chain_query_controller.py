

from data_handler.query_handlers.moralis_query_handler \
    import MoralisQueryHandler
from data_handler.models.base_models.moralis_query_parameters \
    import MoralisTransactionsQueryParameters
from data_handler.models.base_models.moralis_query_parameters \
    import MoralisStatsQueryParameters
from data_handler.models.base_models.wallet import WalletStats
from data_handler.models.base_models.transaction_history \
    import TransactionHistory
from data_handler.models.base_models.transaction import Transaction

class ChainQueryController():
    def __init__(self, api_keys_path):
        self.__moralis_handler = MoralisQueryHandler(api_keys_path)

    def get_wallet_stats(
            self,
            params: MoralisStatsQueryParameters,
        ) -> WalletStats:
        states_response = self.__moralis_handler.query_wallet_stats(params)
        return WalletStats.from_moralis_response(
            params.address,
            params.chain,
            states_response,
        )

    def get_wallet_transaction_history(
            self,
            params: MoralisTransactionsQueryParameters,
        ) -> TransactionHistory:
        tnxs, cursor = self.__moralis_handler.query_wallet_transactions(params)
        tnxs = [Transaction.from_moralis_response(tx) for tx in tnxs]
        return TransactionHistory(
            params.address,
            params.chain,
            tnxs,
            params.from_date,
            params.to_date,
            params.contract_addresses,
            cursor,
        )
        