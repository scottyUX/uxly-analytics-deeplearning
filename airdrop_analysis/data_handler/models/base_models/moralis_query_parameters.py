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
        self.__address = address
        self.__from_date = from_date
        self.__to_date = to_date
        self.__chain = chain
        self.__order = order


    def to_dict(self):
        parameters = {
            ck.CHAIN: self.__chain, 
            ck.ORDER: self.__order, 
            ck.ADDRESS: self.__address,
        }
        if self.__from_date != '':
            parameters[ck.FROM_DATE] = self.__from_date
        if self.__to_date != '':
            parameters[ck.TO_DATE] = self.__to_date

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
        ):
        super().__init__(
            address, 
            contract_addresses, 
            from_date,
            to_date,
            chain,
            order,
        )
        self.__contract_addresses = contract_addresses

    def to_dict(self):
        parameters = super().to_dict()
        if self.__contract_addresses:
            parameters[ck.CONTRACT_ADDRESSES] = self.__contract_addresses
        return parameters