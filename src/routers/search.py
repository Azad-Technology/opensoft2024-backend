from fastapi import APIRouter, HTTPException
from uuid import uuid4
from src.db import Movies
from src.config import config
from promise import Promise
import json
import redis
from src.cache_system import r


router=APIRouter()

@router.get('/autosearch/{arg}')
async def auto_search_movie(arg: str):
    print(arg)
    key=arg+'@'+'auto'
    value = r.get(key)
    print(value)
    if value:
        return json.loads(value)
    pipeline = [
        {
            "$search": {
                "index":"auto-dave",
                "compound": {
                    "should": [
                        {
                            "autocomplete": {
                                "query": arg, 
                                "path": 'title',
                                "tokenOrder": "sequential",
                                "score":{
                                    "boost":{
                                        "value":5
                                    }
                                }
                            }
                        }, {
                            "autocomplete": {
                                "query": arg, 
                                "path": 'genres',
                                "tokenOrder": "sequential",
                                "score":{
                                    "boost":{
                                        "value":3
                                    }
                                }
                            }
                        }, {
                            "autocomplete": {
                                "query": arg, 
                                "path": 'cast',
                                "tokenOrder": "sequential",
                                "score":{
                                    "boost":{
                                        "value":2
                                    }
                                }
                            }
                        }, {
                            "autocomplete": {
                                "query": arg, 
                                "path": 'directors',
                                "tokenOrder": "sequential",
                                "score":{
                                    "boost":{
                                        "value":1
                                    }
                                }
                            }
                        }
                    ], 
                    "minimumShouldMatch": 1
                }
            }
        }, 
        {
            '$limit': 5
        }, 
        {
            '$project': {
                '_id': 1, 'title': 1,  "imdb":1,'score': {'$meta': 'searchScore'}
            }
        },
        { '$sort': { 'score': -1,'imdb': -1} }
    ]
    resultPromise= Movies.aggregate(pipeline)
    resultPromiseResult=[doc async for doc in resultPromise]
    [results] = await Promise.all([resultPromiseResult])
    for result in results:
        result["_id"] = str(result["_id"])
        
    json_result=json.dumps(results)
    
    r.set(key,json_result)
    print(results)
    return results


