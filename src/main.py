from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import config
from src.db import db
from src.routers import movie,cast
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=config['CORS_ORIGINS'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movie.router)
app.include_router(cast.router)

@app.get("/")
async def root():
    print('Hello World')
    return {"message": "Hello World"}