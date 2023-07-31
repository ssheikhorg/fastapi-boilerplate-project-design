from redis import from_url, Redis
from src import settings as c

"""Redis Server Connection"""

broker = Redis(
    host=c.REDIS_HOST,
    port=c.REDIS_PORT,
    username=c.REDIS_USERNAME,
    password=c.REDIS_PASSWORD,
    db=0,
    decode_responses=True,
)

backend = Redis(
    host=c.REDIS_HOST,
    port=c.REDIS_PORT,
    username=c.REDIS_USERNAME,
    password=c.REDIS_PASSWORD,
    db=1,
    decode_responses=True,
)

"""Redis Server Connection"""
broker_url = f"redis://{c.REDIS_USERNAME}:{c.REDIS_PASSWORD}@{c.REDIS_HOST}:{c.REDIS_PORT}/0"
backend_url = f"redis://{c.REDIS_USERNAME}:{c.REDIS_PASSWORD}@{c.REDIS_HOST}:{c.REDIS_PORT}/1"
