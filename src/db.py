from pymongo import mongo_client
from src.config import config
from motor.motor_asyncio import AsyncIOMotorClient
import json

client = AsyncIOMotorClient(config['DATABASE_URL'])
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