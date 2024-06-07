from datetime import datetime
import pandas as pd
import random
import json
import os

from airdrop_analysis.data_handler.graph_query_handler import GraphQueryHandler
from utils.costum_keys import CustomKeys as ck

class GraphDataHandler:
    def __init__(
            self, 
            airdrop_name: str,
            smart_contract_addresses: list, 
            source_address_count: int,
            edge_limit: int,
            parent_degree_limit: int = 5,
            child_degree_limit: int = 5,
            transaction_upper_limit: int = 50000,
            from_date: str = '',
            to_date: str = '',
            airdrop_name_folder_path: str = '',
        ):
        self.__query_handler = GraphQueryHandler()
        self.__airdrop_name = airdrop_name
        self.__smart_contract_addresses = smart_contract_addresses
        self.__source_address_count = source_address_count
        self.__edge_limit = edge_limit
        self.__parent_degree_limit = parent_degree_limit
        self.__child_degree_limit = child_degree_limit
        self.__transaction_upper_limit = transaction_upper_limit
        self.__from_date = from_date
        self.__to_date = to_date
        self.__airdrop_name_folder_path = airdrop_name_folder_path
        self.__current_degree = 0
        self.__current_addresses = None
        self.__current_layer_is_parent = False

    def __get_pat_for_transactions(self, received: bool):
        folder, degree = self.__airdrop_name_folder_path, self.__current_degree
        if received:
            return f'{folder}/network/{degree}_received.json'
        else:
            return f'{folder}/network/{degree}_sent.json'

    def __read_degree_transactions(self,degree):
        received_path = self.__get_pat_for_transactions(True)
        received = json.load(open(received_path, 'r'))
        sent_path = self.__get_pat_for_transactions(False)
        sent = json.load(open(sent_path, 'r'))
        return received, sent

    def __save_degree_transactions(self):
        received_path = f'{self.__airdrop_name_folder_path}/network/{degree}_received.json'
        sent_path = f'{self.__airdrop_name_folder_path}/network/{degree}_sent.json'
        if os.path.exists(received_path) and os.path.exists(sent_path):
            return read_degree_transactions(degree)
        received, sent = handler.get_wallet_transactions(
            addresses, contracts, from_date, to_date,
        )
        json.dump(received, open(received_path, 'w'))
        json.dump(sent, open(sent_path, 'w'))
        return received, sent

    def process_degree():
        tnxs = None
        tnxs = save_degree_transactions(
                handler, addresses, contracts, degree, from_date, to_date,
            )
        tnxs = read_degree_transactions(degree)
        received, sent = tnxs
        parents = [t[ck.FROM_ADDRESS] for tnxs in received.values() for t in tnxs]
        children = [t[ck.TO_ADDRESS] for tnxs in sent.values() for t in tnxs]
        t = f'{len(parents)} parents and {len(children)} children for {degree}.'
        print(t)
        return parents, children

    def __process_layers(self, addresses: list, degree: int, parent: bool):
        count, bt = len(addresses), datetime.now().isoformat()
        print(f'{bt}: Processing degree {degree} for {count} addresses.')
        degree_name = f'degree_{degree}' 
        if degree != 0:
                degree_name += '_parent' if parent else '_child'
        parents, children = process_degree(*degree_args, from_date, to_date)
        et = datetime.now().isoformat()
        print(f'{et}: Processed degree {degree}.')
        if self.__edge_limit is not None:
            random.shuffle(parents); random.shuffle(children)
            parents = parents[:self.__edge_limit]
            children = children[:self.__edge_limit]
        if parent:
            self.__save_addresses_with_stats(parents, degree_name)
            if degree >= self.__parent_degree_limit:
                return
            self.__process_layers(parents, degree + 1, True)
        else:
            save_addresses_with_stats(children, handler, degree_name, from_date, to_date)
            if degree >= self.__child_degree_limit:
                return
            self.__process_layers(children, degree + 1, False)
        return

