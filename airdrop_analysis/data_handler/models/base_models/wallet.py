from pydantic import BaseModel
from typing import Optional
from data_handler.models.base_models.transaction_history \
    import TransactionHistory
from utils.custom_keys import CustomKeys as ck


class WalletStats(BaseModel):
    address: str
    chain: str
    nft_count: int
    collection_count: int
    transaction_count: int
    nft_transfer_count: int
    token_transfer_count: int

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

    def to_dict(self):
        return self.model_dump(exclude_unset=True)


class Wallet(BaseModel):
    address: str
    transaction_history: TransactionHistory
    stats: Optional[WalletStats] = None

    def to_dict(self):
        return self.model_dump(exclude_unset=True)

    class Config:
        arbitrary_types_allowed = True