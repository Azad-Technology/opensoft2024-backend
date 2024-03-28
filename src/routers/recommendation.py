from src.utils.recommend import get_recommendations
from fastapi import APIRouter, Depends, HTTPException, Request, status, Security,Depends,Response 
from src import schemas
from fastapi import APIRouter
from src.db import Movies
from src.routers.auth import get_current_user
from src.cache_system import r
import json

router = APIRouter()


@router.get("/recommend")
async def recommend_movie(user: dict = Depends(get_current_user)):
    if 'fav' not in user:
        liked_movies = []
    else :
        liked_movies = user['fav']
    try:
        key = 'recommend_'

        if len(liked_movies) == 0:
            key += 'default'
            value = r.get(key)
            if value:
                return json.loads(value)
            movies = await Movies.find({}, {"_id":1}).sort([("imdb.rating", -1)]).limit(5).to_list(5)
            for movie in movies:
                liked_movies.append(str(movie["_id"]))
            recommend_movies = await get_recommendations(liked_movies, 17)
            r.set(key, json.dumps(recommend_movies))
            return recommend_movies

        else:
            key += '_'.join(liked_movies)
            value = r.get(key)
            if value:
                return json.loads(value)
            recommended_movies = await get_recommendations(liked_movies, 17)
            r.set(key, json.dumps(recommended_movies))
            return recommended_movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
