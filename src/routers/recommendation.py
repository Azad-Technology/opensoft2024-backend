from src.utils.recommend import get_recommendations
from src import schemas
from fastapi import APIRouter
from src.db import Movies

router = APIRouter()

sample_data = [
    "573a1392f29313caabcd9ca6",
]


@router.get("/recommend")
async def recommend_movie():
    recommended_movies = await get_recommendations(sample_data, 10)
    # print(recommended_movies)
    return recommended_movies
