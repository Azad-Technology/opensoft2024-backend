from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies, projects
from src import schemas
from src.config import config
from bson.objectid import ObjectId
from pymongo import DESCENDING
from typing import Optional
<<<<<<< HEAD
from pymongo import DESCENDING
import redis,json
=======
from datetime import datetime
>>>>>>> c8d6d66f8dbe8ca9552efd03a9969b21428a52da

r = redis.Redis(host='10.105.12.4',port=6379, decode_responses=True)
router=APIRouter()


@router.get('/genre/{genre_name}/')
async def get_movie_by_genre(genre_name:str):
    try:
<<<<<<< HEAD
        projection={"_id":1, "title":1, "poster":1, "released": 1, "runtime":1, 'imdb':1, 'tomatoes':1}
        key=genre_name+'@'+'genre'
        value = r.get(key)
        if value:
            return json.loads(value)
        movies = await Movies.find({"genres": {'$in':[genre_name]}}, projection).to_list(length = None)
        movies = await Movies.find({"genres": {'$in':[genre_name]}}, projection).to_list(length = None)
=======
        projection=projects
        movies = await Movies.find({"genres": {'$in':[genre_name]}}, projection).limit(15).to_list(length = None)
>>>>>>> c8d6d66f8dbe8ca9552efd03a9969b21428a52da
        ret=[]
        
        if movies:
            for movie in movies:
                if '_id' in movie:
                    movie['_id']=str(movie['_id'])
                ret.append(movie)
<<<<<<< HEAD
            r.set(key,json.dumps(ret))
=======
                
>>>>>>> c8d6d66f8dbe8ca9552efd03a9969b21428a52da
        return ret
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@router.get('/genre_top_movies/{genre_name}/')     #name has to be changed
async def get_movies(genre_name:str,  count: Optional[int] = 10):
    
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
            {
                "$match": {
                    "genres": {'$regex': f'^{genre_name}$', '$options': 'i'},
                    "type": "movie"
                }
            },
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


@router.get('/genre_top_series/{genre_name}/')     #name has to be changed
async def get_movies_gts(genre_name:str,  count: Optional[int] = 10):
    
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
            {
                "$match": {
                    "genres": {'$regex': f'^{genre_name}$', '$options': 'i'},
                    "type": "series"
                }
            },
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
<<<<<<< HEAD
            r.set(key,json.dumps(movies))
=======
                 
>>>>>>> c8d6d66f8dbe8ca9552efd03a9969b21428a52da
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


