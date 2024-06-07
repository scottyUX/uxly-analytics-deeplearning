

class TransactionHistory(object):

    def __init__(
            self, 
            address: str,
            chain: str,
            transactions: list,
            from_date: str,
            to_date: str,
            contract_addresses: list,
            last_cursor: str,
        ):
        self.address = address
        self.chain = chain
        self.transactions = transactions
        self.last_cursor = last_cursor
        self.transactions = transactions
        self.transaction_count = len(transactions)
        self.from_date = from_date
        self.to_date = to_date
        self.contract_addresses = contract_addresses
        self.received_transactions = self.__get_received_transactions()
        self.sent_transactions = self.__get_sent_transactions()
        self.sender_addresses = self.__get_sender_addresses()
        self.receiver_addresses = self.__get_receiver_addresses()

    def __get_received_transactions(self):
        t = [tx for tx in self.transactions if tx.to_address == self.address]
        return t
    
    def __get_sent_transactions(self):
        t = [tx for tx in self.transactions if tx.from_address == self.address]
        return t
    
    def __get_sender_addresses(self):
        received_transactions = self.__get_received_transactions()
        return list(set([tx.from_address for tx in received_transactions]))
    
    def __get_receiver_addresses(self):
        sent_transactions = self.__get_sent_transactions()
        return list(set([tx.to_address for tx in sent_transactions]))