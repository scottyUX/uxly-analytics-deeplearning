from data_handler.models.base_models.transaction import Transaction
from utils.custom_keys import CustomKeys as ck


class TransactionHistory(object):

    @staticmethod
    def from_dict(d: dict):
        if ck.FROM_DATE not in d:
            d[ck.FROM_DATE] = ''
        if ck.TO_DATE not in d:
            d[ck.TO_DATE] = ''
        if ck.CONTRACT_ADDRESSES not in d:
            d[ck.CONTRACT_ADDRESSES] = []
        return TransactionHistory(
            address=d[ck.ADDRESS],
            chain=d[ck.CHAIN],
            transactions=d[ck.TRANSACTIONS],
            from_date=d[ck.FROM_DATE],
            to_date=d[ck.TO_DATE],
            contract_addresses=d[ck.CONTRACT_ADDRESSES],
            last_cursor=d[ck.CURSOR],
        )
    
    def __init__(
            self, 
            address: str,
            chain: str,
            transactions: list,
            from_date: str,
            to_date: str,
            contract_addresses: list,
            last_cursor: str,
        ):
        self.address = address
        self.chain = chain
        self.transactions = transactions
        self.last_cursor = last_cursor
        self.transaction_count = len(transactions)
        if len(transactions) > 0 and isinstance(transactions[0], dict):
            transactions = [Transaction.from_dict(tx) for tx in transactions]
        self.transactions = transactions
        self.from_date = from_date
        self.to_date = to_date
        self.contract_addresses = contract_addresses
        self.received_transactions = self.__get_received_transactions()
        self.sent_transactions = self.__get_sent_transactions()
        self.sender_addresses = self.__get_sender_addresses()
        self.receiver_addresses = self.__get_receiver_addresses()

    def __get_received_transactions(self):
        t = [tx for tx in self.transactions if tx.to_address == self.address]
        return t
    
    def __get_sent_transactions(self):
        t = [tx for tx in self.transactions if tx.from_address == self.address]
        return t
    
    def __get_sender_addresses(self):
        received_transactions = self.__get_received_transactions()
        return list(set([tx.from_address for tx in received_transactions]))
    
    def __get_receiver_addresses(self):
        sent_transactions = self.__get_sent_transactions()
        return list(set([tx.to_address for tx in sent_transactions]))
    
    def to_dict(self):
        return {
            ck.ADDRESS: self.address,
            ck.CHAIN: self.chain,
            ck.TRANSACTIONS: [tx.to_dict() for tx in self.transactions],
            ck.TRANSACTION_COUNT: self.transaction_count,
            ck.FROM_DATE: self.from_date,
            ck.TO_DATE: self.to_date,
            ck.CONTRACT_ADDRESSES: self.contract_addresses,
            ck.CURSOR: self.last_cursor,
        }