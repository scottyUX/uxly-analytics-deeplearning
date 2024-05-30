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
    
    def query_wallet_transactions(self, address, contract_addresses, chain = 'eth', order = 'DESC'):
        params = { 'chain': chain, 'order': order,  'address': address, 'contract_addresses': contract_addresses }
        transactions = []
        while ck.CURSOR not in params or params[ck.CURSOR]:
            page = evm_api.transaction.get_wallet_transactions(
                api_key=self.__api_keys[ck.MORALIS], 
                params=params,
            )
            transactions.extend(page[ck.RESULT])
            params[ck.CURSOR] = page[ck.CURSOR]
            break
        return transactions
        
    
    def query_token_transactions(self, address, contract_addresses, chain = 'eth', order = 'DESC'):
        params = { 'chain': chain, 'order': order,  'address': address, 'contract_addresses': contract_addresses }
        transactions = []
        while ck.CURSOR not in params or params[ck.CURSOR]:
            page = evm_api.token.get_token_transfers(
                api_key=self.__api_keys[ck.MORALIS], 
                params=params,
            )
            transactions.extend(page[ck.RESULT])
            params[ck.CURSOR] = page[ck.CURSOR]
            break
        return transactions
    
    def get_wallet_stats(self, address, chain = "eth"):
        params = { 'chain': chain, 'address': address}
        result = evm_api.wallets.get_wallet_stats(
            api_key = self.__api_keys[ck.MORALIS],
            params = params
        )
        return result

    def query_wallet_stats_as_df(self, addresses):
        stats = []
        i = 0
        for address in addresses:
            i += 1
            print(f'Querying stats for {i}/{len(addresses)} adresses', end='\r')
            try:
                r = self.get_wallet_stats(address)
                rd = {
                'nfts': int(r['nfts']), 
                'collections': int(r['collections']),
                    'transactions': int(r['transactions']['total']),
                    'nft_transfers': int(r['nft_transfers']['total']),
                    'token_transfers': int(r['token_transfers']['total']),
                }
                stats.append(rd)
            except:
                print(f'Error querying stats for {address}')
        return pd.DataFrame(stats)

    def get_wallet_transactions(self, addresses, contract_addresses):
        received_transactions = {}
        sent_transactions = {}
        i = 0
        for address in addresses:
            i += 1
            print(f'Querying tnx for {i}/{len(addresses)} adresses', end='\r')
            tnxs = self.query_wallet_transactions(address, contract_addresses)
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

    def get_token_transactions(self, addresses, contract_addresses):
        received_transactions = {}
        sent_transactions = {}
        i = 0
        for address in addresses:
            i += 1
            print(f'Querying tnx for {i}/{len(addresses)} adresses', end='\r')
            tnxs = self.query_token_transactions(address, contract_addresses)
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
    