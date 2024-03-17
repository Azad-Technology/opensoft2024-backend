from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import config
from src.db import db
from src.routers import movie,cast,genre, auth,embeddings,countries
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
app.include_router(countries.router, tags=["Country Top"])
app.include_router(auth.router, tags=["Auth"])
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"message": "OK"}