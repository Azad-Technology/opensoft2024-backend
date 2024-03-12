from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies
from src import schemas
from src.config import config
from bson.objectid import ObjectId
\
router = APIRouter()




@router.get('/movies/{movie_id}')
async def get_movie(movie_id: str):
    movie = await Movies.find_one({'_id': ObjectId(movie_id)})
    if movie:
        if '_id' in movie:
            movie['_id'] = str(movie['_id'])
        return movie
    raise HTTPException(status_code=404, detail='Movie not found')

