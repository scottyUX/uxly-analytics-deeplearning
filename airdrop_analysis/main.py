from fastapi import FastAPI
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
def read_item(token: str, airdrop: str, season: str) -> dict:
    param = AirdropParameters(
        token=token,
        airdrop=airdrop,
        season=season,
        from_date='2012-12-01T00:00:00Z',
        to_date='2024-06-01T00:00:00Z',
        claimer_limit=1,
        parent_depth=2,
        child_depth=2,  
        edge_limit=3,
        edge_order='DESC',
        )
    graph = AirdropAnalyzer().get_airdrop_graph(param)
    return {"nodes": len(graph.nodes), "edges": len(graph.edges)}
