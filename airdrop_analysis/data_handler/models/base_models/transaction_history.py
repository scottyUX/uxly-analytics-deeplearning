from pydantic import BaseModel
from typing import Optional, List

from data_handler.models.base_models.transaction import *
from data_handler.models.base_models.token_transfer import TokenTransfer
from utils.custom_keys import CustomKeys as ck


class TransactionHistory(BaseModel):
    address: str
    chain: str
    transactions: List[TransactionBase]
    from_date: str
    to_date: str
    contract_addresses: List[str]
    last_cursor: Optional[str] = '0'

    @staticmethod
    def from_dict(d: dict):
        if ck.FROM_DATE not in d:
            d[ck.FROM_DATE] = ''
        if ck.TO_DATE not in d:
            d[ck.TO_DATE] = ''
        if ck.CONTRACT_ADDRESSES not in d:
            d[ck.CONTRACT_ADDRESSES] = []
        if len(d[ck.TRANSACTIONS]) == 0:
            d[ck.TRANSACTIONS] = []
        if len(d[ck.TRANSACTIONS]) == 0:
            tnxs = []
        elif ck.HASH in d[ck.TRANSACTIONS][0]:
            tnxs = [Transaction.from_dict(tx) for tx in d[ck.TRANSACTIONS]]
        else:
            tnxs = [TokenTransfer.from_dict(tx) for tx in d[ck.TRANSACTIONS]]
        return TransactionHistory(
            address=d[ck.ADDRESS],
            chain=d[ck.CHAIN],
            transactions=tnxs,
            from_date=d[ck.FROM_DATE],
            to_date=d[ck.TO_DATE],
            contract_addresses=d[ck.CONTRACT_ADDRESSES],
            last_cursor=d[ck.CURSOR],
        )

    def get_transaction_count(self):
        return len(self.transactions)

    def get_received_transactions(self):
        t = [tx for tx in self.transactions if tx.to_address == self.address]
        return t
    
    def get_sent_transactions(self):
        t = [tx for tx in self.transactions if tx.from_address == self.address]
        return t
    
    def get_sender_addresses(self):
        received_transactions = self.get_received_transactions()
        return list(set([tx.from_address for tx in received_transactions]))
    
    def get_receiver_addresses(self):
        sent_transactions = self.get_sent_transactions()
        return list(set([tx.to_address for tx in sent_transactions]))
    
    def to_dict(self):
        return {
            ck.ADDRESS: self.address,
            ck.CHAIN: self.chain,
            ck.TRANSACTIONS: [tx.to_dict() for tx in self.transactions],
            ck.TRANSACTION_COUNT: self.get_transaction_count(),
            ck.FROM_DATE: self.from_date,
            ck.TO_DATE: self.to_date,
            ck.CONTRACT_ADDRESSES: self.contract_addresses,
            ck.CURSOR: self.last_cursor,
        }

    class Config:
        arbitrary_types_allowed = True