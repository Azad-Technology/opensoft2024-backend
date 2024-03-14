from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies
from src import schemas
from src.config import config
from bson.objectid import ObjectId

router = APIRouter()




@router.get('/movies/{movie_id}')
async def get_movie(movie_id: str):
    # projection={"_id":1, "title":1, "poster":1, "released": 1, "runtime":1, 'imdb':1, 'tomatoes':1}
    movie = await Movies.find_one({'_id': ObjectId(movie_id)})
    if movie:
        if '_id' in movie:
            movie['_id'] = str(movie['_id'])
        return movie
    raise HTTPException(status_code=404, detail='Movie not found')

