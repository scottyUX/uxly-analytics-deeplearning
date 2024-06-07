from decimal import Decimal
from typing import Optional

from utils.custom_keys import CustomKeys as ck


class Transaction(object):
    
    def from_dict(response: dict):
        return Transaction(
            hash = response[ck.HASH],
            # nonce = int(response[ck.NONCE]),
            # transaction_index = int(response[ck.TRANSACTION_INDEX]),
            from_address = response[ck.FROM_ADDRESS],
            # from_address_label = response[ck.FROM_ADDRESS_LABEL],
            to_address = response[ck.TO_ADDRESS],
            # to_address_label = response[ck.TO_ADDRESS_LABEL],
            # value = int(response[ck.VALUE]),
            # gas = int(response[ck.GAS]),
            # gas_price = int(response[ck.GAS_PRICE]),
            # input = response[ck.INPUT],
            # receipt_cumulative_gas_used = int(response[ck.REPCEIPT_CUMULATIVE_GAS_USED]),
            # receipt_gas_used = int(response[ck.REPCEIPT_GAS_USED]),
            # receipt_contract_address = response[ck.REPCEIPT_CONTRACT_ADDRESS],
            # receipt_root = response[ck.RECEIPT_ROOT],
            # receipt_status = response[ck.RECEIPT_STATUS],
            # block_timestamp = response[ck.BLOCK_TIMESTAMP],
            # block_number = int(response[ck.BLOCK_NUMBER]),
            # block_hash = response[ck.BLOCK_HASH],
            # transfer_index = response[ck.TRANSFER_INDEX],
            # transaction_fee = Decimal(response[ck.TRANSACTION_FEE]),
        )
    
    def __init__(
            self, 
            hash: str,
            # nonce: int,
            # transaction_index: int,
            from_address: str,
            # from_address_label: Optional[str],
            to_address: str,
            # to_address_label: Optional[str],
            # value: int,
            # gas: int,
            # gas_price: int,
            # input: str,
            # receipt_cumulative_gas_used: int,
            # receipt_gas_used: int,
            # receipt_contract_address: Optional[str],
            # receipt_root: Optional[str],
            # receipt_status: str,
            # block_timestamp: str,
            # block_number: int,
            # block_hash: str,
            # transfer_index: list,
            # transaction_fee: float,
        ):
        self.hash = hash
        # self.nonce = nonce
        # self.transaction_index = transaction_index
        self.from_address = from_address
        # self.from_address_label = from_address_label
        self.to_address = to_address
        # self.to_address_label = to_address_label
        # self.value = value
        # self.gas = gas
        # self.gas_price = gas_price
        # self.input = input
        # self.receipt_cumulative_gas_used = receipt_cumulative_gas_used
        # self.receipt_gas_used = receipt_gas_used
        # self.receipt_contract_address = receipt_contract_address
        # self.receipt_root = receipt_root
        # self.receipt_status = receipt_status
        # self.block_timestamp = block_timestamp
        # self.block_number = block_number
        # self.block_hash = block_hash
        # self.transfer_index = transfer_index
        # self.transaction_fee = transaction_fee

    def to_dict(self):
        return {
            ck.HASH: self.hash,
            # ck.NONCE: self.nonce,
            # ck.TRANSACTION_INDEX: self.transaction_index,
            ck.FROM_ADDRESS: self.from_address,
            # ck.FROM_ADDRESS_LABEL: self.from_address_label,
            ck.TO_ADDRESS: self.to_address,
            # ck.TO_ADDRESS_LABEL: self.to_address_label,
            # ck.VALUE: self.value,
            # ck.GAS: self.gas,
            # ck.GAS_PRICE: self.gas_price,
            # ck.INPUT: self.input,
            # ck.REPCEIPT_CUMULATIVE_GAS_USED: self.receipt_cumulative_gas_used,
            # ck.REPCEIPT_GAS_USED: self.receipt_gas_used,
            # ck.REPCEIPT_CONTRACT_ADDRESS: self.receipt_contract_address,
            # ck.RECEIPT_ROOT: self.receipt_root,
            # ck.RECEIPT_STATUS: self.receipt_status,
            # ck.BLOCK_TIMESTAMP: self.block_timestamp,
            # ck.BLOCK_NUMBER: self.block_number,
            # ck.BLOCK_HASH: self.block_hash,
            # ck.TRANSFER_INDEX: self.transfer_index,
            # ck.TRANSACTION_FEE: self.transaction_fee,
        }