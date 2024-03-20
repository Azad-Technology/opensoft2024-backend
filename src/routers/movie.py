from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies
from src import schemas
from src.config import config
from bson.objectid import ObjectId
from typing import Optional
import redis,json

r = redis.Redis(host='10.105.12.4',port=6379, decode_responses=True)

router = APIRouter()




@router.get('/movies/{movie_id}')
async def get_movie(movie_id: str):
    # projection={"_id":1, "title":1, "poster":1, "released": 1, "runtime":1, 'imdb':1, 'tomatoes':1}
    key=movie_id+'@'+'movie_by_id'
    value = r.get(key)
    if value:
        return json.loads(value)
    movie = await Movies.find_one({'_id': ObjectId(movie_id)})
    if movie:
        if '_id' in movie:
            movie['_id'] = str(movie['_id'])
        r.set(key,json.dumps([movie]))
        return [movie]
    return []

@router.get('/imdb/')
async def get_movies( count: Optional[int] = 10):
    try:
        if count<1:
           return []
        key=str(count)+'@'+'imdb'
        value = r.get(key)
        if value:
            return json.loads(value)
        projection={"_id":1, "title":1, "poster":1, "released": 1, "runtime":1, 'imdb':1, 'tomatoes':1}
        movies_cur = Movies.find({"imdb.rating":{'$ne':''}},projection).sort([("imdb.rating", -1)]).limit(count)
        movies = await movies_cur.to_list(length=None)
        for movie in movies:
             movie['_id']= str(movie['_id'])
        r.set(key,json.dumps(movies))
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
                
