from pymongo import mongo_client
from src.config import config
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient('mongodb+srv://somya:123@cluster0.yhd6kk7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client[config['MONGO_INITDB_DATABASE']]
print('Connected to MongoDB')

db = client.get_database(config['MONGO_INITDB_DATABASE'])

Comments = db.comments
Users = db.users
Embedded_movies = db.embedded_movies
Movies = db.movies
Sessions = db.sessions
Theaters = db.theaters
Movies2=db['movies2']
