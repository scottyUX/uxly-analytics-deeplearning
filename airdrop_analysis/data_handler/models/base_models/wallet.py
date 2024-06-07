from utils.custom_keys import CustomKeys as ck

class WalletStats(object):

    def from_moralis_response(response: dict):
        return WalletStats(
            nft_count = int(response[ck.NFTS]),
            collection_count = int(response[ck.COLLECTIONS]),
            transaction_count = int(response[ck.TRANSACTIONS][ck.TOTAL]),
            nft_transfer_count = int(response[ck.NFT_TRANSFERS][ck.TOTAL]),
            token_transfer_count = int(response[ck.TOKEN_TRANSFERS][ck.TOTAL]),
        )

    def init(
            self, 
            nft_count: int,
            collection_count: int,
            transaction_count: int,
            nft_transfer_count: int,
            token_transfer_count: int,
            ):
        self.nft_count = nft_count
        self.collection_count = collection_count
        self.transaction_count = transaction_count
        self.nft_transfer_count = nft_transfer_count
        self.token_transfer_count = token_transfer_count

    def to_dict(self):
        return {
            ck.NFTS: self.nft_count,
            ck.COLLECTIONS: self.collection_count,
            ck.TRANSACTIONS: self.transaction_count,
            ck.NFT_TRANSFERS: self.nft_transfer_count,
            ck.TOKEN_TRANSFERS: self.token_transfer_count,
        }
