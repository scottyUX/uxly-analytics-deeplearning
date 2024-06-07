from moralis import evm_api
import pandas as pd  
import json
from utils.costum_keys import CustomKeys as ck

class GraphQueryHandler:
    def __init__(self, path_prefix = ''):
        self.__path_prefix = path_prefix
        self.__api_keys =  self.__read_api_key()

    def __read_api_key(self):
        with open(self.__path_prefix + 'data/api_keys.json', 'r') as file:
            self.__api_keys = json.loads(file.read())
        return self.__api_keys
    
    def query_wallet_transactions(
            self, 
            address: str, 
            contract_addresses: list, 
            from_date: str = '',
            to_date: str = '',
            chain: str = 'eth',
            order: str = 'DESC',
        ):
        params = { 
            ck.CHAIN: chain, 
            ck.ORDER: order, 
            ck.ADDRESS: address,
            ck.CONTRACT_ADDRESSES: contract_addresses,
        }
        if from_date != '':
            params[ck.FROM_DATE] = from_date
        if to_date != '':
            params[ck.TO_DATE] = to_date
        transactions = []
        try:
            while ck.CURSOR not in params or params[ck.CURSOR]:
                page = evm_api.transaction.get_wallet_transactions(
                    api_key=self.__api_keys[ck.MORALIS], 
                    params=params,
                )
                transactions.extend(page[ck.RESULT])
                params[ck.CURSOR] = page[ck.CURSOR]
                s = f'Queryied {len(transactions)} transactions for {address}.'
                s += f' Querying next page...'
                print(s, end='\r')
        except Exception as e:
            if 'Reason: Internal Server Error' in str(e):
                print(f'Internal Server Error querying tnxs for {address}')
            else:
                print(e)
        return transactions

    def get_wallet_stats(
            self, 
            address: str, 
            chain: str = "eth", 
            from_date: str = '', 
            to_date: str = '',
            ):
        params = { ck.CHAIN: chain, ck.ADDRESS: address}
        if from_date != '':
            params[ck.FROM_DATE] = from_date
        if to_date != '':
            params[ck.TO_DATE] = to_date
        try:
            result = evm_api.wallets.get_wallet_stats(
                api_key = self.__api_keys[ck.MORALIS],
                params = params
            )
            return result
        except Exception as e:
            print(e)
            return {ck.TRANSACTIONS: {ck.TOTAL: 99999999991212}}

    def query_wallet_stats_as_df(self, addresses: list,
        from_date: str = '',
        to_date: str = '',
        ):
        stats = []
        i = 0
        for address in addresses:
            i += 1
            print(f'Querying stats for {i}/{len(addresses)} adresses',end='\r')
            try:
                r = self.get_wallet_stats(address, from_date=from_date, to_date=to_date)
                rd = {
                    ck.ADDRESS: address,
                    ck.NFTS: int(r[ck.NFTS]), 
                    ck.COLLECTIONS: int(r[ck.COLLECTIONS]),
                    ck.TRANSACTIONS: int(r[ck.TRANSACTIONS][ck.TOTAL]),
                    ck.NFT_TRANSFERS: int(r[ck.NFT_TRANSFERS][ck.TOTAL]),
                    ck.TOKEN_TRANSFERS: int(r[ck.TOKEN_TRANSFERS][ck.TOTAL]),
                }
                stats.append(rd)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e)
                print(f'Error querying stats for {address}')
        return pd.DataFrame(stats)

    def get_wallet_transactions(
            self,
            addresses: list, 
            contract_addresses: list,
            from_date: str = '',
            to_date: str = '',
        ):
        received_transactions = {}
        sent_transactions = {}
        i = 0
        for address in addresses:
            i += 1
            stats = self.get_wallet_stats(
                address, from_date=from_date, to_date=to_date,
            )
            if int(stats[ck.TRANSACTIONS][ck.TOTAL]) > 50000:
                print(f'Skipping {address} because of too many transactions')
                continue
            print(f'Querying tnx for {i}/{len(addresses)} adresses')
            tnxs = self.query_wallet_transactions(
                address, 
                contract_addresses,
                from_date,
                to_date,
            )
            for tnx in tnxs:
                if tnx['to_address'] == address:
                    if address not in received_transactions:
                        received_transactions[address] = []
                    received_transactions[address].append(tnx)
                if tnx['from_address'] == address:
                    if address not in sent_transactions:
                        sent_transactions[address] = []
                    sent_transactions[address].append(tnx)
        return received_transactions, sent_transactions
