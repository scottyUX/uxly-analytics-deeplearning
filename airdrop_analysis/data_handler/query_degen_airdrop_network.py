from datetime import datetime
import pandas as pd
import random
import json
import os

from airdrop_analysis.data_handler.graph_query_handler import GraphQueryHandler
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
        from_date: str = '',
        to_date: str = '',
    ):
    path = f'{DEGEN_AIRDROP_FOLDER}/network/{name}_with_stats.csv'
    if os.path.exists(path):
        return pd.read_csv(path)
    bt = datetime.now().isoformat()
    print(f'{bt}: Querying stats for {len(addresses)}.')
    stats = handler.query_wallet_stats_as_df(addresses, from_date, to_date)
    stats.to_csv(path, index=False)
    et = datetime.now().isoformat()
    print(f'{et}: Queried stats for {len(addresses)}.')
    return stats

def get_n_claimers(
        handler: GraphQueryHandler, 
        n = 50, 
        name: str = 'airdrop1',
        sample = True,
        from_date: str = '',
        to_date: str = '',
    ):
    claimers_name = f'{n}_claimers_from_{name}'
    addresses = get_airdrop_addresses(name)
    if sample:
        addresses = get_airdrop_addresses(name)
        claimers_n = addresses.sample(n)
        save_addresses_with_stats(claimers_n, handler, claimers_name, from_date, to_date)
        return claimers_n
    else:
        p = f'{DEGEN_AIRDROP_FOLDER}/network/{claimers_name}_with_stats.csv'
        return pd.read_csv(p)

def read_degree_transactions(degree):
    received_path = f'{DEGEN_AIRDROP_FOLDER}/network/{degree}_received.json'
    received = json.load(open(received_path, 'r'))
    sent_path = f'{DEGEN_AIRDROP_FOLDER}/network/{degree}_sent.json'
    sent = json.load(open(sent_path, 'r'))
    return received, sent

def save_degree_transactions(
        handler: GraphQueryHandler, 
        addresses: list, 
        contracts: list, 
        degree: str,
        from_date: str = '',
        to_date: str = '',
    ):
    received_path = f'{DEGEN_AIRDROP_FOLDER}/network/{degree}_received.json'
    sent_path = f'{DEGEN_AIRDROP_FOLDER}/network/{degree}_sent.json'
    if os.path.exists(received_path) and os.path.exists(sent_path):
        return read_degree_transactions(degree)
    received, sent = handler.get_wallet_transactions(
        addresses, contracts, from_date, to_date,
    )
    json.dump(received, open(received_path, 'w'))
    json.dump(sent, open(sent_path, 'w'))
    return received, sent

def process_degree(
        handler: GraphQueryHandler,
        addresses: list, 
        contracts: list, 
        degree: str, 
        save = True,
        from_date: str = '',
        to_date: str = '',
    ):
    tnxs = None
    if save:
        tnxs = save_degree_transactions(
            handler, addresses, contracts, degree, from_date, to_date,
        )
    else:
        tnxs = read_degree_transactions(degree)
    received, sent = tnxs
    parents = [t[ck.FROM_ADDRESS] for tnxs in received.values() for t in tnxs]
    children = [t[ck.TO_ADDRESS] for tnxs in sent.values() for t in tnxs]
    t = f'{len(parents)} parents and {len(children)} children for {degree}.'
    print(t)
    return parents, children

def process_layers(
        handler: GraphQueryHandler,
        source_addresses: list, 
        contracts: list, 
        degree: int, 
        from_date: str = '',
        to_date: str = '',
        parent = True,
        degree_limit: int = 5,
        edge_limit: int = None,
    ):
    count, bt = len(source_addresses), datetime.now().isoformat()
    print(f'{bt}: Processing degree {degree} for {count} addresses.')
    degree_name = f'degree_{degree}' 
    if degree != 0:
            degree_name += '_parent' if parent else '_child'
    degree_args = (handler, source_addresses, contracts, degree_name, True)
    parents, children = process_degree(*degree_args, from_date, to_date)
    et = datetime.now().isoformat()
    print(f'{et}: Processed degree {degree}.')
    random.shuffle(parents); random.shuffle(children)
    if edge_limit is not None:
        parents, children = parents[:edge_limit], children[:edge_limit]
    if degree >= degree_limit:
         return
    if parent:
        save_addresses_with_stats(parents, handler, degree_name, from_date, to_date)
        process_layers(
            handler, parents, contracts, degree + 1, 
            from_date, to_date, True, degree_limit, edge_limit,
        )
    else:
        save_addresses_with_stats(children, handler, degree_name, from_date, to_date)
        process_layers(handler, children, contracts, degree + 1,
            from_date, to_date, False, degree_limit, edge_limit,
        )
    return

def main():
    n, k = 50, None
    name = 'airdrop1'
    handler = GraphQueryHandler()
    from_date = '2023-12-25T00:00:00Z'
    to_date = '2024-06-01T00:00:00Z'
    claimers_n = get_n_claimers(handler, n, name, sample = False, from_date = from_date, to_date = to_date)
    degree_0_addresses = claimers_n['wallet_address'].values
    contracts = ['0x4ed4e862860bed51a9570b96d89af5e1b0efefed']
    save_addresses_with_stats(degree_0_addresses, handler, 'degree_0', from_date, to_date)
    process_layers(
        handler, degree_0_addresses, contracts, 0, from_date, to_date, True, 5,
        )
    process_layers(
        handler, degree_0_addresses, contracts, 0, from_date, to_date, False,5,
        )
    print('Done')

if __name__ == '__main__':
    main()