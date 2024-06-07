from utils.custom_keys import CustomKeys as ck


class MoralisQueryParameters(object):

    def __init__(
            self,
            address: str,  
            from_date: str = '',
            to_date: str = '',
            chain: str = 'eth',
            order: str = 'DESC',
        ):
        self.address = address
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


class MoralisStatsQueryParameters(MoralisQueryParameters):

    def __init__(
            self,
            address: str, 
            from_date: str = '',
            to_date: str = '',
            chain: str = 'eth',
            order: str = 'DESC',
        ):
        super().__init__(
            address,  
            from_date,
            to_date,
            chain,
            order,
        )


class MoralisTransactionsQueryParameters(MoralisQueryParameters):

    def __init__(
            self,
            address: str, 
            contract_addresses: list = [], 
            from_date: str = '',
            to_date: str = '',
            chain: str = 'eth',
            order: str = 'DESC',
            cursor: str = '0',
        ):
        super().__init__(
            address,  
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
