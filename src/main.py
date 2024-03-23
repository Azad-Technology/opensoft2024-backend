from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import config
from src.db import db
from src.routers import movie,cast,genre,search,auth,countries,user
import redis
from fastapi import APIRouter, HTTPException
from src.cache_system import set_default_ttl
# import date time
from datetime import datetime


r = redis.Redis(host='127.0.0.1',port=8045, decode_responses=True)
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=config['CORS_ORIGINS'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(movie.router,tags=['movie'])
app.include_router(cast.router,tags=["Cast and Director"])
app.include_router(genre.router, tags=["Genre"])
app.include_router(search.router, tags=["Search"])
app.include_router(countries.router, tags=["Country Top"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(user.router, tags=["Update Info"])
# app.include_router(embeddings.router, tags=["Embeddings"])

@app.get("/")
async def root():
    print(type(datetime.now().year))
    return {"message": "Hello World"}

@app.get("/set_default_ttl")
async def update_default_ttl(ttl: int):
    if ttl <= 0:
        raise HTTPException(status_code=400, detail="TTL must be a positive integer")
    
    await set_default_ttl(ttl)
    return {"message": "Default TTL updated", "ttl": ttl}

@app.get("/flush_cache")
async def flush_cache():
    r.flushdb()
    return {"message": "Cache flushed"}


@app.get("/health")
async def health():
    return {"message": "OK"}