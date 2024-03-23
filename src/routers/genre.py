from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies, projects
from src import schemas
from src.config import config
from bson.objectid import ObjectId
from pymongo import DESCENDING
from typing import Optional
from pymongo import DESCENDING
import redis,json
from datetime import datetime

r = redis.Redis(host='10.105.12.4',port=8045, decode_responses=True)
router=APIRouter()




@router.get('/genre_top/{genre_name}/')     #name has to be changed
async def get_movies_gtop(genre_name:str,  count: Optional[int] = 10):
    
    try:
        if count<1:
           return []
        default_value = 2
        key=genre_name+'_'+str(count)+'@'+'genre_top'
        value = r.get(key)
        if value:
            return json.loads(value)
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
            {
                "$match": {
                    "genres": {'$regex': f'^{genre_name}$', '$options': 'i'}
                }
            },
            {
                "$project": projects
            },
            {"$addFields": {
                "relevance_score": {
                    "$add": [
                        {"$multiply": ["$imdb.rating", 10]},
                        {"$multiply": [{"$abs": {"$subtract":[datetime.now().year , "$year"]}}, -7]},
                    ]
                }
            }},
            {
                '$sort': {'relevance_score':-1}
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
            r.set(key,json.dumps(movies))
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/genre_top_movies/{genre_name}/')     #name has to be changed
async def get_movies(genre_name:str,  count: Optional[int] = 10):
    
    try:
        if count<1:
           return []
        default_value = 2
        key=genre_name+'_'+str(count)+'@'+'genre_top_movies'
        value = r.get(key)
        if value:
            return json.loads(value)
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
            {
                "$match": {
                    "genres": {'$regex': f'^{genre_name}$', '$options': 'i'},
                    "type": "movie"
                }
            },
            {
                "$project": projects
            },
            {"$addFields": {
                "relevance_score": {
                    "$add": [
                        {"$multiply": ["$imdb.rating", 10]},
                        {"$multiply": [{"$abs": {"$subtract":[datetime.now().year , "$year"]}}, -7]},
                    ]
                }
            }},
            {
                '$sort': {'relevance_score':-1}
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
            r.set(key,json.dumps(movies))
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/genre_top_series/{genre_name}/')     #name has to be changed
async def get_movies_gts(genre_name:str,  count: Optional[int] = 10):
    
    try:
        if count<1:
           return []
        default_value = 2
        key=genre_name+'_'+str(count)+'@'+'genre_top_series'
        value = r.get(key)
        if value:
            return json.loads(value)
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
            {
                "$match": {
                    "genres": {'$regex': f'^{genre_name}$', '$options': 'i'},
                    "type": "series"
                }
            },
            {
                "$project": projects
            },
            {"$addFields": {
                "relevance_score": {
                    "$add": [
                        {"$multiply": ["$imdb.rating", 10]},
                        {"$multiply": [{"$abs": {"$subtract":[datetime.now().year , "$year"]}}, -7]},
                    ]
                }
            }},
            {
                '$sort': {'relevance_score':-1}
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
            r.set(key,json.dumps(movies))
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


