from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies
from src import schemas
from src.config import config
from bson.objectid import ObjectId

router=APIRouter()

@router.get('/imdb/{count}')
async def get_movies(count:int):
    try:
        movies_cur = Movies.find({"imdb.rating":{'$ne':''}}).sort([("imdb.rating", -1)]).limit(count)
        movies = await movies_cur.to_list(length=None)
        for movie in movies:
             movie['_id']= str(movie['_id'])
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
                
