from typing import Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
load_dotenv()

from airdrop_analyzer import AirdropAnalyzer
from data_handler.models.base_models.query_parameters import \
    AirdropParameters


app = FastAPI()
AirdropAnalyzer()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/graphs/{token}/{airdrop}/{season}")
def visualize_graph(
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
    param = AirdropParameters(
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
    graph = AirdropAnalyzer().get_airdrop_graph(param)
    return HTMLResponse(content=graph, status_code=200)
