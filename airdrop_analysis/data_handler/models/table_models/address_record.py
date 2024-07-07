from peewee import CharField, DateTimeField, IntegerField, FloatField

from data_handler.models.table_models.base_model import BaseModel
from data_handler.models.base_models.transaction_history \
    import TransactionHistory



class Address_Record(BaseModel):
    address = CharField(unique=True)
    from_date = DateTimeField()
    to_date = DateTimeField()
    balance = FloatField()
    total_transaction_count = IntegerField()
    incoming_transaction_count = IntegerField()
    outgoing_transaction_count = IntegerField()
    first_incoming_transaction_date = DateTimeField()
    first_incoming_transaction_source = CharField()
    last_outgoing_transaction_date = DateTimeField()
    last_outgoing_transaction_destination = CharField()
    chain = CharField()
    contract_address = CharField()

    def create_from(history: TransactionHistory):
        ins = history.get_received_transactions()
        outs = history.get_sent_transactions()
        first_date, last_date = '', ''
        first_source, last_destination = '', ''
        if ins:
            first_date = ins[0].block_timestamp
            first_source = ins[0].from_address
        if outs:
            last_date = outs[-1].block_timestamp
            last_destination = outs[-1].to_address
        balance = sum([t.value for t in ins]) - sum([t.value for t in outs])
        contract_address = ''
        if history.contract_addresses:
            contract_address = history.contract_addresses[0]
        return Address_Record.create(
            address = history.address,
            from_date = history.from_date,
            to_date = history.to_date,
            balance = balance,
            total_transaction_count = history.get_transaction_count(),
            incoming_transaction_count = len(ins),
            outgoing_transaction_count = len(outs),
            first_incoming_transaction_date = first_date,
            first_incoming_transaction_source = first_source,
            last_outgoing_transaction_date = last_date,
            last_outgoing_transaction_destination = last_destination,
            chain = history.chain,
            contract_address = contract_address,
        )
