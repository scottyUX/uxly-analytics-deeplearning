from pydantic import BaseModel
from typing import Optional, List

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
    contract_addresses: List[str] = []


class GraphQueryParameters(BaseModel):
    center_addresses: List[str]
    chain: str
    contract_addresses: List[str]
    from_date: Optional[str] = ''
    to_date: Optional[str] = ''
    parent_depth: Optional[int] = 1
    child_depth: Optional[int] = 1
    edge_limit: Optional[int] = -1
    edge_order: Optional[str] = 'DESC'
    partition: Optional[bool] = False
    user_id: Optional[str] = ""

    def to_dict(self):
        return self.model_dump(exclude_unset=True)

class ClaimersGraphParameters(GraphQueryParameters):
    token: str
    airdrop: str
    season: str
    claimer_limit: Optional[int] = -1
    center_addresses: List[str] = []
    chain: str = ''
    contract_addresses: List[str] = []
