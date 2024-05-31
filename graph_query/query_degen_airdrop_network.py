
import pandas as pd
import random
import json

from graph_query.graph_query_handler import GraphQueryHandler
from utils.costum_keys import CustomKeys as ck

DEGEN_AIRDROP_FOLDER = 'data/datasets/degen_airdrop_claims'

def get_airdrop_addresses(name: str = 'airdrop1'):
    df = pd.read_csv(f'{DEGEN_AIRDROP_FOLDER}/csv/{name}_claims.csv') 
    df  = df[df[ck.CLAIMED] == True]
    print(f'{len(df)} Airdrop Addresses')
    return df[ck.WALLET_ADDRESS]

def save_addresses_with_stats(
        addresses: list,
        handler: GraphQueryHandler, 
        name: str = 'airdrop1',
    ):
    stats = handler.query_wallet_stats_as_df(addresses)
    path = f'{DEGEN_AIRDROP_FOLDER}/network/{name}_with_stats.csv'
    stats.to_csv(path, index=False)


def get_n_claimers(
        handler: GraphQueryHandler, 
        n = 50, 
        name: str = 'airdrop1',
        sample = True,
    ):
    claimers_name = f'{n}_claimers_from_{name}'
    addresses = get_airdrop_addresses(name)
    if sample:
        addresses = get_airdrop_addresses(name)
        claimers_n = addresses.sample(n)
        save_addresses_with_stats(claimers_n, handler, claimers_name)
        return claimers_n
    else:
        return pd.read_csv(f'{DEGEN_AIRDROP_FOLDER}/network/{claimers_name}_with_stats.csv')

def save_degree_transactions(
        handler: GraphQueryHandler, 
        addresses: list, 
        contracts: list, 
        degree: str,
    ):
    received, sent = handler.get_wallet_transactions(addresses, contracts)
    received_path = f'{DEGEN_AIRDROP_FOLDER}/network/{degree}_received.json'
    json.dump(received, open(received_path, 'w'))
    sent_path = f'{DEGEN_AIRDROP_FOLDER}/network/{degree}_sent.json'
    json.dump(sent, open(sent_path, 'w'))
    return received, sent

def read_degree_transactions(degree):
    received_path = f'{DEGEN_AIRDROP_FOLDER}/network/{degree}_received.json'
    received = json.load(open(received_path, 'r'))
    sent_path = f'{DEGEN_AIRDROP_FOLDER}/network/{degree}_sent.json'
    sent = json.load(open(sent_path, 'r'))
    return received, sent

def process_degree(
        handler: GraphQueryHandler,
        addresses: list, 
        contracts: list, 
        degree: str, 
        save = True,
    ):
    tnxs = None
    if save:
        tnxs = save_degree_transactions(handler, addresses, contracts, degree)
    else:
        tnxs = read_degree_transactions(degree)
    received, sent = tnxs
    senders = [t[ck.FROM_ADDRESS] for tnxs in received.values() for t in tnxs]
    receivers = [t[ck.TO_ADDRESS] for tnxs in sent.values() for t in tnxs]
    t = f'{len(senders)} receivers and {len(receivers)} senders for {degree}.'
    print(t)
    return senders, receivers

def process_layers(
        handler: GraphQueryHandler,
        source_addresses: list, 
        contracts: list, 
        degree: int, 
        parent = True,
        degree_limit: int = 5,
        edge_limit: int = 10,
    ):
   
    degree_name = f'degree_{degree}' 
    if degree != 0:
            degree_name += '_parent' if parent else '_child'
    degree_args = (handler, source_addresses, contracts, degree_name, True)
    senders, receivers = process_degree(*degree_args)
    random.shuffle(senders); random.shuffle(receivers)
    senders, receivers = senders[:edge_limit], receivers[:edge_limit]
    if degree >= degree_limit:
         return
    if parent:
        save_addresses_with_stats(senders, handler, degree_name)
        process_layers(handler, senders, contracts, degree + 1, parent)
    else:
        save_addresses_with_stats(receivers, handler, degree_name)
        process_layers(handler, receivers, contracts, degree + 1, parent)
    return

def main():
    n, k = 50, 10
    name = 'airdrop1'
    handler = GraphQueryHandler()
    claimers_n = get_n_claimers(handler, n, name, sample = False)
    degree_0_addresses = claimers_n['wallet_address'].values
    contracts = ['0x4ed4e862860bed51a9570b96d89af5e1b0efefed']
    # save_addresses_with_stats(degree_0_addresses, handler, 'degree_0')
    # process_layers(handler, degree_0_addresses, contracts, 0, True, 5, 10)
    process_layers(handler, degree_0_addresses, contracts, 0, False, 5, 10)

if __name__ == '__main__':
    main()