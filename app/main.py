# from fastapi import FastAPI

# app = FastAPI(title ="personalized news aggregator", version="0.1.0")

# @app.get("/")
# async def health():
#     return {"status": "OK", "Service": "Personalized News aggregator"}

# @app.get("/docs-hello")
# async def doc_hello():
#     return {"message":"open/docs for automati api doc"}

from fastapi import FastAPI
from app.api import auth 

app = FastAPI(title="Personalized News Aggregator", version="0.1.0")

app.include_router(auth.router)

@app.get("/")
async def health():
    return {
        "status": "ok",
        "service": "News Aggregator"
    }
    
    
