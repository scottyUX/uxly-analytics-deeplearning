from typing import List
import pandas as pd
import os

from utils.path_provider import PathProvider
from utils.custom_keys import CustomKeys as ck

class ClaimerListProvider:
    def __init__(self):
        self.__path_provider = PathProvider()
        self.__claimer_lists = self.__path_provider.get_claimer_lists()

    def get_available_tokens(self) -> List[str]:
        return list(self.__claimer_lists.keys())

    def get_token_chain(self, token: str) -> str:
        return self.__claimer_lists[token][ck.CHAIN]

    def get_token_contract_addresses(self, token: str) -> List[str]:
        return self.__claimer_lists[token][ck.CONTRACT_ADDRESSES]
    
    def get_available_airdrops_for_token(self, token: str) -> List[str]:
        return list(self.__claimer_lists[token][ck.AIRDROPS].keys())
    
    def get_available_seasons_for_airdrop(
            self, 
            token: str, 
            airdrop: str,
        ) -> List[str]:
        return list(self.__claimer_lists[token][ck.AIRDROPS][airdrop].keys())

    def get_claimers_list(
            self, 
            token: str, 
            airdrop: str, 
            season: str,
        ) -> List[str]:
        return pd.read_csv(
            self.__claimer_lists[token][ck.AIRDROPS][airdrop][season],
        )[ck.WALLET_ADDRESS].to_list()
