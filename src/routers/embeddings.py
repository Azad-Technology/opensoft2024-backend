from fastapi import APIRouter, Depends, HTTPException, Request, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import bcrypt
from src import schemas
import jwt
from src.config import config
router = APIRouter()
from bson.objectid import ObjectId
from src.utils.text_embedder import embed_movie, get_embedding
from src.utils.ada_embedder import embed_movie as embed_movie_ada, get_embedding as get_embedding_ada
from src.db import Movies, Movies2, Embedded_movies2


@router.get("/init_embeddings")
async def init_embeddings():


    movies = await Movies2.find().to_list(500)
    for movie in movies:
        print(f"Generating embedding for {movie['title']}")
        if "plot" not in movie:
            continue
        embedding = get_embedding_ada([movie['plot']])
        embedding = embedding[0].tolist()[0]
        embedding = [float(value) for value in embedding]
        movie['embedding'] = embedding
        await Embedded_movies2.insert_one(movie)
        if embedding is None:
            print(f"Failed to embed {movie['title']}")
        else :
            print(f"Success")
    
    return {"message": "Embeddings initialized"}

@router.post("/rrf")
async def rrf(request: schemas.RRFQuerySchema):
    query = request
    query = query.query
    vector_penalty = 1
    full_text_penalty = 10

    query_embedding = get_embedding_ada([query])
    query_embedding = query_embedding[0].tolist()[0]
    query_embedding_bson = [float(value) for value in query_embedding]
    query_vector = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding_bson,
                "numCandidates": 100,
                "limit": 20
            }
        }, 
        {
            "$group": {
                "_id": None,
                "docs": {"$push": "$$ROOT"}
            }
        }, 
        {
            "$unwind": {
                "path": "$docs", 
                "includeArrayIndex": "rank"
            }
        }, 
        {
            "$addFields": {
                "vs_score": {
                    "$divide": [1.0, {"$add": ["$rank", vector_penalty, 1]}]
                }
            }
        }, 
        {
            "$project": {
                "vs_score": 1, 
                "_id": "$docs._id", 
                "title": "$docs.title"
            }
        },
        {
            "$unionWith": {
                "coll": "embedded_movies2",
                "pipeline": [
                    {
                        "$search": {
                            "index": "movie_index",
                            "phrase": {
                                "query": query,
                                "path": "title"
                            }
                        }
                    }, 
                    {
                        "$limit": 20
                    }, 
                    {
                        "$group": {
                            "_id": None,
                            "docs": {"$push": "$$ROOT"}
                        }
                    }, 
                    {
                        "$unwind": {
                            "path": "$docs", 
                            "includeArrayIndex": "rank"
                        }
                    }, 
                    {
                        "$addFields": {
                            "fts_score": {
                                "$divide": [
                                    1.0,
                                    {"$add": ["$rank", full_text_penalty, 1]}
                                ]
                            }
                        }
                    },
                    {
                        "$project": {
                            "fts_score": 1,
                            "_id": "$docs._id",
                            "title": "$docs.title"
                        }
                    }
                ]
            }
        },
        {
            "$group": {
                "_id": "$title",
                "vs_score": {"$max": "$vs_score"},
                "fts_score": {"$max": "$fts_score"}
            }
        },
        {
            "$project": {
                "_id": 1,
                "title": 1,
                "vs_score": {"$ifNull": ["$vs_score", 0]},
                "fts_score": {"$ifNull": ["$fts_score", 0]}
            }
        },
        {
            "$project": {
                "score": {"$add": ["$fts_score", "$vs_score"]},
                "_id": 1,
                "title": 1,
                "vs_score": 1,
                "fts_score": 1
            }
        },
        {"$sort": {"score": -1}},
        {"$limit": 10}
    ]
    results = await Embedded_movies2.aggregate(query_vector).to_list(10)
    response = []
    for result in results:
        result["_id"] = str(result["_id"])
        response.append({
            "title": result['_id'],
            "score": result['score'],
            "vs_score": result['vs_score'],
            "fts_score": result['fts_score']
        })
    return response



@router.post("/sem_search")
async def sem_search(request: schemas.RRFQuerySchema):
    query = request.query
    query_vector = get_embedding_ada([query])  
    query_vector = query_vector[0].tolist()[0]
    query_vector_bson = [float(value) for value in query_vector]
    pipeline = [
    {
        '$vectorSearch': {
        'index': 'vector_index', 
            'path': 'embedding',  
            'queryVector': query_vector_bson,
            'numCandidates': 200, 
        'limit': 10
        }
    }, {
        '$project': {
        '_id': 1, 
        'score': {
            '$meta': 'vectorSearchScore'
        }
        }
    }
    ]

    results = await Embedded_movies2.aggregate(pipeline).to_list(10)
    response = []
    for result in results:
        result["_id"] = str(result["_id"])
        movie = await Movies.find_one({"_id": ObjectId(result["_id"])})
        response.append({
            "title": movie['title'],
            "_id": str(movie['_id'])
        })
    return response
