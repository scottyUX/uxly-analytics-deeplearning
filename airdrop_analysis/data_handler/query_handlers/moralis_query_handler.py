import json
import moralis

from data_handler.models.base_models.query_parameters \
    import TransactionsQueryParameters
from data_handler.models.base_models.query_parameters \
    import StatsQueryParameters
from utils.custom_keys import CustomKeys as ck


class MoralisQueryHandler(object):
    def __init__(self, api_keys_path):
        self.__api_key =  self.__read_api_key(api_keys_path)

    def __read_api_key(self, api_keys_path):
        with open(api_keys_path, 'r') as file:
            self.__api_key = json.loads(file.read())
        return self.__api_key[ck.MORALIS]

    def __query_wallet_transactions_page(
            self, 
            params: TransactionsQueryParameters,
        ):
        page = moralis.evm_api.transaction.get_wallet_transactions(
            api_key=self.__api_key, 
            params=params.to_dict(),
        )
        return page[ck.RESULT], page[ck.CURSOR]
    
    def query_wallet_transactions(
            self, 
            params: TransactionsQueryParameters,
        ):
        address = params.address
        transactions = []
        try:
            while params.cursor is not None:
                tnxs, cursor = self.__query_wallet_transactions_page(params)
                transactions.extend(tnxs)
                params.cursor = cursor
                cnt = len(transactions)
                s = f'Queryied {cnt} transactions for {address}.'
                if params.cursor is not None:
                    s += f' Querying next page...'
                else:
                    s += ' Done.' + ' ' * 25
                print(s, end='\r')
        except Exception as e:
            if 'Reason: Internal Server Error' in str(e):
                print(f'Internal Server Error querying tnxs for {address}')
            else:
                print(e)
        return transactions, params.cursor
    
    def query_wallet_stats(
            self, 
            params: StatsQueryParameters,
            ):
        try:
            return moralis.evm_api.wallets.get_wallet_stats(
                api_key=self.__api_key, 
                params=params.to_dict(),
            )
        except Exception as e:
            print(e)
            print(f'Error getting stats for {params.address}')
            return {}