from peewee import SqliteDatabase, Model, CharField, DateTimeField, \
    ForeignKeyField, IntegerField, BigIntegerField

# Ensure foreign-key constraints are enforced.
db = SqliteDatabase('data/airdrops.db', pragmas={'foreign_keys': 1})

class BaseModel(Model):
    class Meta:
        database = db

class Wallet(BaseModel):
    address = CharField(unique=True)
    from_date = DateTimeField()
    to_date = DateTimeField()
    total_transaction_count = IntegerField()
    incoming_transaction_count = IntegerField()
    outgoing_transaction_count = IntegerField()
    first_incoming_transaction_date = DateTimeField()
    first_incoming_transaction_source = CharField()
    last_outgoing_transaction_date = DateTimeField()
    last_outgoing_transaction_destination = CharField()
    chain = CharField()


class TokenTransfer(BaseModel):
    from_address = CharField()
    to_address = CharField()
    value = BigIntegerField()
    block_timestamp = DateTimeField()
    block_hash = CharField()
    transaction_hash = CharField(unique=True)
    token_name = CharField()
    contract_address = CharField()
    chain = CharField()
    sender_wallet = ForeignKeyField(
        Wallet, 
        backref='sent_transfers', 
        field='address', 
        to_field='from_address', 
        null=True,
    )
    receiver_wallet = ForeignKeyField(
        Wallet, 
        backref='received_transfers', 
        field='address', to_field='to_address', 
        null=True,
 )