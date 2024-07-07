from pydantic import BaseModel
from typing import Optional

from utils.custom_keys import CustomKeys as ck


class QueryParameters(BaseModel):
    address: str
    chain: str = 'eth'
    cached_first: Optional[bool] = True
    order: Optional[str] = 'DESC'

    def to_dict(self):
        return self.model_dump(exclude_unset=True)


class StatsQueryParameters(QueryParameters):
    pass


class TransactionsQueryParameters(QueryParameters):
    from_date: Optional[str] = ''
    to_date: Optional[str] = ''
    limit: Optional[int] = 300
    cursor: Optional[str] = '0'

    def to_dict(self):
        super_dict = super().to_dict()
        super_dict[ck.LIMIT] = self.limit
        return super_dict

class TokenTransfersQueryParameters(TransactionsQueryParameters):
    contract_addresses: list = []
