from fastapi import APIRouter, HTTPException
from uuid import uuid4
from bson.objectid import ObjectId
from src.db import Movies
from src import schemas
from src.config import config

router = APIRouter()


@router.get('/cast/{cast_name}')
async def get_cast(cast_name: str):
    projection={"_id":1, "title":1, "poster":1, "released": 1, "runtime":1, 'imdb':1, 'tomatoes':1}
    movie_cursor = Movies.find({"cast": {"$elemMatch": {"$eq": str(cast_name)}}}, projection)
    movies = await movie_cursor.to_list(length=None)  # Convert cursor to a list of documents
    filtered_movies = []
    for movie in movies:
        if '_id' in movie:
            movie['_id']=str(movie['_id'])
        filtered_movies.append(movie)
    if filtered_movies:
        return filtered_movies
    raise HTTPException(status_code=404, detail='Movie with Given Caste not found')

@router.get('/director/{director_name}')
async def get_director(director_name: str):
    projection={"_id":1, "title":1, "poster":1, "released": 1, "runtime":1, 'imdb':1, 'tomatoes':1}
    movie_cursor = Movies.find({"directors": {"$elemMatch": {"$eq": str(director_name)}}}, projection)
    movies = await movie_cursor.to_list(length=None)  # Convert cursor to a list of documents
    filtered_movies = []
    for movie in movies:
        if '_id' in movie:
            movie['_id']=str(movie['_id'])
        filtered_movies.append(movie)
    if filtered_movies:
        return filtered_movies
    raise HTTPException(status_code=404, detail='Movie with Given Caste not found')


