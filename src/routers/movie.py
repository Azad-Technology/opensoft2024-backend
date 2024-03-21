from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies, Comments, projects
from src import schemas
from src.config import config
from bson.objectid import ObjectId
from typing import Optional
import pycountry
import json
from pymongo import TEXT


router = APIRouter()




@router.get('/movies/{movie_id}')
async def get_movie(movie_id: str):
    # projection={"_id":1, "title":1, "poster":1, "released": 1, "runtime":1, 'imdb':1, 'tomatoes':1}
    try:
        movie = await Movies.find_one({'_id': ObjectId(movie_id)},{'tomatoes':0})
        if movie:
            if '_id' in movie:
                movie['_id'] = str(movie['_id'])
            if 'released' in movie:
                movie['released']=movie['released'].strftime('%Y-%m-%d %H:%M:%S')
            return [movie]
        return []
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))



@router.get('/top_series/')     #name has to be changed
async def get_series( count: Optional[int] = 10):
    
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
                
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/top_movies/')     #name has to be changed
async def get_top_movies( count: Optional[int] = 10):
    
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
                if 'released' in movie:
                    movie['released']=movie['released'].strftime('%Y-%m-%d %H:%M:%S')
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/movies/{movie_id}/comments/')
async def get_comments(movie_id : str, count: Optional[int] = 10):
    try:
        if count<1:
            return []
        comments=await Comments.find({'movie_id':ObjectId(movie_id)}).sort([("date", -1)]).limit(count).to_list(length=None)
        for comment in comments:
            comment['_id']=str(comment['_id'])
            comment['movie_id']=str(comment['movie_id'])
            comment['date']=comment['date'].strftime('%Y-%m-%d %H:%M:%S')
        return comments
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))
    
@router.get('/recent_comments/')
async def get_recent_comments(count: Optional[int] = 10):
    try:
        if count<1:
            return []
        comments=await Comments.find().sort([("date", -1)]).limit(count).to_list(length=None)
        for comment in comments:
            comment['_id']=str(comment['_id'])
            comment['movie_id']=str(comment['movie_id'])
            comment['date']=comment['date'].strftime('%Y-%m-%d %H:%M:%S')
        return comments
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))

