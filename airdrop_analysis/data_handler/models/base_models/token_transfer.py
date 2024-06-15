from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

from data_handler.models.base_models.transaction import TransactionBase
from utils.custom_keys import CustomKeys as ck


class TokenTransfer(TransactionBase):
    token_name: Optional[str] = None
    token_symbol: Optional[str] = None
    token_logo: Optional[str] = None
    token_decimals: Optional[Decimal] = None
    address: str
    transaction_hash: str
    transaction_index: int
    log_index: int
    possible_spam: bool
    value_decimal: Optional[Decimal] = None
    verified_contract: bool
    
    def from_dict(response: dict):
        token_decimals = response.get(ck.TOKEN_DECIMALS)
        if token_decimals is not None:
            token_decimals = Decimal(token_decimals)
        value_decimal = response.get(ck.VALUE_DECIMAL)
        if value_decimal is not None:
            value_decimal = Decimal(value_decimal)
        return TokenTransfer(
            token_name = response[ck.TOKEN_NAME],
            token_symbol = response[ck.TOKEN_SYMBOL],
            token_logo = response[ck.TOKEN_LOGO],
            token_decimals = token_decimals,
            from_address = response[ck.FROM_ADDRESS],
            from_address_label = response[ck.FROM_ADDRESS_LABEL],
            to_address = response[ck.TO_ADDRESS],
            to_address_label = response[ck.TO_ADDRESS_LABEL],
            address = response[ck.ADDRESS],
            block_hash = response[ck.BLOCK_HASH],
            block_number = int(response[ck.BLOCK_NUMBER]),
            block_timestamp = response[ck.BLOCK_TIMESTAMP],
            transaction_hash = response[ck.TRANSACTION_HASH],
            transaction_index = int(response[ck.TRANSACTION_INDEX]),
            log_index = int(response[ck.LOG_INDEX]),
            value = int(response[ck.VALUE]),
            possible_spam = response[ck.POSSIBLE_SPAM],
            value_decimal = value_decimal,
            verified_contract = response[ck.VERIFIED_CONTRACT],
        )

    def to_dict(self):
        return self.model_dump(exclude_unset=True)