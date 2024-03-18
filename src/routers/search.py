from fastapi import APIRouter, HTTPException
from uuid import uuid4

from src.db import Movies
from src.config import config
from promise import Promise
import json
import redis

r = redis.Redis(host=config['REDIS_URL'], password=config['PASSWORD_REDIS'],port=config['TTL_PORT'], decode_responses=True)
router=APIRouter()

@router.get('/autosearch/{arg}')
async def auto_search_movie(arg: str):
    print(arg)
    key=arg+'auto'
    value = r.get(key)
    print(value)
    if value:
        return value
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
                '_id': 0, 'title': 1,  "imdb":1,'score': {'$meta': 'searchScore'}
            }
        },
        { '$sort': { 'score': -1,'imdb': -1} }
    ]
    resultPromise= Movies.aggregate(pipeline)
    resultPromiseResult=[doc async for doc in resultPromise]
    [result] = await Promise.all([resultPromiseResult])
    json_result=json.dumps(result)
    
    r.set(key,json_result)
    print(result)
    return json_result

@router.get('/fuzzysearch/{arg}')
async def fuzzy_search_movie(arg: str,tag: str):
    key=arg+'fuzzy'+tag
    value = r.get(key)
    if value:
        return value
    pipeline = [
        {
      '$search': {
        'index': "movie_index",
        'text': {
          'query': arg,
          'path': tag,
          'fuzzy':{},
          'score': {
            'boost': {
              'value': 5
            }
          }
        }
      }
    },
    { '$limit': 5 },
    { '$project': { '_id': 1, 'title': 1 }} 
    ]
    pipeline2=[
    {
      '$search': {
        'index': "movie_index",
        "compound": {
            "should": [
                {
                  "text": {
                    "query": arg, 
                    "path": 'title',
                    "fuzzy":{},
                    "score":{
                      "boost":{
                        "value":5
                      }
                    }
                  }
                }, {
                        "text": {
                            "query": arg, 
                            "path": 'genres',
                            "fuzzy":{},
                            "score":{
                              "boost":{
                                "value":3
                              }
                            }
                        }
                    }, {
                        "text": {
                            "query": arg, 
                            "path": 'cast',
                            "fuzzy":{},
                            "score":{
                              "boost":{
                                "value":2
                              }
                            }
                        }
                    }, {
                        "text": {
                            "query": arg, 
                            "path": 'directors',
                            "fuzzy":{},
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
    }},
    { '$limit': 20 },
    { '$project': { '_id': 1, 'title': 1 }}  
  ]
    if tag == '*':
        finalPipeline=pipeline2
    else:
        finalPipeline=pipeline
    resultPromise= Movies.aggregate(finalPipeline)
    resultPromiseResult=[doc async for doc in resultPromise]
    [result] = await Promise.all([resultPromiseResult])
    json_result=json.dumps(result)
    r.set(key,json_result)
    print(result)
    return json_result

