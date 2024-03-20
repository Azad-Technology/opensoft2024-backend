from dotenv import load_dotenv, find_dotenv
import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

print(BASEDIR)

config = {
    'MONGO_INITDB_DATABASE':os.getenv('MONGO_INITDB_DATABASE'),
    'DATABASE_URL':os.getenv('DATABASE_URL'),
    'JWT_KEY':os.getenv('JWT_KEY'),
    'CORS_ORIGINS':os.getenv('CORS_ORIGINS'),
    'REDIS_URL':os.getenv('REDIS_URL'),
    'DEFAULT_TTL':5,
    'PASSWORD_REDIS':os.getenv('PASSWORD_REDIS'),
    'TTL_PORT':os.getenv('TTL_PORT'),
    'GOOGLE_CLIENT_ID':os.getenv('GOOGLE_CLIENT_ID'),
    'GOOGLE_CLIENT_SECRET':os.getenv('GOOGLE_CLIENT_SECRET'),
    'GOOGLE_REDIRECT_URI':os.getenv('GOOGLE_REDIRECT_URI')
}