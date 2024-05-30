
import pandas as pd
import json

from graph_query.graph_query_handler import GraphQueryHandler

DEGEN_AIRDROP_FOLDER = 'data/datasets/degen_airdrop_claims'

def get_airdrop_addresses(name = 'airdrop1'):
    df = pd.read_csv(f'{DEGEN_AIRDROP_FOLDER}/csv/{name}_claims.csv') 
    df  = df[df['claimed'] == True]
    print(f'{len(df)} Airdrop Addresses')
    return df['wallet_address']

def save_addresses_with_stats(addresses, handler: GraphQueryHandler, name = 'airdrop1'):
    stats = handler.query_wallet_stats_as_df(addresses)
    stats.to_csv(f'{DEGEN_AIRDROP_FOLDER}/network/{name}_with_stats.csv', index=False)


def get_n_claimers(handler: GraphQueryHandler, n = 50, name = 'airdrop1', sample = True):
    claimers_name = f'{n}_claimers_from_{name}'
    addresses = get_airdrop_addresses(name)
    if sample:
        addresses = get_airdrop_addresses(name)
        claimers_n = addresses.sample(n)
        save_addresses_with_stats(claimers_n, handler, claimers_name)
        return claimers_n
    else:
        return pd.read_csv(f'{DEGEN_AIRDROP_FOLDER}/network/{claimers_name}_with_stats.csv')

def save_degree_transactions(handler: GraphQueryHandler, addresses, contracts, degree = 'degree_zero'):
    received_transactions, sent_transactions = \
        handler.get_wallet_transactions(addresses, contracts)
    json.dump(received_transactions, open(f'{DEGEN_AIRDROP_FOLDER}/network/{degree}_received.json', 'w'))
    json.dump(sent_transactions, open(f'{DEGEN_AIRDROP_FOLDER}/network/{degree}_sent.json', 'w'))

def read_degree_transactions(degree = 'degree_zero'):
    received = json.load(open(f'{DEGEN_AIRDROP_FOLDER}/network/{degree}_received.json', 'r'))
    sent = json.load(open(f'{DEGEN_AIRDROP_FOLDER}/network/{degree}_sent.json', 'r'))
    return received, sent

def process_degree(handler, degree_addresses, contracts, degree, save = True):
    if save:
        save_degree_transactions(handler, degree_addresses, contracts, degree = degree)
    received, sent = read_degree_transactions(degree = degree)
    degree_senders = [t['from_address'] for tnxs in received.values() for t in tnxs]
    degree_receivers = [t['to_address'] for tnxs in sent.values() for t in tnxs]
    print(f'{len(degree_senders)} received and {len(degree_receivers)} sent addresses at {degree}.')
    return degree_senders, degree_receivers

def main():
    n, k = 50, 10
    name = 'airdrop1'
    handler = GraphQueryHandler()
    claimers_n = get_n_claimers(handler, n, name, sample = False)
    degree_zero_addresses = claimers_n['wallet_address'].values
    contracts = ['0x4ed4e862860bed51a9570b96d89af5e1b0efefed']
    degree = 'degree_zero'
    senders, receivers = process_degree(handler, degree_zero_addresses, contracts, degree, save = True)
    # senders, receivers = read_degree_transactions(degree = degree)
    # senders, receivers = senders[:k], receivers[:k]
    # save_addresses_with_stats(senders, handler, name = f'{degree}_parent')
    # save_addresses_with_stats(receivers, handler, name = f'{degree}_child')
    # degree = 'degree_two_parent'
    # senders, receivers = process_degree(handler, senders, degree = degree, save = True)


    

if __name__ == '__main__':
    main()