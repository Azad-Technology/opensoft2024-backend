from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies
from src import schemas
from src.config import config
from bson.objectid import ObjectId
from pymongo import DESCENDING

router=APIRouter()


@router.get('/genre/{genre_name}')
async def get_movie_by_genre(genre_name:str):
    try:
        projection={"_id":1, "title":1, "poster":1, "released": 1, "runtime":1, 'imdb':1, 'tomatoes':1}
        movies = await Movies.find({"genres": {'$in':[genre_name]}}).limit(5).to_list(length = None)
        ret=[]
        
        if movies:
            for movie in movies:
                if '_id' in movie:
                    movie['_id']=str(movie['_id'])
                ret.append(movie)
        return ret
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
