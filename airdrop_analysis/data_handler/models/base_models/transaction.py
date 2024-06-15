from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

from utils.custom_keys import CustomKeys as ck


class Transaction(BaseModel):
    hash_: str
    nonce: int
    transaction_index: int
    from_address: str
    from_address_label: Optional[str]
    to_address: str
    to_address_label: Optional[str]
    value: int
    gas: int
    gas_price: int
    input_: str
    receipt_cumulative_gas_used: int
    receipt_gas_used: int
    receipt_contract_address: Optional[str]
    receipt_root: Optional[str]
    receipt_status: str
    block_timestamp: str
    block_number: int
    block_hash: str
    transfer_index: list
    transaction_fee: Decimal
    
    def from_dict(response: dict):
        return Transaction(
            hash_ = response[ck.HASH],
            nonce = int(response[ck.NONCE]),
            transaction_index = int(response[ck.TRANSACTION_INDEX]),
            from_address = response[ck.FROM_ADDRESS],
            from_address_label = response[ck.FROM_ADDRESS_LABEL],
            to_address = response[ck.TO_ADDRESS],
            to_address_label = response[ck.TO_ADDRESS_LABEL],
            value = int(response[ck.VALUE]),
            gas = int(response[ck.GAS]),
            gas_price = int(response[ck.GAS_PRICE]),
            input_ = response[ck.INPUT],
            receipt_cumulative_gas_used = int(response[ck.REPCEIPT_CUMULATIVE_GAS_USED]),
            receipt_gas_used = int(response[ck.REPCEIPT_GAS_USED]),
            receipt_contract_address = response[ck.REPCEIPT_CONTRACT_ADDRESS],
            receipt_root = response[ck.RECEIPT_ROOT],
            receipt_status = response[ck.RECEIPT_STATUS],
            block_timestamp = response[ck.BLOCK_TIMESTAMP],
            block_number = int(response[ck.BLOCK_NUMBER]),
            block_hash = response[ck.BLOCK_HASH],
            transfer_index = response[ck.TRANSFER_INDEX],
            transaction_fee = Decimal(response[ck.TRANSACTION_FEE]),
        )

    def to_dict(self):
        return self.model_dump(exclude_unset=True)