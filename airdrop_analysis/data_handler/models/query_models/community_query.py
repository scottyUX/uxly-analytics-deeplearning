from pydantic import BaseModel
from typing import Optional
from fastapi import Query

class CommunityQuery(BaseModel):
    distributor_addresses: list[str] = Query(...),
    contract_addresses: list[str] = Query(...),
    chain: Optional[str] = 'base',
    from_date: Optional[str] = '2023-12-01T00:00:00Z',
    to_date: Optional[str] = '2024-06-01T00:00:00Z',
    parent_depth: Optional[int] = 1,
    child_depth: Optional[int] = 1,
    edge_limit: Optional[int] = 1,
    edge_order: Optional[str] = 'DESC',
    user_id: Optional[str] = ''
    
    def create_from_json(data):
        return CommunityQuery(
            distributor_addresses=data["distributor_addresses"],
            contract_addresses=data["contract_addresses"],
            chain=data["chain"],
            from_date=data["from_date"],
            to_date=data["to_date"],
            parent_depth=data["parent_depth"],
            child_depth=data["child_depth"],
            edge_limit=data["edge_limit"],
            edge_order=data["edge_order"],
            user_id =data["user_id"]
        )