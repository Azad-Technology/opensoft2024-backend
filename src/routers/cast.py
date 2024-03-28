from fastapi import APIRouter, HTTPException, status
from uuid import uuid4
from bson.objectid import ObjectId
from src.db import Movies, projects
from src import schemas
from src.config import config
import redis,json
from src.cache_system import r

from typing import Optional
from datetime import datetime

router = APIRouter()


@router.get('/cast/{cast_name}')
async def get_cast(cast_name: str, count:Optional[int]=10):
    try:
        if count<1:
           return []
        key=cast_name+'_'+str(count)+'@'+'cast'
        value = r.get(key)
        if value:
            ret=json.loads(value)
            for re in ret:
                if 'released' in re:
                    re['released']=str(re['released'])
            return ret
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



@router.get('/director/{director_name}')
async def get_director(director_name: str, count:Optional[int]=10):
    try:
        if count<1:
           return []
        key=director_name+'_'+str(count)+'@'+'director'
        value = r.get(key)
        if value:
            ret=json.loads(value)
            for re in ret:
                if 'released' in re:
                    re['released']=str(re['released'])
            return ret
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
