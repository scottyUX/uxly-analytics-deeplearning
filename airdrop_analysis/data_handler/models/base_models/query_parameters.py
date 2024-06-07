from utils.custom_keys import CustomKeys as ck


class QueryParameters(object):

    def __init__(
            self,
            address: str,  
            table_name: str,
            from_date: str = '',
            to_date: str = '',
            chain: str = 'eth',
            order: str = 'DESC',
        ):
        self.address = address
        self.table_name = table_name
        self.from_date = from_date
        self.to_date = to_date
        self.chain = chain
        self.order = order

    def to_dict(self):
        parameters = {
            ck.CHAIN: self.chain, 
            ck.ORDER: self.order, 
            ck.ADDRESS: self.address,
        }
        if self.from_date != '':
            parameters[ck.FROM_DATE] = self.from_date
        if self.to_date != '':
            parameters[ck.TO_DATE] = self.to_date
        return parameters


class StatsQueryParameters(QueryParameters):

    def __init__(
            self,
            address: str, 
            table_name: str,
            from_date: str = '',
            to_date: str = '',
            chain: str = 'eth',
            order: str = 'DESC',
        ):
        super().__init__(
            address,  
            table_name,
            from_date,
            to_date,
            chain,
            order,
        )


class TransactionsQueryParameters(QueryParameters):

    def __init__(
            self,
            address: str, 
            table_name: str,
            contract_addresses: list = [], 
            from_date: str = '',
            to_date: str = '',
            chain: str = 'eth',
            order: str = 'DESC',
            cursor: str = '0',
        ):
        super().__init__(
            address,
            table_name,
            from_date,
            to_date,
            chain,
            order,
        )
        self.contract_addresses = contract_addresses
        self.cursor = cursor

    def to_dict(self):
        parameters = super().to_dict()
        if self.contract_addresses:
            parameters[ck.CONTRACT_ADDRESSES] = self.contract_addresses
        if self.cursor != '0':
            parameters[ck.CURSOR] = self.cursor
        return parameters


class WalletQueryParameters(TransactionsQueryParameters):

    def __init__(
            self,
            address: str, 
            stats_table_name: str,
            transaction_table_name: str,
            contract_addresses: list = [], 
            from_date: str = '',
            to_date: str = '',
            chain: str = 'eth',
            order: str = 'DESC',
            cursor: str = '0',
        ):
        super().__init__(
            address,
            transaction_table_name,
            contract_addresses,
            from_date,
            to_date,
            chain,
            order,
            cursor,
        )
        self.stats_table_name = stats_table_name
        self.transaction_table_name = transaction_table_name

    def to_dict(self):
        return super().to_dict()


    def to_stats_query(self) -> StatsQueryParameters:
        return StatsQueryParameters(
            self.address,
            self.stats_table_name,
            self.from_date,
            self.to_date,
            self.chain,
            self.order,
        )