@router.get('/recent_movies/')
async def get_movies( count: Optional[int] = 10):
    try:
        if count<1:
           return []
        projection=projects
        projection['released']=1
        movies_cur = Movies.find({"imdb.rating":{'$ne':''}},projection).sort([("released", -1)]).limit(count)
        movies = await movies_cur.to_list(length=None)
        for movie in movies:
            movie['_id']= str(movie['_id'])
            if 'released' in movie:
                movie['released']=movie['released'].strftime('%Y-%m-%d %H:%M:%S')
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/movies/{movie_id}/related_movies/')
async def get_related_movies(movie_id: str, count: Optional[int]=10):

    try:
        movie = await Movies.find_one({'_id': ObjectId(movie_id)})
        if movie:
            if '_id' in movie:
                movie['_id'] = str(movie['_id'])
            if 'released' in movie:
                movie['released']=movie['released'].strftime('%Y-%m-%d %H:%M:%S')
        fullplot=movie.get("fullplot","")
        default_value=2
        pipeline=[
            {"$match": {"_id": {"$ne": ObjectId(movie_id)}, "$text": {"$search": fullplot}, "type": movie.get("type",'')}},
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
            {"$addFields": {
                "title_similarity": {
                    "$let": {
                        "vars": {
                            "title_words": {"$split": [{"$toLower": "$title"}, " "]},
                            "movie_title_words": {"$split": [{"$toLower": movie.get("title", "")}, " "]}
                        },
                        "in": {
                            "$divide": [
                                {"$size": {"$setIntersection": ["$$title_words", "$$movie_title_words"]}},
                                1
                            ]
                        }
                    }
                }
            }},
            {"$project": {
                "title": 1,
                "poster": 1,
                "released": 1,
                "runtime": 1,
                "imdb": 1,
                
                "genres": 1,
                "poster_path":1,
                'year':1,
                'plot':1,
                'languages':1,
                'fullplot':1,
                'backdrop_path':1,
                'languages_intersection':{
                    "$cond": {
                        "if": {"$and": [{"$isArray": ["$languages"]}, {"$isArray": [movie.get("languages", [])]}]},
                        "then": {"$size": {"$setIntersection": ["$languages", movie.get("languages", [])]}},
                        "else": 0  # Handle null or empty array
                    }
                },
                "genre_intersection": {
                    "$cond": {
                        "if": {"$and": [{"$isArray": ["$genres"]}, {"$isArray": [movie.get("genres", [])]}]},
                        "then": {"$size": {"$setIntersection": ["$genres", movie.get("genres", [])]}},
                        "else": 0  # Handle null or empty array
                    }
                },
                "cast_intersection": {
                    "$cond": {
                        "if": {"$and": [{"$isArray": ["$cast"]}, {"$isArray": [movie.get("cast", [])]}]},
                        "then": {"$size": {"$setIntersection": ["$cast", movie.get("cast", [])]}},
                        "else": 0  # Handle null or empty array
                    }
                },
                "director_intersection": {
                    "$cond": {
                        "if": {"$and": [{"$isArray": ["$directors"]}, {"$isArray": [movie.get("directors", [])]}]},
                        "then": {"$size": {"$setIntersection": ["$directors", movie.get("directors", [])]}},
                        "else": 0  # Handle null or empty array
                    }
                },
                "region_intersection": {
                    "$cond": {
                        "if": {"$and": [{"$isArray": ["$countries"]}, {"$isArray": [movie.get("countries", [])]}]},
                        "then": {"$size": {"$setIntersection": ["$countries", movie.get("countries", [])]}},
                        "else": 0  # Handle null or empty array
                    }
                },
                "relevance_score1": {'$divide':[{"$meta": "textScore"}, {'$add':[len(movie.get('fullplot', ' ')), {'$strLenCP': {"$ifNull": ["$fullplot", " "]}}]}]},
                "title_similarity": 1
            }},
            {"$addFields": {
                "relevance_score": {
                    "$add": [
                        {'$min':[{"$multiply": ["$genre_intersection", 30]},80]},
                        {"$multiply": ["$cast_intersection", 45]},
                        {"$multiply": ["$director_intersection", 36]},
                        {"$multiply": ["$region_intersection", 70]},
                        {'$min':[{"$multiply": ["$languages_intersection", 50]},70]},
                        {"$multiply": ["$relevance_score1", 2000]},
                        {"$multiply": ["$title_similarity", 25]},
                        {"$multiply": ["$imdb.rating", 4]},
                        {"$multiply": [{"$abs": {"$subtract":[movie.get('year', 2000) , "$year"]}}, -1]},
                        
                    ]
                }
            }},
            {"$sort": {"relevance_score": -1}},
            {"$limit": count}
        ]

        similar_movies = await Movies.aggregate(pipeline).to_list(length=None)
        for movie_ in similar_movies:
            if movie_:
                if '_id' in movie_:
                    movie_['_id'] = str(movie_['_id'])
                if 'released' in movie_:
                    movie_['released']=movie_['released'].strftime('%Y-%m-%d %H:%M:%S')
        if similar_movies:
            return similar_movies
        # print("Not found")
        pipeline=[
            {"$match": {"_id": {"$ne": ObjectId(movie_id)},"type": movie.get("type",'')}},
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
            {"$addFields": {
                "title_similarity": {
                    "$let": {
                        "vars": {
                            "title_words": {"$split": [{"$toLower": "$title"}, " "]},
                            "movie_title_words": {"$split": [{"$toLower": movie.get("title", "")}, " "]}
                        },
                        "in": {
                            "$divide": [
                                {"$size": {"$setIntersection": ["$$title_words", "$$movie_title_words"]}},
                                1
                            ]
                        }
                    }
                }
            }},
            {"$project": {
                "title": 1,
                "poster": 1,
                "released": 1,
                "runtime": 1,
                "imdb": 1,
                "genres": 1,
                "poster_path":1,
                'year':1,
                'plot':1,
                'languages':1,
                'backdrop_path':1,
                'languages_intersection':{
                    "$cond": {
                        "if": {"$and": [{"$isArray": ["$languages"]}, {"$isArray": [movie.get("languages", [])]}]},
                        "then": {"$size": {"$setIntersection": ["$languages", movie.get("languages", [])]}},
                        "else": 0  # Handle null or empty array
                    }
                },
                "genre_intersection": {
                    "$cond": {
                        "if": {"$and": [{"$isArray": ["$genres"]}, {"$isArray": [movie.get("genres", [])]}]},
                        "then": {"$size": {"$setIntersection": ["$genres", movie.get("genres", [])]}},
                        "else": 0  # Handle null or empty array
                    }
                },
                "cast_intersection": {
                    "$cond": {
                        "if": {"$and": [{"$isArray": ["$cast"]}, {"$isArray": [movie.get("cast", [])]}]},
                        "then": {"$size": {"$setIntersection": ["$cast", movie.get("cast", [])]}},
                        "else": 0  # Handle null or empty array
                    }
                },
                "director_intersection": {
                    "$cond": {
                        "if": {"$and": [{"$isArray": ["$directors"]}, {"$isArray": [movie.get("directors", [])]}]},
                        "then": {"$size": {"$setIntersection": ["$directors", movie.get("directors", [])]}},
                        "else": 0  # Handle null or empty array
                    }
                },
                "region_intersection": {
                    "$cond": {
                        "if": {"$and": [{"$isArray": ["$countries"]}, {"$isArray": [movie.get("countries", [])]}]},
                        "then": {"$size": {"$setIntersection": ["$countries", movie.get("countries", [])]}},
                        "else": 0  # Handle null or empty array
                    }
                },
                "relevance_score1": {"$literal": 0},
                "title_similarity": 1
            }},
            {"$addFields": {
                "relevance_score": {
                    "$add": [
                        {'$min':[{"$multiply": ["$genre_intersection", 30]},80]},
                        {"$multiply": ["$cast_intersection", 45]},
                        {"$multiply": ["$director_intersection", 36]},
                        {"$multiply": ["$region_intersection", 70]},
                        {'$min':[{"$multiply": ["$languages_intersection", 50]},70]},
                        {"$multiply": ["$relevance_score1", 2000]},
                        {"$multiply": ["$title_similarity", 25]},
                        {"$multiply": ["$imdb.rating", 4]},
                        {"$multiply": [{"$abs": {"$subtract":[movie.get('year', 2000) , "$year"]}}, -1]}, 
                    ]
                }
            }},
            {"$sort": {"relevance_score": -1}},
            {"$limit": count}
        ]
        similar_movies = await Movies.aggregate(pipeline).to_list(length=None)
        for movie in similar_movies:
            if movie:
                if '_id' in movie:
                    movie['_id'] = str(movie['_id'])
                if 'released' in movie:
                    movie['released']=movie['released'].strftime('%Y-%m-%d %H:%M:%S')
        return similar_movies
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))