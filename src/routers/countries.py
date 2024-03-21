from fastapi import APIRouter, HTTPException, Request,Header, status
from uuid import uuid4

from src.db import Movies, countries_dict, projects
from src import schemas
from src.config import config
from bson.objectid import ObjectId
from typing import Optional
import redis,json
import geoip2.database
import pycountry
from datetime import datetime

r = redis.Redis(host='10.105.12.4',port=8045, decode_responses=True)
router=APIRouter()

@router.get('/countries_top/{country_name}/')       #region name case insensitive , count should be optional
async def get_movies_from_country(country_name:str, count: Optional[int] = 10):
    
    try:
        key=country_name+'_'+str(count)+'@'+'country_all'
        value = r.get(key)
        if value:
            return json.loads(value)
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
                    "countries": {'$regex': f'^{country_name}$', '$options': 'i'}
                }
            },
            {
                "$project": projects
            },
            {"$addFields": {
                "relevance_score": {
                    "$add": [
                        {"$multiply": ["$imdb.rating", 10]},
                        {"$multiply": [{"$abs": {"$subtract":[datetime.now().year , "$year"]}}, -7]},
                    ]
                }
            }},
            {
                '$sort': {'relevance_score':-1}
            },
            {
                "$limit": count
            }
        ]

        movies_cur = Movies.aggregate(pipeline)  # handle empty strings
        movies = await movies_cur.to_list(length=None)
        if movies:
            for movie in movies:
                 movie['_id']= str(movie['_id'])
            r.set(key,json.dumps(movies))
                
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_location_from_ip(ip_address):
    try:
        # Open the GeoLite2 database
        with geoip2.database.Reader('GeoLite2-Country.mmdb') as reader:
            # Query the database for location information based on the IP address
            response = reader.country(ip_address)
            # Extract relevant location details
            country = response.country.name
            return True,f"{country}"
    except Exception as e:
        return False,str(e)

def get_standardized_country_name(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        return country.name  # Returns the standardized country name
    except LookupError:
        return None
    

async def get_client_ip(request: Request):
    try:
        forwarded_for = request.headers.get("X-Forwarded-For")
        print(forwarded_for)
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0]
        else:
            # If X-Forwarded-For header is not present, fallback to request.client.host
            client_ip = request.client.host
        print(client_ip)
        return client_ip
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))

@router.get('/my_country/')
async def get_movie_in_my_region(request:Request, count: Optional[int]=10, ip: Optional[str]=None):
    try:
        if not ip:
            ip=await get_client_ip(request)
        if ip:
            status2, country=get_location_from_ip(ip)
            if status2:
                standard_country=get_standardized_country_name(country)
                print(standard_country)
                if standard_country:
                    if standard_country in countries_dict:
                        country_to_search=countries_dict[standard_country]
                        result=await get_movies_from_country(country_to_search, count)
                        return result
                    else:
                        return []
                else:
                    if country in countries_dict['_']:
                        result=await get_movies_from_country(country_to_search, count)
                        return result
                    else:
                        return []
            else:
                return []
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Address not found')
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/countries_top_movies/{country_name}/')       #region name case insensitive , count should be optional
async def get_movies(country_name:str, count: Optional[int] = 10):
    
    try:
        key=country_name+'_'+str(count)+'@'+'country_movies'
        value = r.get(key)
        if value:
            return json.loads(value)
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
                    "countries": {'$regex': f'^{country_name}$', '$options': 'i'},
                    "type": "movie"
                }
            },
            {
                "$project": projects
            },
            {"$addFields": {
                "relevance_score": {
                    "$add": [
                        {"$multiply": ["$imdb.rating", 10]},
                        {"$multiply": [{"$abs": {"$subtract":[datetime.now().year , "$year"]}}, -7]},
                    ]
                }
            }},
            {
                '$sort': {'relevance_score':-1}
            },
            {
                "$limit": count
            }
        ]

        movies_cur = Movies.aggregate(pipeline)  # handle empty strings
        movies = await movies_cur.to_list(length=None)
        if movies:
            for movie in movies:
                movie['_id']= str(movie['_id'])
                if 'released' in movie:
                    movie['released']=movie['released'].strftime('%Y-%m-%d %H:%M:%S')
            r.set(key,json.dumps(movies))
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
                

@router.get('/countries_top_series/{country_name}/')       #region name case insensitive , count should be optional
async def get_movies(country_name:str, count: Optional[int] = 10):
    
    try:
        key=country_name+'_'+str(count)+'@'+'country_series'
        value = r.get(key)
        if value:
            return json.loads(value)
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
                    "countries": {'$regex': f'^{country_name}$', '$options': 'i'},
                    "type": "series"
                }
            },
            {
                "$project": projects
            },
            {"$addFields": {
                "relevance_score": {
                    "$add": [
                        {"$multiply": ["$imdb.rating", 10]},
                        {"$multiply": [{"$abs": {"$subtract":[datetime.now().year , "$year"]}}, -7]},
                    ]
                }
            }},
            {
                '$sort': {'relevance_score':-1}
            },
            {
                "$limit": count
            }
        ]

        movies_cur = Movies.aggregate(pipeline)  # handle empty strings
        movies = await movies_cur.to_list(length=None)
        if movies:
            for movie in movies:
                movie['_id']= str(movie['_id'])
                if 'released' in movie:
                    movie['released']=movie['released'].strftime('%Y-%m-%d %H:%M:%S')
            r.set(key,json.dumps(movies))
            return movies
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
