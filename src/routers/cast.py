from fastapi import APIRouter, HTTPException
from uuid import uuid4
from bson.objectid import ObjectId
from src.db import Movies
from src import schemas
from src.config import config
from typing import Optional

router = APIRouter()


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
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "poster": 1,
                    "released": 1,
                    "runtime": 1,
                    "imdb": 1,
                    "tomatoes": 1
                }
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
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "poster": 1,
                    "released": 1,
                    "runtime": 1,
                    "imdb": 1,
                    "tomatoes": 1
                }
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
