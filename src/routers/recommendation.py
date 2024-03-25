from src.utils.recommend import get_recommendations
from fastapi import APIRouter, Depends, HTTPException, Request, status, Security,Depends,Response 
from src import schemas
from fastapi import APIRouter
from src.db import Movies
from src.routers.auth import get_current_user
router = APIRouter()


@router.get("/recommend")
async def recommend_movie(user: dict = Depends(get_current_user)):
    if 'fav' not in user:
        liked_movies = []
    else :
        liked_movies = user['fav']
    try:
        if len(liked_movies) == 0:
            movies = await Movies.find({}, {"_id":1}).sort([("imdb.rating", -1)]).limit(5).to_list(5)
            for movie in movies:
                liked_movies.append(str(movie["_id"]))
        recommended_movies = await get_recommendations(liked_movies, 17)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return recommended_movies
