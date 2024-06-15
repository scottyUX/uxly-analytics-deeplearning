import pandas as pd
import boto3

from data_handler.models.base_models.wallet import WalletStats
from data_handler.models.base_models.transaction_history \
    import TransactionHistory
from utils.custom_keys import CustomKeys as ck
from data_handler.models.base_models.query_parameters import *

class DynamoDBQueryHandler(object):
    def __init__(self, access_key_path: str):
        self.__resource = self.__get_resource(access_key_path)

    def __get_resource(self, access_key_path: str):
        access_key = pd.read_csv(access_key_path).iloc[0].to_dict()
        self.__session = boto3.Session(
            aws_access_key_id=access_key[ck.ACCESS_KEY_ID],
            aws_secret_access_key=access_key[ck.SECRET_ACCESS_KEY],
            region_name=ck.AWS_REGION,
        )
        self.__resource = self.__session.resource(ck.DYNAMODB)
        return self.__resource

    def __put_item(self, table_name: str, item: dict):
        table = self.__resource.Table(table_name)
        table.put_item(Item=item)

    def put_wallet_stats(self, table_name: str, stats: WalletStats):
        self.__put_item(table_name, stats.to_dict())

    def put_wallet_transactions(
            self, 
            table_name: str, 
            transaction_history: TransactionHistory,
        ):
        self.__put_item(table_name, transaction_history.to_dict())

    def __get_item(self, table_name: str, key: dict):
        table = self.__resource.Table(table_name)
        response = table.get_item(Key=key)
        if ck.ITEM in response:
            return response[ck.ITEM]
        return None

    def get_wallet_stats(self, params: StatsQueryParameters):
        key = {ck.ADDRESS: params.address}
        response = self.__get_item(params.table_name, key)
        if response is None:
            return None
        return WalletStats.from_dict(response)
    
    def get_wallet_transactions(self, params: TransactionsQueryParameters):
        key = {ck.ADDRESS: params.address}
        response = self.__get_item(params.table_name, key)
        if response is None:
            return None
        return TransactionHistory.from_dict(response)

    def put_wallet_token_transfers(
            self, 
            table_name: str, 
            transaction_history: TransactionHistory,
        ):
        self.__put_item(table_name, transaction_history.to_dict())

    def get_wallet_token_transfers(
            self, 
            params: TokenTransfersQueryParameters,
        ):
        key = {ck.ADDRESS: params.address}
        response = self.__get_item(params.table_name, key)
        if response is None:
            return None
        return TransactionHistory.from_dict(response)