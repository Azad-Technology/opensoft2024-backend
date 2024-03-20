from fastapi import APIRouter, HTTPException
from uuid import uuid4
from bson.objectid import ObjectId
from src.db import Movies, projects
from src import schemas
from src.config import config
<<<<<<< HEAD
import redis,json

r = redis.Redis(host='10.105.12.4',port=6379, decode_responses=True)
=======
from typing import Optional
>>>>>>> c8d6d66f8dbe8ca9552efd03a9969b21428a52da

router = APIRouter()


<<<<<<< HEAD
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
=======
@router.get('/cast/{cast_name}/')
async def get_cast(cast_name: str, count:Optional[int]=10):
    try:
        if count<1:
           return []
        default_value = 2

        pipeline = [
            {
                "$addFields": {
                    "imdb.rating": {
                        "$cond": [
                            { "$eq": ["$imdb.rating", ""] },
                            default_value,
                            "$imdb.rating"
                        ]
                    }
                }
            },
            {"$match": {
                "cast": {
                    "$elemMatch": {
                        "$regex": f'^{cast_name}$',
                        "$options": "i"
                    }
                }
            }},
            {
                "$project": projects
            },
            {
                "$sort": {"imdb.rating": -1}
            },
            {
                "$limit": count
            }
        ]

        movies_cur = Movies.aggregate(pipeline)
        movies = await movies_cur.to_list(length=None)
        if movies:
            for movie in movies:
                movie['_id']= str(movie['_id'])
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
>>>>>>> c8d6d66f8dbe8ca9552efd03a9969b21428a52da



@router.get('/director/{director_name}/')
async def get_director(director_name: str, count:Optional[int]=10):
    try:
        if count<1:
           return []
        default_value = 2

        pipeline = [
            {
                "$addFields": {
                    "imdb.rating": {
                        "$cond": [
                            { "$eq": ["$imdb.rating", ""] },
                            default_value,
                            "$imdb.rating"
                        ]
                    }
                }
            },
            {"$match": {
                "directors": {
                    "$elemMatch": {
                        "$regex": f'^{director_name}$',
                        "$options": "i"
                    }
                }
            }}
            ,
            {
                "$project": projects
            },
            {
                "$sort": {"imdb.rating": -1}
            },
            {
                "$limit": count
            }
        ]

        movies_cur = Movies.aggregate(pipeline)
        movies = await movies_cur.to_list(length=None)
        if movies:
            for movie in movies:
                movie['_id']= str(movie['_id'])
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
