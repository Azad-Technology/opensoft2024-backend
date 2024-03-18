import redis
from src.config import config

r = redis.Redis(host=config['REDIS_URL'], password=config['PASSWORD_REDIS'],port=config['TTL_PORT'], decode_responses=True)

# Global variable to store the default TTL value
DEFAULT_TTL_KEY = "app:default_ttl"

async def set_default_ttl(ttl: int):
    await r.set(DEFAULT_TTL_KEY, ttl)

async def get_default_ttl():
    ttl = await r.get(DEFAULT_TTL_KEY)
    return int(ttl) if ttl else config['DEFAULT_TTL']

async def get_from_cache(key: str):
    return await r.get(key)

async def set_to_cache(key: str, value: str):
    expire = await get_default_ttl()
    print(f"Setting {key[:20]}... to cache with TTL {expire} seconds")
    await r.setex(key, expire, value)