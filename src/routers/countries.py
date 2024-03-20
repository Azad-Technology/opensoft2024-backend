from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies
from src import schemas
from src.config import config
from bson.objectid import ObjectId
from typing import Optional
import redis,json

r = redis.Redis(host='10.105.12.4',port=6379, decode_responses=True)
router=APIRouter()

@router.get('/countries_top/{country_name}')       #region name case insensitive , count should be optional
async def get_movies(country_name:str, count: Optional[int] = 10):
    
    try:
        key=country_name+'_'+str(count)+'@'+'country'
        value = r.get(key)
        if value:
            return json.loads(value)
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
            {
                "$match": {
                    "countries": {'$regex': f'^{country_name}$', '$options': 'i'}
                }
            },
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

        movies_cur = Movies.aggregate(pipeline)  # handle empty strings
        movies = await movies_cur.to_list(length=None)
        if movies:
            for movie in movies:
                 movie['_id']= str(movie['_id'])
            r.set(key,json.dumps(movies))
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
                
