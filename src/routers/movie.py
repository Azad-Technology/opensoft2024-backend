from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies, Comments, projects
from src import schemas
from src.config import config
from bson.objectid import ObjectId
from typing import Optional, List
import redis,json
import pycountry
import json
from pymongo import TEXT
from src.cache_system import r
from datetime import datetime, timezone

router = APIRouter()


@router.get('/movies/{movie_id}')
async def get_movie_by_id(movie_id: str):
    try:
        key=movie_id+'@'+'movie_by_id'
        value = r.get(key)
        if value:
            ret=json.loads(value)
            for re in ret:
                if 'released' in re:
                    re['released']=str(re['released'])
            return ret
        movie = await Movies.find_one({'_id': ObjectId(movie_id)},{'tomatoes':0})
        if movie:
            if '_id' in movie:
                movie['_id'] = str(movie['_id'])
            r.set(key,json.dumps([movie]))
            return [movie]
        return []
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))



@router.get('/top_series')     #name has to be changed
async def get_series_top( count: Optional[int] = 10):
    
    try:
        if count<1:
           return []
        default_value = 2
        key='@top_series'+str(count)
        value = r.get(key)
        if value:
            ret=json.loads(value)
            for re in ret:
                if 'released' in re:
                    re['released']=str(re['released'])
            return ret
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
            r.set(key,json.dumps(movies))
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/top_movies')     #name has to be changed
async def get_top_movies( count: Optional[int] = 10):
    
    try:
        if count<1:
           return []
        default_value = 2
        key='@top_movies'+str(count)
        value = r.get(key)
        if value:
            ret=json.loads(value)
            for re in ret:
                if 'released' in re:
                    re['released']=str(re['released'])
            return ret
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
            r.set(key,json.dumps(movies))
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/movies/{movie_id}/comments')
async def get_comments_by_movieid(movie_id : str, count: Optional[int] = 10):
    try:
        if count<1:
            return []
        key=f"comment:{movie_id}:{count}"
        value = r.get(key)
        if value:
            ret=json.loads(value)
            for re in ret:
                if 'released' in re:
                    re['released']=str(re['released'])
            print("Cached")
            return ret
        pipeline=[
        {
            "$match": {
            "movie_id": ObjectId(movie_id)
            }
        },
        {
            "$sort": {
            "date": -1
            }
        },
        {
            "$limit": count
        }
        ]

        comments=await Comments.aggregate(pipeline).to_list(length=None)
        for comment in comments:
            comment['_id']=str(comment['_id'])
            comment['movie_id']=str(comment['movie_id'])
            comment['date']=comment['date'].strftime('%Y-%m-%d %H:%M:%S')
        r.set(key,json.dumps(comments))
        return comments
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))
    
    
def calculate_comment_age(comment_date):
    
    current_datetime = datetime.now(timezone.utc)
    
    comment_datetime = comment_date.replace(tzinfo=timezone.utc)
    
    age_delta = current_datetime - comment_datetime

    
    years = age_delta.days // 365
    months = (age_delta.days % 365) // 30
    days = age_delta.days % 30
    hours = age_delta.seconds // 3600
    minutes = (age_delta.seconds % 3600) // 60
    seconds = age_delta.seconds % 60

    # Construct the age string
    age_string = ""
    if years >= 100:
        age_string = "more than a century"
    elif years > 0:
        age_string += f"{years} {'year' if years == 1 else 'years'}"
    elif months > 0:
        age_string += f"{months} {'month' if months == 1 else 'months'}"
    elif days > 0:
        age_string += f"{days} {'day' if days == 1 else 'days'}"
    elif hours > 0:
        age_string += f"{hours} {'hour' if hours == 1 else 'hours'}"
    elif minutes > 0:
        age_string += f"{minutes} {'minute' if minutes == 1 else 'minutes'}"
    else:
        age_string += f"{seconds} {'second' if seconds == 1 else 'seconds'}"

    return age_string + " ago"


@router.get('/recent_comments')
async def get_recent_comments(count: Optional[int] = 10):
    try:
        if count<1:
            return []
        movies=[]
        key=f"recent_comments:{count}"
        value = r.get(key)
        if value:
            ret=json.loads(value)
            for re in ret:
                if 'released' in re:
                    re['released']=str(re['released'])
            print("Cached")
            return ret
        pipeline = [
        {
            "$sort": {
                "date": -1
            }
        },
        {
            "$limit": count
        }
        ]

        
        comments= await Comments.aggregate(pipeline).to_list(length=None)
        for comment in comments:
            comment['_id']=str(comment['_id'])
            comment['movie_id']=str(comment['movie_id'])
            comment['ago']=calculate_comment_age(comment['date'])
            comment['date']=comment['date'].strftime('%Y-%m-%d %H:%M:%S')
            movies.append(comment['movie_id'])
        movies2= await get_movies_by_ids(movies)
        for i, movie in enumerate(movies2):
            comments[i]['movie_name']=movie['title']
        r.set(key,json.dumps(comments))
        return comments
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))

@router.get('/recent_movies')
async def get_movies_recent( count: Optional[int] = 10):
    try:
        if count<1:
           return []
        key=str(count)+'@'+'recents'
        value = r.get(key)
        if value:
            ret=json.loads(value)
            for re in ret:
                if 'released' in re:
                    re['released']=str(re['released'])
            print("Cached")
            return ret
        projection=projects
        projection['released']=1
        pipeline=[{
                "$addFields": {
                    "imdb.rating": {
                        "$cond": [
                            { "$eq": ["$imdb.rating", ""] },
                            2,
                            "$imdb.rating"
                        ]
                    }
                }
            },
            {
                '$sort':{
                    "released":-1
                }
            },
            {"$limit":count},
            {"$project":projection}
        ]
        movies = await Movies.aggregate(pipeline).to_list(length=None)
        for movie in movies:
            movie['_id']= str(movie['_id'])
        r.set(key,json.dumps(movies))
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/movies/{movie_id}/related_movies')
async def get_related_movies(movie_id: str, count: Optional[int]=10):

    try:
        if count<=0:
            return []
        key=movie_id+'_'+str(count)+'@'+'related_movies'
        value = r.get(key)
        if value:
            ret=json.loads(value)
            for re in ret:
                if 'released' in re:
                    re['released']=str(re['released'])
            print("Cached")
            return ret
        movie = await Movies.find_one({'_id': ObjectId(movie_id)})
        if movie:
            if '_id' in movie:
                movie['_id'] = str(movie['_id'])
        else:
            return []
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
                "backdrop_path":1,
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
        if similar_movies:
            r.set(key,json.dumps(similar_movies))
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
                "backdrop_path":1,
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
        r.set(key,json.dumps(similar_movies))
        return similar_movies
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/movies_list")
async def get_movies_by_ids(movies_ids: List[str]):
    try:
        
        bson_movies_ids = [ObjectId(oid) for oid in movies_ids]

        
        movies = await Movies.find({"_id": {"$in": bson_movies_ids}}, projects).to_list(length=None)

        for movie in movies:
            movie['_id']=str(movie['_id'])
        movies_dict = {str(movie['_id']): movie for movie in movies}
        ret = [movies_dict[str(movie_id)] if (str(movie_id) in movies_dict) else {'_id': str(movie_id), 'title': ''} for movie_id in movies_ids]

        return ret
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))