from typing import Optional

from data_handler.models.query_models.community_query import CommunityQuery

class GraphQuery(CommunityQuery):
    partition: Optional[bool]
    
    def create_from_json(data):
        return GraphQuery(
            distributor_addresses=data["distributor_addresses"],
            contract_addresses=data["contract_addresses"],
            chain=data["chain"],
            from_date=data["from_date"],
            to_date=data["to_date"],
            parent_depth=data["parent_depth"],
            child_depth=data["child_depth"],
            edge_limit=data["edge_limit"],
            edge_order=data["edge_order"],
            partition=data["partition"]
        )