from pydantic import BaseModel
from typing import Optional


class QueryParameters(BaseModel):
    address: str
    table_name: str
    cached_first: Optional[bool] = True
    chain: Optional[str] = 'eth'
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


class TokenTransfersQueryParameters(TransactionsQueryParameters):
    contract_addresses: list = []
