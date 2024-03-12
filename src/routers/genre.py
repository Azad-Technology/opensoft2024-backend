from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies
from src import schemas
from src.config import config
from bson.objectid import ObjectId

router=APIRouter()


@router.get('/genre/{genre_name}')
async def get_movie_by_genre(genre_name:str):
    try:
        
        movies_cur = Movies.find({"genres": {'$in':[genre_name]}}).limit(10)
        movies=await movies_cur.to_list(length=None)
        ret=[]
        
        if movies:
            for movie in movies:
                if '_id' in movie:
                    movie['_id']=str(movie['_id'])
                ret.append(movie)
        if ret:
            return ret
        raise HTTPException(status_code=404, detail="No movie found for this genre")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
