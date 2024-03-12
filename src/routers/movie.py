from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies
from src import schemas
from src.config import config

router = APIRouter()

@router.get('/movies/{movie_id}')
async def get_movie(movie_id: str):
    movie = await Movies.find_one({'_id': movie_id})
    if movie:
        return movie
    raise HTTPException(status_code=404, detail='Movie not found')

@router.get('/movies')
async def get_movies():
    movies = []
    async for movie in Movies.find():
        movies.append(movie)
    return movies