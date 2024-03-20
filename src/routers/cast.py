from fastapi import APIRouter, HTTPException
from uuid import uuid4
from bson.objectid import ObjectId
from src.db import Movies
from src import schemas
from src.config import config
import redis,json

r = redis.Redis(host='10.105.12.4',port=6379, decode_responses=True)

router = APIRouter()


@router.get('/cast/{cast_name}')
async def get_cast(cast_name: str):
    print(cast_name)
    key=cast_name+'@'+'cast'
    value = r.get(key)
    if value:
        return json.loads(value)
    projection={"_id":1, "title":1, "poster":1, "released": 1, "runtime":1, 'imdb':1, 'tomatoes':1}
    movies = await Movies.find({"cast": {"$in": [str(cast_name)]}}, projection).to_list(length=None)
    movies = await Movies.find({"cast": {"$in": [str(cast_name)]}}, projection).to_list(length=None)
    # movies = await movie_cursor  # Convert cursor to a list of documents
    print(movies)
    filtered_movies = []
    for movie in movies:
        if '_id' in movie:
            movie['_id']=str(movie['_id'])
        filtered_movies.append(movie)
    r.set(key,json.dumps(filtered_movies))
    return filtered_movies

@router.get('/director/{director_name}')
async def get_director(director_name: str):
    projection={"_id":1, "title":1, "poster":1, "released": 1, "runtime":1, 'imdb':1, 'tomatoes':1}
    key=director_name+'@'+'director'
    value = r.get(key)
    if value:
        return json.loads(value)
    movies = await Movies.find({"directors": {"$elemMatch": {"$eq": str(director_name)}}}, projection).to_list(length=None)
    # movies = await movie_cursor  # Convert cursor to a list of documents
    filtered_movies = []
    for movie in movies:
        if '_id' in movie:
            movie['_id']=str(movie['_id'])
        filtered_movies.append(movie)
    r.set(key,json.dumps(filtered_movies))
    return filtered_movies


