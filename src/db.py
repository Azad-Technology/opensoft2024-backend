from pymongo import mongo_client
from src.config import config
from motor.motor_asyncio import AsyncIOMotorClient
import json

client = AsyncIOMotorClient(config['DATABASE_URL'])
print(config['DATABASE_URL'])
db = client[config['MONGO_INITDB_DATABASE']]
print('Connected to MongoDB')

with open('countries.json', 'r') as file:
    countries_dict=json.load(file)

db = client.get_database(config['MONGO_INITDB_DATABASE'])

Comments = db.comments
Users = db.users
Embedded_movies = db.embedded_movies
Movies = db.movies
Sessions = db.sessions
Theaters = db.theaters
Movies2 = db.movies2
Embedded_movies_new = db.embedded_movies_new
Embedded_movies2 = db.embedded_movies2
Watchlists=db['watchlists']
projects={
        "_id": { "$toString": "$_id" },
        "title": 1,
        "poster": 1,
        "runtime": 1,
        "imdb": 1,
        "poster_path":1,
        "backdrop_path":1,
        'genres':1,
        'year':1,
        'backdrop_path':1,
        'plot':1
    }


