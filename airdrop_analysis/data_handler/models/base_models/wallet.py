from data_handler.models.base_models.transaction_history \
    import TransactionHistory
from utils.custom_keys import CustomKeys as ck


class WalletStats(object):

    @staticmethod
    def from_dict(response: dict):
        return WalletStats(
            address = response[ck.ADDRESS],
            chain = response[ck.CHAIN],
            nft_count = int(response[ck.NFT_COUNT]),
            collection_count = int(response[ck.COLLECTION_COUNT]),
            transaction_count = int(response[ck.TRANSACTION_COUNT]),
            nft_transfer_count = int(response[ck.NFT_TRANSFER_COUNT]),
            token_transfer_count = int(response[ck.TOKEN_TRANSFER_COUNT]),
        )


    @staticmethod
    def from_moralis_dict(address: str, chain: str, response: dict):
        return WalletStats(
            address = address,
            chain = chain,
            nft_count = int(response[ck.NFTS]),
            collection_count = int(response[ck.COLLECTIONS]),
            transaction_count = int(response[ck.TRANSACTIONS][ck.TOTAL]),
            nft_transfer_count = int(response[ck.NFT_TRANSFERS][ck.TOTAL]),
            token_transfer_count = int(response[ck.TOKEN_TRANSFERS][ck.TOTAL]),
        )

    def __init__(
            self, 
            address: str,
            chain: str,
            nft_count: int,
            collection_count: int,
            transaction_count: int,
            nft_transfer_count: int,
            token_transfer_count: int,
            ):
        self.address = address
        self.chain = chain
        self.nft_count = nft_count
        self.collection_count = collection_count
        self.transaction_count = transaction_count
        self.nft_transfer_count = nft_transfer_count
        self.token_transfer_count = token_transfer_count

    def to_dict(self):
        return {
            ck.ADDRESS: self.address,
            ck.CHAIN: self.chain,
            ck.NFT_COUNT: self.nft_count,
            ck.COLLECTION_COUNT: self.collection_count,
            ck.TRANSACTION_COUNT: self.transaction_count,
            ck.NFT_TRANSFER_COUNT: self.nft_transfer_count,
            ck.TOKEN_TRANSFER_COUNT: self.token_transfer_count,
        }


class Wallet(WalletStats):

    def __init__(
            self,
            stats: WalletStats,
            transaction_history: TransactionHistory,
    ):
        super().__init__(
            stats.address,
            stats.chain,
            stats.nft_count,
            stats.collection_count,
            stats.transaction_count,
            stats.nft_transfer_count,
            stats.token_transfer_count,
        )
        self.__transaction_history = transaction_history

    def get_received_transactions(self):
        return self.__transaction_history.received_transactions
    
    def get_sent_transactions(self):
        return self.__transaction_history.sent_transactions
    
    def get_sender_addresses_to_this_address(self):
        return self.__transaction_history.sender_addresses
    
    def get_receiver_addresses_from_this_address(self):
        return self.__transaction_history.receiver_addresses
    
    def to_dict(self):
        d = super().to_dict()
        d[ck.TRANSACTIONS] = self.__transaction_history.to_dict()
        return d