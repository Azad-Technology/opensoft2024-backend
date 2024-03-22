from src.utils.recommend import get_recommendations
from src import schemas
from fastapi import APIRouter
from src.db import Movies

router = APIRouter()

sample_data = [
    "573a1392f29313caabcd9ca6",
    "573a1390f29313caabcd587d",
    "573a1392f29313caabcd9c1b",
    "573a1392f29313caabcda6b3",
    "573a1390f29313caabcd4eaf",
    "573a1391f29313caabcd9688",
    "573a1392f29313caabcd980d",
    "573a1391f29313caabcd6f98",
    "573a1391f29313caabcd935e",
    "573a1392f29313caabcda70a"
]

@router.get("/recommend")
async def recommend_movie():
    recommended_movies = await get_recommendations(sample_data, 10)
    # print(recommended_movies)
    return {"message": "Ok"}
