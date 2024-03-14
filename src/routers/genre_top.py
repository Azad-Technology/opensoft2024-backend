from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies
from src import schemas
from src.config import config
from bson.objectid import ObjectId
from typing import Optional
router=APIRouter()

@router.get('/genre_top/{genre_name}')     #name has to be changed
async def get_movies(genre_name:str,  count: Optional[int] = 10):
    
    try:
        if count<1:
           raise HTTPException(status_code=404, detail="Please enter a valid count of movies to be fetched ")
        projection={"_id":1, "title":1, "poster":1, "released": 1, "runtime":1, 'imdb':1, 'tomatoes':1}
        movies_cur = Movies.find({"imdb.rating":{'$ne':''},"genres": {'$regex': f'^{genre_name}$', '$options': 'i'}},projection).sort([("imdb.rating", -1)]).limit(count)
        movies = await movies_cur.to_list(length=None)
        if movies:
            for movie in movies:
                 movie['_id']= str(movie['_id'])
            return movies
        raise HTTPException(status_code=404, detail="No movie found for this genre")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
                
