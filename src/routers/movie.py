from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies
from src import schemas
from src.config import config
from bson.objectid import ObjectId
from typing import Optional


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

@router.get('/imdb/')
async def get_movies( count: Optional[int] = 10):
    try:
        if count<1:
           return []
        projection={"_id":1, "title":1, "poster":1, "released": 1, "runtime":1, 'imdb':1, 'tomatoes':1}
        movies_cur = Movies.find({"imdb.rating":{'$ne':''}},projection).sort([("imdb.rating", -1)]).limit(count)
        movies = await movies_cur.to_list(length=None)
        for movie in movies:
             movie['_id']= str(movie['_id'])
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
                
