from pymongo import mongo_client
from src.config import config
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(config['DATABASE_URL'])
db = client[config['MONGO_INITDB_DATABASE']]
print('Connected to MongoDB')

db = client.get_database(config['MONGO_INITDB_DATABASE'])

Comments = db.comments
Users = db.users
Embedded_movies = db.embedded_movies
Movies = db.movies
Sessions = db.sessions
Theaters = db.theaters
