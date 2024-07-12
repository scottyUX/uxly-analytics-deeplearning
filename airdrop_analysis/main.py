from typing import Optional, List
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
load_dotenv()

from airdrop_analyzer import AirdropAnalyzer
from data_handler.models.base_models.query_parameters import \
    GraphQueryParameters, ClaimersGraphParameters


app = FastAPI()
AirdropAnalyzer()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/claimers_graph/{token}/{airdrop}/{season}")
def visualize_claimers_graph(
    token: str, 
    airdrop: str, 
    season: str,
    from_date: Optional[str] = '2023-12-01T00:00:00Z',
    to_date: Optional[str] = '2024-06-01T00:00:00Z',
    claimers: Optional[int] = 1,
    parent_depth: Optional[int] = 2,
    child_depth: Optional[int] = 2,
    edge_limit: Optional[int] = 3,
    edge_order: Optional[str] = 'DESC',
    ) -> HTMLResponse:
    param = ClaimersGraphParameters(
        token=token,
        airdrop=airdrop,
        season=season,
        from_date=from_date,
        to_date=to_date,
        claimer_limit=claimers,
        parent_depth=parent_depth,
        child_depth=child_depth,  
        edge_limit=edge_limit,
        edge_order=edge_order,
        )
    graph = AirdropAnalyzer().get_claimers_graph(param)
    return HTMLResponse(content=graph, status_code=200)

@app.get("/distribution_graph/")
def visualize_distribution_graph(
    distributor_address: str,
    contract_address: str,
    chain: Optional[str] = 'base',
    from_date: Optional[str] = '2023-12-01T00:00:00Z',
    to_date: Optional[str] = '2024-06-01T00:00:00Z',
    parent_depth: Optional[int] = 1,
    child_depth: Optional[int] = 1,
    edge_limit: Optional[int] = 1,
    edge_order: Optional[str] = 'DESC',
    ) -> HTMLResponse:
    param = GraphQueryParameters(
        center_addresses=[distributor_address],
        chain=chain,
        contract_addresses=[contract_address],
        from_date=from_date,
        to_date=to_date,
        parent_depth=parent_depth,
        child_depth=child_depth,  
        edge_limit=edge_limit,
        edge_order=edge_order,
        )
    graph = AirdropAnalyzer().get_distribution_graph(param)
    return HTMLResponse(content=graph, status_code=200)
