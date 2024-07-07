from peewee import CharField, DateTimeField, FloatField

from data_handler.models.table_models.base_model import BaseModel
from utils.custom_keys import CustomKeys as ck

class Token_Transfer(BaseModel):
    from_address = CharField()
    to_address = CharField()
    value = FloatField()
    block_timestamp = DateTimeField()
    block_hash = CharField()
    transaction_hash = CharField()
    token_name = CharField()
    contract_address = CharField()
    chain = CharField()
    
    def create_from_dict(chain: str, response: dict):
        return Token_Transfer.create(
            from_address = response[ck.FROM_ADDRESS],
            to_address = response[ck.TO_ADDRESS],
            value = float(response[ck.VALUE]) / 10**18,
            block_timestamp = response[ck.BLOCK_TIMESTAMP],
            block_hash = response[ck.BLOCK_HASH],
            transaction_hash = response[ck.TRANSACTION_HASH],
            token_name = response[ck.TOKEN_NAME],
            contract_address = response[ck.ADDRESS],
            chain = chain,
        )

